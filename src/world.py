## \file world.py
#
#  This file contains main game core classes.

import os
import pygame
import general
import time
import sys
import numpy

#=======================================================================

## Represents a game tile type. I.e. not a single tile but rather
#  a type of tile, such as grass, road etc.

class TileType:
  last_identifier = 0

  ## Private method, initialises the default attribute values

  def __init_attributes(self):
    ## tile with higher priority will overlap the tile with lower
    #  priority at their borders
    self.priority = 0
    ## tile name
    self.name = ""
    ## whether the tile is animated
    self.animated = False
    ## number of tile variants in range <1,4>
    self.variants = 1
    ## whether the tile is steppable
    self.steppable = True
    ## whether the tile can be flied over
    self.flyable = True
    ## whether the tile can be swimmed on
    self.swimmable = False
    ## unique tile identifier
    self.identifier = TileType.last_identifier
    TileType.last_identifier += 1

  def __init__(self):
    self.__init_attributes()

  ## Initialises a new object with given attribute values.
  #
  #  @param priority integer tile priority, this affects how the tiles
  #         overlap
  #  @param name name of the the tile, it is not a filename, so only  a
  #         name must be given without a path to it or a file extension,
  #         for example: "grass"
  #  @param variants number of tile variants (if not animated) or
  #         animation frames (if animated), must be integer in range
  #         <1,4>
  #  @param steppable whether the tile can be stepped on (bool)
  #  @param flyable whether the tile can be flied over (bool)
  #  @param swimmable whether the tile can be swimmed on (bool)

  def __init__(self, priority = 0, name = "", steppable = True, variants = 1, animated = False, flyable = True, swimmable = False):
    self.__init_attributes()
    self.priority = priority
    self.steppable = steppable
    self.variant = variants
    self.animated = animated
    self.flyable = flyable
    self.name = name
    self.swimmable = swimmable

  def __str__(self):
    return "Tile: '" + self.name + "' (" + str(self.identifier) + "), prior.: " + str(self.priority) + ", step.: " + str(self.steppable) + ", fly.: " + str(self.flyable) + ", swim.: " + str(self.swimmable)

#=======================================================================

## Represents a part of world. It is basically a 2D array of triplets
#  [TileType reference,variant (int),object list] where object list is
#  reference to a list of objects at given tile or None.

class WorldArea:
  def __init__(self, width, height):

    ## the terrain array, it's format is [x][y][tiletype,variant,object_list]:
    self.terrain_array = numpy.zeros((width,height),dtype=object)

    for j in range(len(self.terrain_array[0])):
      for i in range(len(self.terrain_array)):
        self.terrain_array[i,j] = numpy.array([None,0,None])

    #self.terrain_array = [[[None,0,None] for i in range(height)] for j in range(width)]

  ## the area width in tiles

  @property
  def width(self):
    return len(self.terrain_array)

  ## the area height in tiles

  @property
  def height(self):
    return len(self.terrain_array[0])

  ## Sets the tile at given position. If the position is outside the
  #  terrain, nothing happens.

  def set_tile(self, x, y, tile_type, variant, object_list):
    try:
      self.terrain_array[x][y][0] = tile_type
      self.terrain_array[x][y][1] = variant
      self.terrain_array[x][y][2] = object_list
    except IndexError:
      return

  ## Gets the tile type at given position.
  #
  #  @return tile type object at [x,y], if the position is outside
  #          terrain array, closest tile type is returned

  def get_tile_type(self, x, y):
    return self.terrain_array[general.saturate(x,0,self.get_width() - 1)][general.saturate(y,0,self.get_height() - 1)][0]

  ## Same as get_tile_type, just returns the tile variant.

  def get_tile_variant(self, x, y):
    return self.terrain_array[general.saturate(x,0,self.get_width() - 1)][general.saturate(y,0,self.get_height() - 1)][1]

  ## Same as get_tile_type, just returns the object list.

  def get_object_list(self, x, y):
    return self.terrain_array[general.saturate(x,0,self.get_width() - 1)][general.saturate(y,0,self.get_height() - 1)][2]

  ## Debug purpose method.

  def print_out(self):
    print("--------")

    for j in range(ter_ar.get_height()):
      for i in range(ter_ar.get_width()):
        tile = self.get_tile_type(i,j)
        variation = self.get_tile_variant(i,j)

        if tile == None:
          sys.stdout.write("N " + str(variation) + "    ")
        else:
          sys.stdout.write(tile.name + " " + str(variation) + "    ")
      print("")

#=======================================================================

## Represents a concrete tile in game world, consists of tile type
#  plus objects at the tile.

class TileInfo:

  def __init__(self, tile_type, game_object_list):
    ## type of the tile
    self.tile_type = tile_type
    ## objects at the tile
    self.objects = game_object_list

#=======================================================================

## Represents the game world and a proxy for game world file.
#
#  The world consists of 2D array of game tiles plus NPCs, objects, items
#  etc. There is always an active area of the world, which is the
#  player's close area, the class provides methods for setting the
#  and handling the active area as well as the rest of the world.

class World:

  ## Private method, loads all the items from the world file except for
  #  terrain, this is done with __load_active_terrain().

  def __load_non_terrain(self):
    world_file = open(self.filename,'r')

    for line in world_file:

      if line[:6] == "tiles:":       # load tiles
        while True:
          line2 = world_file.readline()

          if line2[:3] == "end":
            break

          split_line = line2.split()

          print(split_line)

          self.tile_types.append(TileType(int(split_line[2]),split_line[1],split_line[5] == "T",int(split_line[3]),split_line[4] == "T",split_line[6] == "T",split_line[7] == "T"))

    world_file.close()
    return

  ## Private method, loads the active terrain area from the world file.

  def __load_active_terrain(self):
    return

  ## Private method, initialises the default attribute values

  def __init_attributes(self):
    ## contains the name of the world file for which the object is a proxy
    self.filename = ""
    ## active world (player's close) area in format (x,y,width,height) in tiles
    self.active_area = (0, 0, 0, 0)
    ## WorldArea object reference
    self.world_area = None
    ## all world tile types loaded from the world file
    self.tile_types = []
    ## world width in tiles
    self.world_width = 0
    ## world height in tiles
    self.world_height = 0

  ## Initialises a new world proxy for given world file.
  #
  #  @param filename name of the world file for which the object will
  #         be proxy

  def __init__(self, filename):
    self.__init_attributes()
    self.filename = filename
    self.__load_non_terrain()
    self.__load_active_terrain()

  @property
  def width(self):
    return self.world_width

  @property
  def height(self):
    return self.world_height

  ## Sets the active area of the world (the player's close area which
  #  can then be handled in a detailed way).
  #
  #  @param x integer x coordinate of the active area in world
  #         coordinates
  #  @param y integer y coordinate of the active area in world
  #         coordinates
  #  @param width width of the active area in tiles
  #  @param height height of the active area in tiles

  def set_active_area(self, x, y, width, height):
    self.active_area = (x, y, width, height)
    self.__load_active_terrain()

t1 = TileType()
print(t1)

w = World(general.RESOURCE_PATH + "/world")

