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
    for byte in range(len(digest)):
        result += [[digest[byte-1], digest[byte]]]
    return result

def quick_pbkdf(password: str, salt: str = "genericsalt", iters: int = 100) -> bytes:
    der_key = bytes(password, "utf-8")
    for iter in range(iters):
        der_key = hmac.digest(bytes(salt+str(iter), "utf-8"), der_key, hashlib.sha3_512)
    return der_key

def convert_to_png(ps_file):
    img = Image.open(ps_file).rotate(90, expand=True)
    img.save("img.png")

colours = ["#777777", "#77ff77", "#7777ff", "#ff7777"]

hmac_key = quick_pbkdf("securepassword1", "securesalt1", 10000)
digest0 = hmac.new(hmac_key, b"0", hashlib.sha3_512).digest()
digest0 += hmac.new(hmac_key, b"1"+digest0, hashlib.sha3_512).digest()
digest1 = hmac.new(hmac_key, b"2"+digest0, hashlib.sha3_512).digest()
digest2 = hmac.new(hmac_key, b"3"+digest1, hashlib.sha3_512).digest()

for loop in range(0,0):
    if loop & 511 == 0: print(loop)
    digest0 += hmac.new(hmac_key, b"digest0seed"+digest2[-128:], hashlib.sha3_512).digest()
    digest0 += hmac.new(hmac_key, b"digest01seed"+digest0[-128:], hashlib.sha3_512).digest()
    digest1 += hmac.new(hmac_key, b"digest1seed"+digest0[-128:], hashlib.sha3_512).digest()
    digest2 += hmac.new(hmac_key, b"digest2seed"+digest1[-128:], hashlib.sha3_512).digest()
# digest1 += hmac.new(hmac_key, b"information2"+digest0, hashlib.sha3_512).digest()

screenX = 2970/2.2
screenY = 2100/2.2
turtle.setup(screenX, screenY)
turtle.speed(0)
turtle.hideturtle()
turtle.up()
# turtle.bgcolor("#000000")
turtle.fillcolor("#dfddff")
turtle.begin_fill()
turtle.goto(-1000, 1000)
turtle.down()
for i in range(4):
    turtle.forward(2000)
    turtle.right(90)
turtle.end_fill()
# turtle.goto(-400,400)
digest_colours = bytes_to_colours(digest0)
digest_direction = bytes_to_pos(digest1)
digest_size = len(digest1)
sX_16 = screenX/256
sY_16 = screenY/256
colour_max = digest_size*4
m = 0
for n in range(0,digest_size):
    if n & 31 == 0: print(n)
    turtle.down()
    turtle.setheading(digest2[(n)%digest_size]*1.4)
    for i in range(0,5):
        turtle.pensize(2)
        turtle.color(colours[digest_colours[m%colour_max]])
        turtle.forward(7)
        print(turtle.position())
        m+=1
    turtle.up()
    
    turtle.sety((digest_direction[n][1]*sY_16)-(screenY/2)+10)
    turtle.setx((digest_direction[n][0]*sX_16)-(screenX/2)+10)
    
    if n & 15 == 15:
        turtle.getscreen().getcanvas().postscript(file="output.ps")
        convert_to_png("output.ps")

# turtle.up()

# turtle.setpos(-screenX/2+20, screenY/2-(20+43))
# turtle.write("information1\ninformation2\ninformation3", font=("Verdana", 11, "bold"))

turtle.getscreen().getcanvas().postscript(file="output.ps")
convert_to_png("output.ps")
