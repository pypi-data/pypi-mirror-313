from enum import Enum
from galtea.models.base_fields import BaseTemplateFields

class ABTestingFields(BaseTemplateFields):
    prompt: str
    answer_a: str
    answer_b: str

class TemplateType(Enum):
    ab_testing = "ab_testing"