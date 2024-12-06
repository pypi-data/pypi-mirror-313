from media import *
from html_helper import *
from messages import *
from string_table import *




def run_me():
    run_banner_rnd()
    

def random_from_group(*args):
   return random.choice(list(args))
    

def print_order_togo(my_name, num_slices, total_price, is_my_birthday =False):
  if not type(num_slices) is int:
    s = get_string_from_string_table('pizzeria1', 'print_order_1')
    error_msg("print_order", s)
    return
  html = '''
  <html>
<head>
<meta charset="utf-8">
</head>
<body>
<div style="width: 500px; height: 480px; padding: 10px; font-family: Arial; position: relative;text-align:center; background-color:#FFFBDB">
    <span style="font-size: 30px; font-weight: bold;">{***print_order_2***}</span><br>
	<span style="font-size: 15px; font-weight: bold;">{*order_date*}</span><br>
	<span style="font-size: 20px; font-weight: bold;"> {*order_num*} {***print_order_3***}</span><br>
	<span style="font-size: 20px; font-weight: bold;">{***print_order_41***} {*name1*} </span><br><br>
		
	<div style="width: 500px; height: 200px;display: flex;justify-content: space-between;  align-items: flex-start;">
	  <div style="width: 23%; display: inline-block; height: 100%; ">
		<img src="https://ontopnew.s3.il-central-1.amazonaws.com/pizzeria2/Images/messenger3.png" width="117" height="100"/>
	  </div>
	  <div style="width: 50%; display: inline-block; height: 100%;text-align: center;">
		<img src="https://ontopnew.s3.il-central-1.amazonaws.com/pizzeria1/Images/intro1_pizza_box.png" width="220" height="160"/>
	  </div>
	  <div style="width: 24%; display: inline-block; height: 100%; text-align: center;"></div>
	</div>

	<div style="width: 500px; height: 200px;display: flex;justify-content: space-between;  align-items: flex-start;">
	  <div style="width: 23%; display: inline-block; height: 100%; "></div>
	  <div style="width: 50%; display: inline-block; height: 100%;text-align: center;">
        <span style="font-size: 20px; font-weight: bold;"> {*slices*} {***print_order_6***}</span><br>
		<span style="font-size: 20px; font-weight: bold;"> {*price*} {***print_order_7***}</span><br><br>
	  </div>
	  <div style="width: 24%; display: inline-block; height: 100%; text-align: center;">
	    {*birthday*}
	  </div>
	</div>
</div>
</body>
</html>'''
  today = datetime.date.today()
  html = html.replace('{*order_date*}', str(today.day) + "." +  str(today.month) + "." +  str(today.year))
  html = html.replace('{*order_num*}', str(101))
  html = html.replace('{*name*}', my_name)
  html = html.replace('{*name1*}', my_name)
  #html = html.replace('{*topping*}', topping)
  html = html.replace('{*slices*}', str(num_slices))
  html = html.replace('{*price*}', str(total_price))
  html_img_tag = ''
  encoded_image = ''
  if not is_file_exist('/content/photo.jpg'):
    download_image_from_web("https://ontopnew.s3.il-central-1.amazonaws.com/pizzeria1/Images/intro1_pizza_box.png")
	
  
  encoded_image = convert_img_to_base64('/content/photo.jpg')
  html_img_tag = f"""
<img src="data:image/jpeg;base64,{encoded_image}" width="220" height="160"/>
"""
  html = html.replace('{*img*}', str(html_img_tag))

  s = get_string_from_string_table('pizzeria1', 'print_order_2')
  html = html.replace('{***print_order_2***}', s)
  s = get_string_from_string_table('pizzeria1', 'print_order_3')
  html = html.replace('{***print_order_3***}', s)
  s = get_string_from_string_table('pizzeria1', 'print_order_4')
  html = html.replace('{***print_order_4***}', s)
  html = html.replace('{***print_order_41***}', s)
  #s = get_string_from_string_table('pizzeria1', 'print_order_5')
  #html = html.replace('{***print_order_5***}', s)
  s = get_string_from_string_table('pizzeria2', 'pizza_tray')
  html = html.replace('{***print_order_6***}', s)
  s = get_string_from_string_table('pizzeria1', 'print_order_7')
  html = html.replace('{***print_order_7***}', s)
  
  birthday_html = '''
    <img src="https://ontopnew.s3.il-central-1.amazonaws.com/pizzeria2/Images/balloons4.png" width="65" height="90"/><br>
		<span style="font-size: 20px; font-weight: bold;">{*birthday_msg*} </span>'''
 
  s = get_string_from_string_table('pizzeria2', 'birthday_msg')
  birthday_html = birthday_html.replace('{*birthday_msg*}',s)
      
  no_birthday_html = '''
    <img src="https://ontopnew.s3.il-central-1.amazonaws.com/pizzeria2/Images/no_balloons.png" width="65" height="90"/><br>
		<span style="font-size: 20px; font-weight: bold;"></span>'''
  if is_my_birthday:
    html = html.replace('{*birthday*}', birthday_html)
  else:
    html = html.replace('{*birthday*}', no_birthday_html)  

  display(HTML(html))
  if os.path.exists('/content/photo.jpg'):
    # Delete the file
    os.remove('/content/photo.jpg')





