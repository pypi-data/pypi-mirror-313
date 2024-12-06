from importlib import metadata
from os.path import dirname

__version__ = metadata.version(__package__)
BASEDIR = dirname(__file__)

commands_doc = """
   torchl_onnx                  Convert a trained PyTorch Lightning model to ONNX
   torchl_predict               Run PyTorch Lightning predict on a trained model
   torchl_train                 Train a model using PyTorch Lightning
"""
