from IPython.display import display, Javascript
import requests
from IPython.core.display import HTML


def download_html(url):
  response = requests.get(url)
  html = response.text
  return html
  