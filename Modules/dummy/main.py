import os
from Modules.dummy.example import test
from WebAnalyzer.utils.media import frames_to_timecode

class Dummy:
    model = None
    result = None
    path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        # TODO
        #   - initialize and load model here
        model_path = os.path.join(self.path, "model.txt")
        self.model = open(model_path, "r")

    def inference_by_image(self, image_path):
        result = []
        # TODO
        #   - Inference using image path

        # result sample
        result = {"frame_result": [
            {
                # 1 bbox & multiple object
                'label': [
                    {'description': 'person', 'score': 1.0},
                    {'description': 'chair', 'score': 1.0}
                ],
                'position': {
                    'x': 0.0,
                    'y': 0.0,
                    'w': 0.0,
                    'h': 0.0
                }
            },
            {
                # 1 bbox & 1 object
                'label': [
                    {'description': 'car', 'score': 1.0},
                ],
                'position': {
                    'x': 100.0,
                    'y': 100.0,
                    'w': 100.0,
                    'h': 100.0
                }
            }
        ]}
        self.result = result

        return self.result

    def inference_by_video(self, frame_path_list, video_info):
        results = []

        fps = video_info['fps']
        for idx, frame_path in enumerate(frame_path_list):
            result = self.inference_by_image(frame_path)
            result["frame_number"] = idx + 1
            result["timestamp"] = frames_to_timecode((idx + 1) * fps, fps)
            results.append(result)

        self.result = results

        return self.result

    def inference_by_audio(self, audio_path, video_info):
        result = []
        # TODO
        #   - Inference using image path
        #   -
        result = {"audio_result": [
            {
                # 1 timestamp & multiple class
                'label': [
                    {'score': 1.0, 'description': 'class_name'},
                    {'score': 1.0, 'description': 'class_name'}
                ],
                'timestamp': "00:00:01:00"
            },
            {
                # 1 timestamp & 1 class
                'label': [
                    {'score': 1.0, 'description': 'car'}
                ],
                'timestamp': "00:00:01:00"
            }
        ]}
        self.result = result

        return self.result

    def inference_by_text(self, data, video_info):
        result = []
        # TODO
        #   - Inference using image path
        #   -
        result = {"text_result": [
            {
                # 1 timestamp & multiple class
                'label': [
                    {'score': 1.0, 'description': 'word_name'},
                    {'score': 1.0, 'description': 'word_name'}
                ],
            },
            {
                # 1 timestamp & 1 class
                'label': [
                    {'score': 1.0, 'description': 'word_name'}
                ],
            }
        ]}
        self.result = result

        return self.result