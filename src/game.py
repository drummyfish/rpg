## \file general.py
#  this file is the main game file


import graphics
import general
import world
import pygame
import math

#=======================================================================

pygame.init()
screen = pygame.display.set_mode((800,480))

done = False

w = world.World(general.RESOURCE_PATH + "/world")
renderer = graphics.WorldRenderer(w)

renderer.view_top_left = (20,50)

go_up = False
go_down = False
go_left = False
go_right = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        go_left = True
      elif event.key == pygame.K_RIGHT:
        go_right = True
      if event.key == pygame.K_UP:
        go_up = True
      elif event.key == pygame.K_DOWN:
        go_down = True
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        go_left = False
      elif event.key == pygame.K_RIGHT:
        go_right = False
      if event.key == pygame.K_UP:
        go_up = False
      elif event.key == pygame.K_DOWN:
        go_down = False

  if go_up:
    renderer.view_top_left = (renderer.view_top_left[0],renderer.view_top_left[1] - 5)
  if go_down:
    renderer.view_top_left = (renderer.view_top_left[0],renderer.view_top_left[1] + 5)
  if go_left:
    renderer.view_top_left = (renderer.view_top_left[0] - 5,renderer.view_top_left[1])
  if go_right:
    renderer.view_top_left = (renderer.view_top_left[0] + 5,renderer.view_top_left[1])

  screen.fill((255,255,255))

  screen.blit(renderer.render(),(0,0))

  pygame.display.flip()
