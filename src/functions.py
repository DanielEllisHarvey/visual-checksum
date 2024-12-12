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

def convert_to_png(ps_filename: str, output_filename: str = "img") -> None:
    img = Image.open(ps_filename).rotate(90, expand=True)
    img.save(output_filename+".png")

def set_bg(colour: str) -> None:
    turtle.speed(0)
    turtle.pensize(1)
    turtle.up()
    turtle.goto(-1000, 1000)
    turtle.down()
    turtle.fillcolor(colour)
    turtle.color(colour)
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(2000)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()

colours = ["#777777", "#77ff77", "#7777ff", "#ff7777"]
colours1 = ["#777777", "#ff77ff", "#ffbb77", "#77ffff"]

step = 5
pen_size = 2
turtle.speed(0)

def hmac_single(
    data0: str,
    data1: str,
    data2: str,
    data3: str,
    filename: str = "img.png",
    hmac_pw: str = "",
    hmac_salt: str = "salt123",
    straight_lines: bool = True
) -> None:
    hmac_key = quick_pbkdf(hmac_pw, hmac_salt, 10000)
    digest0 = hmac.new(hmac_key, bytes(data0, "utf-8"), hashlib.sha3_512).digest()
    digest0 += hmac.new(hmac_key, bytes(data1, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest1 = hmac.new(hmac_key, bytes(data2, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest2 = hmac.new(hmac_key, bytes(data3, "utf-8")+digest1, hashlib.sha3_512).digest()

    draw_settings(
        digest0,
        digest1,
        digest2,
        filename,
        straight_lines
    )
    
def hmac_cycle(
    data0: str,
    data1: str,
    data2: str,
    data3: str,
    iters: int,
    filename: str = "img.png",
    hmac_pw: str = "",
    hmac_salt: str = "salt123",
    straight_lines: bool = True
) -> None:
    hmac_key = quick_pbkdf(hmac_pw, hmac_salt, 10000)
    digest0 = hmac.new(hmac_key, bytes(data0, "utf-8"), hashlib.sha3_512).digest()
    digest0 += hmac.new(hmac_key, bytes(data1, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest1 = hmac.new(hmac_key, bytes(data2, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest2 = hmac.new(hmac_key, bytes(data3, "utf-8")+digest1, hashlib.sha3_512).digest()

    for loop in range(0,iters):
        if loop & 511 == 0: print(loop)
        digest0 = hmac.new(hmac_key, b"digest0seed"+digest2[-128:], hashlib.sha3_512).digest()
        digest0 += hmac.new(hmac_key, b"digest01seed"+digest0[-128:], hashlib.sha3_512).digest()
        digest1 = hmac.new(hmac_key, b"digest1seed"+digest0[-128:], hashlib.sha3_512).digest()
        digest2 = hmac.new(hmac_key, b"digest2seed"+digest1[-128:], hashlib.sha3_512).digest()

    draw_settings(
        digest0,
        digest1,
        digest2,
        filename,
        straight_lines
    )

def hmac_cycle_expand(data0: str,
    data1: str,
    data2: str,
    data3: str,
    iters: int,
    filename: str = "img.png",
    hmac_pw: str = "",
    hmac_salt: str = "salt123",
    straight_lines: bool = True
) -> None:
    hmac_key = quick_pbkdf(hmac_pw, hmac_salt, 10000)
    digest0 = hmac.new(hmac_key, bytes(data0, "utf-8"), hashlib.sha3_512).digest()
    digest0 += hmac.new(hmac_key, bytes(data1, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest1 = hmac.new(hmac_key, bytes(data2, "utf-8")+digest0, hashlib.sha3_512).digest()
    digest2 = hmac.new(hmac_key, bytes(data3, "utf-8")+digest1, hashlib.sha3_512).digest()

    for loop in range(0,iters):
        if loop & 511 == 0: print(loop)
        digest0 += hmac.new(hmac_key, b"digest0seed"+digest2[-128:], hashlib.sha3_512).digest()
        digest0 += hmac.new(hmac_key, b"digest01seed"+digest0[-128:], hashlib.sha3_512).digest()
        digest1 += hmac.new(hmac_key, b"digest1seed"+digest0[-128:], hashlib.sha3_512).digest()
        digest2 += hmac.new(hmac_key, b"digest2seed"+digest1[-128:], hashlib.sha3_512).digest()

    draw_settings(
        digest0,
        digest1,
        digest2,
        filename,
        straight_lines
    )

def draw_settings(
    digest0: bytes,
    digest1: bytes,
    digest2: bytes,
    filename: str,
    straight_lines: bool = True
) -> None:
    filename = filename.replace(".png", "")
    screenX = 2970/2.2
    screenY = 2100/2.2
    turtle.setup(screenX, screenY)
    turtle.hideturtle()
    turtle.up()
    digest_colours = bytes_to_colours(digest0)
    digest_direction = bytes_to_pos(digest1)
    digest_size = len(digest1)
    sX_16 = screenX/256
    sY_16 = screenY/256
    colour_max = digest_size*4
    m = 0
    turtle.pensize(pen_size)
    for n in range(0,digest_size):
        if n & 31 == 0: print(n)
        turtle.down()
        if straight_lines: turtle.setheading(digest2[n%digest_size]*1.4)
        for i in range(0,5):
            if not straight_lines: turtle.setheading(digest2[(m)%digest_size]*1.4)
            turtle.color(colours[digest_colours[m%colour_max]])
            turtle.forward(step)
            m+=1
        turtle.up()
        
        turtle.sety((digest_direction[n][1]*sY_16)-(screenY/2)+10)
        turtle.setx((digest_direction[n][0]*sX_16)-(screenX/2)+10)
        
        if n & 15 == 15:
            turtle.getscreen().getcanvas().postscript(file=filename+".ps")
            convert_to_png(filename+".ps", filename)

    turtle.getscreen().getcanvas().postscript(file=filename+".ps")
    convert_to_png(filename+".ps", filename)
    turtle.reset()
