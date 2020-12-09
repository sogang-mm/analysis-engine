import json
import os
import ast
from Modules.dummy.example import test

class Dummy:
    model = None
    result = None
    path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        # TODO
        #   - initialize and load model here
        model_path = os.path.join(self.path, "model.txt")
        self.model = open(model_path, "r")

    def inference_by_data(self, aggregation_result):
        aggregation_result = ast.literal_eval(aggregation_result)
        result = []
        # TODO
        #   - Inference using aggregation result
        #   - how to use aggregation_result
        #     for data in aggregation_result :
        #         aggregation_result[data] # Using this data
        result = {"aggregation_result": [
            {
                # 1 timestamp & multiple class
                'label': [
                    {'description': 'word_name', 'score': 1.0},
                    {'description': 'word_name', 'score': 1.0}
                ],
            },
            {
                # 1 timestamp & 1 class
                'label': [
                    {'description': 'word_name', 'score': 1.0}
                ],
            }
        ]}
        self.result = result

        return self.result