"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.
"""
import asyncio
import aiohttp
from typing import Any
from collections.abc import Callable
import random
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import httpx
import pandas as pd
import backoff
import ssl
from navconfig.logging import logging
# Internals
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported,
    ConfigError
)
from .flow import FlowComponent
from ..interfaces import HTTPService, SeleniumService
from ..interfaces.http import ua


logging.getLogger(name='selenium.webdriver').setLevel(logging.WARNING)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)
logging.getLogger(name='seleniumwire').setLevel(logging.WARNING)


ProductPayload = {
    "locationId": None,
    "zipCode": None,
    "showOnShelf": True,
    "lookupInStoreQuantity": True,
    "xboxAllAccess": False,
    "consolidated": True,
    "showOnlyOnShelf": False,
    "showInStore": True,
    "pickupTypes": [
        "UPS_ACCESS_POINT",
        "FEDEX_HAL"
    ],
    "onlyBestBuyLocations": True,
    "items": [
        {
            "sku": None,
            "condition": None,
            "quantity": 1,
            "itemSeqNumber": "1",
            "reservationToken": None,
            "selectedServices": [],
            "requiredAccessories": [],
            "isTradeIn": False,
            "isLeased": False
        }
    ]
}


def bad_gateway_exception(exc):
    """Check if the exception is a 502 Bad Gateway error."""
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 502


class BestBuy(FlowComponent, SeleniumService, HTTPService):
    """BestBuy.

    Combining API Key and Web Scrapping, this component will be able to extract
    Best Buy Information (stores, products, Product Availability, etc).
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._fn = kwargs.pop('type', None)
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        self.product_info: bool = kwargs.get('product_info', False)
        if not self._fn:
            raise ConfigError(
                "BestBuy: require a `type` Function to be called, ex: availability"
            )
        super(BestBuy, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False
        ctt_list: list = [
            "f3dbf688e45146555bb2b8604a993601",
            "06f4dfe367e87866397ef32302f5042e",
            "4e07e03ff03f5debc4e09ac4db9239ac"
        ]
        sid_list: list = [
            "d4fa1142-2998-4b68-af78-46d821bb3e1f",
            "9627390e-b423-459f-83ee-7964dd05c9a8"
        ]
        self.cookies = {
            # "CTT": ,
            "CTT": random.choice(ctt_list),
            "SID": random.choice(sid_list),
            "bby_rdp": "l",
            "bm_sz": "9F5ED0110AF18594E2347A89BB4AB998~YAAQxm1lX6EqYHGSAQAAw+apmhkhXIeGYEc4KnzUMsjeac3xEoQmTNz5+of62i3RXQL6fUI+0FvCb/jgSjiVQOcfaSF+LdLkOXP1F4urgeIcqp/dBAhu5MvZXaCQsT06bwr7j21ozhFfTTWhjz1HmZN8wecsE6WGbK6wXp/33ODKlLaGWkTutqHbkzvMiiHXBCs9hT8jVny0REfita4AfqTK85Y6/M6Uq4IaDLPBLnTtJ0cTlPHk1HmkG5EsnI46llghcx1KZnCGnvZfHdb2ME9YZJ2GmC2b7dNmAgyL/gSVpoNdCJOj5Jk6z/MCVhZ81OZfX4S01E2F1mBGq4uV5/1oK2KR4YgZP4dsTN8izEEPybUKGY3CyM1gOUc=~3556420~4277810",  # noqa
            "bby_cbc_lb": "p-browse-e",
            "intl_splash": "false"
        }
        self.headers: dict = {
            "Host": "www.bestbuy.com",
            "Referer": "https://www.bestbuy.com/",
            "X-Requested-With": "XMLHttpRequest",
            "TE": "trailers",
            "Accept-Language": "en-US,en;q=0.5",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **self.headers
        }
        self.semaphore = asyncio.Semaphore(10)

    async def close(self, **kwargs) -> bool:
        self.close_driver()
        return True

    async def start(self, **kwargs) -> bool:
        await super(BestBuy, self).start(**kwargs)
        if self.previous:
            self.data = self.input
            if not isinstance(self.data, pd.DataFrame):
                raise ComponentError(
                    "Incompatible Pandas Dataframe"
                )
        #else:
        #    raise DataNotFound(
        #        "Data Not Found",
        #        status=404
        #    )
        self.api_token = self.get_env_value(self.api_token) if hasattr(self, 'api_token') else self.get_env_value('BEST_BUY_API_KEY')
        if self._fn == 'availability':
            if not hasattr(self, 'brand'):
                raise ConfigError(
                    "BestBuy: A Brand is required for using Product Availability"
                )
        if not hasattr(self, self._fn):
            raise ConfigError(
                f"BestBuy: Unable to found Function {self._fn} in BBY Component."
            )

    def _search_product(self, brand: str, sku: str) -> str:
        front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
        middle_url = "&searchType=search&st="
        page_count = 1
        # TODO: Get the Brand and Model from the Component.
        search_term = f'{brand}%20{sku}'
        end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"  # noqa
        url = front_url + str(page_count) + middle_url + search_term + end_url
        print('SEARCH URL: ', url)
        return url

    async def _extract_product_list(self, content: str) -> dict:
        soup = BeautifulSoup(content, 'html.parser')
        # Find all elements with class "sku-item"
        product_items = soup.find_all('li', {'class': ['sku-item']})
        # Iterate over each product item
        result = {}
        for item in product_items:
            # Get the "data-sku-id" attribute
            sku_id = item.get("data-sku-id")
            # Check if the SKU ID matches your target SKU ID
            if sku_id == self.sku:
                print(f"Found matching SKU ID: {sku_id}")
                # Now look for the child with class "sku-title"
                pd = item.find('h4', {'class': ['sku-title']})
                anchor = pd.a
                title = anchor.text
                price = item.find(
                    'div', {'class': ['priceView-customer-price']}
                ).select_one(
                    'span:nth-child(1)'
                ).text
                # Image:
                image = item.find('img', {"class": ['product-image']})['src']
                # Product Model
                model = item.select_one(
                    'div.sku-attribute-title:nth-child(1) span.sku-value'
                ).text
                url = "https://www.bestbuy.com{url}".format(
                    url=anchor['href']
                )
                self._logger.notice(
                    f':: Product URL: {url}'
                )
                result = {
                    "sku": sku_id,
                    "brand": self.brand,
                    "model": model,
                    "product_name": title,
                    "image_url": image,
                    "price": price,
                    "url": url
                }
                # if product found, break
                return result
        return result

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def api_post(self, url: str, cookies: httpx.Cookies, payload: dict):
        self._free_proxy = False
        proxies = await self.get_proxies()
        proxy = proxies[0]
        proxy_config = {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}"  # Using the same proxy for HTTPS
        }
        # Define custom SSL context
        ssl_context = ssl.create_default_context()
        # Disable older protocols if needed
        ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        # Ensure at least TLS 1.2 is used
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Use AsyncHTTPTransport to pass in SSL context explicitly
        transport = httpx.AsyncHTTPTransport(retries=2, verify=ssl_context)
        timeout = httpx.Timeout(connect=5.0, read=20.0, write=5.0, pool=20.0)

        async with httpx.AsyncClient(
            cookies=cookies,
            proxies=proxy_config,
            transport=transport
        ) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=timeout
                )
                response.raise_for_status()
                if response.status_code == 200:
                    return response.json()
                else:
                    print(
                        f"API request failed with status code {response.status_code}"
                    )
                return {}
            except httpx.TimeoutException:
                raise
            except (httpx.HTTPError) as ex:
                raise httpx.HTTPError(ex)
            except Exception as exc:
                print('EXC > ', exc)
                raise ComponentError(
                    f"An error occurred: {exc}"
                )

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectTimeout, httpx.HTTPStatusError),
        max_tries=2,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _check_store_availability(self, idx, row, cookies):
        async with self.semaphore:
            # Prepare payload for the API request
            zipcode = row['zipcode']
            location_code = row['location_code']
            sku = row['sku']
            payload = ProductPayload.copy()
            payload["locationId"] = location_code
            payload["zipCode"] = zipcode
            for item in payload["items"]:
                item["sku"] = sku

            # checking if this current store is already marked as checked:
            matching_store = self.data[
                (self.data['location_code'] == location_code) & (self.data['sku'] == sku)
            ]
            if not matching_store.empty and matching_store.iloc[0]['checked'] == True:
                # exit without making any HTTP call.
                return row

            try:
                result = await self.api_post(
                    url="https://www.bestbuy.com/productfulfillment/c/api/2.0/storeAvailability",
                    cookies=cookies,
                    payload=payload
                )
                self._num_iterations += 1
            except (httpx.TimeoutException, httpx.HTTPError) as ex:
                self._logger.warning(f"Request failed: {ex}")
                return row
            except Exception as ex:
                self._logger.error(f"An error occurred: {ex}")
                return row

            if not result:
                self._logger.warning(
                    f"No availability data found for {sku} at zipcode {zipcode}"
                )
                return row

            # Extract the availability data from the API response
            items = result.get('ispu', {}).get('items', [])
            for item in items:
                locations = item.get('locations', [])
                for location in locations:
                    lid = location.get('locationId')
                    # Find matching store and SKU in DataFrame
                    matching_store = self.data[
                        (self.data['location_code'] == lid) & (self.data['sku'] == sku)
                    ]
                    if not matching_store.empty:
                        idx = matching_store.index[0]
                        if self.data.loc[idx, 'checked'] is True:
                            print('Already checked, continue ...')
                            continue  # Skip this row if it's already marked as checked
                        if 'availability' not in location:
                            self.data.loc[idx, 'locationId'] = lid
                            self.data.loc[idx, 'checked'] = True
                            continue  # This store doesn't have availability
                        print(f'Found matching store {lid} for sku {sku}')

                        # Update the DataFrame row with new availability data
                        self.data.loc[idx, ['brand', 'location_data']] = [self.brand, location]
                        for key, val in location.items():
                            if key in self.data.columns:
                                self.data.at[idx, key] = val
                            else:
                                self.data.at[idx, key] = None
                            if key == 'inStoreAvailability':
                                try:
                                    self.data.loc[idx, 'availableInStoreQuantity'] = val.get(
                                        'availableInStoreQuantity', 0
                                    )
                                except KeyError:
                                    self.data.loc[idx, 'availableInStoreQuantity'] = None
                        # Mark the row as checked
                        self.data.loc[idx, 'checked'] = True
            return row

    def column_exists(self, column: str, default_val: Any = None):
        if column not in self.data.columns:
            self._logger.warning(
                f"Column {column} does not exist in the Dataframe"
            )
            self.data[column] = default_val
            return False
        return True

    async def availability(self):
        """availability.

        Best Buy Product Availability.
        """
        httpx_cookies = httpx.Cookies()
        # if self.product_info is True:
        #     # 1. Get the Product List URL
        #     url = self._search_product(self.brand, self.sku)
        #     await self.get_page(url, self.cookies)
        #     content = self.driver().page_source
        #     product_info = await self._extract_product_list(content)
        #     if not product_info:
        #         raise DataNotFound(
        #             f"BestBuy: Cannot found product information for {self.brand}-{self.sku}"
        #         )
        #     # With Product info, extract the cookies from Selenium:
        #     # Get the cookies from Selenium WebDriver
        #     selenium_cookies = self.driver().get_cookies()
        #     # Convert Selenium cookies to httpx format
        #     cookies_avail = ["CTT", "SID", '_abck', 'bby_rdp', 'bm_sz']
        #     for cookie in selenium_cookies:
        #         if cookie['name'] in cookies_avail:
        #             httpx_cookies.set(
        #                 cookie['name'], cookie['value'],
        #                 domain=cookie['domain'],
        #                 path=cookie['path']
        #             )

        #     # make a join between current df and product info:
        #     new_df = pd.DataFrame([product_info] * len(self.data))
        #     # Concatenate the DataFrames horizontally
        #     self.data = pd.concat([self.data, new_df], axis=1)
        # else:
        for key, value in self.cookies.items():
            httpx_cookies.set(
                key, value,
                domain='.bestbuy.com',
                path='/'
            )

        # define the columns returned:
        self.column_exists('brand')
        self.column_exists('location_data')
        self.column_exists('locationId')
        self.column_exists('availability')
        self.column_exists('inStoreAvailability')
        self.column_exists('onShelfDisplay', False)
        self.column_exists('availableInStoreQuantity', 0)

        # With available cookies, iterate over dataframe for stores:
        self.data['checked'] = False  # Add 'checked' flag column

        # Iterate over each row in the DataFrame
        print('starting ...')

        tasks = [
            self._check_store_availability(
                idx,
                row,
                httpx_cookies
            ) for idx, row in self.data.iterrows()
        ]

        self._num_iterations = 0
        await self._processing_tasks(tasks)

        self.add_metric('NUM_HTTP_CALLS', self._num_iterations)

        # # Fetch the rows where 'checked' is False
        # unchecked_rows = self.data.loc[self.data['checked'] == False]

        # # Break the loop if no unchecked rows are left
        # if unchecked_rows.empty:
        #     return self.data

        # # Iterate over unchecked rows
        # for idx, row in unchecked_rows.iterrows():
        #     if self.data.loc[idx, 'checked'] == True:
        #         continue  # Skip this row if it's already marked as checked
        #     await self._check_store_availability(
        #         row, httpx_cookies
        #     )
        #     # if self.data.loc[idx, 'checked'] == True:
        #     #     print(f"Row at index {idx} marked as checked.")
        #     # else:
        #     #     print(f"Row at index {idx} remains unchecked.")
        #     await asyncio.sleep(
        #         random.uniform(0.5, 1.5)
        #     )

        # show the num of rows in final dataframe:
        self._logger.notice(
            "Ending Checking Availability."
        )

        # return existing data
        return self.data

    async def products(self):
        """
            Fetch all products from the Best Buy API by paginating through all pages.

            Returns:
                list: A combined list of all products from all pages.
        """
        all_products = []
        current_page = 1
        total_pages = None
        show = 'sku,upc,modelNumber,name,manufacturer,type,salePrice,url,productTemplate,classId,class,subclassId,subclass,department,image,longDescription,customerReviewCount,customerReviewAverage'
        self._num_iterations = 0
        try:
            while True:
                url = f"https://api.bestbuy.com/v1/products?page={current_page}&pageSize=100&apiKey={self.api_token}&show={show}&format=json"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as result:
                        response = await result.json()
                        #response = await self.api_get(url, httpx_cookies)
                        self._num_iterations += 1
                        
                        # Extract products from the response
                        products = response.get("products", [])
                        if len(products) == 0:
                            continue
                        all_products.extend(products)
                        #all_products += products

                        # Pagination control
                        current_page = response.get("currentPage", current_page)
                        total_pages = response.get("totalPages", current_page) if total_pages is None else total_pages
                        self._logger.debug(f"{url}\n    Current Page: {current_page}, Total Pages: {total_pages}, Products: {len(all_products)}")

                        # Break if we've processed all pages
                        if current_page >= total_pages: # or current_page == 3:
                            break

                        # Increment page for the next request
                        current_page += 1

            self.add_metric('NUM_HTTP_CALLS', self._num_iterations)
            df_products = pd.DataFrame(all_products)

            # return existing data
            return df_products

        except Exception as exc:
            self._logger.error(f"Error while fetching products: {exc}")
            return []

    async def stores(self):
        """
            Fetch all stores from the Best Buy API by paginating through all pages.

            Returns:
                list: A combined list of all stores from all pages.
        """
        all_stores = []
        current_page = 1
        total_pages = None
        self._num_iterations = 0
        try:
            while True:
                url = f"https://api.bestbuy.com/v1/stores?page={current_page}&pageSize=100&apiKey={self.api_token}&format=json"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as result:
                        response = await result.json()
                        self._num_iterations += 1
                        
                        # Extract stores from the response
                        stores = response.get("stores", [])
                        if len(stores) == 0:
                            continue
                        all_stores.extend(stores)
                        #all_stores += stores

                        # Pagination control
                        current_page = response.get("currentPage", current_page)
                        total_pages = response.get("totalPages", current_page) if total_pages is None else total_pages
                        self._logger.debug(f"{url}\n    Current Page: {current_page}, Total Pages: {total_pages}, Stores: {len(all_stores)}")

                        # Break if we've processed all pages
                        if current_page >= total_pages: # or current_page == 3:
                            break

                        # Increment page for the next request
                        current_page += 1

            self.add_metric('NUM_HTTP_CALLS', self._num_iterations)
            df_stores = pd.DataFrame(all_stores)

            # return existing data
            return df_stores

        except Exception as exc:
            self._logger.error(f"Error while fetching stores: {exc}")
            return []

    async def run(self):
        # we need to call the "function" for Best Buy Services.
        fn = getattr(self, self._fn)
        result = None
        if not callable(fn):
            raise ComponentError(
                f"Best Buy: Function {self._fn} doesn't exists."
            )
        try:
            result = await fn()
        except (ComponentError, TimeoutError, NotSupported):
            raise
        except Exception as exc:
            raise ComponentError(
                f"BestBuy: Unknown Error: {exc}"
            ) from exc
        # Print results
        print(result)
        print("::: Printing Column Information === ")
        for column, t in result.dtypes.items():
            print(column, "->", t, "->", result[column].iloc[0])
        self._result = result
        return self._result

    def split_parts(self, task_list, num_parts: int = 5) -> list:
        part_size = len(task_list) // num_parts
        remainder = len(task_list) % num_parts
        parts = []
        start = 0
        for i in range(num_parts):
            # Distribute the remainder across the first `remainder` parts
            end = start + part_size + (1 if i < remainder else 0)
            parts.append(task_list[start:end])
            start = end
        return parts

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            for chunk in self.split_parts(tasks, self.task_parts):
                result = await asyncio.gather(
                    *[
                        loop.run_in_executor(executor, asyncio.run, task) for task in chunk
                    ],
                    return_exceptions=True
                )
                results.extend(result)
        return results
