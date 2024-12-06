import time

import requests, os, uuid
from bgeditor.common.utils import cache_file, download_file, upload_file, upload_static_file, get_dir, getVideoDuration
from moviepy.editor import *
from PIL import Image

def add_static_lyric(data, retries=3):
    try:
        obj = requests.post("http://api-magicframe.automusic.win/static-lyric/add", json=data).json()
        vid_id=None
        if "id" in obj:
            vid_id=obj["id"]
        else:
            if retries > 0:
                time.sleep(1)
                return add_static_lyric(data, retries-1)
    except:
        if retries > 0:
            time.sleep(1)
            return add_static_lyric(data, retries-1)
    return vid_id
def create_lyric_static(arr_comp, mix_data, font_url, lyric_lines=2, only_audio=0):
    path_img = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-comp-static-img.png")
    CompositeVideoClip(arr_comp).save_frame(path_img, 0)
    im = Image.open(path_img)
    rgb_im = im.convert('RGB')
    ejpg = path_img.replace(".png", ".jpg")
    rgb_im.save(ejpg)
    im.close()
    rgb_im.close()
    rs_static_img = upload_static_file(ejpg)
    arr_lyric_video_id=[]
    arr_static_lyric_data=[]
    if "success" in rs_static_img and rs_static_img['success'] == 1:
        # mix_data.pop(0)
        idx=0
        for item in mix_data:
            datainfo = {}
            datainfo['artist_name'] = item['artist_name']
            datainfo['song_name'] = item['song_name']
            datainfo['duration_ms'] = item['duration_ms']
            datainfo['idx'] = idx
            datainfo['vid_id'] = None
            datainfo['success'] = False
            if idx==0:
                datainfo['success']=True
                datainfo['vid_id'] = 1
            if idx > 0:
                data = {}
                data['audio_url'] = item['audio_url']
                data['lyric_sync'] = item['lyric_sync']
                data['group_number'] = lyric_lines
                data['bg_image'] = rs_static_img['url']
                data['artist_name'] = item['artist_name']
                data['song_name'] = item['song_name']
                data['font_url'] = font_url
                data['only_audio'] = only_audio
                data['idx']= idx
                # obj = requests.post("http://api-magicframe.automusic.win/static-lyric/add", json=data).json()
                # if "id" in obj:
                #     arr_lyric_video_id.append(obj['id'])
                vid_id = add_static_lyric(data)
                if vid_id:
                    datainfo['vid_id'] = vid_id
                    arr_lyric_video_id.append(vid_id)
            arr_static_lyric_data.append(datainfo)
            idx += 1
    return arr_lyric_video_id, arr_static_lyric_data

def wait_lyric_video(arr_id, wait_time=10*60):
    util_time = time.time() + wait_time
    arr_id_downloaded = []
    arr_rs = {}
    while time.time() < util_time and len(arr_id_downloaded) < len(arr_id):
        for idx in arr_id:
            if idx not in arr_id_downloaded:
                try:
                    obj = requests.get(f"http://api-magicframe.automusic.win/static-lyric/load/{idx}").json()
                    if "id" in obj and int(obj['status']) == 3:
                        arr_id_downloaded.append(idx)
                        path_video = download_file(obj['result'])
                        arr_rs[idx] = path_video
                        if len(arr_id_downloaded) == len(arr_id):
                            break
                except:
                    pass
        time.sleep(10)
    return arr_rs

def set_info_static_lyric_data(vid_id, data={}, arr_static_lyric_data=[]):
    def update_dict(target, updates):
        for key, value in updates.items():
            target[key] = value
    for item in arr_static_lyric_data:
        if item['vid_id'] == vid_id:
            update_dict(item, data)
            return True
    return False
def load_lyric_video(arr_id, arr_static_lyric_data=[], wait_time=10*60):
    arr_rs = wait_lyric_video(arr_id, wait_time)
    arr_retries = []
    arr_video_path = []
    arr_all = {}
    for idx in arr_id:
        arr_all[idx]=None
        if idx in arr_rs and getVideoDuration(arr_rs[idx])>0:
            arr_all[idx] = arr_rs[idx]
        else:
            obj = requests.get(f"http://api-magicframe.automusic.win/static-lyric/change-oa/{idx}").json()
            if "id" in obj:
                arr_retries.append(obj['id'])
                set_info_static_lyric_data(idx, {"vid_id": obj['id']}, arr_static_lyric_data)
    #retries if err
    if len(arr_retries)>0:
        arr_rs = wait_lyric_video(arr_retries, 5*60)
        for idx in arr_retries:
            if idx in arr_rs:
                arr_all[idx] = arr_rs[idx]

    for key, value in arr_all.items():
        duration_video = getVideoDuration(value)
        if value and duration_video>0:
            arr_video_path.append(value)
            set_info_static_lyric_data(key, {"success": True, "duration_real": duration_video}, arr_static_lyric_data)
    return arr_video_path