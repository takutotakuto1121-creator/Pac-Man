import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("名前入力")
font = pygame.font.Font(None, 40)

name = ""
confirmed_name = ""

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN:
        confirmed_name = name
      elif event.key == pygame.K_BACKSPACE:
        name = name[:-1]
      else:
        if len(name) < 12 and event.unicode.isprintable():
          name += event.unicode

  screen.fill((30, 30, 30))

  prompt = font.render("Enter your name:", True, (255, 255, 255))
  input_box = font.render(name + "_", True, (255, 220, 100))
  screen.blit(prompt, (50, 70))
  screen.blit(input_box, (50, 120))

  if confirmed_name:
    msg = font.render(f"Hello, {confirmed_name}!", True, (120, 255, 160))
    screen.blit(msg, (50, 200))

  pygame.display.flip()
