from media import *
from html_helper import *
from messages import *
from string_table import *


student_name=''
student_school = ''
score = 0


def run_me():
    run_banner_rnd()

name=""
school=""

def print_who_rules(text):
  global score
  if score < 1:
    s = get_string_from_string_table('school_bell', 'print_who_rules')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
  else:
    print(text,"\n")
    validate_ex2(text)

# ===========================
# return current score
# ===========================
def get_score():
    global score
    return score

# ===========================
# 2nd section: 'password'
# ===========================
# after print_image: score=3
# after print_password: score=4
# ===========================

def print_image(w, h):
  global score
  if score < 2:
    s=get_string_from_string_table('school_bell', 'print_image_2')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
    return
  html = '''
<img src='https://ontopnew.s3.il-central-1.amazonaws.com/Riddle1.jpg' alt="password" width="*w*" height="*h*">
  '''
  html = html.replace("*w*", str(w));
  html = html.replace("*h*", str(h));
  display(HTML(html))
  if score == 2:
    score = 3 #score + 1

def print_password(text):
  global score
  if score < 3:
    s=get_string_from_string_table('school_bell', 'print_image_3')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
  else:
    print(text, "\n")
    validate_ex4(text)


# ===========================
# 3rd section: 'video'
# ===========================
# after play_video: score=5
# ===========================

# NEW function that uses mp4 from our amazon server
def play_video(start, end):
  global score
  language = get_language()
  if score < 4:
    s=get_string_from_string_table('school_bell', 'print_video')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
    return
  else:
    if language == 'hebrew':
        if ((start >= 5 and start <=7) ) and (end >= 42 and end <= 45):
          if score == 4:
            score = 5
    else:
        if ((start >= 5 and start <=7) ) and (end >= 29 and end <= 31):
          if score == 4:
            score = 5
  video_width = 700
  if language == 'hebrew':
    video_path = 'https://ontopnew.s3.il-central-1.amazonaws.com/school_bell/video/bell.mp4'
  else:
    video_path = 'https://ontopnew.s3.il-central-1.amazonaws.com/school_bell/video/bell_arabic.mp4'
  return play_video_from_to(video_width, video_path, start, end)

def take_selfie(timer):
  global score

  if score < 5:
    s=get_string_from_string_table('school_bell', 'take_selfie')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
    return

  if (timer > 0):
    score = 6
  selfie(timer);


def download_pic(link):
  global score
  if score < 5:
    s=get_string_from_string_table('school_bell', 'download_pic')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
    return
  score = 6
  download_image_from_web(link)
  #display(Image.open('photo.jpg'))
  display(Image('photo.jpg'))


# ===========================
# certificate
# ===========================
def add_greetings():
  global student_name, student_school
  html = download_html('https://ontopnew.s3.il-central-1.amazonaws.com/school_bell/HTML/Certificate08.html') #(url) #
  s=get_string_from_string_table('school_bell', 'add_greetings_1')
  html = html.replace('{*name*}', s + student_name)

  #convert img to base64
  if(is_file_exist('/content/photo.jpg')):
    encoded_image = convert_img_to_base64('/content/photo.jpg')
    html_img_tag = '<img src="data:image/jpeg;base64,'+encoded_image+ '" alt="Image description" width="593" height="444"/>'
  else:
    s=get_string_from_string_table('school_bell', 'add_greetings_2')
    error_msg(s)
  html = html.replace('{*image*}',html_img_tag)
  s3=get_string_from_string_table('school_bell', 'add_greetings_3')
  s4=get_string_from_string_table('school_bell', 'add_greetings_4')
  html = html.replace('{*school*}', s3 + student_school + s4)
  s5=get_string_from_string_table('school_bell', 'add_greetings_5')
  html = html.replace('{*content*}', s5)
  return html

def make_certificate():
  global score
  if score > 5 :
    display(HTML(add_greetings()))
  else:
     s = get_string_from_string_table('school_bell', 'make_certificate')
     print(print_background(print_color(s, colors.WHITE), colors.RED))



def get_score():
    global score
    return score

# ===========================
# Validations of exercises
# ===========================
# ex1 - name+school form
def validate_ex1(name, school ):
  #global result_list

  global score
  global student_name
  global student_school
  if name=="" or school=="":
    if score == 1:
      score = 0 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex1_1')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
  else:
    student_name = name
    student_school = school
    if score == 0:
      score = 1
    s = get_string_from_string_table('school_bell', 'validate_ex1_2')
    print(print_background(print_color(s, colors.WHITE), colors.GREEN))

# ex2 - print "OnTop Rules"
# shany 16.6.2022 mevoot2.0: give specific case-sensitive error msg
def validate_ex2(text):
  global score
  if text =="OnTop Rules":
    if score == 1:
      score = 2
    s = get_string_from_string_table('school_bell', 'validate_ex2_1')
    print(print_background(print_color(s, colors.WHITE), colors.GREEN))
  # check for spaces
  elif text.strip() != text:
    if score == 2:
      score = 1 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex2_2')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
  elif text.lower() =="ontop rules":
    if score == 2:
      score = 1 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex2_3')
    print(print_background(print_color(s, colors.WHITE), colors.RED))
  elif text.lower() =="ontop":
    if score == 2:
      score = 1 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex2_4')
    print(print_background(print_color(2, colors.WHITE), colors.RED))
  else:
    if score == 2:
      score = 1 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex2_5')
    print(print_background(print_color(s, colors.WHITE), colors.RED))


# ex3 - print image
#def validate_ex3(text):
#  global result_list
#  global score

#ex4 - print password
def validate_ex4(text):
  global score
  if text =="We are the best":
    if score == 3:
      score = 4
    s = get_string_from_string_table('school_bell', 'validate_ex4_1')
    print(print_background(print_color(s, colors.WHITE), colors.GREEN))
  else:
    if score == 4:
      score = 3 #Shany: lower the score only if students play with current section...
    s = get_string_from_string_table('school_bell', 'validate_ex4_2')
    print(print_background(print_color(s, colors.WHITE), colors.RED))