# REVOLVE: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization for More Stable and Effective Progress
<!--- BADGES: START --->
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zou-group/TextGrad/blob/main/examples/notebooks/Prompt-Optimization.ipynb)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)][#license-gh-package]
[![Documentation Status](https://readthedocs.org/projects/textgrad/badge/?version=latest)][#docs-package]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/textgrad)][#pypi-package]
[![PyPI](https://img.shields.io/pypi/v/textgrad)][#pypi-package]
[![Conda - Platform](https://img.shields.io/conda/pn/conda-forge/textgrad?logo=anaconda&style=flat)][#conda-forge-package]
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/textgrad?logo=anaconda&style=flat&color=orange)][#conda-forge-package]

[#license-gh-package]: https://lbesson.mit-license.org/
[#arxiv-paper-package]: https://arxiv.org/abs/2406.07496
[#docs-package]: https://textgrad.readthedocs.io/en/latest/?badge=latest
[#pypi-package]: https://pypi.org/project/textgrad/
[#conda-forge-package]: https://anaconda.org/conda-forge/textgrad
<!--- BADGES: END --->

## About
- This is the code for paper: [REVOLVE: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization for More Stable and Effective Progress](https://arxiv.org/pdf/123456.pdf).
- REVOLVE is an optimization framework that enhances the stability and efficiency of AI system optimization by tracking the evolution of model responses across iterations. Building on textual feedback from LLMs, Revolve simulates higher-order optimization effects, ensuring that adjustments are guided not only by immediate feedback but also by the model’s performance trajectory, leading to faster and more stable optimization without relying on traditional derivative-based methods.
- REVOLVE offers an intuitive API, built upon the foundation of [TextGrad] (https://github.com/zou-group/textgrad), that allows users to define custom optimization tasks and loss functions. This makes it an adaptable and effective tool for optimizing LLM-based systems across a range of applications, including prompt optimization, solution refinement, and code optimization.

![Analogy with Second-order Optimization](assets/method_comparison.png)

## Installation
```bash
pip install REVOLVE
```


## Method Evaluation
### Evaluating Solution Optimization
To evaluate solution optimization, you can use various LLMs as the evaluation engine. For example, we use the gpt-4o as the evaluation engine. 
- For GPQA_diamond dataset:
```
python evaluation/solution_optimization.py --task GPQA_diamond --engine gpt-4o --num_threads 10 --optimizer_version v2

```
- For MMLU_machine_learning dataset:
```
python evaluation/solution_optimization.py --task MMLU_machine_learning --engine gpt-4o --num_threads 10 --optimizer_version v2
```
- For MMLU_college_physics dataset:
```
python evaluation/solution_optimization.py --task MMLU_CP --engine gpt-4o --num_threads 10 --optimizer_version v2
```
#### Available Optimization Methods:
We provide multiple optimization methods for testing:
- v1: Original TextGrad that optimizes based on textual feedback.
- v1_momentum: Momentum-TextGrad which adjusts optimization steps using feedback trends across iterations.
- v2: Our REVOLVE method that tracks response evolution over time for more stable and efficient optimization.
You can use the --optimizer_version flag to select the desired method.

### Evaluating Prompt Optimization

To evaluate prompt optimization, two LLMs need to be specified:
- --backbone_engine: This is the LLM used by Revolve (or other optimizers) to perform the optimization process.
- --model: This is the LLM on which the prompt is being optimized.
For example, we use the gpt-4o as the backbone_engine, using gpt-3.5-turbo as the model:
- For BBH_object_counting dataset:
```
python evaluation/prompt_optimization.py --task BBH_object_counting --backbone_engine gpt-4o --model gpt-3.5-turbo --num_threads 10 --optimizer_version v2

```
- For GSM8K dataset:
```
python evaluation/prompt_optimization.py --task GSM8K_DSPy --backbone_engine gpt-4o --model gpt-3.5-turbo --num_threads 10 --optimizer_version v2

```

### Evaluating Code Optimization

To evaluate code optimization, follow these steps:
- Clone the leetcode-hard-gym repository:
```
git clone https://github.com/GammaTauAI/leetcode-hard-gym.git && cd leetcode-hard-gym
```
- Install the package in editable mode:
```
python -m pip install -e .
```
- Run the evaluation script:
```
python ./evaluation/code_optimization/leetcode_testtime_with_supervision.py --engine meta-llama/Meta-Llama-3.1-70B-Instruct --optimizer_version v1 (for TextGrad) / v1_momentum (for Momentum-TextGrad) / v2 (for Revolve) --size 200
```

## Resources

### Inspiration
Many existing works greatly inspired this project! Here is a non-exhaustive list:
- 📚 [PyTorch](https://github.com/pytorch/pytorch/) The one and only. We owe a ton to PyTorch, hard to do justice here.
- 📚 [DSPy](https://github.com/stanfordnlp/dspy) is a pioneer in writing LM-based programs in many different ways! Has been a huge inspiration for us.
- 📚 [Micrograd](https://github.com/karpathy/micrograd): A tiny autograd engine greatly inspired our simple design!
- 📚 [ProTeGi](https://github.com/microsoft/LMOps/tree/main/prompt_optimization): We owe the term "Textual Gradients" to ProTeGi!
- 📚 [Reflexion](https://github.com/noahshinn/reflexion): A self-reflection that showed us the power of text-based reflection!
- 📚 [TextGrad](https://github.com/zou-group/textgrad): A Python package that provides a simple interface to implement LLM-“gradients” pipelines for text optimization! 