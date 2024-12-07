from openai import OpenAI
from .openai_evaluator import OpenaiPromptEvaluator
from .gemini_evaluator import GeminiPromptEvaluator

class PromptEvaluator():
    def __init__(self, openai_api_key=None,google_api_key=None,model="gpt-4"):
        if model == "gpt-4":
            self.openai_obj = OpenaiPromptEvaluator(openai_api_key)
        else:
            self.gemini_obj = GeminiPromptEvaluator(google_api_key)
        self.model = model

    def query_model(self, model , prompt, criterion, question):
        if self.model == "gpt-4":
            return self.openai_obj.query_model(prompt, criterion, question)    
        else:
            return self.gemini_obj.query_model(prompt, criterion, question)

    def evaluate_prompt(self, model,prompt: str):
        if self.model == "gpt-4":
            return self.openai_obj.evaluate_prompt(prompt)
        else:
            return self.gemini_obj.evaluate_prompt(prompt)

    def token_length(self,prompt: str,model: str = "gpt-4") -> int:
        if self.model == "gpt-4":
            return self.openai_obj.token_length(prompt)
        else:
            return self.gemini_obj.token_length(prompt)

    



