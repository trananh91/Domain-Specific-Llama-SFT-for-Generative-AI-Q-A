# Data Preparation for Domain-Specific Llama SFT

This document details the data preparation phase of the **Domain-Specific Llama SFT for Generative AI Q&A** project.

---

## Data Sources and Collection Strategy

Our data collection strategy involved a dual approach to ensure comprehensive coverage and diversity within four key sub-topics in Generative AI: Prompt Engineering, Foundation Models, Agentic AI, and Responsible AI. This approach allowed for both leveraging existing knowledge and addressing specific content gaps.

1.  **Publicly Curated Datasets:**
    * I integrated a small number of relevant Q&A pairs from high-quality publicly available datasets used for SFT.
    * Sources included Hugging Face Datasets.
    * The selection criteria focused on data relevance, diversity of topics, and factual accuracy.

2.  **Synthetic Data Generation via Advanced Prompt Engineering:**
    * Since publicly curated datasets about Generative AI topics are not many and the data is manually extracted from public datasets, to enrich the dataset and target specific knowledge areas or linguistic variations not sufficiently covered by public data, I executed **synthetic data generation** using **AWS PartyRock**.
    * The process to generate informative Q&A pairs for each sub-topic: Sub-topic -> N Aspects -> M Subjects -> K Questions -> K Answers -> Q&A Format 
    * This was achieved through **advanced prompt engineering techniques** such as Prompt Chaining, Few-shot Prompting and Chain-of-Thought, applied to many advanced LLMs (Claude 3.5, Llama 3.1 Instruct 70B).
    * The process involved crafting sophisticated prompts to:
        * Generate novel, contextually relevant question-answer pairs for specific scenarios.
        * Create diverse paraphrases of existing questions and answers to enhance linguistic robustness.
        * Expand on complex concepts within Prompt Engineering, Foundation Models, Agentic AI, and Responsible AI, ensuring a deeper and broader understanding.
    * This was an iterative process, with prompts refined based on the quality of generated output and subsequent manual review.

---
## Data Cleaning & Preprocessing

The raw collected and synthetically generated data underwent a meticulous cleaning and preprocessing pipeline. This **careful curation** was essential to transform the raw information into **high-quality model input**, optimizing it for the Llama model's fine-tuning.

1.  **Format Validation and Transformation:**
    * All data was consistently transformed into a Question-Answer pair with JSONL format, aligning with the expected input structure for supervised fine-tuning of Llama models.
    * I implemented checks to ensure each entry adhered to the required schema and data types.
    * A JSONL-formatted example, where the "instruction" key is for the Question, the "response" key is for the Answer and the "context" provides additional context (optional): 
    ```json
    {"instruction": "What are the key ethical principles that should guide the development of responsible AI systems?", "context":"", "response":"Responsible AI development should be guided by principles including transparency, fairness, accountability, privacy protection, human oversight, non-maleficence (avoiding harm), beneficence (promoting good), and respect for human autonomy. These principles ensure AI systems serve humanity's best interests while minimizing potential risks."}

2.  **Special Token and Artifact Removal:**
    * A critical step involved **removing special tokens, control characters, and extraneous markdown/HTML artifacts** (e.g., `\n`, `\t`, `[CLS]`, `[SEP]`, `<a>` tags, or excessive punctuation) that could introduce noise or misinterpretations during training.
    * Leading/trailing whitespace was consistently trimmed from all text fields.

3.  **Token Distribution Analysis:**
    * I conducted **analysis of token distribution** across the entire dataset. This involved examining the length of questions and answers in terms of tokens.
    * This analysis helped in:
        * Identifying and handling outliers (e.g., extremely short or excessively long sequences) that might negatively impact training stability or efficiency. The outlier ones are then grouped by two groups:
            * Extremely short: These outliers are refined to have longer, more detailed answers.
            * Excessively long: These outliers are refined to have shorter, more concise answers.
            * Example: ![Example](data_prep/token_distribution_analysis_example.png)
        * Informing decisions regarding optimal *max_input_length* hyperparameter, ensuring efficient batching and memory utilization during fine-tuning.

4.  **Quality Curation and Validation:**
    * Beyond automated cleaning, the dataset underwent a **careful curation** process, including using another LLM for fact-checking.
    * This validation step was crucial for verifying the factual accuracy, contextual relevance, and overall linguistic quality of a representative subset of the data, especially for synthetically generated examples.
    * Inconsistencies, factual errors, or low-quality examples identified during this phase were refined to be correct.
