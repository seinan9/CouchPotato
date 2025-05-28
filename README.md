# Couch Potato

This repository contains the code and data used for the ACL 2025 paper: "*A Couch Potato is not a Potato on a Couch: Visual Compositionality Prediction using Prompting Strategies and Image Generation for Adequate Image Retrieval*".

**Table of Contents**

- [Data](#data)
- [Installation](#installation)
- [Usage](#usage)
- [Reproducing Results from the Paper](#reproducing-results-from-the-paper)
- [License](#license)

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

### ChatGPT Predictions

The file `data/chatgpt_predictions.yaml` contains ChatGPT-generated compositionality predictions for each of the 88 target compounds.

### Concreteness Annotations

The file `data/concreteness_annotations.csv` includes human-annotated concreteness ratings for the 88 compound nouns used in our experiments.

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

## Usage

CouchPotato uses a modular **workflow system** based on YAML files. Each workflow defines a series of **nodes** (self-contained components) that are executed sequentially.

### How it Works

At the core is the `engine`, which loads a workflow, resolves variables, and runs each node step by step. Each **node** performs a single task (e.g., generating images, extracting features, computing correlations). You define nodes and their parameters in a YAML file, and then run the workflow via:

```bash
python couch_potato/main.py --workflow workflows/example.yaml --output_dir output/example
```

This command:

- Loads the workflow from workflows/example.yaml
- Creates the output structure under output/example
- Copies the workflow YAML into the output directory for reproducibility
- Runs (and logs) all nodes in the specified order
- Stores any artifacts in designated subdirectories

### Using Existing Nodes

The *couch_potato/task/nodes* directory contains all nodes used for the experiments in our paper. Each node is a Python class that inherits from Node (*couch_potato/core/node.py) and defines:

- A PARAMETERS dictionary specifying required inputs
- An __init__() method that handles these inputs
- A run() method that implements the nodes behavior

### Creating a Workflow

A workflow is a YAML file consisting of:

- Optional *global_parameters* shared across nodes
- A list of nodes with name and parameters

Each node corresponds to a Python module in task/nodes/, and its class name is derived from the module name.

Example:

TODO

The name must match the module in task.nodes, and the parameters must match the class’s PARAMETERS.

### YAML Variables

To simplify file path and directory references, you can use the following YAML variables:

|Variable|Description|
|---|---|
|`${this}`|The output directory of the current node|
|`${prev}`|The output directory of the previous node|
|`${node:<index>}`|The output directory of the specified node (e.g. `${node:3}`)|

These variables are automatically resolved by the engine.

Example:

### Creating New Nodes

To add a new node:
1. Create a new Python file in couch_potato/task/nodes/, e.g. my_node.py
2. Inherit from Node and define the required parameters and behavior:

TODO: Example

3. Reference it in a workflow:

TODO: Example

### Example Node and Workflow

Here is a minimal example node that just prints a message:

```python
from couch_potato.core.node import Node

class ExampleNode(Node):
    PARAMETERS = {"message": str}

    def __init__(self, message: str) -> None:
        self.message = message

    def run(self):
        print(self.message)
```

and here a workflow making use of it:

```yaml
nodes:
- name: example_node
  parameters:
    message: "Hello World!"
```

Use the following command to run the workflow:

        python couch_potato/main.py --workflow workflows/example.yaml --output_dir output/example

You should see:

        "Hello World!"

## Reproducing Results from the Paper


We provide workflow YAML files to reproduce most of the results reported in our paper.

Please note that not all results can be reproduced exactly due to external or practical constraints. For example:

- Images retrieved from Bing may vary between runs, as the underlying API does not guarantee consistent results or support a fixed random seed.
- We cannot share the full preprocessed text corpus used to train the skip-gram model due to its size.

Despite these limitations, the provided workflows closely replicate the original pipeline structure, allowing for a high-level reproduction of our experiments.

### Table 1

Each row in Table 1 of the paper can be reproduced by running the corresponding workflow file with `main.py`. The (final and intermediate) results can be found in the specified output directory under *artifacts*.

| Table 1 Result                | Workflow File                           |
|-----------------------------|------------------------------------------|
| Bing Images                 | `workflows/bing.yaml`                    |
| PixArt - Word Prompts       | `workflows/pixart_word.yaml`            |
| PixArt - Sentence Prompts   | `workflows/pixart_sentence.yaml`        |
| PixArt - Definition Prompts | `workflows/pixart_definition.yaml`      |
| PixArt - Scenario Prompts   | `workflows/pixart_scenario.yaml`        |

#### Example

To reproduce the **PixArt - Scenario Prompts** result:

        python couch_potato/main.py --workflow workflows/pixart_scenario.yaml --output_dir output/pixart_scenario

The modifier and head correlation can then be found under output/pixart_scenario/artifacts/7_correlation_calculator/similarities.csv

### Table 2

### Table 3

### Combining Textual and Visual

### Compounds by Concreteness

## License

