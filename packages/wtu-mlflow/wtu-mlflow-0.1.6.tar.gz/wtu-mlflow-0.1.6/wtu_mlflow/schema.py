from typing import Dict
import numpy as np


class Schema(Dict[str, np.ndarray]):
    def __init__(self, params: Dict[str, np.ndarray]):
        super().__init__(params)


class ModelInputOutput:
    def __init__(self, input_schema: Schema, output_schema: Schema):
        self.inputs = input_schema
        self.outputs = output_schema
