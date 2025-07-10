from openai import OpenAI
import os
from openai import OpenAIError 
from scripts.LLM_judge.utils import LLM_JUDGE_EVAL_PROMPT

class LLM_Judge:
    def __init__(self, api_key=None, model="gpt-4.1"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it in the .env file or pass it explicitly.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def evaluate_answers(self, question, answer1, answer2):
        prompt = LLM_JUDGE_EVAL_PROMPT.format(question=question, answer1=answer1, answer2=answer2)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            evaluation = response.choices[0].message.content
            return {"evaluation": evaluation}
        
        except OpenAIError as e:
            return {"error in eval answer": str(e)}