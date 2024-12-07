# REVOLVE: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization for More Stable and Effective Progress
<!--- BADGES: START --->
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)][#license-gh-package]
[![Arxiv](https://img.shields.io/badge/arXiv-2412.03092-B31B1B.svg)][#arxiv-paper-package]
![cuda 11.2](https://img.shields.io/badge/cuda-11.2-green.svg)
![python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)

[#license-gh-package]: https://lbesson.mit-license.org/
[#arxiv-paper-package]: https://arxiv.org/abs/2412.03092/
<!--- BADGES: END --->

## About
- This is the code for paper: [REVOLVE: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization for More Stable and Effective Progress](https://arxiv.org/pdf/2412.03092).
- REVOLVE is an optimization framework that enhances the stability and efficiency of AI system optimization by tracking the evolution of model responses across iterations. Building on textual feedback from LLMs, Revolve simulates higher-order optimization effects, ensuring that adjustments are guided not only by immediate feedback but also by the model’s performance trajectory, leading to faster and more stable optimization without relying on traditional derivative-based methods.
- REVOLVE offers an intuitive API, built upon the foundation of [TextGrad](https://github.com/zou-group/textgrad), that allows users to define custom optimization tasks and loss functions. This makes it an adaptable and effective tool for optimizing LLM-based systems across a range of applications, including prompt optimization, solution refinement, and code optimization.

![Analogy with Second-order Optimization](assets/method_comparison.png)

## Installation
```bash
pip install revolve
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
python evaluation/solution_optimization.py --task MMLU_college_physics --engine gpt-4o --num_threads 10 --optimizer_version v2
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

## Related Links

This project has been inspired by numerous excellent works! Below is a non-exhaustive list of key references:
- 📖 [DSPy](https://github.com/stanfordnlp/dspy) A pioneering framework for leveraging LMs in diverse applications, which significantly influenced our approach.
- 📖 [ProTeGi](https://github.com/microsoft/LMOps/tree/main/prompt_optimization): The term 'Textual Gradients' was inspired by ProTeGi’s prompt optimization methods.
- 📖 [Reflexion](https://github.com/noahshinn/reflexion): A self-reflection framework that demonstrated the power of text-based reflection in optimization.
- 📖 [TextGrad](https://github.com/zou-group/textgrad): Laying the foundation for implementing LLM-based "gradient" pipelines, TextGrad offers a streamlined interface for text optimization tasks, which directly contributed to the development of our approach.


## BibTeX citation
If you find our work useful, please consider citing us:
```bibtex
@misc{zhang2024revolveoptimizingaisystems,
      title={Revolve: Optimizing AI Systems by Tracking Response Evolution in Textual Optimization}, 
      author={Peiyan Zhang and Haibo Jin and Leyang Hu and Xinnuo Li and Liying Kang and Man Luo and Yangqiu Song and Haohan Wang},
      year={2024},
      eprint={2412.03092},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.03092}, 
}
```
