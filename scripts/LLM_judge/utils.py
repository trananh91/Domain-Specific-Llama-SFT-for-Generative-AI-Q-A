LLM_JUDGE_EVAL_PROMPT = """
You are an expert evaluator for answers related to Generative AI domain. Your task is to compare two answers to a given question and decide which one is better based on there criteria as follow:
1. Accuracy: Measures the factual correctness of the generated response. Does the answer contain verifiable information that is true within the Generative AI domain?
2. Comprehensiveness: Evaluates whether the response provides a complete and holistic answer to the question, covering all necessary aspects without being overly verbose.
3. Level of Detail: Assesses the depth and specificity of the information provided in the response. Does it offer sufficient detail for a domain-specific query, or is it too general?

Provide a detailed evaluation and declare the better answer or if it's a tie.

Question: {question}

Answer 1: {answer1}

Answer 2: {answer2}

"""