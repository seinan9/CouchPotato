# Couch Potato

This repository contains the code and data used for the ACL 2025 paper: "*A Couch Potato is not a Potato on a Couch: Visual Compositionality Prediction using Prompting Strategies and Image Generation for Adequate Image Retrieval*".

**Table of Contents**

- [Data](#data)
- [Installation](#installation)
- [Reproducing Results from the Paper](#reproducing-results-from-the-paper)

## Data

Below is an overview of the data in this repository.

### Targets

We use 88 out of the 90 compound nouns, along with their corresponding gold-standard compositionality ratings, originally provided by [Reddy et al.](https://aclanthology.org/I11-1024/). These are stored in:

- `data/targets.yaml`: The 88 target compounds.
- `data/gold.csv`: Human compositionality ratings.

Please refer to the original paper for more details.

### Prompts

Prompts used in our image generation experiments are located under the `data/prompts` directory:

- `sentence/`: Prompts extracted from the ENCOW16AX corpus.
- `definition/`: Definitions generated using ChatGPT.
- `scenario/`: Scenario-based descriptions generated using ChatGPT.

Details on the prompt construction process can be found in our paper.

### Predictions

We provide the full predictions for all results presented in the paper, so people that are interested can have a deeper look and also quickly work with the data if they want.

### Concreteness Annotations

The file `data/concreteness/annotations.csv` includes human-annotated concreteness ratings for the 88 compound nouns used in our experiments.

## Installation

1. **Clone the repository:**
   
        git clone https://github.com/seinan9/CouchPotato.git
        cd ImageCompositionality

2. (Optional) **Create and activate a virtual environment:**

        python -m venv ./venv
        source .venv/bin/activate

3. **Install the dependencies:**

        pip install -r requirements.txt

4. **Set your HuggingFace token** (required for some models):

        export HF_TOKEN=your_token_here

## Reproducing Results from the Paper

For easy reproducibility we provide YAML workflows. In order to reproduce a result, select the corresponding workflow YAML file and pass it to the main module.
```bash
python3 couch_potato/main.py -w workflows/example_workflow.yaml -o path/to/desired/output_dir
```

### Example
To reproduce **PixArt + Scenario** from Table 1:
```bash
python couch_potato/main.py --workflow workflows/pixart_scenario.yaml --output_dir output/pixart_scenario
```
The modifier and head correlation can then be found under output/pixart_scenario/artifacts/7_correlation_calculator/similarities.csv

We provide two options:
1. Starting from the predictions: Very fast, in most cases this only correlates the predictions to the gold data.
2. Starting from Scratch: Very slow, this does all the steps from start to finish (downloading/generating images, feature extraction and so on)

### Table 1

| Table | Results | Workflow File | Workflow File (full) |
|---|---|---|
| 1 | Bing | `workflows/bing.yaml`|
| 1 | PixArt + Word | `workflows/pixart-sigma_word.yaml` |
| 1 | PixArt + Sentence | `workflows/pixart-sigma_sentence.yaml` |
| 1 | PixArt + Definition | `workflows/pixart-sigma_definition.yaml` |
| 1 | PixArt + Scenario | `workflows/pixart-sigma_scenario.yaml` |
| 1 | Skip-gram (T) | `workflows/skip-gram.yaml` |
| 1 | Combined (T + V) | `workflows/combined.yaml` |
| 1 | ChatGPT (direct) | `workflows/chat-gpt.yaml` |


### Table 2

| Table | Results | Workflow File |
|---|---|---|
| 2 | Concrete: PixArt + Scenario | `workflows/concrete_pixart-sigma_scenario.yaml`|
| 2 | Abstract: PixArt + Scenario | `workflows/abstract_pixart-sigma_scenario.yaml`|
| 2 | Concrete: Skip-gram | `workflows/concrete_skip-gram.yaml`|
| 2 | Abstract: Skip-gram | `workflows/abstract_skip-gram.yaml`|

### Table 3

| Table | Results | Workflow File |
|---|---|---|
| 3 | SDXLBase + Word | `workflows/sdxl-base_word.yaml` |
| 3 | SDXLBase + Sentence | `workflows/sdxl-base_sentence.yaml` |
| 3 | SDXLBase + Definition | `workflows/sdxl-base_definition.yaml` |
| 3 | SDXLBase + Scenario | `workflows/sdxl-base_scenario.yaml` |
| 3 | JuggernautXL + Word | `workflows/sdxl-juggernaut_word.yaml` |
| 3 | JuggernautXL + Sentence | `workflows/sdxl-juggernaut_sentence.yaml` |
| 3 | JuggernautXL + Definition | `workflows/sdxl-juggernaut_definition.yaml` |
| 3 | JuggernautXL + Scenario | `workflows/sdxl-juggernaut_scenario.yaml` |
| 3 | PixArt + Word | `workflows/pixart-sigma_word.yaml` |
| 3 | PixArt + Sentence | `workflows/pixart-sigma_sentence.yaml` |
| 3 | PixArt + Definition | `workflows/pixart-sigma_definition.yaml` |
| 3 | PixArt + Scenario | `workflows/pixart-sigma_scenario.yaml` |


Please note that not all results can be reproduced exactly due to external or practical constraints. For example:

- Images retrieved from Bing may vary between runs, as the underlying API does not guarantee consistent results or support a fixed random seed.
- We cannot share the full preprocessed text corpus used to train the skip-gram model due to its size.

Despite these limitations, the provided workflows closely replicate the original pipeline structure, allowing for a high-level reproduction of our experiments.
