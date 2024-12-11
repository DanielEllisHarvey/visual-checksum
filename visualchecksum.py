import turtle
import hashlib

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

colours = ["#000000", "#000088", "#880000", "#008800"]
digest0 = hashlib.sha3_512(b"foobar", usedforsecurity=True).digest()
digest1 = hashlib.sha3_512(b"barfoo"+digest0, usedforsecurity=True).digest()
digest2 = hashlib.sha3_512(b"b4rf00"+digest1, usedforsecurity=True).digest()

turtle.speed(0)
turtle.up()
# turtle.goto(-400,400)
digest_colours = bytes_to_colours(digest0)
digest_direction = bytes_to_pos(digest1)
m = 0
for n in range(0,64):
    for i in range(0,5):
        turtle.down()
        turtle.setheading(digest2[n%64])
        turtle.color(colours[digest_colours[m%256]])
        turtle.forward(5)
        turtle.up()
        m+=1
    turtle.sety((375)-digest_direction[n][1]*40)
    turtle.setx((275)-digest_direction[n][0]*25)
turtle.setpos(1000,1000)
input("done.")
