import datasets

class CustomDataset(datasets.Dataset):
    def __init__(self, data_dir):
        self.dataset = datasets.load_dataset("imagefolder", data_dir=data_dir)
    
    def get_dataset(self):
        return self
