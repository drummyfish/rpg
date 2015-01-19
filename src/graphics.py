  ## \file graphics.py
  #
  #  This file contains classes working with graphics.

import os
import pygame
import general
import time
import world
import draw
import random

#=======================================================================

  ## Holds images (i.e. main tile variations, corners etc.) of a game
  # (terrain) tile, the corners are represented by a string in following
  # format: cornar_AB_XY, where A is U or D (up, down), B is L or R
  # (left, right) and X and Y are either 0 (opposite not present) or 1
  # (opposite present).
  # For example if there is a part of terrain as follows:
  #   0 1
  # 0 K L
  # 1 K L
  # then for example in the upper left corner of L at [1,1] there should
  # be drawn a corner of K with identifier corner_UL_01.

class TileImageContainer:
  def init(self):
    self.main_tile = [None,None,None,None] # main tile variations or alternatively animation frames
    self.corner_UL_00 = None
    self.corner_UL_01 = None
    self.corner_UL_10 = None
    self.corner_UL_11 = None

    self.corner_UR_00 = None
    self.corner_UR_01 = None
    self.corner_UR_10 = None
    self.corner_UR_11 = None

    self.corner_DL_00 = None
    self.corner_DL_01 = None
    self.corner_DL_10 = None
    self.corner_DL_11 = None

    self.corner_DR_00 = None
    self.corner_DR_01 = None
    self.corner_DR_10 = None
    self.corner_DR_11 = None

  def __init__(self,filename):
    self.init()
    self.load_from_file(filename)

  def load_from_file(self,filename):
    image = pygame.image.load(filename)

    self.main_tile[0] = image.subsurface(68,0,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[1] = image.subsurface(102,0,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[2] = image.subsurface(68,28,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[3] = image.subsurface(102,28,general.TILE_WIDTH,general.TILE_HEIGHT)

    self.corner_UL_00 = image.subsurface(51,42,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UL_01 = image.subsurface(17,42,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UL_10 = image.subsurface(51,14,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UL_11 = image.subsurface(17,14,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UR_00 = image.subsurface(0,42,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UR_01 = image.subsurface(34,42,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UR_10 = image.subsurface(0,14,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_UR_11 = image.subsurface(34,14,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DL_00 = image.subsurface(51,0,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DL_01 = image.subsurface(17,0,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DL_10 = image.subsurface(51,28,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DL_11 = image.subsurface(17,28,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DR_00 = image.subsurface(0,0,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DR_01 = image.subsurface(34,0,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DR_10 = image.subsurface(0,28,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)
    self.corner_DR_11 = image.subsurface(34,28,general.SUBTILE_WIDTH,general.SUBTILE_HEIGHT)

#=======================================================================

  ## Assembles images out of image resources.

class ImageCompositor:

  #---------------------------------------------------------------------

  ## Makes a character image with given body, head, animation type, frame
  #  and gear
  #
  #  @param self object pointer
  #  @param body_name resource name of the body
  #
  #  @return Surface object - the generated image

  def make_character_image(self, race, gender, head_number, animation_type, animation_frame):

    animation_string = ""
    direction_string = ""
    race_string = ""
    gender_string = ""

    head_coordinates = (0,0)

    if race == general.RACE_HUMAN:
      race_string = "human"

    if gender == general.GENDER_MALE:
      gender_string = "male"
    else:
      gender_string = "female"

    if animation_type == general.ANIMATION_IDLE_UP:
      animation_string = "idle"
      direction_string = "up"
      head_coordinates = (4,0)
    elif animation_type == general.ANIMATION_IDLE_RIGHT:
      animation_string = "idle"
      direction_string = "right"
      head_coordinates = (6,0)
    elif animation_type == general.ANIMATION_IDLE_DOWN:
      animation_string = "idle"
      direction_string = "down"
      head_coordinates = (4,0)
    else:                         # idle left
      animation_string = "idle"
      direction_string = "left"
      head_coordinates = (3,0)

    image_head = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_head_" + str(head_number) + "_" + direction_string + ".png"))

    if animation_type in (general.ANIMATION_IDLE_RIGHT,general.ANIMATION_IDLE_LEFT):
      image1 = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_body_" + animation_string + "_" + direction_string + "_layer1.png"))
      image2 = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_body_" + animation_string + "_" + direction_string + "_layer2.png"))
      image3 = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_body_" + animation_string + "_" + direction_string + "_layer3.png"))

      image1.blit(image2,(0,0))
      image1.blit(image3,(0,0))
      image1.blit(image_head,head_coordinates)
    else:
      image1 = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_body_" + animation_string + "_" + direction_string + ".png"))
      image1.blit(image_head,head_coordinates)

    return image1

  #---------------------------------------------------------------------

  ## Helper private method that returns the priority of given tile type
  #  or 0 if the argument is not of TileType class.

  def __tile_priority(self, tile_type):
    try:
      return tile_type.get_priority()
    except Exception:
      return 0

  #---------------------------------------------------------------------

  ## Helper private method, returns ordered list of all tile priorities
  #  that appear in given TerrainArray object.

  def __make_tile_priority_list(self, terrain_array):
    result = []

    for j in range(terrain_array.get_height()):
      for i in range(terrain_array.get_width()):
        priority = self.__tile_priority(terrain_array.get_tile_type(i,j))

        if not priority in result:
          result.append(priority)

    return sorted(result)

  #---------------------------------------------------------------------

  ## Makes a terrain image.
  #
  #  @param terrain_array TerrainArray object to be drawn
  #  @return Surface object - the generated image

  def make_terrain_image(self, terrain_array):
    result_image = pygame.Surface((terrain_array.get_width() * general.TILE_WIDTH, terrain_array.get_height() * general.TILE_HEIGHT))
    result_image.fill((255,255,255,0))

    tile_pictures = {}

    for current_priority in self.__make_tile_priority_list(terrain_array):      # draw the terrain in layers

      for j in range(terrain_array.get_height()):
        for i in range(terrain_array.get_width()):
          tile_type = terrain_array.get_tile_type(i,j)

          if tile_type == None:
            continue

          tile_priority = tile_type.get_priority()

          if not tile_priority == current_priority:   # only draw one priority at a time
            continue

          variant = terrain_array.get_tile_variant(i,j)
          tile_id = tile_type.get_identifier()

          if not (tile_id in tile_pictures):  # lazy image loading
            tile_pictures[tile_id] = TileImageContainer(os.path.join(general.RESOURCE_PATH,tile_type.get_filename()))

          # draw the main tile:
          result_image.blit(tile_pictures[tile_id].main_tile[variant],(i * general.TILE_WIDTH,j * general.TILE_HEIGHT))

          # draw corners and borders:

          # UL corner:
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j)):
           result_image.blit(tile_pictures[tile_id].corner_DR_00,(i * general.TILE_WIDTH - general.SUBTILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

          # UR corner
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j)):
            result_image.blit(tile_pictures[tile_id].corner_DL_00,(i * general.TILE_WIDTH + general.TILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

          # DR corner
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j + 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j + 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j)):
            result_image.blit(tile_pictures[tile_id].corner_UL_00,(i * general.TILE_WIDTH + general.TILE_WIDTH,j * general.TILE_HEIGHT + general.TILE_HEIGHT))

          # DL corner
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j + 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j + 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j)):
            result_image.blit(tile_pictures[tile_id].corner_UR_00,(i * general.TILE_WIDTH - general.SUBTILE_WIDTH,j * general.TILE_HEIGHT + general.TILE_HEIGHT))

          # upper border
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j - 1)):
            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j - 1)):  # left
              helper_image = tile_pictures[tile_id].corner_DL_01
            else:
              helper_image = tile_pictures[tile_id].corner_DL_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j - 1)):  # right
              helper_image = tile_pictures[tile_id].corner_DR_01
            else:
              helper_image = tile_pictures[tile_id].corner_DR_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH + general.SUBTILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

          # left border
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j)):
            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j - 1)):  # up
              helper_image = tile_pictures[tile_id].corner_UR_10
            else:
              helper_image = tile_pictures[tile_id].corner_UR_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH - general.SUBTILE_WIDTH,j * general.TILE_HEIGHT))

            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j + 1)):  # down
              helper_image = tile_pictures[tile_id].corner_DR_10
            else:
              helper_image = tile_pictures[tile_id].corner_DR_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH - general.SUBTILE_WIDTH,j * general.TILE_HEIGHT + general.SUBTILE_HEIGHT))

          # right border
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j)):
            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j - 1)):  # up
              helper_image = tile_pictures[tile_id].corner_UL_10
            else:
              helper_image = tile_pictures[tile_id].corner_UL_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH + general.TILE_WIDTH,j * general.TILE_HEIGHT))

            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j + 1)):  # down
              helper_image = tile_pictures[tile_id].corner_DL_10
            else:
              helper_image = tile_pictures[tile_id].corner_DL_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH + general.TILE_WIDTH,j * general.TILE_HEIGHT + general.SUBTILE_HEIGHT))

          # lower border
          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j + 1)):
            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j + 1)):  # left
              helper_image = tile_pictures[tile_id].corner_UL_01
            else:
              helper_image = tile_pictures[tile_id].corner_UL_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH,j * general.TILE_HEIGHT + general.TILE_HEIGHT))

            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i + 1,j + 1)):  # right
              helper_image = tile_pictures[tile_id].corner_UR_01
            else:
              helper_image = tile_pictures[tile_id].corner_UR_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH + general.SUBTILE_WIDTH,j * general.TILE_HEIGHT + general.TILE_HEIGHT))

    pygame.draw.rect(result_image,(0,0,0,255),pygame.Rect(0,0,result_image.get_width(),result_image.get_height()),1)

    return result_image

  #---------------------------------------------------------------------

#=======================================================================

pygame.init()
screen = pygame.display.set_mode((900,600))

done = False

myyy = ImageCompositor()

imgs = []

imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_RIGHT,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_DOWN,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_LEFT,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_UP,1))

tile1 = world.TileType(1,"tile_grass.png")
tile2 = world.TileType(2,"tile_snow.png")

print(tile1.get_identifier())
print(tile2.get_identifier())

ter_array = world.TerrainArray(12,10)

for j in range(10):
  for i in range(12):
    number = random.randint(0,2)

    if number == 0:
      ter_array.set_tile(i,j,tile1,0)
    elif number == 1:
      ter_array.set_tile(i,j,tile2,0)

#ter_array.set_tile(2,1,tile1,0)
#ter_array.set_tile(3,1,tile1,0)
#ter_array.set_tile(1,2,tile1,0)
#ter_array.set_tile(2,2,tile1,0)
#ter_array.set_tile(3,2,tile1,0)
#ter_array.set_tile(4,2,tile2,0)
#ter_array.set_tile(2,3,tile1,0)
#ter_array.set_tile(3,3,tile2,0)
#ter_array.set_tile(4,3,tile2,0)
#ter_array.set_tile(2,4,tile1,0)
#ter_array.set_tile(4,4,tile2,0)
#ter_array.set_tile(4,5,tile2,0)
#ter_array.set_tile(1,6,tile2,0)
#ter_array.set_tile(2,6,tile2,0)
#ter_array.set_tile(4,6,tile2,0)

ter = myyy.make_terrain_image(ter_array)

i = 0

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  screen.fill((255,255,255))

  frame = int(round(time.time())) % 4

  screen.blit(imgs[frame],(20,30))
  screen.blit(imgs[(frame + 1) % 4],(50,65))
  screen.blit(imgs[(frame + 2) % 4],(90,45))
  screen.blit(imgs[(frame + 3) % 4],(110,80))
  screen.blit(imgs[frame],(55,10))

  screen.blit(imgs[frame],(200,300))
  screen.blit(imgs[(frame + 1) % 4],(500,650))
  screen.blit(imgs[(frame + 2) % 4],(400,200))
  screen.blit(imgs[(frame + 3) % 4],(310,120))
  screen.blit(imgs[frame],(200,190))

  screen.blit(ter,(300,200))

  pygame.display.flip()
