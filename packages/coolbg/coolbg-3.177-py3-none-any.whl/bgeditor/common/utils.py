import time

import requests
import os
import tempfile
from moviepy.config import IMAGEMAGICK_BINARY
from moviepy.tools import subprocess_call
import uuid
from gbackup import Client
from gbackup import DriverHelper
import numpy as np
import subprocess ,json
from os import listdir
from os.path import isfile, join
from moviepy.editor import VideoFileClip,AudioFileClip
def always_even(number):
    number = int(number)
    if number % 2 != 0:
        number += 1
    return number
def get_files_in_folder(folder_path,prefix=None):
    if prefix:
        onlyfiles = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f)) and prefix in f]
    else:
        onlyfiles = [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]
    sorted_items = sorted(onlyfiles, key=os.path.getctime)
    return sorted_items
def upload_file_old(path):
    public_folder_id = "1kl75TP6zJiuFBdjhJUw1GHhdcIEjueoE"
    file_name = os.path.basename(path)
    return Client("/u02/drive_config/public_config/coca_idrive.json", "upload", path, "").upload_file(file_name, path, public_folder_id)
def upload_static_file(path):
    url = "http://api-magicframe.automusic.win/resource-static/upload"
    payload = {}
    files = [
        ('file_input', (os.path.basename(path),
                        open(path, 'rb'),
                        'image/jpeg'))
    ]
    headers = {}
    return requests.request("POST", url, headers=headers, data=payload, files=files).json()


def upload_file(path, retries=3):
    dh = DriverHelper()
    x = dh.upload_file_auto("studio-result", [path])
    rs = x[0].split(";;")[-1]
    if rs == 'None':
        if retries > 0:
            rs = dh.upload_file_r2(path)
    return rs
def upload_file_resource(path):
    dh = DriverHelper()
    x = dh.upload_file_auto("studio", [path])
    return x[0].split(";;")[-1]
def remove(path):
    try:
        os.remove(path)
    except:
        pass
def download_file(url, root_dir=None, ext= None, cached_list=None):
    file_path = None
    if cached_list and url in cached_list:
        print(f"get file from cached: {url}")
        file_path = cached_list[url]
    if not file_path:
        dh = DriverHelper()
        file_path = dh.download_file(url, root_dir, ext)
        if cached_list:
            cached_list[url]=file_path
    return file_path
def cache_file(url):
    rs = None
    try:
        rs = os.path.join(get_dir('cached'), os.path.basename(url))
        if os.path.exists(rs):
            return rs #cached
        r = requests.get(url)
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs = None
        pass
    return rs

def get_dir(dir):
    tmp_download_path = os.path.join(tempfile.gettempdir() ,dir)
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path
def hex_to_rgb(hex_string):
    return np.array(list(int(hex_string.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)))

def change_color_alpha(img, hex_color):
    rgb_color = hex_to_rgb(hex_color)
    alpha_arr = img[:,:,3]
    new_img = np.zeros( (100, 100, 4), dtype='uint8')
    shape_alpha= np.shape(alpha_arr)
    for i in range(shape_alpha[0]):
        for j in range(shape_alpha[1]):
            if alpha_arr[i, j] != 0:
                new_img[i, j, 0] = rgb_color[0]
                new_img[i, j, 1] = rgb_color[1]
                new_img[i, j, 2] = rgb_color[2]
                new_img[i, j, 3] = alpha_arr[i, j]
    return new_img

def probe_file(filename):
    cmnd = ['ffprobe', '-print_format', 'json', '-show_streams', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    rs1=json.loads(out)
    return rs1
def normal_audio(file_path, is_del=True):
    obj = probe_file(file_path)
    rs= None
    if "streams" in obj:
        for stream in obj['streams']:
            if stream['codec_type'] == "audio":
                if stream['codec_name'] != "mp3" or int(stream['bit_rate']) != 128000 or int(
                        stream['sample_rate']) != 44100:
                    tmp_file=os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4())+".mp3")
                    cmd = f"ffmpeg -i \"{file_path}\" -b:a 128000 -ar 44100 -c:a mp3 \"{tmp_file}\""
                    os.system(cmd)
                    if is_del:
                        os.remove(file_path)
                    rs=tmp_file
                else:
                    rs=file_path
    return rs
def create_text_img(
        txt=None,
        filename=None,
        size=None,
        color="black",
        bg_color="transparent",
        fontsize=None,
        font="Courier",
        stroke_color=None,
        stroke_width=1,
        method="label",
        kerning=None,
        align="center",
        interline=None,
        tempfilename=None,
        temptxt=None,
        remove_temp=True,
        print_cmd=False,
):
    if txt is not None:
        if temptxt is None:
            temptxt_fd, temptxt = tempfile.mkstemp(suffix=".txt")
            try:  # only in Python3 will this work
                os.write(temptxt_fd, bytes(txt, "UTF8"))
            except TypeError:  # oops, fall back to Python2
                os.write(temptxt_fd, txt)
            os.close(temptxt_fd)
        txt = "@" + temptxt
    else:
        # use a file instead of a text.
        txt = "@%" + filename

    if size is not None:
        size = (
            "" if size[0] is None else str(size[0]),
            "" if size[1] is None else str(size[1]),
        )

    cmd = [
        IMAGEMAGICK_BINARY,
        "-background",
        bg_color,
        "-fill",
        color,
        "-font",
        font,
    ]

    if fontsize is not None:
        cmd += ["-pointsize", "%d" % fontsize]
    if kerning is not None:
        cmd += ["-kerning", "%0.1f" % kerning]
    if stroke_color is not None:
        cmd += ["-stroke", stroke_color, "-strokewidth", "%.01f" % stroke_width]
    if size is not None:
        cmd += ["-size", "%sx%s" % (size[0], size[1])]
    if align is not None:
        cmd += ["-gravity", align]
    if interline is not None:
        cmd += ["-interline-spacing", "%d" % interline]

    if tempfilename is None:
        tempfile_fd, tempfilename = tempfile.mkstemp(suffix=".png",prefix='txt_', dir=get_dir("coolbg_ffmpeg"))
        os.close(tempfile_fd)

    cmd += [
        "%s:%s" % (method, txt),
        "-type",
        "truecolormatte",
        "PNG32:%s" % tempfilename,
    ]

    if print_cmd:
        print(" ".join(cmd))

    try:
        subprocess_call(cmd, logger=None)
    except (IOError, OSError) as err:
        error = (
            f"MoviePy Error: creation of {filename} failed because of the "
            f"following error:\n\n{err}.\n\n."
            "This error can be due to the fact that ImageMagick "
            "is not installed on your computer, or (for Windows "
            "users) that you didn't specify the path to the "
            "ImageMagick binary. Check the documentation."
        )
        raise IOError(error)

    if remove_temp:
        if temptxt is not None and os.path.exists(temptxt):
            os.remove(temptxt)
    return tempfilename

def getVideoDuration(video_path):
    duration_f=0
    try:
        final_vid = VideoFileClip(video_path);
        duration_f = final_vid.duration
        final_vid.close()
    except:
        pass
    return duration_f
def getAudioDuration(audio_path):
    duration_f=0
    try:
        final_vid = AudioFileClip(audio_path);
        duration_f = final_vid.duration
        final_vid.close()
    except:
        pass
    return duration_f

