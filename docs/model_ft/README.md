# Model Fine-Tuning for Domain-Specific Llama SFT

This document details the process of fine-tuning a Llama model for domain-specific Generative AI Q&A.


## Base Model Selection

* **Model:** For this project, **Llama 3.1 8B Instruct** was selected as the base model for fine-tuning.
* **Rationale:** Llama 3.1 8B offers a strong balance between model capability, computational footprint, and accessibility for domain adaptation. Its robust pre-training provides an excellent foundation for specialized tasks.


## Fine-Tuning Environment: Nebius AI

The fine-tuning process was conducted using **Nebius AI**, a powerful and scalable platform for machine learning workloads. This environment was chosen for its capabilities in handling large-scale model training and its efficient resource management.


## Fine-Tuning Strategy: LoRA-based Supervised Fine-Tuning (SFT)

I employed **Supervised Fine-Tuning (SFT)** using a causal language modeling objective. The model was trained to predict the next token in a sequence, learning from structured `(instruction, context, response)` pairs. To ensure efficiency and manage computational resources effectively, **LoRA (Low-Rank Adaptation)** was utilized.

### LoRA Implementation:
LoRA is a Parameter-Efficient Fine-Tuning (PEFT) technique that injects small, trainable rank-decomposition matrices into the existing pre-trained model layers, while keeping the original model weights frozen. This significantly reduces the number of trainable parameters and memory footprint, making fine-tuning more accessible and faster.

### Key Aspects of SFT with LoRA:

1.  **Dataset Integration:** The custom, meticulously prepared JSONL dataset (as detailed in `data_preparation.md`) was formatted to align with Llama's instruction-tuning schema (e.g., `"[INST] {prompt} [/INST] {completion}"`).
2.  **Tokenizer Alignment:** The tokenizer corresponding to the Llama 3.1 8B model was used to ensure consistent tokenization between pre-training and fine-tuning.
3.  **Model Adaptation:** LoRA layers were strategically added to the attention and feed-forward modules of the Llama model, allowing for efficient adaptation to the new domain.


## Hyperparameter Optimization

**Systematic experimentation and hyperparameter optimization** were crucial for achieving optimal model performance. Key hyperparameters tuned included:

* **LoRA Configuration:**
    * `r` (LoRA rank): Explored values like `8`, `16`, `32` to balance expressiveness and parameter efficiency.
    * `lora_alpha`: Typically set as `2 * r` (e.g., `16`, `32`, `64`) to scale the LoRA weights.
    * `target_modules`: Focused on applying LoRA to critical layers such as query (`q_proj`) and value (`v_proj`) projections in the self-attention mechanism.
    * `lora_dropout`: Applied a small dropout rate (e.g., `0.05`) to the LoRA layers to prevent overfitting.
* **Training Parameters:**
    * **Learning Rate:** A carefully selected learning rate (e.g., `2e-5` to `5e-5`) with a cosine learning rate scheduler and warm-up steps was employed to ensure stable and effective convergence.
    * **Batch Size:** Optimized for available GPU memory (e.g., `8` to `16`), often combined with gradient accumulation steps (e.g., `gradient_accumulation_steps=4`) to simulate larger effective batch sizes.
    * **Number of Epochs:** Typically `3` to `5` epochs, with early stopping based on validation loss to prevent overfitting.
    * **Max Input Length:** Determined based on the token distribution analysis from the data preparation phase. This parameter (e.g., `512` or `1024` tokens) defines the maximum sequence length that the model can process, ensuring that input sequences fit within the model's architectural limits and GPU memory, while minimizing truncation of relevant information.


## Training Process & Monitoring

The fine-tuning process was closely monitored using Nebius AI's integration with Weights & Biases.

* **Loss Curves:** Training and validation loss were tracked across epochs to visualize convergence behavior and identify signs of overfitting.
* **Metrics:** Perplexity on the validation set was monitored as an indicator of the model's generalization ability.
* **Hyperparameters:** Key hyperparameters such as learning rate and number of epochs were consistently tracked and logged in Weights & Biases for comprehensive experiment management and reproducibility.
* **Model Checkpointing:** Regular checkpoints of the fine-tuned model were saved, allowing for recovery from interruptions and selection of the best-performing model based on validation metrics.