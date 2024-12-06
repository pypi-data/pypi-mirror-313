import random

import requests, uuid
from bgeditor.common.utils import cache_file, download_file, upload_file, upload_static_file, upload_file_resource
from bgeditor.dao.FootageHelper import split_videos, zip_video_file, extract_zip_files, make_footage_video
from gbackup import DriverHelper
from moviepy.editor import *
from bgeditor.common.utils import get_dir
import os
class FootageController:

    def __init__(self):
        self.cache_list_download={"1":"ok"}
        self.zip_loc="/tmp/user/download"
    def put_req_normalize_video(self, vid, arr_split_vids):
        zip_path = zip_video_file(arr_split_vids)
        dh = DriverHelper()
        x = dh.upload_file_auto("moonseo", [zip_path])
        vid['video_normalize']=x[0]
        url = f"https://moonseo.app/api/source/data/update"
        headers = {"platform": "autowin"}
        os.remove(zip_path)
        res = requests.post(url,headers=headers,json=vid).json()
        print(res)
    def load_source_data(self, vid_id):
        url=f"https://moonseo.app/api/source/data/load/{vid_id}"
        headers = {"platform": "autowin"}
        res = requests.get(url, headers=headers).json()
        return res

    def report_source_error(self, source_id, vid_id):
        print(f"report_source_error {source_id}/{vid_id}")
        url = f"https://moonseo.app/api/source/user/footage-report/{source_id}/{vid_id}"
        headers = {"platform": "autowin"}
        res = requests.get(url, headers=headers).json()

    def get_list_source(self, source_id, duration):
        url=f"https://moonseo.app/api/source/user/footage/{source_id}/{duration}"
        headers={"platform" : "autowin"}
        res=requests.get(url, headers=headers).json()
        arr_list_vid=[]
        cache_folder_vid={"0":[]}
        if res and res['status']==1:
            for vid in res['data']:
                arr_tmp_vid=cache_folder_vid.get(vid['id'])
                if arr_tmp_vid:
                    # arr_list_vid.append(arr_tmp_vid.copy()) khong trung effect
                    arr_list_vid.append(arr_tmp_vid) #tan dung render effect
                else:
                    arr_tmp_vid = self.normalize_vid_source(vid)
                    if arr_tmp_vid:
                        arr_list_vid.append(arr_tmp_vid)
                        cache_folder_vid[vid['id']] = arr_tmp_vid
                    else:
                        self.report_source_error(source_id, vid['id'])
            #delete all zip file
            os.system(f"rm -rf {self.zip_loc}/*.zip")
            return arr_list_vid
        return None

    def normalize_vid_source(self, vid):
        if not vid['video_normalize']:
            #reload source
            arr_rs=None
            res = self.load_source_data(vid['id'])
            if res and "video_normalize" in res and res['video_normalize']:
                zip_path = download_file(res['video_normalize'], ext='zip', cached_list=self.cache_list_download)
                arr_rs = extract_zip_files(zip_path)
                self.zip_loc = os.path.abspath(zip_path)
            else:
                video_path=download_file(vid['download_link'], ext='mp4')
                arr_split_vds=split_videos(video_path)
                self.put_req_normalize_video(vid, arr_split_vds)
                arr_rs = arr_split_vds
        else:
            zip_path = download_file(vid['video_normalize'], ext='zip', cached_list=self.cache_list_download)
            arr_rs = extract_zip_files(zip_path)
        return arr_rs

    def make_footage_videos(self, source_id, duration):
        arr_list_video= self.get_list_source(source_id, duration)
        if arr_list_video:
            return make_footage_video(arr_list_video)
        return None
    def check_and_remove_bg(self, arr_composite):
        def get_opacity(clip):
            opacity = 1.0
            if hasattr(clip, 'mask') and hasattr(clip.mask, 'get_frame'):
                mask_frame = clip.mask.get_frame(0)
                opacity = mask_frame.max()
            return opacity

        arr_tmp=[]
        for item in arr_composite:
           if item.size[0] == 1920 and item.start == 0 and item.duration>500 and get_opacity(item) == 1.0:
               # arr_composite.remove(item)
                print("ignore check_and_remove_bg")
           else:
               arr_tmp.append(item)
        return arr_tmp

    def add_duration_video(self, current_duration, video_path):
        tmp_vid=VideoFileClip(video_path)
        current_duration+=tmp_vid.duration
        tmp_vid.close()
        return current_duration
    def create_video_with_effect_composite(self, bg_video, arr_composite):
        if "-comp-effect-vid-rendered" in bg_video:
            return bg_video
        vid_intro_bg = VideoFileClip(bg_video)
        vid_intro_bg.set_start(0)
        arr_composite_tmp=arr_composite.copy()
        arr_composite_tmp.insert(0, vid_intro_bg)
        tmp_path_composite_intro = os.path.join(get_dir('coolbg_ffmpeg'),
                                                str(uuid.uuid4().hex) + "-comp-effect-vid-rendered.mp4")
        tmp_clip = CompositeVideoClip(arr_composite_tmp).subclip(0, vid_intro_bg.duration)
        tmp_clip.write_videofile(tmp_path_composite_intro, bitrate='10M', fps=30, codec='libx264', audio=False)
        for ele in arr_composite_tmp:
            ele.close()
        return tmp_path_composite_intro
    def make_footage_videos_with_effect(self, source_id, audio_path, arr_composite_intro, arr_composite_no_intro):
        if not arr_composite_intro or len(arr_composite_intro)<1 :
            arr_composite_intro=arr_composite_no_intro
        arr_composite_intro = self.check_and_remove_bg(arr_composite_intro)
        arr_composite_no_intro = self.check_and_remove_bg(arr_composite_no_intro)
        audio_compilation = AudioFileClip(audio_path)
        arr_list_video = self.get_list_source(source_id, audio_compilation.duration)
        video_path_footage=None
        if arr_list_video:
            print(arr_list_video)
            if len(arr_composite_intro)>0:
                intro_bg = arr_list_video[0][1]
                # arr_list_video[0][1]=self.create_video_with_effect_composite(intro_bg, arr_composite_intro)
                arr_tmp=arr_list_video[0].copy()
                arr_tmp[1]=self.create_video_with_effect_composite(intro_bg, arr_composite_intro)
                arr_list_video[0]=arr_tmp
            if len(arr_composite_no_intro)>0:
                i=1
                max_video=3
                cnt_video=1
                total_intro_time=0
                total_video_logo=0
                while i < len(arr_list_video):
                    if i < 20 and total_intro_time < 300:

                        arr_list_video[i][0] = self.create_video_with_effect_composite(arr_list_video[i][0],
                                                                                       arr_composite_no_intro)
                        intro_bg=arr_list_video[i][1]
                        print(f"Apply Effect first 5 at {i}: {intro_bg}")
                        total_intro_time = self.add_duration_video(total_intro_time, intro_bg)
                        arr_list_video[i][1] = self.create_video_with_effect_composite(intro_bg, arr_composite_no_intro)
                        arr_list_video[i][2] = self.create_video_with_effect_composite(arr_list_video[i][2], arr_composite_no_intro)
                    else:
                        if random.randint(0, 10)>8 and cnt_video < max_video and total_video_logo < 150:
                            intro_bg = arr_list_video[i][1]
                            print(f"Apply Effect percent at {i}: {intro_bg}")
                            cnt_video+=1

                            arr_list_video[i][0] = self.create_video_with_effect_composite(arr_list_video[i][0],
                                                                                           arr_composite_no_intro)
                            total_video_logo = self.add_duration_video(total_intro_time, intro_bg)
                            arr_list_video[i][1] = self.create_video_with_effect_composite(intro_bg,
                                                                                           arr_composite_no_intro)
                            arr_list_video[i][2] = self.create_video_with_effect_composite(arr_list_video[i][2],
                                                                                           arr_composite_no_intro)
                    i+=1
            video_path_footage=make_footage_video(arr_list_video)
        audio_compilation.close()
        return video_path_footage


