import asyncio
from collections.abc import Callable
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    BertForSequenceClassification,
    BertTokenizer,
    BertweetTokenizer,
    RobertaTokenizer,
    RobertaForSequenceClassification,
    pipeline
)
from nltk.tokenize import sent_tokenize
import torch
from ..exceptions import ComponentError
from .flow import FlowComponent


class ModelPrediction:
    """
    SentimentAnalysis

        Overview

            The SentimentAnalysis is a component for applying sentiment analysis and emotion detection on a
            text corpus using Hugging Face’s Transformers. It supports various models and tokenizers, including
            BERT, BERTweet, and RoBERTa, and handles text chunking to accommodate length limitations. This component
            returns detailed sentiment and emotion scores, as well as predicted sentiment labels.

        .. table:: Properties
        :widths: auto

            +--------------------+----------+-----------+---------------------------------------------------------------+
            | Name               | Required | Summary                                                                |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | text_column        |   Yes    | The column name in the DataFrame containing the text to analyze.       |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | sentiment_model    |   No     | Model name for sentiment analysis. Defaults to 'tabularisai/robust-sentiment-analysis'. |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | emotions_model     |   No     | Model name for emotion detection. Defaults to 'cardiffnlp/twitter-roberta-base-emotion'. |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | pipeline_classification | No  | Classification type for pipeline (e.g., 'sentiment-analysis').         |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | with_average       |   No     | Boolean to aggregate sentiment across all rows, if applicable.        |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | sentiment_levels   |   No     | Number of sentiment levels (2, 3, or 5). Default is 5.                |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | use_bert           |   No     | Boolean to use BERT model for sentiment analysis.                     |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | use_roberta        |   No     | Boolean to use RoBERTa model for sentiment analysis.                  |
            +--------------------+----------+-----------+---------------------------------------------------------------+
            | use_bertweet       |   No     | Boolean to use BERTweet model for sentiment analysis.                 |
            +--------------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component returns a DataFrame with columns for predicted sentiment and emotion scores, including:

            - `sentiment_scores`: List of sentiment scores for each text.
            - `sentiment_score`: Maximum sentiment score for each text.
            - `emotions_score`: Score of the most probable emotion.
            - `predicted_emotion`: Label of the predicted emotion.
            - `predicted_sentiment`: Label of the predicted sentiment.

            If debugging is enabled, detailed column information is logged. If an error occurs during text processing,
            a `ComponentError` is raised with details.
    """

    def __init__(
        self,
        sentiment_model: str = "tabularisai/robust-sentiment-analysis",
        emotions_model: str = "bhadresh-savani/distilbert-base-uncased-emotion",
        classification: str = 'sentiment-analysis',
        levels: int = 5,
        max_length: int = 512,
        use_bertweet: bool = False,
        use_bert: bool = False,
        use_roberta: bool = False
    ):
        self.max_length = max_length
        self.levels = levels
        self.use_bertweet: bool = use_bertweet
        if use_bert:
            self.model = BertForSequenceClassification.from_pretrained(
                sentiment_model,
                num_labels=abs(levels),
                ignore_mismatched_sizes=True
            )
            self.tokenizer = BertTokenizer.from_pretrained(sentiment_model)
        elif use_roberta:
            self.model = RobertaForSequenceClassification.from_pretrained(sentiment_model)
            self.tokenizer = RobertaTokenizer.from_pretrained(sentiment_model)
        elif use_bertweet:
            self.model = AutoModelForSequenceClassification.from_pretrained(sentiment_model)
            self.tokenizer = BertweetTokenizer.from_pretrained(sentiment_model)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(
                sentiment_model,
                # normalization=True
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                sentiment_model,
            )
        # And the Emotional Model:
        self.emotional_model = AutoModelForSequenceClassification.from_pretrained(
            emotions_model
        )
        self.emo_tokenizer = AutoTokenizer.from_pretrained(emotions_model)
        self._device = self._get_device()
        self.emotion_classifier = pipeline(
            classification,
            model=self.emotional_model,
            tokenizer=self.emo_tokenizer,
            device=self._device,
            return_all_scores=True
        )
        # sentiment classifier:
        self.sentiment_classifier = pipeline(
            classification,
            model=self.model,
            tokenizer=self.tokenizer,
            device=self._device,
            return_all_scores=True
        )

    def _get_device(self, use_device: str = 'cpu', cuda_number: int = 0):
        torch.backends.cudnn.deterministic = True
        if torch.cuda.is_available():
            # Use CUDA GPU if available
            device = torch.device(f'cuda:{cuda_number}')
        elif torch.backends.mps.is_available():
            # Use CUDA Multi-Processing Service if available
            device = torch.device("mps")
        elif use_device == 'cuda':
            device = torch.device(f'cuda:{cuda_number}')
        else:
            device = torch.device(use_device)
        return device

    def predict_emotion(self, text: str) -> dict:
        """Predict emotion using the pipeline, splitting long text if necessary."""
        if not text:
            return {}

        # Tokenize the text to check its length
        encoded_text = self.emo_tokenizer.encode(
            str(text),
            truncation=False,
            add_special_tokens=True
        )

        # Handle long texts by splitting them into chunks if needed
        if len(encoded_text) > self.max_length:
            text_chunks = self._split_text(text, self.max_length)
            return self._predict_multiple_emotion_chunks(text_chunks)

        # Use the pipeline to predict emotion for shorter texts
        prediction = self.emotion_classifier(str(text))

        if len(prediction) > 0 and isinstance(prediction[0], list):  # When return_all_scores=True
            emotions = [emo_pred for emo_pred in prediction[0] if emo_pred['score'] >= 0.5]  # Apply threshold
            if not emotions:
                emotions.append({"label": "neutral", "score": 0})
            return {'emotions': emotions}

        return {}

    def _predict_multiple_emotion_chunks(self, chunks: list) -> dict:
        """Predict emotion for each chunk using the pipeline and aggregate results."""
        all_emotions = []

        for chunk in chunks:
            predictions = self.emotion_classifier(chunk)
            if len(predictions) > 0 and isinstance(predictions[0], list):
                # Filter predictions for significant emotions
                emotions = [emo_pred for emo_pred in predictions[0] if emo_pred['score'] >= 0.5]
                if emotions:
                    all_emotions.extend(emotions)

        # Aggregate emotions across all chunks
        if not all_emotions:
            return {'emotions': [{"label": "neutral", "score": 0}]}

        # Optionally, you can further process and aggregate emotions, but this returns them all
        return {'emotions': all_emotions}

    def _get_sentiment_map(self) -> dict:
        """Get the sentiment map based on the levels."""
        if self.levels == -3:  # Inverted
            return {
                0: "Neutral",
                1: "Positive",
                2: "Negative",
            }
        elif self.levels == 5:
            return {
                0: "Very Negative",
                1: "Negative",
                2: "Neutral",
                3: "Positive",
                4: "Very Positive"
            }
        elif self.levels == 3:
            return {
                0: "Negative",
                1: "Neutral",
                2: "Positive",
            }
        else:
            return {
                0: "Negative",
                1: "Positive",
            }

    def predict_sentiment(self, text: str) -> dict:
        """Predict sentiment using the pipeline.

        Args:
            text (str): Text to be analyzed.

        Returns:
            dict: Predicted Sentiment with scores.
        """
        if not text:
            return None
        if isinstance(text, float):
            text = str(text)

        # Tokenize the text to check its length
        encoded_text = self.tokenizer.encode(text, truncation=False, add_special_tokens=True)

        # Handle long texts by splitting them into chunks if needed
        if len(encoded_text) > self.max_length:
            text_chunks = self._split_text(text, self.max_length)
            return self._predict_multiple_chunks_pipeline(text_chunks)

        # Use the pipeline to predict sentiment for shorter texts
        predictions = self.sentiment_classifier(text)

        # Since return_all_scores=True, predictions is a list of lists
        # Each inner list contains dicts with 'label' and 'score'
        scores = predictions[0]

        # Extract scores and labels
        probabilities = [item['score'] for item in scores]
        labels = [item['label'] for item in scores]

        # Check if labels are descriptive (e.g., 'positive', 'neutral', 'negative')
        if all(label.lower() in ['positive', 'neutral', 'negative'] for label in labels):
            # If labels are descriptive, no need for custom mapping
            predicted_label = max(scores, key=lambda x: x['score'])['label']
            return {
                "score": probabilities,
                "predicted_sentiment": predicted_label.capitalize()
            }

        # Map labels to indices
        label_to_index = {}
        for _, label in enumerate(labels):
            if label.startswith("LABEL_"):
                label_idx = int(label.replace("LABEL_", ""))
                label_to_index[label] = label_idx
        if not label_to_index:
            label_to_index = {label: idx for idx, label in enumerate(labels)}

        predicted_label = max(scores, key=lambda x: x['score'])['label']
        predicted_class = label_to_index[predicted_label]

        # Map predicted_class to sentiment
        sentiment_map = self._get_sentiment_map()

        predicted_sentiment = sentiment_map.get(predicted_class, predicted_label)

        return {
            "score": probabilities,
            "predicted_sentiment": predicted_sentiment
        }

    def _predict_multiple_chunks_pipeline(self, chunks: list) -> dict:
        """Predict sentiment for each chunk using the pipeline and aggregate results."""
        all_probabilities = []
        for chunk in chunks:
            predictions = self.sentiment_classifier(chunk)
            scores = predictions[0]
            probabilities = [item['score'] for item in scores]
            all_probabilities.append(torch.tensor(probabilities))

        # Averaging probabilities across chunks
        avg_probabilities = torch.mean(torch.stack(all_probabilities), dim=0)
        predicted_class = torch.argmax(avg_probabilities).item()

        sentiment_map = self._get_sentiment_map()
        predicted_sentiment = sentiment_map.get(predicted_class, "Unknown")

        return {
            "score": avg_probabilities.tolist(),
            "predicted_sentiment": predicted_sentiment
        }

    def _split_text(self, text: str, max_length: int) -> list:
        """Split text into chunks to handle texts longer than max token length."""
        sentences = text.split('. ')  # Split by sentences
        chunks = []
        current_chunk = ''
        for sentence in sentences:
            if len(
                self.tokenizer.encode(current_chunk + sentence, return_tensors='pt')[0]
            ) < max_length:
                current_chunk += sentence + '. '
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def split_into_sentences(self, text):
        """Split text into sentences."""
        return sent_tokenize(text)

    def aggregate_sentiments(self, sentiments, levels):
        """Aggregate sentiments from multiple texts."""
        # Initialize an array to hold cumulative scores
        cumulative_scores = torch.zeros(levels)
        for sentiment in sentiments:
            scores = torch.tensor(sentiment['score'][0])
            cumulative_scores += scores

        # Calculate average scores
        avg_scores = cumulative_scores / len(sentiments)
        predicted_class = torch.argmax(avg_scores).item()

        if levels == 5:
            sentiment_map = {
                0: "Very Negative",
                1: "Negative",
                2: "Neutral",
                3: "Positive",
                4: "Very Positive"
            }
        elif levels == 3:
            sentiment_map = {
                0: "Negative",
                1: "Neutral",
                2: "Positive",
            }
        else:
            sentiment_map = {
                0: "Negative",
                1: "Positive",
            }

        return sentiment_map[predicted_class]


class SentimentAnalysis(FlowComponent):
    """SentimentAnalysis.
        Applying Huggingfaces transformers over a corpus of text,
        and extracting sentiment analysis and emotion detection.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Extract sentiment analysis."""
        self.text_column: str = kwargs.pop('text_column', 'text')
        self._sentiment_model: str = kwargs.pop(
            'sentiment_model',
            'tabularisai/robust-sentiment-analysis'
        )
        self._emotion_model: str = kwargs.pop(
            'emotions_model',
            "cardiffnlp/twitter-roberta-base-emotion"
        )
        self._classification: str = kwargs.pop(
            'pipeline_classification',
            'sentiment-analysis'
        )
        self.with_average: bool = kwargs.pop('with_average', True)
        self.sentiment_levels: int = kwargs.pop('sentiment_levels', 5)
        self._use_bert: bool = kwargs.pop('use_bert', False)
        self._use_roberta: bool = kwargs.pop('use_roberta', False)
        self._use_bertweet: bool = kwargs.pop('use_bertweet', False)
        self.chunk_size: int = 100
        self.max_workers: int = 5
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "Data Not Found",
                status=404
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Data, we need a Pandas Dataframe",
                status=404
            )
        # instanciate the model:
        self._predictor = ModelPrediction(
            sentiment_model=self._sentiment_model,
            emotions_model=self._emotion_model,
            classification=self._classification,
            max_length=512,
            levels=self.sentiment_levels,
            use_bertweet=self._use_bertweet,
            use_bert=self._use_bert,
            use_roberta=self._use_roberta
        )
        return True

    async def close(self):
        pass

    def _analyze_chunk(self, chunk: pd.DataFrame):
        """Analyze each row in the chunk and add sentiment and emotion."""
        chunk['sentiment'] = chunk[self.text_column].apply(
            self._predictor.predict_sentiment
        )
        chunk['emotions'] = chunk[self.text_column].apply(
            self._predictor.predict_emotion
        )
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass
        return chunk

    async def run(self):
        # Split the dataframe into chunks
        num_chunks = np.ceil(len(self.data) / self.chunk_size).astype(int)
        chunks = np.array_split(self.data, num_chunks)

        # Run analysis in parallel using a thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            processed_chunks = list(executor.map(self._analyze_chunk, chunks))

        # Concatenate all the chunks back into a single DataFrame
        df = pd.concat(processed_chunks)
        # extract the predicted sentiment and emotion
        try:
            # Extract 'sentiment_score' from 'sentiment' column (e.g., first score in the list)
            df['sentiment_scores'] = df['sentiment'].apply(
                lambda x: x.get('score', []) if x and isinstance(x.get('score', []), list) else []
            )
            # Max value of sentiments
            df['sentiment_score'] = df['sentiment_scores'].apply(
                lambda x: max(x) if isinstance(x, list) and len(x) > 0 else None
            )
            # Extract 'emotions_score' from 'emotions' column (e.g., score from the first emotion)
            df['emotions_score'] = df['emotions'].apply(
                lambda x: x.get('emotions', [{'score': None}])[0]['score'] if x and isinstance(x.get('emotions', []), list) and len(x['emotions']) > 0 else None
            )
            # Expand the 'emotions' and 'sentiments' column to extract the label
            df['predicted_emotion'] = df['emotions'].apply(
                lambda x: x.get('emotions', [{'label': None}])[0]['label'] if x and isinstance(x.get('emotions', []), list) and len(x.get('emotions', [])) > 0 else None
            )
            df['predicted_sentiment'] = df['sentiment'].apply(
                lambda x: x.get('predicted_sentiment', None) if x else None
            )
        except Exception as e:
            print(e)
            pass
        self._result = df
        if self._debug is True:
            print("== DATA PREVIEW ==")
            print(self._result)
            print()
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        return self._result
