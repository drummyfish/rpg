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
  VIEW_WIDTH = 640

  ## view height in pixels
  VIEW_HEIGHT = 480

  ## view width in pixels
  VIEW_WIDTH_TILES = math.ceil(VIEW_WIDTH / general.TILE_WIDTH)

  ## view height in pixels
  VIEW_HEIGHT_TILES = math.ceil(VIEW_HEIGHT / general.TILE_HEIGHT)

  ## along with VIEW_WIDTH and VIEW_HEIGHT determines the active area
  #  size, which is width: VIEW_WIDTH_TILES + 2 * TILE_PADDING, height:
  #  VIEW_HEIGHT_TILES + 2 * TILE_PADDING

  TILE_PADDING = 10

  ## active area width in tiles

  ACTIVE_AREA_WIDTH = VIEW_WIDTH_TILES + 2 * TILE_PADDING

  ## active area height in tiles

  ACTIVE_AREA_HEIGHT = VIEW_HEIGHT_TILES + 2 * TILE_PADDING

  def _view_top_left_tiles(self):
    return (math.floor(self._view_top_left[0] / general.TILE_WIDTH),math.floor(self._view_top_left[1] / general.TILE_HEIGHT))

  @property
  def view_top_left(self):
    return self._view_top_left

  @view_top_left.setter
  def view_top_left(self,value):
    self._view_top_left = value
    in_tiles = self._view_top_left_tiles()

    # here the world active area is being potentially changed if the view rectangle is at the border of the active area:
    if ((self.world.active_area[0] > 0 and in_tiles[0] <= self.world.active_area[0]) or
        (self.world.active_area[1] > 0 and in_tiles[1] <= self.world.active_area[1]) or
        (self.world.active_area[0] + self.world.active_area[2] < self.world.width and in_tiles[0] + WorldRenderer.VIEW_WIDTH_TILES >= self.world.active_area[0] + self.world.active_area[2]) or
        (self.world.active_area[1] + self.world.active_area[3] < self.world.height and in_tiles[1] + WorldRenderer.VIEW_HEIGHT_TILES >= self.world.active_area[1] + self.world.active_area[3])):
      print("changing active area")

      self.__change_active_area()

  def __init_attributes(self):
    ## prerendered terrain of the active part of the world
    self.terrain_image = None
    ## position of the top left corner of the view rectangle in pixels
    self._view_top_left = (0,0)
    ## image to which the terrain will be rendered and which will be
    #  returned as the rendered part of the world
    self.canvas = pygame.Surface((WorldRenderer.VIEW_WIDTH,WorldRenderer.VIEW_HEIGHT))
    ## world that is being rendered
    self.world = None

  ## Gets the pixel coordinates of the top left corner of the view
  #  rectangle relative to the world active area.
  #
  #  @return pixel coordinates in format (x,y)

  def view_top_left_relative(self):
    return (self.view_top_left[0] - self.world.active_area[0] * general.TILE_WIDTH,self.view_top_left[1] - self.world.active_area[1] * general.TILE_HEIGHT)

  def __init__(self,world):
    self.__init_attributes()
    self.world = world
    self.__change_active_area()

  ## Private method that is called to change the world active area and
  #  prerender the terrain for it. The active area is set depending on
  #  the current view coordinates.

  def __change_active_area(self):
    image_compositor = graphics.ImageCompositor()
    view_tile_coordinates = self._view_top_left_tiles()

    new_area = (general.saturate(view_tile_coordinates[0] - WorldRenderer.TILE_PADDING,0,self.world.width - WorldRenderer.ACTIVE_AREA_WIDTH),
                general.saturate(view_tile_coordinates[1] - WorldRenderer.TILE_PADDING,0,self.world.height - WorldRenderer.ACTIVE_AREA_HEIGHT),
                WorldRenderer.ACTIVE_AREA_WIDTH,
                WorldRenderer.ACTIVE_AREA_HEIGHT)

    self.world.active_area = new_area
    self.terrain_image = image_compositor.make_terrain_image(self.world.world_area)

  ## Renders the current world view.
  #
  #  @return the image (Surface object) of the rendered world area, its
  #          size is defined by VIEW_WIDTH and VIEW_HEIGHT constants,
  #          if the image couldn't be rendered (no world assigned etc.),
  #          None is returned

  def render(self):
    self.canvas.fill((255,0,0,0))
    view_relative = self.view_top_left_relative()
    subsurface_rect = pygame.Rect(view_relative[0],view_relative[1],WorldRenderer.VIEW_WIDTH,WorldRenderer.VIEW_HEIGHT)
    subsurface_rect = subsurface_rect.clip(self.terrain_image.get_rect())
    self.canvas.blit(self.terrain_image,(-1 * view_relative[0],-1 * view_relative[1]))

    return self.canvas

#=======================================================================

pygame.init()
screen = pygame.display.set_mode((900,600))

done = False

w = world.World(general.RESOURCE_PATH + "/world")
renderer = WorldRenderer(w)

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

  screen.blit(renderer.render(),(10,10))

  pygame.display.flip()
