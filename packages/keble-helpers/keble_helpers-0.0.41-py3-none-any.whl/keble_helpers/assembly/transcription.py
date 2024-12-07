from redis import Redis
import time
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain_community.document_loaders.assemblyai import TranscriptFormat
from pathlib import Path
from langchain_core.documents import Document
from typing import List

class AssemblyTranscription:

    def __init__(self, *, api_key: str, redis: Redis, concurrent_limit: int = 5):
        self.__redis = redis
        self.__limit = concurrent_limit
        self.__api_key = api_key

    @property
    def __limit_key(self) -> str:
        return "AssemblyTranscription:limit"

    def load(self, filepath: str | Path, *, transcript_format=TranscriptFormat.PARAGRAPHS) -> List[Document]:
        # see: https://python.langchain.com/docs/integrations/document_loaders/assemblyai
        loader = AssemblyAIAudioTranscriptLoader(file_path=filepath,
                                                 transcript_format=transcript_format,
                                                 api_key=self.__api_key)
        return loader.load()


    def __wait_for_allow(self):
        max_seconds = 2 * 60  # wait for maximum 2 minute
        tried = 0
        while True:
            if self.__allow_to_proceed():
                return True
            tried += 1
            if tried > max_seconds:
                raise ValueError(f"Failed to convert to text due to maximum waiting has been reached")
            time.sleep(1)

    def __increment(self):
        self.__redis.incr(self.__limit_key)

    def __decrement(self):
        self.__redis.decr(self.__limit_key)

    def __get_current_processing(self) -> int:
        h = self.__redis.get(self.__limit_key)
        if h is None: return 0
        return int(h)

    def __allow_to_proceed(self):
        current = self.__get_current_processing()
        return current < self.__limit
