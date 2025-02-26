from langchain_core.prompts import PromptTemplate

class Prompt:
    def __init__(
        self,
        prompt_template,
    ):
        self.prompt_template = PromptTemplate.from_template(prompt_template)

    def invoke(self, **kwargs):
        return self.prompt_template.invoke(kwargs)