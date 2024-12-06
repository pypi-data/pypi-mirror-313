import random
from moviepy.editor import VideoFileClip
from bgeditor.dao.FFmpeg import merge_list_video
from bgeditor.common.utils import get_dir, always_even, get_files_in_folder, remove
import uuid
import os
import  json, subprocess
def get_video_info(video_path):
    clip = VideoFileClip(video_path)
    duration=clip.duration
    fps=clip.fps
    width, height=clip.size
    nb_frames=fps*duration
    return fps, nb_frames, width, height

def zoom_in(video_path, max_zoom, x=0,y=0, base_zoom=1.0, output_wh=[], is_hfilp=False, is_del=True):
    fps, duration, width, height=get_video_info(video_path)
    scale_factor=4
    zoom_speed=(max_zoom-base_zoom)/duration
    base_zoom2 = base_zoom + 0.001
    print(f"{max_zoom},{base_zoom},{zoom_speed}")
    zoom_point_x = scale_factor*width/2
    zoom_point_y = scale_factor * height / 2
    zoom_point_x+=x
    zoom_point_y+=y
    if output_wh and len(output_wh) > 1:
        width=output_wh[0]
        height=output_wh[1]
    hfilp_cmd = "hflip,"
    if not is_hfilp:
        hfilp_cmd = ""
    clip_output_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + '-zoom_in.mp4')
    cmd=f"ffmpeg -y -i \"{video_path}\" -vf \"{hfilp_cmd}fps={fps},scale=4*iw:-1,zoompan=z='if(lt(pzoom,{base_zoom}),{base_zoom}, min({max_zoom},pzoom+{zoom_speed}))':x={x}:y={y}:d=1:s={width}x{height}:fps={fps}\" -c:v libx264 -pix_fmt yuv420p \"{clip_output_path}\""
    print(cmd)
    subprocess.call(cmd, shell=True)
    if is_del:
        remove(video_path)
    return clip_output_path
def pan(video_path, zoom_factor, direction='left',output_wh=[], is_hfilp=False, is_del=True):
    fps, nb_frames, width, height=get_video_info(video_path)
    if output_wh and len(output_wh) > 1:
        width=output_wh[0]
        height=output_wh[1]
    scale_w = always_even(zoom_factor*width)
    scale_h = always_even(zoom_factor*height)
    duration = nb_frames / fps
    lx=scale_w-width
    ly=scale_h-height
    speed= lx/duration
    speedy = ly / duration
    x_value=f"-{lx}+t*{speed}"
    y_value=ly/2
    if direction == 'right':
        lx=0
        x_value=f"{lx}-t*{speed}"
        y_value = -1*(ly / 2)
    if direction== 'left':
        x_value = f"-{lx}+t*{speed}"
        y_value = -1*(ly / 2)
    if direction=='up':
        x_value=-1*(lx/2)
        ly=0
        y_value=f"{ly}-t*{speedy}"
    if direction=='down':
        x_value=-1*(lx/2)
        y_value=f"-{ly}+t*{speedy}"
    hfilp_cmd = f"hflip[vtmp];[vtmp]"
    if not is_hfilp:
        hfilp_cmd = ""
    clip_output_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + '-pan.mp4')
    cmd = f" ffmpeg -y -i \"{video_path}\" -i \"{video_path}\" -filter_complex \"[0:v]scale=5*{width}:5*{height}[bg];[1:v]{hfilp_cmd}scale=5*{scale_w}:5*{scale_h}[v1];[bg][v1]overlay={x_value}:{y_value}[out1];[out1]scale={width}:{height}[out]\" -map [out] -map ?0:a  -c:v libx264 -pix_fmt yuv420p \"{clip_output_path}\""
    print(cmd)
    subprocess.call(cmd, shell=True)
    if is_del:
        remove(video_path)
    return clip_output_path
def zoom_out(video_path, max_zoom, x=0, y=0, base_zoom=1.0,output_wh=[], is_hfilp=False, is_del=True):
    fps, duration, width, height = get_video_info(video_path)
    scale_factor = 4
    zoom_speed = (max_zoom - base_zoom) / (duration/2)
    base_zoom2=base_zoom+0.001
    zoom_point_x = scale_factor * width / 2
    zoom_point_y = scale_factor * height / 2
    zoom_point_x += x
    zoom_point_y += y
    hfilp_cmd="hflip,"
    if not is_hfilp:
        hfilp_cmd=""
    if output_wh and len(output_wh) > 1:
        width=output_wh[0]
        height=output_wh[1]
    clip_output_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + '-zoom-out.mp4')
    cmd = f"ffmpeg -y -i \"{video_path}\" -vf \"{hfilp_cmd}fps={fps},scale=4*iw:-1,zoompan=z='if(lte(pzoom,{base_zoom}),{max_zoom},max({base_zoom2}, pzoom-{zoom_speed}))':x={x}:y={y}:d=1:s={width}x{height}:fps={fps}\" -c:v libx264 -pix_fmt yuv420p \"{clip_output_path}\""
    print(cmd)
    subprocess.call(cmd, shell=True)
    if is_del:
        remove(video_path)
    return clip_output_path

def split_video(video_path, duration=10):
    prefix= "split-"+str(uuid.uuid4())
    output_path=os.path.join(get_dir('coolbg_ffmpeg'),f"{prefix}-%d.mp4")
    cmd=f"ffmpeg -i \"{video_path}\" -c copy -f segment -segment_time {duration} -reset_timestamps 1 \"{output_path}\""
    print(cmd)
    subprocess.call(cmd, shell=True)
    rs=get_files_in_folder(get_dir('coolbg_ffmpeg'),prefix)
    return rs
def apply_vf_effect(video_path, output_wh=[], is_flip=False, max_zoom=1.5, base_zoom=1.1):
    random_x=random.randint(0,100)
    random_y = random.randint(0, 100)
    effect=random.choice(["pan-left","pan-right","pan-up","pan-down","zoom-in","zoom-out"])
    if effect=="pan-left":
        return pan(video_path, base_zoom, direction='left',output_wh=output_wh, is_hfilp=is_flip)
    if effect=="pan-right":
        return pan(video_path, base_zoom, direction='right',output_wh=output_wh, is_hfilp=is_flip)
    if effect=="pan-up":
        return pan(video_path, base_zoom, direction='up',output_wh=output_wh, is_hfilp=is_flip)
    if effect=="pan-down":
        return pan(video_path, base_zoom, direction='down',output_wh=output_wh, is_hfilp=is_flip)
    if effect == "zoom-in":
        return zoom_in(video_path, max_zoom, x=random_x, y=random_y, base_zoom=base_zoom,output_wh=output_wh, is_hfilp=is_flip)
    if effect == "zoom-out":
        return zoom_out(video_path, max_zoom, x=random_x, y=random_y, base_zoom=base_zoom,output_wh=output_wh, is_hfilp=is_flip)


def auto_apply_vf_effect(video_path, output_wh=[], is_flip=False, max_zoom=1.5, base_zoom=1.1, duration_seg=10):
    list_seq_video=split_video(video_path, duration_seg)
    arr_vid=[]
    for item in list_seq_video:
        arr_vid.append(apply_vf_effect(item,output_wh,is_flip,max_zoom=max_zoom, base_zoom=base_zoom))
    rs=merge_list_video(arr_vid)
    return rs

# x=auto_apply_vf_effect(r"C:\Users\Hoa Bui\Downloads\Snapinsta.app_video_434469431_900455811767381_8904755832968059764_n.mp4",output_wh=[],is_flip=True,  max_zoom=1.3, base_zoom=1.15, duration_seg=5)
# print(x)