

import os
from bgeditor.common.utils import get_dir, download_file
from moviepy.editor import *
import uuid
from cloudflare import CloudFlareHelper
from gbackup import DriverHelper
import requests

def get_video_aspect_ratio(w, h, tolerance=0.1):
    # Danh sách các tỉ lệ tiềm năng
    aspect_ratios = [(16, 9), (9, 16), (1, 1)]

    min_error = float('inf')  # Khởi tạo sai số tối thiểu với giá trị vô cực
    best_aspect_ratio = None

    for ratio in aspect_ratios:
        target_ratio = ratio[0] / ratio[1]
        actual_ratio = w / h
        error = abs(actual_ratio - target_ratio)

        if error <= tolerance and error < min_error:
            min_error = error
            best_aspect_ratio = ratio

    if best_aspect_ratio:
        return f"{best_aspect_ratio[0]}:{best_aspect_ratio[1]}"
    else:
        closest_ratio = min(aspect_ratios, key=lambda x: abs(x[0] / x[1] - actual_ratio))
        return f"{closest_ratio[0]}:{closest_ratio[1]}"

def get_proxy_iproyal():
    proxy_tmp = f"http://victor69:dota2hoabt2@geo.iproyal.com:12321"
    proxies = {"http": proxy_tmp, "https": proxy_tmp}
    return proxies

def get_download_nwm_tiktok(url, retries=3):
    try:
        video_id=url.split('/')[-1]
        urld = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        proxies=get_proxy_iproyal()
        headers={'user-agent':'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'}
        res=requests.get(urld, headers=headers, proxies=proxies).json()
        # print(res)
        data=res['aweme_list'][0]
        nwm_video_url_HQ= data['video']['bit_rate'][0]['play_addr']['url_list'][0]
        return nwm_video_url_HQ
    except:
        if retries > 1:
            return get_download_nwm_tiktok(url,retries-1)
        pass
    return None

def download_ytdlp(videoId):
    videoId = videoId.strip()
    result = get_dir("download",f"{videoId}.webm")
    cmd = f"yt-dlp -f bv+ba/b -o {result} {videoId}"
    os.system(cmd)
    return result
def download_tiktok_video(video_url):
    download_url = get_download_nwm_tiktok(video_url)
    return download_file(download_url,None,"mp4")
def get_thumbs(video_path, duration):
    number_get_thumb = (duration/10)
    if number_get_thumb <1:
        number_get_thumb=1
    video_rs= os.path.join(get_dir("results"), f"{str(uuid.uuid4())}_animaton_thumbs.webm")
    tmp_thumbs = os.path.join(get_dir("coolbg_ffmpeg"), f"{str(uuid.uuid4())}-thumbs%03d.jpg")
    thumb_path =  os.path.join(get_dir("results"), f"{str(uuid.uuid4())}-thumb.jpg")
    cmd_get_thumb = f"ffmpeg -i \"{video_path}\" -ss {duration/2} -filter:v scale=\"iw/2:ih/2\" -frames:v 1 \"{thumb_path}\""
    os.system(cmd_get_thumb)
    cmd_get_thumbs = f"ffmpeg -i \"{video_path}\"  -vf fps=1/{number_get_thumb} \"{tmp_thumbs}\""
    os.system(cmd_get_thumbs)
    cmd_create_animation_thumbs=f"ffmpeg -y -framerate 3 -i \"{tmp_thumbs}\" -filter:v scale=\"iw/2:ih/2\" \"{video_rs}\""
    os.system(cmd_create_animation_thumbs)
    os.system(f"rm -rf {tmp_thumbs.replace('%03d','*')}")
    return thumb_path, video_rs
def process_video_sd(video_path):
    rs = VideoFileClip(video_path)
    duration = rs.duration
    width, height = rs.size
    ratio = get_video_aspect_ratio(width,height)
    thumb_path, thumb_video=get_thumbs(video_path, duration)
    cf = CloudFlareHelper("moonseo-source")
    dh = DriverHelper()
    download_link = dh.upload_file_auto("moonseo",[video_path])[0]
    if "None"==download_link:
        download_link = cf.upload(video_path,'download')
    thumb_link = cf.upload(thumb_path, 'thumb')
    animation_thumb_link = cf.upload(thumb_video,'ani_thumb')
    data = {
        "duration": duration,
        "width": width,
        "height": height,
        "ratio": ratio,
        "download_link": download_link,
        "thumb_link": thumb_link,
        "animation_thumb_link": animation_thumb_link
    }
    os.unlink(thumb_path)
    os.unlink(thumb_video)
    return data


# rs=process_video_sd(r"C:\Users\Hoa Bui\AppData\Local\Temp\Hoa_Bui\download\ddcc333f-65aa-45c6-8e44-378d334605bf.mp4")
# rs=download_tiktok_video("https://www.tiktok.com/@deanscheider.offfical/video/7281227303630376238")
# print(rs)
