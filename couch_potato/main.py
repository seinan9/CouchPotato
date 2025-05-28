import argparse
import logging
from pathlib import Path

from couch_potato.core.engine import Engine
from couch_potato.core.utils import load_yaml, save_yaml, setup_logging

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Run the specified workflow YAML file."
    )
    argparser.add_argument(
        "-f", "--file", required=True, help="Path to workflow YAML file."
    )
    argparser.add_argument(
        "-o", "--output_dir", required=True, help="Directory to store outputs and logs."
    )
    args = argparser.parse_args()

    # Parse and create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup logger
    setup_logging(output_dir / "workflow.log")

    # Check if this is potentially a rerun or extension
    workflow_output_file = output_dir / "workflow.yaml"
    if workflow_output_file.exists():
        logging.info(
            "Detected existing workflow.yaml in output directory. "
            "This run may be a continuation, rerun, or extension of a previous run."
        )

    # Load workflow
    workflow = load_yaml(args.file)

    # Save workflow in output directory
    save_yaml(workflow, workflow_output_file)

    # Run the workflow engine
    engine = Engine(workflow, output_dir)
    engine.start()
