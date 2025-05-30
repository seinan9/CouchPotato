import csv
import os

import torch
import yaml
from natsort import natsorted
from PIL import Image


def load_targets(file_path: str) -> dict:
    # Load YAML file containing target compounds
    with open(file_path, "r", encoding="utf-8") as f:
        targets = yaml.safe_load(f)
    return targets


def load_sentences(file_path: str) -> list:
    # Read lines from a file (e.g., prompts or sentences)
    with open(file_path, "r", encoding="utf-8") as f:
        sentences = f.readlines()
    return sentences


def list_files(directory_path: str, include_extensions: bool) -> list[str]:
    # List files in directory sorted naturally, optionally strip file extensions
    files = natsorted(os.listdir(directory_path))
    if not include_extensions:
        files = [file.split(".")[0] for file in files]
    return files


def move_file(current_file_path, new_file_path):
    # Rename or move a file from current path to new path
    os.rename(current_file_path, new_file_path)


def load_image(file_path: str) -> Image.Image:
    # Load an image from disk using PIL
    image = Image.open(file_path)
    return image


def save_image(image: Image.Image, file_path: str) -> None:
    # Save a PIL image to disk
    image.save(file_path)


def load_vector(file_path: str) -> torch.Tensor:
    # Load a PyTorch tensor from file
    vector = torch.load(file_path)
    return vector


def save_vector(vector: torch.Tensor, file_path: str) -> None:
    # Save a PyTorch tensor to file
    torch.save(vector, file_path)


def load_csv(file_path: str) -> list:
    # Load CSV file as list of dictionaries (rows)
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        header = csv_reader.fieldnames
        for row in csv_reader:
            data.append(row)
    return data


def save_csv(header: list, values: list, file_path: str) -> None:
    # Save list of dicts to CSV file with specified header
    with open(file_path, "w", encoding="utf-8") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(values)
