import base64
with  open("tree.ico","rb") as f:
    b64str = base64.b64encode(f.read())
icon_data = "icon = %s" % b64str
with open("icon.py","w+") as f:
    f.write(icon_data)