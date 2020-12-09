from AnalysisModule import settings

import os, datetime
import subprocess
import cv2

def get_directory():
    date_today = datetime.date.today()
    directory = date_today.strftime("%Y%m%d")
    return directory


def get_timestamp():
    date_now = datetime.datetime.now()
    timestamp = date_now.strftime("%H%M%S")
    return timestamp


def get_filename(path):
    return str(path).split("/")[-1].split(".")[0]


def get_video_dir_path(video_url):
    date_dir_path = os.path.join(settings.MEDIA_ROOT, get_directory())
    if not os.path.exists(date_dir_path):
        os.mkdir(date_dir_path)

    if "http" in video_url:
        dir_path = os.path.join(settings.MEDIA_ROOT, get_directory(), str(video_url).split("/")[-1]).split(".")[0]
        url = os.path.join(get_directory(), str(video_url).split("/")[-1]).split(".")[0]
    else :
        dir_path = video_url.split(".")[0]
        url = dir_path.replace(settings.MEDIA_ROOT, "")

    if not os.path.exists(dir_path) :
        os.mkdir(dir_path)
    else :
        timestamp = get_timestamp()
        dir_path = dir_path + "_" + timestamp
        url = dir_path.replace(settings.MEDIA_ROOT, "")

        os.mkdir(dir_path)

    return dir_path, url


def get_audio_filename(filename, ext):
    date_dir_path = os.path.join(settings.MEDIA_ROOT, get_directory())
    path = os.path.join(settings.MEDIA_ROOT, get_directory(), filename + ext)
    url = os.path.join(get_directory(), filename + "_"  + ext)

    if not os.path.exists(date_dir_path):
        os.mkdir(date_dir_path)

    if not os.path.exists(path):
        timestamp = get_timestamp()
        url = os.path.join(get_directory(), filename + "_" + timestamp + ext)
        path = os.path.join(settings.MEDIA_ROOT, get_directory(), filename + "_" + timestamp + ext)

    return path, url

def extract_audio(video_url):
    video_name = get_filename(video_url)
    dir_path = get_directory()
    path, url = get_audio_filename(video_name, ".mp3")
    audio_path = os.path.join(dir_path, path)
    
    command = "ffmpeg -y -i {} {}".format(video_url, audio_path)
    print(command)
    os.system(command)

    return url


def extract_frames(video_url, extract_fps):
    frame_dir_path, url = get_video_dir_path(video_url)

    command = "ffmpeg -y -hide_banner -loglevel panic -i {} -vsync 2 -q:v 0 -vf fps={} {}/%d.jpg".format(video_url, extract_fps, frame_dir_path)
    os.system(command)

    framecount = len(os.listdir(frame_dir_path))
    frame_url_list = []
    frame_path_list = []
    for frame_num in range(1, framecount + 1):
        path = settings.MEDIA_ROOT + os.path.join(url, str(frame_num) + ".jpg")
        frame_url_list.append(os.path.join(url, str(frame_num) + ".jpg"))
        frame_path_list.append(path)

    return frame_path_list, frame_url_list


def get_video_metadata(video_path):
    ffprobe_command = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', video_path]

    ffprobe_process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    metadata, error = ffprobe_process.communicate()
    metadata = metadata.decode("utf-8")

    infos = metadata.split("\n")
    json_metadata = {}
    for info in infos:
        if "=" in info:
            info = info.split("=")
            key = info[0]
            value = info[1]
            json_metadata[key] = value
    video_capture = cv2.VideoCapture(video_path)
    json_metadata['extract_fps'] = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    return json_metadata

def frames_to_timecode (frames, fps):
    h = int(frames / 86400)
    m = int(frames / 1440) % 60
    s = int((frames % 1440)/fps)
    f = frames % 1440 % fps
    return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))