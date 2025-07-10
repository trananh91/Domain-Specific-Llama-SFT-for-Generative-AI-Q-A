import os
from openai import OpenAI
import time
import json
import random
from dotenv import load_dotenv

load_dotenv()

class LlamaFineTuner:
    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct"):
        self.client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=os.environ.get("NEBIUS_API_KEY"),
        )
        self.model_name = model_name
        self.training_dataset = None
        self.validation_dataset = None
        self.ft_job = None
        
    def prepare_data(self, dataset_file_path, train_file_path, valid_file_path, train_ratio=0.9):
        with open(dataset_file_path, "r") as f:
            data = f.readlines()
        random.shuffle(data)
        
        split_index = int(len(data) * train_ratio)
        train_data = data[:split_index]
        valid_data = data[split_index:]
        
        with open(train_file_path, "w") as f:
            f.writelines(train_data)

        with open(valid_file_path, "w") as f:
            f.writelines(valid_data)
            
        # Upload a training dataset
        self.training_dataset = self.client.files.create(
            file=open(train_file_path, "rb"), # Specify the dataset name
            purpose="fine-tune"
        )

        # Upload a validation dataset
        self.validation_dataset = self.client.files.create(
            file=open(valid_file_path, "rb"), # Specify the dataset name
            purpose="fine-tune"
        )

    def create_fine_tune_job(self, n_epochs, batch_size, learning_rate, lora=True, lora_r=16, lora_alpha=32, lora_dropout=0.1, seed=42, wandb_project="llama-ft-project"):
        wandb_api_key = os.environ.get("WANDB_API_KEY")
        
        job_request = {
            "model": self.model_name,
            "training_file": self.training_dataset.id,
            "validation_file": self.validation_dataset.id,
            "hyperparameters": {
                "n_epochs": n_epochs, 
                "batch_size": batch_size, 
                "learning_rate": learning_rate,
                "lora": lora,
                "lora_r": lora_r,
                "lora_alpha": lora_alpha,
                "lora_dropout": lora_dropout,
            },
            "seed": seed,
            "integrations": [
                {
                "type": "wandb",
                "wandb": {
                    "api_key": wandb_api_key,
                    "project": wandb_project,
                }
            }
            ],
        }
        # Create and run the fine-tuning job
        self.ft_job = self.client.fine_tuning.jobs.create(**job_request)

    def monitor_job(self):
        # Make sure that the job has been finished or cancelled
        active_statuses = ["validating_files", "queued", "running"]
        while self.ft_job.status in active_statuses:
            time.sleep(15)
            self.ft_job = self.client.fine_tuning.jobs.retrieve(self.ft_job.id)
            print("current status is", self.ft_job.status)

        print("Job ID:", self.ft_job.id)
        
    def retrieve_ft_checkpoints(self, checkpoint_dir="checkpoints"):
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        
        if self.ft_job.status == "succeeded":
            # Check the job events
            events = self.client.fine_tuning.jobs.list_events(self.ft_job.id)
            print(events)

            for checkpoint in self.client.fine_tuning.jobs.checkpoints.list(self.ft_job.id).data:
                print("Checkpoint ID:", checkpoint.id)

                # Create a directory for every checkpoint
                os.makedirs(os.path.join(checkpoint_dir, checkpoint.id), exist_ok=True)

                for model_file_id in checkpoint.result_files:
                    # Get the name of a model file
                    filename = self.client.files.retrieve(model_file_id).filename

                    # Retrieve the contents of the file
                    file_content = self.client.files.content(model_file_id)

                    # Save the contents into a local file
                    file_content.write_to_file(filename)

                    
    def fine_tuned_model_inference(self, user_question, temperature=0.6, top_p=0.9, max_tokens=1024, top_k=50):
        response = self.client.chat.completions.create(
            model=os.environ.get("MODEL_ID"),
            messages=[
                {"role": "system",
                "content": "You are an expert in Generative AI. In particular, you have strong understanding of four subtopics: Responsible AI, Agentic AI, Prompt Engineering and Foundation models.\nYou are given a fact-based and exam-style question about one of these subtopics. Write a response that is the best possible answer to the given question. The answer MUST have:\n- High accuracy: factually accurate, well-researched and precise.\n- Maximum comprehensiveness: long, nuanced, and detailed.\n- Diverse viewpoints, key points and perspectives: Include multiple key aspects and perspectives with the discussions on each.\n- Well-structured output: Use Markdown for clear formatting and better readability.\n- No hallucination: Stick to verifiable facts. Do not make up any information."
                },
                {"role": "user",
                "content": user_question
                }
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={
                "top_k": top_k
            },
        )

        ft_model_generation = response.choices[0].message.content
        return ft_model_generation
