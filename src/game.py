## \file general.py
#  this file is the main game file

import general
import world
import pygame
import graphics
import math

## Efficiently renders a part of the game world with given settings.
#
#  The object of WorldRenderer class keeps a reference to World object
#  which it will be rendering. It keeps a pre-rendered image of the
#  world's active area terrain so it can be rendered quickly for
#  real-time viewing. WorldRenderer will smartly change the world active
#  area when the view shifts to the edge of the current area.

class WorldRenderer:

  ## view width in pixels
  VIEW_WIDTH = 100

  ## view height in pixels
  VIEW_HEIGHT = 75

  ## view width in pixels
  VIEW_WIDTH_TILES = math.ceil(VIEW_WIDTH / general.TILE_WIDTH)

  ## view height in pixels
  VIEW_HEIGHT_TILES = math.ceil(VIEW_HEIGHT / general.TILE_HEIGHT)

  ## along with VIEW_WIDTH and VIEW_HEIGHT determines the active area
  #  size, which is width: VIEW_WIDTH_TILES + 2 * TILE_PADDING, height:
  #  VIEW_HEIGHT_TILES + 2 * TILE_PADDING

  TILE_PADDING = 3

  ## active area width in tiles

  ACTIVE_AREA_WIDTH = VIEW_WIDTH_TILES + 2 * TILE_PADDING

  ## active area height in tiles

  ACTIVE_AREA_HEIGHT = VIEW_HEIGHT_TILES + 2 * TILE_PADDING

  @property
  def view_top_left(self):
    return self._view_top_left

  @view_top_left.setter
  def view_top_left(self,value):
    self._view_top_left = value
    # here the world active area is being potentially changed:
    if (value[0] <= self.world.active_area[0] or
        value[1] <= self.world.active_area[0] or
        value[0] + WorldRenderer.VIEW_WIDTH >= self.world.active_area[0] + self.world.active_area[2] or
        value[1] + WorldRenderer.VIEW_HEIGHT >= self.world.active_area[1] + self.world.active_area[3]):
      print("changing")

      self.__change_active_area()

  def __init_attributes(self):
    ## prerendered terrain of the active part of the world
    self.terrain_image = None
    ## position of the top left corner of the view rectangle in world
    #  coordinates (floating point, 1.0 = 1 tile)
    self._view_top_left = (0.0,0.0)
    ## world that is being rendered
    self.world = None

  def __init__(self,world):
    self.__init_attributes()
    self.world = world
    self.__change_active_area()

  ## Private method that is called to change the world active area and
  #  prerender the terrain for it. The active area is set depending on
  #  the current view coordinates.

  def __change_active_area(self):
    image_compositor = graphics.ImageCompositor()
    self.world.active_area = (self.view_top_left[0] - WorldRenderer.TILE_PADDING,self.view_top_left[1] - WorldRenderer.TILE_PADDING,WorldRenderer.ACTIVE_AREA_WIDTH,WorldRenderer.ACTIVE_AREA_HEIGHT)
    self.terrain_image = image_compositor.make_terrain_image(self.world.world_area)

  ## Renders the current world view.
  #
  #  @return the image (Surface object) of the rendered world area, its
  #          size is defined by VIEW_WIDTH and VIEW_HEIGHT constants,
  #          if the image couldn't be rendered (no world assigned etc.),
  #          None is returned

  def render(self):
    return self.terrain_image

#=======================================================================

pygame.init()
screen = pygame.display.set_mode((900,600))

done = False

w = world.World(general.RESOURCE_PATH + "/world")
renderer = WorldRenderer(w)

renderer.view_top_left = (20,50)

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        print("l")
        renderer.view_top_left = (renderer.view_top_left[0] - 1,renderer.view_top_left[1])
      elif event.key == pygame.K_RIGHT:
        print("r")
        renderer.view_top_left = (renderer.view_top_left[0] + 1,renderer.view_top_left[1])
      if event.key == pygame.K_UP:
        print("u")
        renderer.view_top_left = (renderer.view_top_left[0],renderer.view_top_left[1] - 1)
      elif event.key == pygame.K_DOWN:
        print("d")
        renderer.view_top_left = (renderer.view_top_left[0],renderer.view_top_left[1] + 1)

  screen.fill((255,255,255))

  screen.blit(renderer.render(),(10,10))

  pygame.display.flip()
