import copy
import random

from moviepy.editor import *
from moviepy.video.fx import loop, mask_color, crop, speedx
from bgeditor.common import utils
from bgeditor.common.utils import cache_file, download_file, upload_file, upload_static_file, upload_file_resource
from bgeditor.dao.FootageController import FootageController
from bgeditor.dao.LyricVer2 import LyricVer2
from bgeditor.dao.Matrix import Matrix
from bgeditor.dao import MusicHelper
from PIL import Image, ImageDraw, ImageFont
from PIL import Image
import numpy as np
import requests, time
from bgeditor.dao import FFmpeg, LyricStatic
from bgeditor.dao.FFmpeg import create_suource_can_loop_path, create_loop, create_loop_audio, create_video_audio, merge_intro_outro, merge_list_video, sub_clip_no_encode, split_audio
from proglog import ProgressBarLogger
from bgeditor.common.utils import get_dir, always_even, getVideoDuration,getAudioDuration
import uuid, textwrap
import math
import traceback

import json
from moviepy.video.fx import make_loopable
import base64
from io import BytesIO
class MyBarLogger(ProgressBarLogger):
    def __init__(self,job_id, mf_server):
      self.is_final_vid=False
      self.old_index_frame=0
      self.start_count_time_30=0
      self.job_id=job_id
      self.MF_SERVER= mf_server
      super().__init__()

    def update_progress(self, total, index, rate):
        try:
            if "error" in requests.get(self.MF_SERVER + "job/progress/%s/%s/%s/%s" %
                         (str(self.job_id), str(total), str(index), str(rate))).text:
                return False
        except:
            pass
        return True

    def callback(self, **changes):
        # Every time the logger is updated, this function is called with
        # the `changes` dictionnary of the form `parameter: new value`.
        for (parameter, new_value) in changes.items():
            if "final-vid" in new_value and "Writing video" in new_value:
              self.is_final_vid=True
              self.old_index_frame = 0
              self.start_count_time_30= time.time()
              print("Start Render main Video")
              self.update_progress(999, 999, 999)
            print ('Parameter %s is now %s' % (parameter, new_value))
    def bars_callback(self, bar, attr, value, old_value):
        if self.is_final_vid:
          if time.time() - self.start_count_time_30 > 30:
            rate = (self.bars[bar]['index']-self.old_index_frame)/30
            self.old_index_frame= self.bars[bar]['index']
            print("Speed: "+str(rate))
            self.update_progress(self.bars[bar]['total'], self.bars[bar]['index'], rate)
            self.start_count_time_30= time.time()

def update_static_lyric_data(job_id, mf_server,  music_data):
    try:
        data = {"id": job_id, "data": music_data, "key" : "mix_data_real"}
        return requests.post(mf_server + "job/b-data/update", json=data).text
    except:
        traceback.print_exc()
        return ""
def create_lyric_outro(deezer_artist_id, lyric_outro_repeat,  arr_comp, outro_claim_topic = None, time_o=5):
    if deezer_artist_id == 977996688 or deezer_artist_id == 96969996688:
        return None
    path_video = None
    try:
        outro_sound = MusicHelper.create_lyric_outro_songs(deezer_artist_id, lyric_outro_repeat, outro_claim_topic)
        path_video = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-comp-outro-lyric-vid-audio.mp4")
        tmp_path_composite_outro = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-comp-outro-lyric-vid.mp4")
        tmp_clip = CompositeVideoClip(arr_comp).subclip(0, time_o)
        tmp_clip.write_videofile(tmp_path_composite_outro, bitrate='10M', fps=24, codec='libx264', audio=False)
        tmp_clip.close()
        audio_compilation = AudioFileClip(outro_sound)
        final_clip_path = create_loop(tmp_path_composite_outro, audio_compilation.duration)
        utils.remove(tmp_path_composite_outro)
        audio_compilation.close()
        create_video_audio(final_clip_path, outro_sound, path_video)
    except:
        path_video = None
        pass
    return path_video

def create_image(list_comp_data, path_img, t=0):
    arr_comps = []
    for comp_data in list_comp_data:
        comp_data["job_id"] = 1
        comp_data["mf_server"] = "http://api-magicframe.automusic.win/"
        if comp_data['type'] == "video":
            comp_data['c_type'] = 'image'
        if comp_data['type'] == "compilation" or comp_data['type'] == "lyric" or comp_data['type'] == 'mix_lyric':
            continue

        arr_comps.append(Component.convert(comp_data))
    arr_comps_maked=[]
    for comp in arr_comps:
        arr_comps_maked.append(comp.make())
    CompositeVideoClip(arr_comps_maked).save_frame(path_img, t)
    for compm in arr_comps_maked:
        compm.close()
    for comp in arr_comps:
        comp.delete_res()
    return path_img

def create_video(list_comp_data, path_video, job_id, mf_server):
    print('get list--create ver2')
    intro_time=10
    intro_time_real=0
    arr_comps=[]
    for comp_data in list_comp_data:
        comp_data["job_id"] = job_id
        comp_data["mf_server"] = mf_server
        comp_tmpx=Component.convert(comp_data)
        if comp_tmpx:
            #ignore compt has url=None
            arr_comps.append(comp_tmpx)
    arr_comps.sort(key=lambda obj: obj.index)
    arr_composite = []
    arr_composite_no_intro=[]
    composite_intro_time=0
    tmp_path_composite_intro = None
    max_duration = 0
    max_real_duration=3 # thoi gian cua 1 video
    is_compilation=False
    is_lyric = False
    is_music= False
    is_lyric_outro = False
    deezer_artist_id = None
    audio_compilation_path=None
    outro_claim_topic=None
    cnt_effect_vid=0
    intro_path = None
    outro_path = None
    firstImageOrVideoBG=[] #purpose for loop lyric outro
    indexVidBG=0
    arr_static_lyric_id=[]
    arr_static_lyric_data=[]
    is_mix_lyric=False
    is_lyric_ver2=True
    is_footage_music=False
    footage_element=None
    lyric_comp=None
    base_fps=24
    base_bitrate='4M'
    is_intro_use_music_bg=False
    #check if videos are compilation
    for comp in arr_comps:
        if comp.type == "lyric":
            is_lyric = True
            is_music = True
            is_lyric_outro = comp.is_lyric_outro
            if is_lyric_outro:
                deezer_artist_id = comp.deezer_artist_id
                lyric_outro_repeat = comp.lyric_outro_repeat
                is_outro_claim = comp.is_outro_claim
                if is_outro_claim:
                    outro_claim_topic = comp.outro_claim_topic
        if comp.type == "mix_lyric":
            is_mix_lyric = True
            is_music = True
        if comp.type == "compilation":
            is_music = True
            is_compilation = True
        if comp.type == "footage":
            is_footage_music= True
            footage_element=comp
            base_fps = 30
            base_bitrate = '10M'

    for comp in arr_comps:
        if is_music and comp.duration>intro_time:
            if comp.type=="video" and (comp.is_intro or comp.is_outro):
                print("don't change duration")
            else:
                comp.duration=intro_time

        if is_mix_lyric and indexVidBG < 5 and  (comp.type == "image" or comp.type == "video"):
            firstImageOrVideoBG.append(comp.make())
            indexVidBG+=1

        if comp.type == "mix_lyric":
            arr_static_lyric_id, arr_static_lyric_data = LyricStatic.create_lyric_static(firstImageOrVideoBG, comp.mix_data, comp.font_url, int(comp.lyric_lines))
            is_mix_lyric = True
            is_music = True
        if comp.type == "compilation":
            is_music = True
            is_compilation = True
            audio_compilation_path = comp.get_audio()

    #tinh toan thoi gian intro, main video, make video element
    for comp in arr_comps:
        if comp.type == "compilation":
            continue
        if comp.type=="footage":
            continue
        if is_lyric_ver2 and (comp.type == "lyric" or comp.type == "mix_lyric"):
            audio_compilation_path = comp.get_audio()
            lyric_comp = comp
            if deezer_artist_id and f"{deezer_artist_id}".isnumeric() and int(deezer_artist_id) < 977996688:
                audio_compilation_path = MusicHelper.create_lyric_outro_songs(deezer_artist_id, lyric_outro_repeat, outro_claim_topic,
                                                               audio_compilation_path)
            continue
        if comp.type == "video":
            if comp.duration < 0:
                cnt_effect_vid += 1
            is_cont = False
            if comp.is_intro:
                is_intro_use_music_bg=comp.is_intro_use_music_bg
                intro_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-intro.mp4")
                rs = comp.get_clip()
                if not rs.audio and not is_intro_use_music_bg:
                    rs.close()
                    vidPathTmp = FFmpeg.add_null_sound(comp.video_path)
                    rs = VideoFileClip(vidPathTmp)
                rs.write_videofile(intro_path, bitrate=base_bitrate, fps=base_fps, codec='libx264', audio_bitrate='128000')
                is_cont = True
                rs.close()
            if comp.is_outro:
                outro_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-outro.mp4")
                rs = comp.get_clip()
                if not rs.audio:
                    rs.close()
                    vidPathTmp = FFmpeg.add_null_sound(comp.video_path)
                    rs = VideoFileClip(vidPathTmp)
                rs.write_videofile(outro_path, bitrate=base_bitrate, fps=base_fps, codec='libx264', audio_bitrate='128000')
                is_cont = True
                rs.close()
            if is_cont:
                continue
        if comp.type == "element":
            comp.set_bg_clip(CompositeVideoClip(arr_composite.copy()))
            arr_composite = [comp.make()]
            arr_composite_no_intro = [comp.make()]
            if max_real_duration < 10:
                max_real_duration = 10
        else:
            #cut tat ca comp nho hon 10s la intro
            if is_music:
                is_in_intro= True
                if  is_music and comp.duration > 0 and comp.duration + comp.start_time <= intro_time:
                    if comp.duration + comp.start_time > intro_time_real:
                        intro_time_real = comp.duration + comp.start_time
                    compTmp = comp.make()
                else:
                    #comp duration nam ngoai intro =600 -1
                    if 0 < comp.start_time and comp.start_time < intro_time:
                        #check if comp appear in intro but also appear in main video
                        comp_intro = comp.xcopy()
                        arr_composite.append(comp_intro.make())
                        duration_tmp=comp_intro.duration
                        if duration_tmp > 500:
                            duration_tmp=3
                        if duration_tmp + comp.start_time > intro_time_real:
                            intro_time_real = duration_tmp + comp.start_time

                        #reset time ve 0 cho main video
                        comp.start_time=0
                        is_in_intro=False
                    compTmp = comp.make()
                    arr_composite_no_intro.append(compTmp)
                if is_in_intro:
                    arr_composite.append(compTmp)
            else:
                #tiktok no check render intro or not
                compTmp = comp.make()
                arr_composite.append(compTmp)
        if comp.duration > 0 and comp.duration + comp.start_time > max_duration:
            max_duration = comp.duration + comp.start_time
        if comp.real_duration + comp.start_time > max_real_duration:
            max_real_duration = comp.real_duration + comp.start_time
    if intro_time_real <= 0:
        for item in arr_composite_no_intro:
            tmp_start=item.start - intro_time_real
            if tmp_start <0:
                tmp_start=0
            item.set_start(tmp_start)

    #----------------------Render---------------------------#
    logger = MyBarLogger(job_id, mf_server)
    if is_lyric_ver2 and is_lyric:
        is_compilation = True
    tmp_path_maked_loop=None
    if not is_music:
        #make vide like tiktok
        if max_duration <= 0 or max_duration > max_real_duration:
            max_duration = max_real_duration
        final_clip = CompositeVideoClip(arr_composite).subclip(0, max_duration)
        final_clip.write_videofile(path_video,  fps=base_fps, codec='libx264', logger=logger)
        final_clip.close()
    elif is_footage_music:
        if audio_compilation_path is None:
            raise Exception("Audio Compilation Error!!!")
        footCtr = FootageController()
        final_clip_path = footCtr.make_footage_videos_with_effect(footage_element.source_id,
                                                                 audio_compilation_path, arr_composite, arr_composite_no_intro)
        if intro_path and is_intro_use_music_bg:
            #merge video intro prevent lag music
            final_clip_path = merge_intro_outro(final_clip_path, intro_path)
            intro_path=None
        create_video_audio(final_clip_path, audio_compilation_path, path_video)
    else:
        # make Compilation
        #ca lyric + compilation deu tao background truoc
        if audio_compilation_path is None:
            raise Exception("Audio Compilation Error!!!")
        cnt_real_duration = 1
        while max_real_duration < 60*2/3 and cnt_real_duration<2 and cnt_effect_vid>1:
            max_real_duration*=2
            cnt_real_duration+=1
        #make intro composite
        if intro_time_real > 0:
            tmp_path_composite_intro = os.path.join(get_dir('coolbg_ffmpeg'),str(uuid.uuid4()) + "-comp-intro-vid.mp4")
            tmp_clip = CompositeVideoClip(arr_composite).subclip(0, intro_time_real)
            tmp_clip.write_videofile(tmp_path_composite_intro, bitrate=base_bitrate, fps=base_fps, codec='libx264', audio=False, logger=logger)
            # tmp_clip.close()

        tmp_path = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-final-vid.mp4")
        tmp_path_maked_loop = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-final-vid.mp4")
        final_clip = CompositeVideoClip(arr_composite_no_intro).subclip(0, max_real_duration)
        final_clip.write_videofile(tmp_path, bitrate=base_bitrate, fps=base_fps, codec='libx264', audio=False, logger=logger)
        #crop big video
        # x_center=final_clip.w/2
        # w_new=math.ceil(final_clip.h*final_clip.h/final_clip.w)
        # y1=0
        # h_new=final_clip.h
        # final_clip= crop.crop(final_clip, x_center=x_center, y1=y1, width=w_new, height=h_new)
        # final_clip.write_videofile(tmp_path, bitrate='4M', fps=24, codec='libx264', audio=False)
        final_clip.close()
        if cnt_effect_vid > 1:
            final_clip = VideoFileClip(tmp_path, audio=False)
            cross = final_clip.duration / 5
            if cross > 3:
                cross = 3
            clip = make_loopable.make_loopable(final_clip, cross)
            clip.write_videofile(tmp_path_maked_loop, bitrate=base_bitrate, fps=base_fps, codec='libx264', audio=False, logger=logger)
            clip.close()
            final_clip.close()
            utils.remove(tmp_path)
        else:
            tmp_path_maked_loop = tmp_path
        audio_compilation = AudioFileClip(audio_compilation_path)
        final_clip_path = create_loop(tmp_path_maked_loop, audio_compilation.duration)
        final_clip_path = merge_intro_outro(final_clip_path, tmp_path_composite_intro)
        utils.remove(tmp_path_composite_intro)
        audio_compilation.close()
        if intro_path and is_intro_use_music_bg:
            #merge video intro prevent lag music
            final_clip_path = merge_intro_outro(final_clip_path, intro_path)
            intro_path=None
        create_video_audio(final_clip_path, audio_compilation_path, path_video)
    final_vid = VideoFileClip(path_video)
    duration_f = final_vid.duration
    final_vid.close()

    if (is_lyric or is_mix_lyric) and is_lyric_ver2:
        path_video=lyric_comp.create_lyric(path_video)
    if is_mix_lyric:
        arr_vids = []
        tmp_path_audio = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-final-vid-audio.mp4")
        cmd=f"ffmpeg -i \"{path_video}\" -c:v copy -b:a 128000 -ar 44100 -c:a mp3 \"{tmp_path_audio}\""
        os.system(cmd)
        arr_vids.append(tmp_path_audio)
        arr_static_lyric_data[0]['duration_real']=getVideoDuration(tmp_path_audio)
        arr_vids += LyricStatic.load_lyric_video(arr_static_lyric_id, arr_static_lyric_data)
        update_static_lyric_data(job_id, mf_server, arr_static_lyric_data)
        path_video = merge_list_video(arr_vids, True)
    path_video = merge_intro_outro(path_video, intro_path, outro_path)
    for comp in arr_comps:
        comp.close()
    if tmp_path_maked_loop:
        utils.remove(tmp_path_maked_loop)

    return path_video


class Component:


    def replace_code(self, ori_text):
        if "@@" in ori_text:
            try:
                data = {"id": self.job_id, "ori_text": ori_text}
                return requests.post(self.mf_server+"job/text/replace",data=data).text
            except:
                traceback.print_exc()
                return ""
                pass
        return ori_text
    def get_max_font_size(self,font_url, text, width, font_size_want):
        try:
            data = {"font_url": font_url, "text": text,
                    "width": width, "font_size_want": font_size_want}
            obj = requests.post(self.mf_server + "text/font/max-size", data=data).json()
            return obj['font_size'], obj['h_text']
        except:
            return None, None
            pass
    def __init__(self, json_data):
        self.job_id=json_data['job_id']
        self.mf_server=json_data['mf_server']
        self.index = json_data['index']
        self.position = json_data['position']
        self.start_time = json_data['startTime']
        self.duration = json_data['duration']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
        self.audio_loop = json_data['audio_loop']
        self.type = json_data['type']
        self.real_duration=0
        self.rs=None
        self.is_background=False
        if "isBackground" in json_data:
            self.is_background =json_data['isBackground']
        self.json_data=json_data
        print("init")

    def xcopy(self):
        return self.convert(self.json_data)
    @staticmethod
    def convert(json_data):
        if json_data['type'] == "text":
            return TextComp(json_data)
        if json_data['type'] == "image":
            return ImageComp(json_data)
        if json_data['type'] == "video":
            if json_data['video_url'] == "None":
                return None
            return VideoComp(json_data)
        if json_data['type'] == "mix_lyric":
            return MixLyricComp(json_data)
        if json_data['type'] == "lyric":
            return LyricComp(json_data)
        if json_data['type'] == "element":
            return ElementComp(json_data)
        if json_data['type'] == "compilation":
            return CompilationComp(json_data)
        if json_data['type'] == "inoutro":
            return InOutroComp(json_data)
        if json_data['type'] == "text_list":
            return TextListComp(json_data)
        if json_data['type'] == "footage":
            return FootageComp(json_data)
    def setup(self):
        print('setup')
    def order(self):
        print('order')
    def get_clip(self):
        print('get clip')
    def set_bg_clip(self,bg_clip):
        print('set bg clip')
    def delete_res(self):
        if hasattr(self,'audio_path') and self.audio_path:
            utils.remove(self.audio_path)
        if hasattr(self,'video_path') and self.video_path:
            utils.remove(self.video_path)
        if hasattr(self,'image_path') and self.image_path:
            utils.remove(self.image_path)
    def get_audio(self):
        self.audio_path=None
        self.audio_moviepy=None
        if self.audio_url and self.audio_ext:
            self.audio_path = download_file(self.audio_url, ext=self.audio_ext)
            if self.audio_loop:
                self.audio_path = create_loop_audio(self.audio_path, self.duration)
            self.audio_moviepy = AudioFileClip(self.audio_path)
        return self.audio_path

    def make(self):
        rs=None
        try:
            self.get_audio()
            rs = self.get_clip()
            if self.audio_moviepy:
              rs = rs.set_audio(self.audio_moviepy)
            if self.type !='element':
              rs = rs.set_position((self.position['x'], self.position['y']))
            if self.duration > 0:
                if self.type != "video":
                    rs = rs.set_duration(self.duration).crossfadeout(0.5)
                else:
                    rs = rs.set_duration(self.duration)
            elif self.duration < 0:
                rs = rs.set_duration(600)

            if self.start_time > 0:
                if self.type!="video":
                    rs = rs.set_start(self.start_time).crossfadein(0.5)
                else:
                    rs = rs.set_start(self.start_time)
            if self.start_time == 0:
                rs = rs.set_start(self.start_time)
            if self.type !='element' and self.position['rotation'] != 0:
                rs = rs.rotate(-1*self.position['rotation'])
            self.rs=rs
        except:
            log_err=traceback.format_exc()
            log_data=f"Error Make Component: index-{self.index} \n"+log_err
            raise TypeError(log_data)
        return rs
    def close(self):
        try:
            if self.rs:
                self.rs.close()
        except :
            pass
        try:
            if self.audio_moviepy:
                self.audio_moviepy.close()
        except :
            pass

class InOutroComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.intro = None
        self.outro = None
        if json_data['intro'] and len(json_data['intro']) > 0:
            self.intro = download_file(json_data['intro'], ext=json_data['ext'])
        if json_data['outro'] and len(json_data['outro']) > 0:
            self.outro = download_file(json_data['outro'], ext=json_data['ext'])

class CompilationComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.audio_duration=0
        self.music_data = json_data['music_data']
        self.is_trim_silence=False
        self.silence_threshold=-30
        if 'is_trim_silence' in json_data:
            self.is_trim_silence = json_data['is_trim_silence']
        if 'silence_threshold' in json_data:
            self.silence_threshold = json_data['silence_threshold']

    def get_audio(self):
        return MusicHelper.create_compilation_songs(self.music_data, self.job_id, self.mf_server, self.is_trim_silence, self.silence_threshold)


class ElementComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.rate_summon = json_data['rate_summon']
        self.arr_summon_template =  json_data['arr_summon_template']
        self.arr_direction =  np.array(json_data['arr_direction'])
        self.rang_locx =  np.array(json_data['rang_locx'])
        self.rang_locy =  np.array(json_data['rang_locy'])
        self.rang_speedx = np.array(json_data['rang_speedx'])*2
        self.rang_speedy = np.array(json_data['rang_speedy'])*2
        self.rang_opacity =  np.array(json_data['rang_opacity'])
        self.rang_size =  np.array(json_data['rang_size'])
        self.delay= json_data['delay']
        self.arr_color = json_data['arr_color']
        self.bg_clip= None
        self.arr_local_template=[]
    def set_bg_clip(self,bg_clip):
        self.bg_clip=bg_clip
    def cache_summon(self):
        for template in self.arr_summon_template:
            self.arr_local_template.append(cache_file(template))
    def get_clip(self):
        self.cache_summon()
        matrix = Matrix (self.bg_clip, self.rate_summon,  self.arr_local_template, self.arr_direction, self.rang_locx,
                         self.rang_locy,self.rang_speedx ,self.rang_speedy , self.rang_opacity, self.rang_size, self.arr_color, self.delay)
        matrix.setup()
        rs = matrix.make()
        return rs

class TextComp(Component):
    def calcWidthHigh(self):
        cnt=self.text.count("\n")
        ori_height = int(self.position['height'])
        ori_y=int(self.position['y'])
        self.position['height'] = ori_height
        self.position['y']=ori_y
        for i in range(cnt):
            self.position['height'] += ori_height
            self.position['y'] -= ori_y
            if self.position['y'] < 0 :
                self.position['y'] = 0
                break
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        #fontsize px need to convert to pt
        # self.font_size = int(math.ceil(float(self.font_size)*3.0/4.0))
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = json_data['color']
        self.text = json_data['text']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']
        self.is_replaced_text = False
        if "@@" in self.text:
            self.is_replaced_text = True
            self.wrap_width = 50
            if "wrap_width" in json_data and json_data['wrap_width']:
                self.wrap_width = int(json_data['wrap_width'])

    def get_clip(self):
        self.font_path = cache_file(self.font_url)
        if self.is_replaced_text:
            self.text = self.replace_code(self.text)
            wrapper = textwrap.TextWrapper(width=self.wrap_width)
            self.text = wrapper.fill(text=self.text)
            # self.calcWidthHigh()
            font_size, h_text = self.get_max_font_size(self.font_url, self.text,
                                                       int(self.position['width']), self.font_size)
            h_text = int(h_text + math.ceil(h_text / 3))
            if font_size:
                self.font_size = font_size
                if h_text > self.position['height']:
                    h_text = int(h_text + math.ceil(h_text / 3))
                    self.position['y'] = self.position['y'] - (h_text - self.position['height'])
                    self.position['height'] = h_text
                    if self.position['y'] < 50:
                        self.position['y']=50

        rs = TextClip(txt = self.text, font = self.font_path.replace("\\","/"), fontsize=self.font_size, color=self.color,
                        bg_color = self.bg_color, size=(int(self.position['width']), int(self.position['height'])+10),
                        stroke_color = self.stroke_color, stroke_width=self.stroke_width)
        # if self.position['rotation'] != 0:
        #     tmp_text= os.path.join(get_dir("coolbg_ffmpeg"),str(uuid.uuid4())+"-text.png")
        #     rs.save_frame(tmp_text)
        #     im=rs.get_frame(0)
        #     if rs.mask is not None:
        #         mask = 255 * rs.mask.get_frame(0)
        #         im = np.dstack([im, mask]).astype("uint8")
        #     else:
        #         im = im.astype("uint8")
        #     im=Image.fromarray(im)
        #     rs = ImageClip(np.asarray(im.rotate(-1 * self.position['rotation'])))
        # with Image.fromarray(rs.get_frame(0).astype("uint8")) as im:
        #     rs = ImageClip(np.asarray(im))
        return rs

class ImageComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.image_url = json_data['image_url']
        self.ext = json_data['ext']
        self.isMask = json_data['isMask']
        self.maskColor = json_data['maskColor']
        self.opacity = json_data['opacity']
    def get_clip(self):
        self.image_path = download_file(self.image_url, ext=self.ext)
        im = Image.open(self.image_path)
        if im.mode =="L" or im.mode =="P" or im.mode =="1":
            formatter = {"PNG": "RGBA", "JPEG": "RGB"}
            rgbimg = Image.new(formatter.get(im.format, 'RGB'), im.size)
            rgbimg.paste(im)
            im = rgbimg
        width, height = im.size
        if width != self.position['width'] or height != self.position['height']:
            im1 = im.resize((self.position['width'], self.position['height']))
            rs = ImageClip(np.asarray(im1))
        else:
            rs = ImageClip(np.asarray(im))
        if self.isMask:
            rs = mask_color.mask_color(rs, self.maskColor)
        if self.opacity < 1.0:
            rs = rs.set_opacity(self.opacity)
        return rs

class VideoComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.video_url = json_data['video_url']
        self.ext = json_data['ext']
        self.isMute = json_data['isMute']
        self.isLoop = json_data['isLoop']
        self.isSmoothLoop = json_data['isSmoothLoop']
        self.isMask = json_data['isMask']
        self.maskColor = json_data['maskColor']
        self.md5 = json_data['md5']
        self.opacity = json_data['opacity']
        self.real_duration=0
        self.is_canva = json_data['isCanva']
        self.kind = "video"
        self.is_intro=False
        self.is_outro=False
        self.video_path = None
        self.c_type='video' #type get clip
        self.t_start=0
        self.t_end=0
        self.is_speedx=False
        self.mask_img=None
        self.is_intro_use_music_bg=True
        # self.is_duration=False
        if "is_speedx" in json_data:
            self.is_speedx = json_data['is_speedx']
        if "t_start" in json_data:
            self.t_start = json_data['t_start']
        if "t_end" in json_data:
            self.t_end = json_data['t_end']
        if "c_type" in json_data:
            self.c_type = json_data['c_type']
        if "is_intro" in json_data:
            self.is_intro = json_data['is_intro']
        if "is_intro_use_music_bg" in json_data:
            self.is_intro_use_music_bg = json_data['is_intro_use_music_bg']
        if "is_outro" in json_data:
            self.is_outro = json_data['is_outro']
        if "mask_img" in json_data:
            self.mask_img =json_data['mask_img']

        # if "is_duration" in json_data:
        #     self.is_duration = json_data['is_duration']
        if self.is_canva:
            self.kind = "canva"
    def zoom_in(self,rs, width, height, zoom_in, zoom_in_pos='center'):
        ww = width + int(width * zoom_in / 100)
        hh = height + int(height * zoom_in / 100)
        ww = always_even(ww)
        hh = always_even(hh)
        space_x = (ww - width)
        space_y = (hh - height)
        if zoom_in_pos == 'random':
            x1 = random.randint(0, space_x)
            y1 = random.randint(0, space_y)
        elif zoom_in_pos == 'center':
            x1 = int(space_x / 2)
            y1 = int(space_y / 2)
        x2 = x1 + width
        y2 = y1 + height
        rs = rs.resize((ww, hh))
        rs = rs.crop(x1, y1, x2, y2)
        return rs
    def get_clip(self):

        if self.c_type == 'image':
            self.isLoop = False
            self.isSmoothLoop = False
        if self.isLoop and self.isSmoothLoop and self.ext != "gif" and not self.is_intro and not self.is_outro and self.md5 != "tiktok":
            obj = requests.get(self.mf_server+"resource/get-md5/"+self.kind+"/"+self.md5).json()
            is_loop_mk=False
            if "id" in obj:
                if "loop_link" in obj and obj['loop_link'] is not None and "gdrive" in obj['loop_link']:
                    try:
                        self.video_path = download_file(obj['loop_link'], ext=self.ext)
                    except:
                        is_loop_mk = True
                        pass
                    if not self.video_path:
                        is_loop_mk = True
                else:
                    is_loop_mk = True
                if is_loop_mk:
                    self.video_path = download_file(self.video_url, ext=self.ext)
                    path_loop = create_suource_can_loop_path(self.video_path, True, ext=self.ext)
                    if path_loop is None:
                        raise Exception(" Error create source loop")
                    else:
                        drive_id = upload_file_resource(path_loop)
                    requests.get(self.mf_server+"resource/set-md5/"+self.kind+"/" + self.md5+"/"+ drive_id)
                    self.video_path = path_loop
        else:
            self.video_path = download_file(self.video_url, ext=self.ext)
        has_mask = False
        if self.ext == "gif":
            if self.opacity < 1.0:
                self.video_path = FFmpeg.convert_gif_moviepy(self.video_path)
            else:
                has_mask = True
                self.video_path = FFmpeg.convert_gif(self.video_path)
        if self.ext == "mov":
            has_mask = True
        rs = VideoFileClip(self.video_path, audio=not self.isMute, has_mask=has_mask)
        #cut clip
        if self.duration > 0:
            rs_duration = rs.duration - self.t_start
            if self.duration > 0 and self.duration < rs_duration:
                rate_vid = rs_duration / self.duration
                if self.is_speedx and rate_vid >1:
                    rs.close()
                    self.video_path= sub_clip_no_encode(self.video_path, self.t_start)
                    rs = VideoFileClip(self.video_path, audio=not self.isMute, has_mask=has_mask)
                    rs = speedx.speedx(rs, final_duration=self.duration)
                else:
                    rs = rs.subclip(self.t_start, self.t_start + self.duration)
                rs.duration = self.duration
            elif self.t_end > 0:
                rs = rs.subclip(self.t_start, -1*self.t_end)
            else:
                rs = rs.subclip(self.t_start)
        elif self.t_start>0 or self.t_end >0:
            t_end=-1*self.t_end
            if t_end==0:
                t_end=None
            rs=rs.subclip(self.t_start, t_end)
        if self.duration > 0 or not self.isLoop:
            self.duration = rs.duration


        self.real_duration = rs.duration
        if ((self.index == 0 or self.isLoop) and self.c_type=='video') and rs.duration < 600: #max 20 mins loop
            rs.close()
            # self.real_duration = 0
            self.video_path = create_loop(self.video_path, 600)
            rs = VideoFileClip(self.video_path, audio=not self.isMute, has_mask=has_mask)
        if self.isMask:
            rs = mask_color.mask_color(rs, self.maskColor, thr=150, s=5)
        if self.mask_img:
            self.mask_img_path = download_file(self.mask_img, ext="png")
            maskclip = ImageClip(self.mask_img_path, ismask=True)
            rs = rs.set_mask(maskclip)

        if self.opacity < 1.0:
            rs = rs.set_opacity(self.opacity)
        w, h = rs.size
        if 'keep_ori_wh' in self.position and self.position['keep_ori_wh']:
            self.position['width'] = w
            self.position['height'] = h

        f_w = self.position['width']
        f_h = self.position['height']
        if f_w != w or f_h != h or 'zoom_in' in self.position:
            if 'zoom_in' in self.position:
                zoom_in_pos = 'center'
                if 'zoom_in_pos' in self.position:
                    zoom_in_pos = self.position['zoom_in_pos']
                f_rate=f_w/f_h
                v_rate=w/h
                if  v_rate<f_rate+0.1:
                    #video good rate
                    rs= self.zoom_in(rs, f_w, f_h, self.position['zoom_in'], zoom_in_pos)
                else:
                    if v_rate > 1 and f_rate < 1:
                        # process video 16:9 crop to 9:9
                        rs = rs.crop(x_center=always_even(int(w / 2)), width=h, y1=0, y2=h)
                        w=h
                    #scale width
                    new_w=f_w
                    new_h=int(f_w*h/w)
                    rs = self.zoom_in(rs, new_w, new_h, self.position['zoom_in'], zoom_in_pos)
                    #re-caculate x,y
                    space_x = (new_w - f_w)
                    space_y = (f_h - new_h)
                    x_new = int(space_x / 2)
                    y_new = int(space_y / 2)
                    self.position['x']= x_new
                    self.position['y'] = y_new
            else:
                rs = rs.resize((f_w, f_h))
        return rs

class MixLyricComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = json_data['color']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
        self.lyric_sync = json_data['lyric_sync']
        self.wrap_width = json_data['wrap_width']
        self.lyric_moving = json_data['lyric_moving']
        self.fade_in = json_data['fade_in']
        self.fade_out = json_data['fade_out']
        self.mix_data = json_data['mix_data']
        self.lyric_lines = json_data['lyric_lines']

    def get_clip(self):
        self.lyric = LyricVer2(self.lyric_sync, self.font_url, self.font_size, self.color,
                               self.audio_moviepy.duration, self.stroke_color, self.stroke_width, self.bg_color,
                               self.lyric_moving, self.fade_in, self.fade_out, self.position['x'], self.position['y'],
                               self.wrap_width, self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make()

    def create_lyric(self, bg_video):
        self.lyric = LyricVer2(self.lyric_sync, self.font_url, self.font_size, self.color,
                               self.audio_moviepy.duration, self.stroke_color, self.stroke_width, self.bg_color,
                               self.lyric_moving, self.fade_in, self.fade_out, self.position['x'], self.position['y'],
                               self.wrap_width, self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make(bg_video)

class LyricComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = json_data['color']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
        self.lyric_sync = json_data['lyric_sync']
        self.wrap_width = json_data['wrap_width']
        self.lyric_moving = json_data['lyric_moving']
        self.fade_in = json_data['fade_in']
        self.fade_out = json_data['fade_out']
        self.is_lyric_outro=False
        self.is_outro_claim=False
        self.outro_claim_topic =None
        if "is_lyric_outro" in json_data:
            self.is_lyric_outro = json_data['is_lyric_outro']
            if "deezer_artist_id" in json_data:
                self.deezer_artist_id = json_data['deezer_artist_id']
            if "lyric_outro_repeat" in json_data:
                self.lyric_outro_repeat = json_data['lyric_outro_repeat']
            if "is_outro_claim" in json_data:
                self.is_outro_claim = json_data['is_outro_claim']
            if "outro_claim_topic" in json_data:
                self.outro_claim_topic = json_data['outro_claim_topic']

    def get_clip(self):
        self.lyric = LyricVer2(self.lyric_sync, self.font_url, self.font_size, self.color,
                           self.audio_moviepy.duration, self.stroke_color, self.stroke_width, self.bg_color,
                           self.lyric_moving, self.fade_in, self.fade_out, self.position['x'], self.position['y'], self.wrap_width, self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make()
    def create_lyric(self, bg_video):
        self.lyric = LyricVer2(self.lyric_sync, self.font_url, self.font_size, self.color,
                           self.audio_moviepy.duration, self.stroke_color, self.stroke_width, self.bg_color,
                           self.lyric_moving, self.fade_in, self.fade_out, self.position['x'], self.position['y'], self.wrap_width, self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make(bg_video)

class TextListComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
        self.color = self.rgba_to_a255(json_data['color'])
        self.text = json_data['text']
        self.num_columns=int(json_data['num_columns'])
        self.margin=int(json_data['margin'])
        self.min_spacing=int(json_data['min_spacing'])
        self.padding_h = int(json_data['padding_h'])
        self.stroke_color = self.rgba_to_a255(json_data['stroke_color'])
        self.stroke_width = json_data['stroke_width']
        self.is_replaced_text = False
        if "@@" in self.text:
            self.is_replaced_text = True
            self.wrap_width = 50
            if "wrap_width" in json_data and json_data['wrap_width']:
                self.wrap_width = int(json_data['wrap_width'])

    def find_font_size(self, songs, font_path, image_width, image_height, num_columns, min_spacing, padding_h=10, margin=10, max_font_size=40):
        fontsize = max_font_size
        font = ImageFont.truetype(font_path, fontsize)
        max_song_length = max([font.getbbox(song)[2] for song in songs])
        max_song_height = max([font.getbbox(song)[3] for song in songs])
        # Giảm kích thước font chữ cho đến khi nó phù hợp
        while fontsize > 1 and ((max_song_length * num_columns + min_spacing * (num_columns - 1) + margin*2) > image_width or (
                (max_song_height + padding_h) * (len(songs) / num_columns)  + margin*2) > image_height):
            fontsize -= 1
            font = ImageFont.truetype(font_path, fontsize)
            max_song_length = max([font.getbbox(song)[2] for song in songs])
            max_song_height = max([font.getbbox(song)[3] for song in songs])
        return fontsize, max_song_length

    def rgba_to_a255(self, rgba_color):
        if rgba_color:
            # Tách giá trị Red, Green, Blue và Alpha từ chuỗi màu
            rgba_values = rgba_color.split(',')
            red = int(rgba_values[0][5:])
            green = int(rgba_values[1])
            blue = int(rgba_values[2])
            alpha = float(rgba_values[3].replace(")","")[:4])
            alpha_a255 = round(alpha * 255)
            return f'rgba({red}, {green}, {blue}, {alpha_a255})'
        return rgba_color
    def find_good_spacing(self, image_width, min_spacing, max_song_length, num_columns, magin):
        max_last_position = magin + (num_columns - 1) * (max_song_length + min_spacing)
        spacex = image_width - (max_last_position + max_song_length)
        if spacex > 0 and num_columns>1:
            return min_spacing + (spacex // (num_columns - 1))
        return min_spacing

    def distribute_songs(self, songs, num_cols):
        for i, song in enumerate(songs):
            index_song = "{:02d}".format(i + 1)
            songs[i] = f"{index_song}. {song}"

        ns_pc = len(songs) // num_cols
        odd_songs=len(songs)%num_cols
        if odd_songs>0:
            for i in range(num_cols-odd_songs):
                songs.append("")
            ns_pc = len(songs) // num_cols
        print(len(songs))
        songs_tmp = []
        for i in range(ns_pc):
            for j in range(num_cols):
                x = i + ns_pc * j
                if (x < len(songs)):
                    songs_tmp.append(songs[x])
        return songs_tmp

    def get_clip(self, is_get_pillow=False):
        self.font_path = cache_file(self.font_url)
        if self.is_replaced_text:
            self.text = self.replace_code(self.text)
        self.arr_text= self.text.split("\n")
        image_width = int(self.position['width'])
        image_height = int(self.position['height'])
        num_columns = self.num_columns
        min_spacing = self.min_spacing
        padding_h = self.padding_h
        max_font_size = int(self.font_size)
        margin = self.margin
        self.arr_text = self.distribute_songs(self.arr_text, num_columns)
        fontsize, max_song_length = self.find_font_size(self.arr_text, self.font_path, image_width, image_height, num_columns=num_columns, min_spacing=min_spacing, margin=margin,
                                                   padding_h=padding_h, max_font_size=max_font_size)

        min_spacing = self.find_good_spacing(image_width, min_spacing, max_song_length, num_columns, margin)
        img = Image.new('RGBA', (image_width, image_height), color=(255, 255, 255, 0))
        font = ImageFont.truetype(self.font_path, fontsize)
        d = ImageDraw.Draw(img)
        column_width = max_song_length
        start_positions = [(margin + i * (column_width + min_spacing), margin) for i in range(num_columns)]
        for index, song in enumerate(self.arr_text):
            column = index % num_columns
            x, y = start_positions[column]
            d.text((x, y), song, font=font, fill=self.color, stroke_fill= self.stroke_color, stroke_width=self.stroke_width)
            start_positions[column] = (x, y + font.getbbox(song)[3] + padding_h)
        if is_get_pillow:
            return img
        return ImageClip(np.asarray(img))
    def get_img(self,name):
        imc=self.get_clip()
        imc.save_frame(name)
    def get_img_base64(self):
        imc = self.get_clip(True)
        buffered = BytesIO()
        imc.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str.decode("ascii")


class FootageComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.source_id = json_data['source_id']
    def get_clip(self):
        return None