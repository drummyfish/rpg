  ## \file graphics.py
  #
  #  This file contains classes working with graphics.

import os
import pygame
import general
import time
import world
import draw

#-----------------------------------------------------------------------

  ## Assembles images out of image resources.

class ImageCompositor:

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

  ## Makes a terrain image.
  #
  #  @param terrain_array list of lists of tuples(2D array or pairs) of
  #         representing the terrain, where the pair at each position is
  #         (A, B), where A is an integer value corresponding to tiles
  #         in tile_key, i.e. 0 is first tile in tile_keys, 1 is
  #         the second etc., if the value is out of range of tile_key
  #         list (even negative), transparent tile is drawn, B is
  #         the tile variant (0 to 3 including)
  #  @param tile_key list of TileType objects
  #  @return Surface object - the generated image

  def make_terrain_image(self, terrain_array, tile_key):
    result_image = pygame.Surface((len(terrain_array[0]) * general.TILE_WIDTH,len(terrain_array) * general.TILE_HEIGHT))

    result_image.fill((255,255,255,0))

    for j in range(len(terrain_array)):
      for i in range(len(terrain_array[j])):

        tile_number = terrain_array[j][i][0]
        tile_variant = terrain_array[j][i][1]

        if tile_number in range(len(tile_key)):
          result_image.blit(tile_key[tile_number].main_tile[tile_variant],(i * general.TILE_WIDTH,j * general.TILE_HEIGHT))

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

tile1 = general.TileImageContainer("../resources/tile_grass.png")
tile2 = general.TileImageContainer("../resources/tile_snow.png")

ter_array = [[(1,0), (1,0), (1,2), (0,2), (0,0)],
             [(1,2), (1,0), (1,1), (1,0), (1,0)],
             [(1,1), (1,1), (1,1), (1,0), (1,0)],
             [(1,1), (1,1), (1,2), (1,1), (1,1)],
             [(1,2), (2,0), (0,0), (0,0), (0,0)],
             [(0,1), (1,0), (0,2), (2,1), (0,1)],
             [(0,2), (1,2), (0,0), (2,1), (2,0)]]

ter = myyy.make_terrain_image(ter_array,[tile1,tile2])

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
