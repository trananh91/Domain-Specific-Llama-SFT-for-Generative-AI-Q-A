# Initial Research for Domain-Specific Llama SFT

This document details the initial research phase of the **Domain-Specific Llama SFT for Generative AI Q&A** project.

## Problem Statement

Our primary problem statement is: **How can we fine-tune a large language model (LLM) like Llama to excel in providing accurate, contextually relevant answers within a specific domain, thereby overcoming the limitations of general-purpose LLMs in specialized use cases?**

General-purpose LLMs, while versatile, often struggle with:
* **Domain-Specific Nuances:** Lack deep understanding of specialized terminology, jargon, and implicit knowledge within a particular field.
* **Hallucinations:** Tendency to generate plausible but incorrect information when faced with topics outside their core training distribution.
* **Accuracy:** May not provide precise or verifiable facts for highly specialized queries.


## Domain Selection

This project's domain is directly inspired by my participation in the AWS ASEAN LLM League 2025. The competition focused on Generative AI, divided into four key sub-topics:
- Prompt Engineering
- Foundation Models
- Agentic AI
- Responisble AI


## Literature Review

* **Supervised Fine-Tuning (SFT) Techniques:** Reviewed methods for effective SFT, including instruction tuning and parameter-efficient fine-tuning (PEFT) approaches like LoRA.
* **Domain Adaptation for LLMs:** Explored existing research on how LLMs are adapted to specific fields.
* **Evaluation Metrics:** Researched standard and advanced metrics for assessing the quality of generated answers.


## Desired Outcomes & Success Metrics

* Significantly higher accuracy and relevance of answers compared to a general-purpose Llama model on domain-specific test sets.
* Reduced instances of hallucinations for domain-specific queries.


## Further Reading & Key Resources

The following papers and technical blogs were instrumental in shaping the initial research direction and understanding the core concepts for this project:
- *LIMA: Less Is More for Alignment*: [ArXiv](https://arxiv.org/abs/2305.11206)
- *LIMO: Less is More for Reasoning*: [ArXiv](https://arxiv.org/abs/2502.03387)
- *Fine-tune Llama 3 for text generation on Amazon SageMaker JumpStart*: [Link](https://aws.amazon.com/blogs/machine-learning/fine-tune-llama-3-for-text-generation-on-amazon-sagemaker-jumpstart/)
- *Prompt Engineering: Be clear, direct, and detailed*: [Link](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)