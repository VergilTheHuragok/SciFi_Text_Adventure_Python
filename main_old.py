import pygame
from display_old import Text, Font


pygame.init()

display = pygame.display.set_mode([500, 500], pygame.RESIZABLE)

text = Text("hi", Font(color=(255, 0, 0), italic=True))

text.render(display, [500//2, 500//2])

pygame.display.flip()

input()
