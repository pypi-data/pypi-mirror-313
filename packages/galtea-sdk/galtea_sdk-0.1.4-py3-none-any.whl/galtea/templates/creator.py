from abc import ABC, abstractmethod
from typing import Optional

class TemplateFactory(ABC):
    @abstractmethod
    def get_template(self, template_type: str, min_submitted: Optional[int] = None, guidelines: Optional[str] = None):
        pass

