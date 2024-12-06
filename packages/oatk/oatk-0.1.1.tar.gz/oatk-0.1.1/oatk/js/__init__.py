import os

script = os.path.join(os.path.dirname(os.path.realpath(__file__)), "oatk.js")
with open(script, "r") as file:
  src = file.read()

def as_src():
  return src
