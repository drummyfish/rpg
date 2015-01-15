import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  pygame.draw.line(screen, (0, 0, 255), (0, 0), (639, 479))

  pygame.display.flip()
