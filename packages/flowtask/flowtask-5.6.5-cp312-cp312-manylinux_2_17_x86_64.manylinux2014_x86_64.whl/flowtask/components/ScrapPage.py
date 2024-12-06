"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.
"""
import asyncio
from collections.abc import Callable
from pathlib import Path, PurePath
from navconfig import BASE_DIR
# Internals
from ..exceptions import (
    ComponentError,
    DataNotFound,
    TimeOutError
)
from .flow import FlowComponent
from ..interfaces import HTTPService, SeleniumService


class ScrapPage(SeleniumService, HTTPService, FlowComponent):
    """ScrapPage.
        Scrapping a Web Page using Selenium.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.url: str = kwargs.get("url", None)
        self.urls: list = kwargs.get('urls', [])
        self.rotate_ua: bool = True
        kwargs['rotate_ua'] = True  # Forcing UA Rotation.
        # Fix the Headers for Scrapping:
        self.headers: dict = {
            "Host": self.extract_host(self.url),
            "Referer": self.url,
            "X-Requested-With": "XMLHttpRequest",
            "TE": "trailers",
        }
        # Configure Cookies:
        self.cookies: dict = kwargs.get('cookies', {})
        self.use_selenium: bool = kwargs.pop(
            "use_selenium",
            False
        )
        # URL Function: generate the URL based on a function:
        self.url_function: str = kwargs.pop('url_function', None)
        # Return the Driver (avoid closing the Driver at the end of the process).
        self.return_driver: bool = kwargs.pop('return_driver', False)
        super(ScrapPage, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs) -> bool:
        await super(ScrapPage, self).start(**kwargs)
        if self.use_selenium is True:
            await self.get_driver()
        # Generate a URL based on a URL Function:
        if self.url_function:
            fn = getattr(self, self.url_function, None)
            if fn:
                self.url = await fn()
        return True

    async def close(self, **kwargs) -> bool:
        if self.use_selenium is True:
            if self.return_driver is False:
                self.close_driver()
        return True

    async def run_http(self):
        """Run the Scrapping Tool Using HTTPx."""
        result, error = await self.session(
            url=self.url,
            method=self.method,
            headers=self.headers,
            cookies=self.cookies,
            follow_redirects=True,
            use_proxy=self.use_proxy
        )
        if error:
            raise ComponentError(
                f"Error running Scrapping Tool: {error}"
            )
        if not result:
            raise DataNotFound(
                f"No content on URL {self.url}"
            )
        return result

    async def run_selenium(self):
        """Run the Scrapping Tool Using Selenium."""
        try:
            await self.get_page(self.url, self.cookies)
            file = None
            content = None
            if self.inner_tag:
                content = self.driver().find_element(*self.inner_tag).get_attribute('innerHTML')
            else:
                content = self.driver().page_source
            if hasattr(self, 'screenshot'):
                # capture an screenshot from the page and save it (and returning as binary as well)
                filename = self.screenshot.get('filename', 'screenshot.png')
                directory = Path(self.screenshot.get(
                    'directory', BASE_DIR.joinpath('static', 'images', 'screenshots')
                ))
                if not directory.is_absolute():
                    directory = BASE_DIR.joinpath('static', 'images', directory)
                if directory.exists() is False:
                    directory.mkdir(parents=True, exist_ok=True)
                # Take the screenshot
                file = directory.joinpath(filename)
                self.save_screenshot(str(file))
            # Return the content of the page.
            return content, file
        except (TimeOutError, ComponentError):
            raise
        except Exception as exc:
            raise ComponentError(
                f"Error running Scrapping Tool: {exc}"
            )

    def _build_result_content(self, content: str, screenshot: PurePath) -> dict:
        """Build the Result Content."""
        soup = self.get_soup(content)
        _xml, _html = self.get_etree(content)
        return {
            "raw": content,
            "soup": soup,
            "html": _html,
            "xml": _xml,
            "screenshot": screenshot
        }

    async def run(self):
        """Run the Scrapping Tool."""
        self._result = None
        screenshot = None
        try:
            if self.use_selenium is True:
                if self.urls:
                    results = []
                    for url in self.urls:
                        self.url = url
                        self.headers['Host'] = self.extract_host(url)
                        self.headers['Referer'] = url
                        content, screenshot = await self.run_selenium()
                        result = self._build_result_content(content, screenshot)
                        results.append(
                            {"url": url, "content": result}
                        )
                    self._result = results
                    return results
                else:
                    content, screenshot = await self.run_selenium()
            else:
                content = await self.run_http()
            if not content:
                raise DataNotFound(
                    f"No content on URL {self.url}"
                )
        except ComponentError:
            raise
        except Exception as exc:
            raise ComponentError(
                f"Error running Scrapping Tool: {exc}"
            )
        if self.return_driver is True:
            self._result = self.driver()
        else:
            self._result = self._build_result_content(content, screenshot)
        return self._result
