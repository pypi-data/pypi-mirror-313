import json
import os.path
import random
import uuid

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx import fadein, fadeout
from os import listdir
from os.path import isfile, join,basename
from bgeditor.common.utils import get_dir
from bgeditor.dao.FFmpeg import merge_list_video, check_video_ok
import zipfile

def zip_video_file(arr_path):
    parent_path=os.path.dirname(arr_path[0])
    zip_path=os.path.join(parent_path, uuid.uuid4().hex+"-video.zip")
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for _path in arr_path:
        zipf.write(_path, os.path.basename(_path))
    print(zipf.namelist())
    zipf.close()
    return zip_path
def extract_zip_files(zip_path):
    arr_files=None
    try:
        zipf = zipfile.ZipFile(zip_path, 'r')
        parent_path = os.path.join(os.path.dirname(zip_path),f"zipx-{uuid.uuid4().hex}")
        arr_files=[os.path.join(parent_path, f) for f in zipf.namelist()]
        zipf.extractall(parent_path)
        zipf.close()
    except:
        pass
    return arr_files
def split_videos(video_path,sub=1):
    clip = VideoFileClip(video_path, audio=False)
    w, h =clip.size
    if w != 1920 or h != 1080:
        clip = clip.resize((1920, 1080))
    c1 = clip.subclip(0, sub)
    c2 = clip.subclip(sub, -1*sub)
    c3 = clip.subclip(-1*sub)
    c1_path = os.path.join(get_dir("coolbg_ffmpeg"), "1c-"+uuid.uuid4().hex + "-c1.mp4")
    c2_path = os.path.join(get_dir("coolbg_ffmpeg"), "2c-"+uuid.uuid4().hex + "-c2.mp4")
    c3_path = os.path.join(get_dir("coolbg_ffmpeg"), "3c-"+uuid.uuid4().hex + "-c3.mp4")

    c1.write_videofile(c1_path,  fps=30, codec='libx264', audio=False)
    c2.write_videofile(c2_path,  fps=30, codec='libx264', audio=False)
    c3.write_videofile(c3_path,  fps=30, codec='libx264', audio=False)
    return [c1_path, c2_path, c3_path]
def transistion_video(video_path_1, video_path_2,is_delete=False):
    try:
        rs_path = os.path.join(get_dir("coolbg_ffmpeg"),uuid.uuid4().hex+"-tran.mp4")
        cmd=f"ffmpeg -i \"{video_path_1}\" -i \"{video_path_2}\" -filter_complex \"[0:v][1:v]xfade=transition=fade:duration=1:offset=0 [v1]\" -map [v1] -c:v libx264 -crf 23 -flags global_header -pix_fmt yuv420p -b:v 4M \"{rs_path}\""
        print(cmd)
        os.system(cmd)
        if is_delete:
            os.remove(video_path_1)
            os.remove(video_path_2)
    except:
        rs_path=None
        pass
    return rs_path


def make_footage_video(arr_splited_video=[]):
    items=[]
    i=0
    cnt_err_vid=0
    while i < len(arr_splited_video):
        if i == 0:
            print("skipp append first video")
            # items.append(arr_splited_video[i][0])
        if check_video_ok(arr_splited_video[i][1]):
            items.append(arr_splited_video[i][1])
        else:
            cnt_err_vid += 1
        if i == len(arr_splited_video)-1:
            if check_video_ok(arr_splited_video[i][2]):
                items.append(arr_splited_video[i][2])
            else:
                cnt_err_vid += 1
        else:
            if i > 60:
                #skip render transistion
                if check_video_ok(arr_splited_video[i][2]):
                    items.append(arr_splited_video[i][2])
                else:
                    cnt_err_vid += 1
                if check_video_ok(arr_splited_video[i+1][0]):
                    items.append(arr_splited_video[i+1][0])
                else:
                    cnt_err_vid += 1
            else:
                trans_vid_path = transistion_video(arr_splited_video[i][2], arr_splited_video[i + 1][0], is_delete=False)
                if check_video_ok(trans_vid_path):
                    items.append(trans_vid_path)
                else:
                    cnt_err_vid += 1
        i += 1
    if cnt_err_vid>len(arr_splited_video)/2:
        print("super error break")
        return None
    for i in range(cnt_err_vid):
        print("add more video to fix error")
        items.append(items[i % (len(items)-1)+1])
    print("list-----mergs")
    return merge_list_video(items)
