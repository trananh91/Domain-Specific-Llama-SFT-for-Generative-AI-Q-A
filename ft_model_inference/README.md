# Model Inference & Merging Guide

This guide explains how to prepare and merge a fine-tuned LoRA adapter into the base **LLaMA 3 model**, and save the final model in **Hugging Face Transformers format**, ready for inference with tools like **vLLM**.

## Step 1: Prepare the LoRA Adapter

Create a `.zip` file that contains your LoRA adapter files.

**Example of the directory structure:**
```text
lora_adapter/
├── adapter_model.safetensors
└── adapter_config.json
```

The outer folder (`lora_adapter/`) must contain both files.  
Zip this folder before uploading (e.g., `lora_adapter.zip`).


## Step 2: Upload and Extract

Upload the zipped file (`lora_adapter.zip`) to your environment (e.g., Google Colab), then unzip it to make the adapter accessible.


## Step 3: Load the Base Model and Adapter

Load the **base LLaMA 3 model** (`meta-llama/Meta-Llama-3-8B-Instruct`) using Hugging Face Transformers, then apply the LoRA adapter using the PEFT library.


## Step 4: Merge LoRA Weights

Merge the LoRA adapter into the base model to create a standalone merged model.

This step fuses the adapter weights into the original model weights, making it independent of LoRA during inference.


## Step 5: Save the Merged Model

Save the merged model in Hugging Face Transformers format using `save_pretrained`.

The saved directory should have the following structure:

```text
llama3-8b-merged/
├── config.json
├── model.safetensors
├── tokenizer_config.json
├── tokenizer.json / tokenizer.model
├── special_tokens_map.json
└── generation_config.json (optional)
```

This format is compatible with vLLM, Hugging Face Transformers, and other inference engines.

## Result

You now have a standalone, merged LLaMA 3 model that can be used for:

- Inference with **vLLM**
- Transformers-based pipelines
- Text Generation Inference (TGI)
- Deployment to Hugging Face Hub or inference APIs
