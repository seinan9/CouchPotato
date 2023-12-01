#!bin/sh

data_dir=$1

# Create data directory
mkdir -p $1/data/datasets
mkdir -p $1/data/models
mkdir -p $1/data/output

# Create and activate virtual environment
python -m venv ./venv
source venv/bin/activate

# TODO: Install dependencies
