import json
import os

def json_write(data,name):

  template = {
    "messages":[]
  }

  if not os.path.isfile(name):
    jsonfile = open(name, "x") 
    json.dump(template, jsonfile,indent = 4)
    jsonfile.close()
    
  with open(name,'r+') as file:
      file_data = json.load(file)
      file_data["messages"].append(data)
      file.seek(0)
      json.dump(file_data, file, indent = 4)
      file.close()


def reset_json(name):
  if os.path.isfile(name):
    os.remove(name)

def send_json(name):
  with open(name,'r+') as file:
    file_data = json.load(file)
    return file_data