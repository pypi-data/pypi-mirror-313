from moviepy.editor import *
from bgeditor.common.image_helper import create_virgin_layer
from bgeditor.common.utils import *
import os, json, textwrap, requests
os.environ["IMAGEMAGICK_BINARY"] = "magick"
from moviepy.tools import subprocess_call
class LyricVer2:

    def __init__(self, lyric_json, font_url, font_size, color, duration, stroke_color, stroke_width, bg_color,
                 lyric_moving, fade_in, fade_out, x, y,
                 wrap_width= 30, w=1920, h=1080):
        self.lyric_json = lyric_json
        self.lyric_data = json.loads(self.lyric_json)
        self.font_url = font_url
        self.font_path=None
        self.font_size = font_size
        self.duration = duration
        self.color = color
        self.w = w # width of group textbox
        self.h = h # high of group textbox
        self.x= x
        self.y= y
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.bg_color=bg_color
        self.wrap_width= wrap_width
        self.lyric_moving = lyric_moving
        self.fade_in = round(float(fade_in),1)
        self.fade_out = round(float(fade_out),1)
        if self.bg_color is None or self.bg_color == "":
            self.bg_color="transparent"
    def init(self):
        self.font_path = cache_file(self.font_url)
        if self.font_path is None:
            return False
        self.normalnize()
        return True
    def optimize_font(self):
        wrapper = textwrap.TextWrapper(width=self.wrap_width)
        for lyric in self.lyric_data:
            lyric['line'] = wrapper.fill(text=lyric['line'])
        data_post = {}
        data_post['w'] = self.w
        data_post['font_url'] = self.font_url
        data_post['json_lyric'] = json.dumps(self.lyric_data)
        data_post['font_size_want'] = self.font_size
        data_post['wrap_width'] = self.wrap_width
        font_size_tmp = requests.post("http://db.automusic.win/music/lyric/font", json = data_post).text
        if font_size_tmp.isdigit():
            self.font_size = int(font_size_tmp)
            return True
        return False

    def normalnize(self):
        lyric_data_normal = []
        for lyric in self.lyric_data:
            try:
                if 'milliseconds' in lyric and 'line' in lyric and int(lyric['milliseconds']) >= 0 and lyric['line'] is not None and len(lyric['line'])>0:
                    lyric_data_normal.append(lyric)
            except:
                pass
        self.lyric_data=lyric_data_normal


    def make(self, bg_video):
        last_time = 0
        arr_lyric_img = []
        last_frame = "[0:v]"
        i=1
        filter_complex=""
        for lyric in self.lyric_data:
            cur_frame = f"[t{i+1}]"
            txt = create_text_img(lyric['line'], size=(self.w, ""), font = self.font_path.replace("\\","/"), color=self.color, fontsize=self.font_size, method="caption",
                           bg_color=self.bg_color, stroke_color=self.stroke_color, stroke_width=self.stroke_width, print_cmd = True)
            arr_lyric_img+=["-i", f"{txt}"]
            start_time = int(lyric['milliseconds']) / 1000
            if i < len(self.lyric_data):
                end_time = int(self.lyric_data[i]['milliseconds']) / 1000
            else:
                if self.duration:
                    end_time = self.duration
                else:
                    end_time= start_time+ 5
            filter_complex += f"{last_frame}[{i}:v] overlay={self.x}:{self.y}:enable='between(t,{start_time},{end_time})' {cur_frame};"
            last_frame = cur_frame
            last_time = end_time
            i += 1
        # if last_time < self.duration:
        #     txt = create_text_img("...", size=(self.w, ""), font = self.font_path.replace("\\","/"), color=self.color, fontsize=self.font_size,
        #                    bg_color=self.bg_color, stroke_color=self.stroke_color, stroke_width=self.stroke_width)
        #     arr_lyric_img+=["-i", f"{txt}"]
        #     cur_frame = f"[t{i + 1}]"
        #     filter_complex += f"{last_frame}[{i}:v] overlay={self.x}:{self.y}:enable='between(t,{last_time},{self.duration})' {cur_frame};"
        cmd=[
            "ffmpeg",
            "-i",
            bg_video,
        ]
        cmd += arr_lyric_img
        filter_complex=filter_complex.strip(";")
        cmd += ["-filter_complex", filter_complex]
        cmd += ["-map", "0:a", "-map", cur_frame]
        cmd += ["-c:v", "libx264", "-flags", "global_header", "-pix_fmt", "yuv420p"]
        cmd += ["-crf", "23", "-b:v", "4M"]
        # cmd += ["-c:a", "mp3", "-b:a", "128000", "-ar", "44100"]
        tmp_lyric_final = os.path.join(get_dir('coolbg_ffmpeg'), str(uuid.uuid4()) + "-lyric-final.mp4")

        cmd += [f"{tmp_lyric_final}"]
        print(" ".join(cmd))
        try:
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            print(err)
        return tmp_lyric_final



