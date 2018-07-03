import pygame
import random
import time

from configs import add_from_dict
from display import Textbox, Text

patd_text = """You remind me of a former love that I once knew
And you carry a little speech with you
We were holding hands walking through the middle of the street
It's fine with me, I'm just taking in the scenery
You remind me of a few of my famous friends
Well, that all depends what you qualify as friends
You remind me of a few of my famous friends
Well, that all depends what you qualify as friends
Take a chance, take your shoes off, dance in the rain
And I was flashing around and the news spread all over town
I'm not complaining that it's raining, I'm just saying that I like it a lot
More than you think, if the sun would come out and sing with me
You remind me of a few of my famous friends
Well, that all depends what you qualify as friends
You remind me of a few of my famous friends
Well, that all depends what you qualify as friends"""

pygame.init()

tb = Textbox("test", .1, .1, .9, .9)

for fontname in pygame.font.get_fonts():
    add_from_dict(
        {"FONTS": {fontname: {"name": fontname, "size": 20, "color": (255, 255, 255), "highlight color": (0,0,0,255)}}})
tb.add_text_list([Text(fontname + " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$%^&*()-=_+[]{}\\|:\";',.<>/?\n", font_name=fontname) for fontname in
                  pygame.font.get_fonts()])

# chars = ""
# code = 1
# while True:
#     try:
#         chars += chr(code)
#         code += 1
#         if code >= 10000:
#             break
#     except ValueError:
#         break
# print(chars)
# tb.add_text_list([Text(chars)])

display = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

letters = "abcdefghijklmnopqrstuvwxyz1234567890\n"
names = pygame.font.get_fonts()


def gen_font():
    size = random.randint(3, 50)
    color = tuple(random.randint(1, 255) for i in range(0, 3))
    name = names[random.randint(0, len(names) - 1)]
    bold = random.choice([True, False])
    italic = random.choice([True, False])
    path = {"FONTS": {
        name: {"size": size, "color": color, "bold": bold, "italic": italic}}}
    add_from_dict(path)
    return name


def gen_word():
    word = ""
    # for i in range(1, random.randint(1, 100)):
    word += random.choice(letters)
    return word


add_time = time.time() * 1000

quit = False
while not quit:
    display.fill((0, 0, 0))
    if time.time() * 1000 > add_time + 10:
        # tb.add_text_list([Text(gen_word(), gen_font())])
        add_time = time.time() * 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.dict["size"]
            display = pygame.display.set_mode([width, height], pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            # tb.add_text_list([Text(gen_word(), gen_font())])
            pass
        else:
            tb.handle_event(event, display)

    tb.render(display)
    pygame.display.flip()
