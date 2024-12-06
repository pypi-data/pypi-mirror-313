from typing import Optional
import argilla as rg

from galtea.models.template_fields import ABTestingFields 
from galtea.templates.template import Template

class SimpleABTestingTemplate(Template):
    def __init__(self, name, min_submitted: Optional[int] = 1, guidelines: Optional[str] = ""):
        self.name = name        
        self.guidelines = guidelines
        self.fields_model = ABTestingFields
        self.min_submitted = min_submitted

    def build_settings(self):

        settings = rg.Settings(
            allow_extra_metadata=True,
            guidelines=self.guidelines,
            distribution=rg.TaskDistribution(min_submitted=self.min_submitted),
            fields=[
                rg.TextField(name="prompt", title="Prompt", required=True),
                rg.TextField(name="answer_a", title="Answer A", required=True),
                rg.TextField(name="answer_b", title="Answer B", required=True),
            ],
            questions=[
                rg.LabelQuestion(
                    name="label",
                    title="What is the best response given the prompt?",
                    description="Select the one that applies.",
                    required=True,
                    labels={"answer_a": "Answer A", "answer_b": "Answer B", "both": "Both", "none": "None"}
                ),
            ]
        )


        return settings
        