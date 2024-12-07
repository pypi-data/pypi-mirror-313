# README for `prompt-program`

## `prompt-program`: A Python Library for Crafting Optimal Prompts

`prompt-program` is a lightweight library designed to assist users in creating well-structured and intent-aligned prompts for NLP models. Leveraging the principles from state-of-the-art research in prompt engineering and text perplexity analysis, it enables users to create, refine, and evaluate prompts to ensure maximum model performance and coherence.

---

## Features

1. **Improved Prompt Suggestions**  
   Automatically refine input prompts to align with best practices for clarity and intent.

2. **System Prompt Generation**  
   Generate system-level prompts by defining the purpose (`why`), methodology (`how`), and content (`what`).

3. **Prompt Perplexity Calculation**  
   Quantify the quality of a prompt using perplexity metrics to gauge its readability and predictability.

---

## Installation

To install `prompt-program`, use pip:

```bash
pip install prompt-program
```

---

## How It Works

The library is inspired by key insights from:  
- *"Prompt Injection and Chaining: Mastering NLP Prompting"* ([arXiv:2409.12447v1](https://arxiv.org/pdf/2409.12447v1))  
- *"Understanding Perplexity in Prompt Design"* ([arXiv:2103.10385v2](https://arxiv.org/pdf/2103.10385v2))  

These studies highlight the importance of prompt clarity, chaining, and perplexity evaluation in enhancing model responses. 

---

## Code Examples

### 1. **Improving Prompts**

Refine a user-provided prompt for better structure and intent.

```python
from prompt_program import prompts

prompt = "Explain AI in simple terms."
improved_prompt = get_improved_prompt(prompt)

print("Improved Prompt:", improved_prompt)
```

**Output:**  
```plaintext
Improved Prompt: "Explain artificial intelligence (AI) in simple, easy-to-understand terms suitable for a general audience."
```

---

### 2. **Creating System Prompts**

Generate a system prompt based on *why*, *how*, and *what* inputs.

```python
from prompt_program import prompts

why = "Assist users with technical questions."
how = "By providing step-by-step explanations."
what = "Covering topics related to Python and AI."

system_prompt = prompts.get_system_prompt(why, how, what)

print("System Prompt:", system_prompt)
```

**Output:**  
```plaintext
System Prompt: "You are a helpful assistant designed to assist users with technical questions. Provide step-by-step explanations covering topics related to Python and AI."
```

---

### 3. **Calculating Prompt Perplexity**

Evaluate the quality of a prompt using perplexity.

```python
from prompt_program import scores

prompt = "What are the applications of AI?"
perplexity_score = scores.calculate_perplexity(prompt)

print("Prompt Perplexity Score:", perplexity_score)
```

**Output:**  
```plaintext
Prompt Perplexity Score: 13.57
```

---

## Contributing

Contributions to `prompt-program` are welcome! If you'd like to report issues, request features, or contribute code, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

The development of `prompt-program` was guided by insights from the following research papers:  
- *"Prompt Injection and Chaining: Mastering NLP Prompting"* ([arXiv:2409.12447v1](https://arxiv.org/pdf/2409.12447v1))  
- *"Understanding Perplexity in Prompt Design"* ([arXiv:2103.10385v2](https://arxiv.org/pdf/2103.10385v2))  

--- 

**Happy Prompting!**