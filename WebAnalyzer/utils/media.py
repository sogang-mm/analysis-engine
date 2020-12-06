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


def get_video_dirpath(video_url):
    if "http" in video_url:
        dirpath = os.path.join(settings.MEDIA_ROOT, get_directory(), str(video_url).split("/")[-1]).split(".")[0]
        url = os.path.join(get_directory(), str(video_url).split("/")[-1]).split(".")[0]
    else :
        dirpath = video_url.split(".")[0]
        url = dirpath.replace(settings.MEDIA_ROOT, "")

    if not os.path.exists(dirpath) :
        os.mkdir(dirpath)
    else :
        timestamp = get_timestamp()
        dirpath = dirpath + "_" + timestamp
        url = dirpath.replace(settings.MEDIA_ROOT, "")

        os.mkdir(dirpath)

    return dirpath, url


def get_audio_filename(filename, ext):
    path = os.path.join(settings.MEDIA_ROOT, get_directory(), filename + ext)
    url = os.path.join(get_directory(), filename + "_"  + ext)

    if not os.path.exists(path):
        timestamp = get_timestamp()
        url = os.path.join(get_directory(), filename + "_" + timestamp + ext)
        path = os.path.join(settings.MEDIA_ROOT, get_directory(), filename + "_" + timestamp + ext)
        os.mkdir(path)

    return path, url

def extract_audio(video_url):
    video_name = get_filename(video_url)
    dir_path = get_directory()
    path, url = get_audio_filename(video_name, ".mp3")
    audio_path = os.path.join(dir_path, path)

    command = "ffmpeg -y -i {} -vn -acodec copy {}".format(video_url, audio_path)
    os.system(command)

    return url


def extract_frames(video_url, extract_fps):
    frame_dirpath, url = get_video_dirpath(video_url)

    command = "ffmpeg -y -hide_banner -loglevel panic -i {} -vsync 2 -q:v 0 -vf fps={} {}/%d.jpg".format(video_url, extract_fps, frame_dirpath)
    os.system(command)

    framecount = len(os.listdir(frame_dirpath))
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
    json_metadata['fps'] = video_capture.get(cv2.CAP_PROP_FPS)
    video_capture.release()

    return json_metadata

def frames_to_timecode (frames, fps):
    h = int(frames / 86400)
    m = int(frames / 1440) % 60
    s = int((frames % 1440)/fps)
    f = frames % 1440 % fps
    return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))