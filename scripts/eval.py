from scripts.LLM_judge.llm_judge import LLM_Judge
from llama_ft.llama_ft import LlamaFineTuner
import os

class BaseModelInference:
    def __init__(self, client):
        self.client = client

    def base_model_inference(self, user_question, model_name, temperature=0.6, top_p=0.9, max_tokens=1024, top_k=50):
        response = self.client.chat.completions.create(
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={
                "top_k": top_k
            },
            messages=[
                {"role": "system",
                "content": "You are an expert in Generative AI. In particular, you have strong understanding of four subtopics: Responsible AI, Agentic AI, Prompt Engineering and Foundation models.\nYou are given a fact-based and exam-style question about one of these subtopics. Write a response that is the best possible answer to the given question. The answer MUST have:\n- High accuracy: factually accurate, well-researched and precise.\n- Maximum comprehensiveness: long, nuanced, and detailed.\n- Diverse viewpoints, key points and perspectives: Include multiple key aspects and perspectives with the discussions on each.\n- Well-structured output: Use Markdown for clear formatting and better readability.\n- No hallucination: Stick to verifiable facts. Do not make up any information."
                },
                {"role": "user",
                "content": user_question
                }
            ],
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the fine-tuner client
    fine_tuner = LlamaFineTuner()

    # Use the same client for base model inference
    inference = BaseModelInference(client=fine_tuner.client)

    # Initialize the LLM Judge
    judge = LLM_Judge(api_key=openai_api_key)

    # Define the question
    question = "What is Responsible AI?"

    # Perform inference using the base model
    base_model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct"  # Replace with the base model name
    answer1 = inference.base_model_inference(question, base_model_name)

    # Perform inference using the fine-tuned model
    answer2 = fine_tuner.fine_tuned_model_inference(question)

    # Evaluate the answers using LLM_Judge
    result = judge.evaluate_answers(question, answer1, answer2)
    
    print("Base Model Answer:", answer1)
    print("")
    print("Fine-Tuned Model Answer:", answer2)
    print("")
    print("Evaluation Result:", result)
    
    # Save the outputs to text files
    output_folder = "eval_outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Create a subfolder for this evaluation
    eval_output_folder = os.path.join(output_folder, "eval_outputs_1")
    os.makedirs(eval_output_folder, exist_ok=True)

    # Save the base model answer
    with open(os.path.join(eval_output_folder, "base_model_answer.txt"), "w", encoding="utf-8") as f:
        f.write(answer1)

    # Save the fine-tuned model answer
    with open(os.path.join(eval_output_folder, "fine_tuned_model_answer.txt"), "w", encoding="utf-8") as f:
        f.write(answer2)

    # Save the evaluation result
    with open(os.path.join(eval_output_folder, "evaluation_result.txt"), "w", encoding="utf-8") as f:
        f.write(str(result))