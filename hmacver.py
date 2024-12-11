import turtle
import hashlib
import hmac
from PIL import Image

def bytes_to_colours(digest: bytes) -> list:
    result = []
    for byte in digest:
        result += [byte & 3, (byte & 12) >> 2, (byte & 48) >> 4, (byte & 192) >> 6]
    return result

def bytes_to_pos(digest: bytes) -> list:
    result = []
    for byte in digest:
        result += [[byte & 15, (byte & 240) >> 4]]
    return result

def quick_pbkdf(password: str, salt: str = "genericsalt", iters: int = 100) -> bytes:
    der_key = bytes(password, "utf-8")
    for iter in range(iters):
        der_key = hmac.digest(bytes(salt+str(iter), "utf-8"), der_key, hashlib.sha3_512)
    return der_key

def convert_to_png(ps_file):
    img = Image.open(ps_file)
    img.save("img.png")

colours = ["#777777", "#77ff77", "#7777ff", "#ff7777"]

hmac_key = quick_pbkdf("password1", "genericsalt", 1000)
digest0 = hmac.new(hmac_key, b"information1", hashlib.sha3_512).digest()
digest1 = hmac.new(hmac_key, b"information2"+digest0, hashlib.sha3_512).digest()
digest2 = hmac.new(hmac_key, b"information3"+digest1, hashlib.sha3_512).digest()

screenX = 2100/3
screenY = 2970/3
turtle.setup(screenX, screenY)
turtle.speed(100)
turtle.up()
# turtle.goto(-400,400)
digest_colours = bytes_to_colours(digest0)
digest_direction = bytes_to_pos(digest1)
m = 0
for n in range(0,64):
    for i in range(0,5):
        turtle.pensize(2)
        turtle.setheading(digest2[n%64])
        turtle.color(colours[digest_colours[m%256]])
        turtle.forward(10)
        m+=1
    turtle.up()
    
    turtle.sety((digest_direction[n][1]*screenY/16)-screenY/2)
    turtle.setx((digest_direction[n][0]*screenX/16)-screenX/2)
    
    turtle.down()

turtle.up()

# turtle.setpos(-screenX/2+20, screenY/2-(20+43))
# turtle.write("information1\ninformation2\ninformation3", font=("Verdana", 11, "bold"))

turtle.setpos(1000,1000)

turtle.getscreen().getcanvas().postscript(file="output.ps")
convert_to_png("output.ps")
