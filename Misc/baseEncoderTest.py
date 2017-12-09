import base64
jpgtxt = base64.encodestring(open("clip_image00455.jpg","rb").read())
print(jpgtxt)
f = open("jpg1_b64.txt", "wb")
f.write(jpgtxt.decode("utf-8"))
f.close()

# ----
newjpgtxt = open("jpg1_b64.txt","rb").read()

g = open("out.jpg", "w")
g.write(base64.decodestring(newjpgtxt))
g.close()