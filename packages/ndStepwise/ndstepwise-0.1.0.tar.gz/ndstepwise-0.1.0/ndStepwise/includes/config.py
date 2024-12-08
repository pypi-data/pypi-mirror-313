from ndStepwise.includes.logging import setup_logger

class Config:
    def __init__(self, dataset):
        self.settings = {}
        self.model_path = 'C:\\Users\\maxdi\\OneDrive\\Documents\\uni_honours\\models'
        self.log = setup_logger(dataset)