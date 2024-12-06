from typing import Optional
from galtea.models.template_fields import TemplateType
from galtea.templates.simple_ab_testing import SimpleABTestingTemplate
from galtea.templates.creator import TemplateFactory

class ConcreteTemplateFactory(TemplateFactory):
    def get_template(self, name: str, template_type: TemplateType, min_submitted: Optional[int] = 1, guidelines: Optional[str] = None):
        if template_type == TemplateType.ab_testing:
            return SimpleABTestingTemplate(name, min_submitted, guidelines)
        else:
            raise ValueError(f"Unknown template type: {template_type.value}")