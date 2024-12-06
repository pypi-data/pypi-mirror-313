from pandas.core.frame import DataFrame
import pandas as pd
from google.colab import data_table
import numpy as np
import time
import datetime

language = 'hebrew'

def set_language(lang):
  global language
  language = lang

def get_language():
  global language
  return language 

def read_table(url):
  return pd.read_csv(url, encoding='utf-8')

def filter_data(data, field, value, to_value=None):
  if str(value).isnumeric():
    value = int(value)
  if to_value is None:
    return data[data[field].eq(value)]
  else:
    if str(to_value).isnumeric():
       to_value = int(to_value)
  ge = data[data[field].ge(value)]
  return ge[ge[field].le(to_value)]

def get_columns(data, field):
  return data[field]

'''def string_replace(html, marker, field):
  pizzeria_table = table.query("project == 'pizzeria1'")
  result = filter_data(pizzeria_table, "name","draw_pizza_1")
  column = get_columns(result, 'hebrew')
  column[0]'''

def get_string_from_string_table(project, name):
  global language
  #print(project, " " , name)

  table = read_table('https://ontopnew.s3.il-central-1.amazonaws.com/library/StringTable/string_table_utf_08.csv')
  #table = read_table('/content/string_table_utf_03.csv')
  pizzeria_table = table.query("project == @project")
  result = filter_data(pizzeria_table, "name", name)
  column = get_columns(result, language)

  #print(column.index[len(column)-1] )
  for item in column:
    #print(item)
    return item
  return '0'#column[0]

def get_banners_strings():
  global language
  project_name = 'banner'
  csv_file='https://ontopnew.s3.il-central-1.amazonaws.com/library/StringTable/string_table_utf_06.csv'
  table = pd.read_csv(csv_file, encoding='utf-8')
  project_data = table.query("project == @project_name")
  strings = project_data[language].tolist()
  return strings
 