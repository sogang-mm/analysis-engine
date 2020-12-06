# -*- coding: utf-8 -*-
from AnalysisModule.config import DEBUG
from AnalysisModule.celerys import app
from celery.signals import worker_init, worker_process_init
from billiard import current_process


@worker_init.connect
def model_load_info(**__):
    print("====================")
    print("Worker Analyzer Initialize")
    print("====================")


@worker_process_init.connect
def module_load_init(**__):
    global analyzer

    if not DEBUG:
        worker_index = current_process().index
        print("====================")
        print(" Worker Id: {0}".format(worker_index))
        print("====================")

    # TODO:
    #   - Add your model
    #   - You can use worker_index if you need to get and set gpu_id
    #       - ex) gpu_id = worker_index % TOTAL_GPU_NUMBER
    from Modules.dummy.main import Dummy
    analyzer = Dummy()


@app.task
def analyzer_by_image(file_path):
    result = analyzer.inference_by_image(file_path)
    return result

@app.task
def analyzer_by_video(data, video_info, analysis_type):
    if analysis_type == 'video' :
        result = analyzer.inference_by_video(data, video_info)
    elif analysis_type == 'audio' :
        result = analyzer.inference_by_audio(data, video_info)
    elif analysis_type == 'text' :
        result = analyzer.inference_by_text(data, video_info)
    return result


# For development version
if DEBUG:
    print("====================")
    print("Development")
    print("====================")
    module_load_init()