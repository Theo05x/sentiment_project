# metrics service (placeholder)

from pathlib import Path
import logging
import pandas as pd
import re
from collections import Counter
from typing import Dict, Any, List, Optional, Tuple
from app.config import settings
from app.core.preprocess import Preprocessor

logger = logging.getLogger(__name__)

DEFAULT_CSV = settings.DATA_PATH

class MetricsService:
    def __init__(self, csv_path: Path | None = None):
        self.csv_path = Path(csv_path) if csv_path else DEFAULT_CSV
        self._df = None
        self._cache: Dict[str, Any] = {}
        self.pre = Preprocessor()

    def _load_df(self) -> pd.DataFrame | None:
        if self._df is not None:
            return self._df
        try:
            if not self.csv_path.exists():
                return None
            # Use python engine to support on_bad_lines
            self._df = pd.read_csv(self.csv_path, sep=";", engine="python", on_bad_lines="skip")
            return self._df
        except Exception as e:
            logger.exception("Error loading CSV: %s", e)
            self._df = None
            return None

    def clear_cache(self):
        self._cache = {}

    def sentiment_summary(self) -> Dict[str, Any]:
        """Return counts and average sentiment score."""
        df = self._load_df()
        if df is None or df.empty:
            return {"total_tweets": 0, "by_sentiment": {"positive": 0, "neutral": 0, "negative": 0}, "avg_score": 0.0}
        # normalize label column
        col_sent = next((c for c in ["airline_sentiment", "sentiment", "label"] if c in df.columns), None)
        if not col_sent:
            return {"total_tweets": len(df), "by_sentiment": {"positive": 0, "neutral": 0, "negative": 0}, "avg_score": 0.0}
        s = df[col_sent].astype(str).str.lower().map(lambda x: 'positive' if 'pos' in x else ('negative' if 'neg' in x else ('neutral' if 'neu' in x else x)))
        counts = s.value_counts().to_dict()
        total = int(len(s))
        by_sent = {"positive": int(counts.get('positive', 0)), "neutral": int(counts.get('neutral', 0)), "negative": int(counts.get('negative', 0))}
        # average score: positive=1, neutral=0, negative=-1
        score_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        avg_score = 0.0
        try:
            avg_score = float(s.map(score_map).dropna().mean())
        except Exception:
            avg_score = 0.0
        return {"total_tweets": total, "by_sentiment": by_sent, "avg_score": avg_score}

    def sentiment_time_series(self, freq: str = 'D') -> List[Dict[str, Any]]:
        """Return time series aggregated by `freq` (Pandas offset alias: 'D','W','M')."""
        key = f"ts:{freq}"
        if key in self._cache:
            return self._cache[key]
        df = self._load_df()
        if df is None or df.empty:
            return []
        date_col = 'tweet_created' if 'tweet_created' in df.columns else None
        if date_col is None:
            return []
        tmp = df.dropna(subset=[date_col]).copy()
        tmp[date_col] = pd.to_datetime(tmp[date_col], errors='coerce')
        col_sent = next((c for c in ["airline_sentiment", "sentiment", "label"] if c in tmp.columns), None)
        if col_sent is None:
            return []
        tmp['sent_norm'] = tmp[col_sent].astype(str).str.lower().map(lambda x: 'positive' if 'pos' in x else ('negative' if 'neg' in x else ('neutral' if 'neu' in x else x)))
        tmp = tmp.dropna(subset=['sent_norm'])
        tmp = tmp.set_index(date_col)
        grouped = tmp.groupby([pd.Grouper(freq=freq), 'sent_norm']).size().unstack(fill_value=0)
        result = []
        for idx, row in grouped.iterrows():
            result.append({"period": str(idx), "positive": int(row.get('positive', 0)), "neutral": int(row.get('neutral', 0)), "negative": int(row.get('negative', 0))})
        self._cache[key] = result
        return result

    def _tokenize(self, text: str) -> List[str]:
        s = self.pre.clean_text(text)
        tokens = [w for w in s.split() if len(w) > 2]
        return tokens

    def top_keywords(self, sentiment: Optional[str] = None, top: int = 50) -> List[Tuple[str, int]]:
        key = f"kw:{sentiment}:{top}"
        if key in self._cache:
            return self._cache[key]
        df = self._load_df()
        if df is None or df.empty:
            return []
        col_sent = next((c for c in ["airline_sentiment", "sentiment", "label"] if c in df.columns), None)
        texts = df['text'].astype(str)
        if sentiment and col_sent:
            mask = df[col_sent].astype(str).str.lower().str.contains(sentiment.lower())
            texts = df.loc[mask, 'text'].astype(str)
        counter = Counter()
        for t in texts:
            toks = self._tokenize(t)
            counter.update(toks)
        common = counter.most_common(top)
        self._cache[key] = common
        return common

    def topic_breakdown(self, sentiment: str = 'negative') -> Dict[str, int]:
        """Simple rule-based topic mapping for negative mentions."""
        # define simple keyword->topic mapping
        mapping = {
            'customer service': ['service', 'support', 'representative', 'agent', 'customer'],
            'flight issues': ['delay', 'cancel', 'flight', 'boarding', 'late'],
            'product issue': ['broken', 'defect', 'damage', 'issue', 'problem'],
            'price/fees': ['price', 'fee', 'expensive', 'cost']
        }
        df = self._load_df()
        if df is None or df.empty:
            return {}
        col_sent = next((c for c in ["airline_sentiment", "sentiment", "label"] if c in df.columns), None)
        if not col_sent:
            return {}
        s = df[df[col_sent].astype(str).str.lower().str.contains(sentiment.lower(), na=False)]
        counts = {k: 0 for k in mapping.keys()}
        for text in s['text'].astype(str):
            t = text.lower()
            for topic, kws in mapping.items():
                for kw in kws:
                    if kw in t:
                        counts[topic] += 1
                        break
        return counts

    def top_influencers(self, sentiment: Optional[str] = None, limit: int = 20, sort_by: str = 'count') -> List[Dict[str, Any]]:
        df = self._load_df()
        if df is None or df.empty:
            return []
        col_sent = next((c for c in ["airline_sentiment", "sentiment", "label"] if c in df.columns), None)
        tmp = df.copy()
        if sentiment and col_sent:
            tmp = tmp[tmp[col_sent].astype(str).str.lower().str.contains(sentiment.lower(), na=False)]
        g = tmp.groupby('name').agg(count=('text', 'count'), retweets=('retweet_count', lambda s: pd.to_numeric(s, errors='coerce').fillna(0).sum()))
        g = g.reset_index()
        if sort_by == 'retweets':
            g = g.sort_values('retweets', ascending=False)
        else:
            g = g.sort_values('count', ascending=False)
        res = g.head(limit).to_dict(orient='records')
        return res

    def geo_distribution(self, top: int = 100) -> List[Dict[str, Any]]:
        df = self._load_df()
        if df is None or df.empty:
            return []
        if 'tweet_location' not in df.columns:
            return []
        locs = df['tweet_location'].astype(str).replace({'nan': None}).dropna()
        counts = locs.value_counts().head(top).to_dict()
        return [{"location": k, "count": int(v)} for k, v in counts.items()]

    def summary(self) -> Dict[str, Any]:
        df = self._load_df()
        if df is None or df.empty:
            return {
                "total_tweets": 0,
                "by_sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                "top_airlines": []
            }
        col_sent = None
        for c in ["airline_sentiment","sentiment","label"]:
            if c in df.columns:
                col_sent = c
                break
        col_airline = "airline" if "airline" in df.columns else None
        total = len(df)
        if col_sent:
            counts = df[col_sent].astype(str).str.lower().value_counts().to_dict()
            by_sentiment = {
                "positive": int(counts.get("positive", 0)),
                "neutral": int(counts.get("neutral", 0)),
                "negative": int(counts.get("negative", 0))
            }
        else:
            by_sentiment = {"positive": 0, "neutral": 0, "negative": 0}
        if col_airline:
            top = df[col_airline].value_counts().head(10).to_dict()
            top_list = [{"airline": k, "count": int(v)} for k,v in top.items()]
        else:
            top_list = []
        return {"total_tweets": int(total), "by_sentiment": by_sentiment, "top_airlines": top_list}
