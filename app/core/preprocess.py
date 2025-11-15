# Preprocessing utilities (placeholder)

import re
import unicodedata

class Preprocessor:
    url_pattern = re.compile(r"http\S+|www\.\S+")
    mention_pattern = re.compile(r"@\w+")
    hashtag_pattern = re.compile(r"#(\w+)")
    non_alphanum = re.compile(r"[^a-zA-Z0-9\sáéíóúüñÁÉÍÓÚÜÑ]")

    def clean_text(self, text: str) -> str:
        if text is None:
            return ""
        s = str(text)
        s = s.lower()
        s = self.url_pattern.sub("", s)
        s = self.mention_pattern.sub("", s)
        s = self.hashtag_pattern.sub(r"\1", s)
        s = unicodedata.normalize("NFKD", s)
        s = self.non_alphanum.sub(" ", s)
        s = " ".join(s.split())
        return s
