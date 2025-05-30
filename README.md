# Couch Potato

THIS IS WORK IN PROGRESS!

This repository contains the code and data used for the ACL 2025 paper: "*A Couch Potato is not a Potato on a Couch: Visual Compositionality Prediction using Prompting Strategies and Image Generation for Adequate Image Retrieval*".

**Table of Contents**

- [Data](#data)
- [Installation](#installation)
- [Reproducing Results from the Paper](#reproducing-results-from-the-paper)

## Data

Below is an overview of the data in this repository.

| **Category**               | **File/Directory**                               | **Description**                                                                |
|---------------------------|--------------------------------------------------|---------------------------------------------------------------------------------|
| **Targets**               | `data/targets.yaml`                              | List of 88 compound (and constituents) nouns used in the experiments.           |
|                           | `data/gold.csv`                                  | Human-annotated compositionality ratings from [Reddy et al.](https://aclanthology.org/I11-1024/)|
| **Prompts**               | `data/prompts/sentence/`                         | **Sentence** prompts from the ENCOW16AX corpus.                                 |
|                           | `data/prompts/definition/`                       | **Definition** prompts generated via ChatGPT.                                   |
|                           | `data/prompts/scenario/`                         | **Scenario** prompts generated via ChatGPT.                                     |
| **Predictions**           | `data/predictions/`                              | Full set of predictions for all experiments.                                    |
| **Concreteness Ratings**  | `data/concreteness/annotations.csv`              | Human-annotated concreteness scores for the 88 compounds.                       |

## Installation

1. **Clone the repository:**
```bash   
git clone https://github.com/seinan9/CouchPotato.git
cd ImageCompositionality
```
2. (Optional) **Create and activate a virtual environment:**
```bash
python3 -m venv ./venv
source .venv/bin/activate
```
3. **Install the dependencies:**
```bash
pip install -r requirements.txt
```
4. **Set your HuggingFace token** (required for some models):
```bash
export HF_TOKEN=your_token_here
```

## Reproducing Results from the Paper

For easy reproducibility we provide a set of YAML workflows. Each workflow defines all necessary steps to run a specific experiment or analysis.

You can execute any workflow using the following command:
```bash
python3 couch_potato/main.py --workflow workflows/workflow.yaml --output_dir path/to/output_dir
```

### Example
To reproduce **PixArt + Scenario** from Table 1:
```bash
python3 couch_potato/main.py --workflow workflows/from_scratch/pixart-sigma_scenario.yaml --output_dir output/pixart_scenario
```
The modifier and head correlation scores will be saved at:
```
output/pixart_scenario/artifacts/7_correlate/similarities.csv
```

### Options for Reproduction

We provide two types of workflows:

1. **From Predictions**: Fast. These workflows assume model predictions are already available and typically only perform correlation against gold-standard labels.
2. **From Scratch**: Slow. These workflows reproduce the full pipeline, including resource intensive steps such as image generation.

### Table 1

| Results | Workflow (From Predictions) | Workflow (From Scratch) |
|---|---|---|
| Bing | `workflows/bing.yaml`| TBD |
| PixArt + Word | `workflows/from_predictions/pixart-sigma_word.yaml` | TBD |
| PixArt + Sentence | `workflows/from_predictions/pixart-sigma_sentence.yaml` | TBD |
| PixArt + Definition | `workflows/from_predictions/pixart-sigma_definition.yaml` | TBD |
| PixArt + Scenario | `workflows/from_predictions/pixart-sigma_scenario.yaml` | TBD |
| Skip-gram (T) | `workflows/from_predictions/skip-gram.yaml` | TBD |
| Combined (T + V) | `workflows/from_predictions/combined.yaml` | TBD |
| ChatGPT (direct) | `workflows/from_predictions/chat-gpt.yaml` | TBD |


### Table 2

| Results | Workflow (From Predictions) | Workflow (From Scratch) |
|---|---|---|
| Concrete: PixArt + Scenario | `workflows/from_predictions/concrete_pixart-sigma_scenario.yaml`| TBD |
| Abstract: PixArt + Scenario | `workflows/from_predictions/abstract_pixart-sigma_scenario.yaml`| TBD |
| Concrete: Skip-gram | `workflows/from_predictions/concrete_skip-gram.yaml`| TBD |
| Abstract: Skip-gram | `workflows/from_predictions/abstract_skip-gram.yaml`| TBD |

### Table 3

| Results | Workflow (From Predictions) | Workflow (From Scratch) |
|---|---|---|
| SDXLBase + Word | `workflows/from_predictions/sdxl-base_word.yaml` | TBD |
| SDXLBase + Sentence | `workflows/from_predictions/sdxl-base_sentence.yaml` | TBD |
| SDXLBase + Definition | `workflows/from_predictions/sdxl-base_definition.yaml` | TBD |
| SDXLBase + Scenario | `workflows/from_predictions/sdxl-base_scenario.yaml` | TBD |
| JuggernautXL + Word | `workflows/from_predictions/sdxl-juggernaut_word.yaml` | TBD |
| JuggernautXL + Sentence | `workflows/from_predictions/sdxl-juggernaut_sentence.yaml` | TBD |
| JuggernautXL + Definition | `workflows/from_predictions/sdxl-juggernaut_definition.yaml` | TBD |
| JuggernautXL + Scenario | `workflows/from_predictions/sdxl-juggernaut_scenario.yaml` | TBD |
| PixArt + Word | `workflows/from_predictions/pixart-sigma_word.yaml` | TBD |
| PixArt + Sentence | `workflows/from_predictions/pixart-sigma_sentence.yaml` | TBD |
| PixArt + Definition | `workflows/from_predictions/pixart-sigma_definition.yaml` | TBD |
| PixArt + Scenario | `workflows/from_predictions/pixart-sigma_scenario.yaml` | TBD |


Please note that not all results can be reproduced exactly due to external or practical constraints. For example:

- **Bing image retrieval is non-deterministic**: Image results may vary across runs, as the Bing API does not support a fixed random seed or guarantee consistent results.
- **Skip-gram training corpus**: Due to size constraints, we cannot share the full preprocessed text corpus used to train the skip-gram model.

Despite these limitations, the provided workflows replicate the structure and logic of our experiments, making it possible to reproduce the overall behavior and trends reported in the paper.
