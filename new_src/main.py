from runner import Runner
from helpers.storage_helper import StorageHelper

if __name__ == "__main__":
    config_file = "workflow_config.yaml"
    workflow_config = StorageHelper.load_yaml(config_file)
    runner = Runner(workflow_config)
    runner.run()
