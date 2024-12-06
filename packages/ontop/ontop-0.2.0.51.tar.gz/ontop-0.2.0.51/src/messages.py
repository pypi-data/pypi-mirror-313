
from media import *

# Error msg
def error_msg(func, msg):
  print("\n")
  print(print_background(print_color(func+" שגיאה בפקודה", colors.WHITE), colors.RED))
  print(msg)
  print("נסו לתקן והריצו שוב")
  print("\n")