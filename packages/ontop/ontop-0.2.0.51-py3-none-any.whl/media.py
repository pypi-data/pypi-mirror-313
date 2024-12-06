# media.py
import os
from pickle import NONE
from IPython.display import display, Javascript
from IPython.core.display import HTML
import time
import datetime
import random
import requests
from IPython.display import Image
from urllib.request import urlopen
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import base64
import urllib.request

from string_table import *

class colors:
    RED = (234, 50, 31)
    ORANGE = (245, 170, 66)
    YELLOW = (245, 252, 71)
    GREEN = (0, 183, 77)
    BLUE = (71, 177, 252)
    PURPLE = (189, 71, 252)
    WHITE = (255, 255, 255)

def print_color(text, rgb):
    return "\033[38;2;{};{};{}m{}\033[0m".format(str(rgb[0]), str(rgb[1]), str(rgb[2]), text)

def print_background(text, rgb):
    return "\033[48;2;{};{};{}m{}\033[0m".format(str(rgb[0]), str(rgb[1]), str(rgb[2]), text)

# banners = ["https://data.cyber.org.il/OnTopTech/school_bell/images/colab_celebrate_1.gif",
           # "https://data.cyber.org.il/OnTopTech/school_bell/images/colab_celebrate_2.gif",
           # "https://data.cyber.org.il/OnTopTech/school_bell/images/colab_celebrate_3.gif",
           # "https://data.cyber.org.il/OnTopTech/school_bell/images/colab_celebrate_4.gif"]
# greetings=["כל הכבוד! אנחנו שולטיםםםם",
           # "אליפות! סיימנו עוד משימה",
           # "נהדר! זה כבר כמעט הסוף",
           # "כל הכבוד לי! סיימתי עוד שלב",
           # "כל הכבוד לי!"]


def run_banner_rnd():
    greetings = read_greeting_txt()
    banners = read_banner_gifs()
    banner_num = random.randint(0, len(banners)-1)
    greetings_num = random.randint(0, len(greetings)-1)
    run_banner(greetings, banners[banner_num] )

def run_banner_manual(greetings_str):
    banners = read_banner_gifs()
    banner_num = random.randint(0, len(banners)-1)
    run_banner(greetings_str, banners[banner_num] )

#def read_greeting_txt():
#    url = "https://ontopnew.s3.il-central-1.amazonaws.com/library/greetings01.txt"
#    response = urllib.request.urlopen(url)
#    data = response.read().decode("utf-8")  # Decode bytes to string
#    list = []
#    for line in data.splitlines():
#        list.append(line.strip())
#    return list


def read_greeting_txt():
  list = get_banners_strings()
  banner_num = random.randrange(len(list))  # שינוי ל-random.randrange
  return list[banner_num]

def read_banner_gifs():
    url = "https://ontopnew.s3.il-central-1.amazonaws.com/library/banners.txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")  # Decode bytes to string
    list = []
    for line in data.splitlines():
        list.append(line.strip())
    return list

def read_gifs():
    url = "https://ontopnew.s3.il-central-1.amazonaws.com/library/gifs.txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")  # Decode bytes to string
    list = []
    for line in data.splitlines():
        list.append(line.strip())
    return list


def run_banner(greetings_str, banner_link="" ):
  html = '''
  <svg width='970'  style="background-color:aliceblue">
   <image href={banner} />
   <defs>
    <filter id="f3" x="0" y="0" width="100%" height="100%">
      <feOffset result="offOut" in="SourceAlpha" dx="0" dy="0" />
      <feGaussianBlur result="blurOut" in="offOut" stdDeviation="10" />
      <feBlend in="SourceGraphic" in2="blurOut" mode="normal" />
    </filter>
  </defs>
   <text x="50%" y="80" dominant-baseline="middle" text-anchor="middle" font-size="30" fill="#1F33BE" font-weight="bold" filter="url(#f3)">{*}</text>
   <text x="50%" y="45" dominant-baseline="middle" text-anchor="middle" font-size ="20" fill="#1F33BE"  filter="url(#f3)">{date}</text>
 </svg>
'''
  today = datetime.date.today()
  html = html.replace("{*}", greetings_str)
  html = html.replace("{date}", str(today.day) + "." +  str(today.month) + "." +  str(today.year))
  html = html.replace("{banner}", banner_link)
  display(HTML(html))

def show_gif(gif_url, gif_width=NONE, gif_height=NONE):
  if gif_width != NONE and gif_height != NONE:
    display(Image(url = gif_url,width = int(gif_width), height=int(gif_height)))
  else:
    display(Image(url = gif_url))


def show_image(gif_url):
  html = '''
  <html>
<head>
  <title>הצגת תמונה</title>
</head>
<body>
  <img src="{image_url}">
</body>
</html>
'''
  html = html.replace("{image_url}", gif_url)
  display(HTML(html))

def play_video_from_to(video_width, video_path, from_time, to_time):
  video_path = video_path+'#t={from},{to}'
  video_path = video_path.replace('{from}', str(from_time))
  video_path = video_path.replace('{to}', str(to_time))
  return HTML(f"""<video width={video_width} controls autoplay><source src="{video_path}"></video>""")


#***********************************************
#  Take Selfie
#***********************************************
def selfie(timer):
  if (timer > 0):
    score = 6
  show_video()
  time.sleep(timer)
  display(Image.open(take_photo()))


def show_video():
  js = Javascript('''
    var stream;
    async function showVideo() {
      const div = document.createElement('div');
      div.id = 'VideoContainer';
      const video = document.createElement('video');
      video.id = 'CaptureVideo';
      video.style.display = 'block';
      stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      // await new Promise((resolve) => capture.onclick = resolve);
    }

    function takePhoto(quality) {
      const div = document.getElementById('VideoContainer');
      const video = document.getElementById('CaptureVideo');
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  eval_js('showVideo()')

def download_image_from_web(url):
  response = requests.get(url)
  save_photo(response.content)

def save_photo(binary, filename='photo.jpg'):
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

def take_photo(filename='photo.jpg', quality=0.8):
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  return save_photo(binary, filename)

def convert_img_to_base64(url):
    with open('/content/photo.jpg', 'rb') as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    return encoded_image

def is_file_exist(file_name):
  if os.path.exists(file_name):
    return True
  else:
    return False