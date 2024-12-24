
import abc
from typing import List


class ContentSplitter:

    @abc.abstractmethod
    def split_content(content: str) -> List[str]:
        pass
