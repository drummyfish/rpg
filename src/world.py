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

    if (len(self.terrain_array) != 0):
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
    if self.width == 0:
      return 0
    else:
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
    return self.terrain_array[general.saturate(x,0,self.width - 1)][general.saturate(y,0,self.height - 1)][0]

  ## Same as get_tile_type, just returns the tile variant.

  def get_tile_variant(self, x, y):
    return self.terrain_array[general.saturate(x,0,self.width - 1)][general.saturate(y,0,self.height - 1)][1]

  ## Same as get_tile_type, just returns the object list.

  def get_object_list(self, x, y):
    return self.terrain_array[general.saturate(x,0,self.width - 1)][general.saturate(y,0,self.height - 1)][2]

  def __str__(self):
    result = ""

    for j in range(self.height):
      for i in range(self.width):
        tile_type = self.get_tile_type(i,j)
        tile_variant = self.get_tile_variant(i,j)

        if tile_type == None:
          result += "N (" + str(tile_variant) + ") "
        else:
          result += str(tile_type.identifier) + " (" + str(tile_variant) + ") "

      result += "\n"

    return result

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

          self.tile_types[int(split_line[0])] = TileType(int(split_line[2]),split_line[1],split_line[5] == "T",int(split_line[3]),split_line[4] == "T",split_line[6] == "T",split_line[7] == "T")

      if line[:8] == "terrain:":       # load world size
        self.world_width = int(world_file.readline())
        self.world_height = int(world_file.readline())

        while True:
          line2 = world_file.readline()

          if line2[:3] == "end":
            break

        # TODO LOAD TERRAAAAAAAAAIN

    world_file.close()

  ## Private method, loads the active terrain area from the world file.

  def __load_active_terrain(self):
    world_file = open(self.filename,'r')
    end_it = False

    self.world_area = WorldArea(self._active_area[2],self._active_area[3])

    helper_width = self._active_area[2]
    helper_height = self._active_area[3]

    for line in world_file:

      if line[:8] == "terrain:":     # load tiles
        world_file.readline()        # skip the width and height lines
        world_file.readline()

        counter = 0

        while counter < self._active_area[1]:
          world_file.readline()
          counter += 1

        y = 0

        while counter < self._active_area[1] + helper_height:
          line2 = world_file.readline()

          if line2[:3] == "end":
            end_it = True
            break

          terrain_line = line2.split()

          for x in range(0,helper_width):
            try:
              self.world_area.set_tile(x,y,self.tile_types[int(terrain_line[(self._active_area[0] + x) * 2])],int(terrain_line[(self._active_area[0] + x) * 2 + 1]),None)
            except Exception:
              pass

          counter += 1
          y += 1

        # TODO LOAD TERRAAAAAAAAAIN

      if end_it:
        break

    world_file.close()

  ## Private method, initialises the default attribute values

  def __init_attributes(self):
    ## contains the name of the world file for which the object is a proxy
    self.filename = ""
    ## active world (player's close) area in format (x,y,width,height) in tiles
    self._active_area = (0, 0, 0, 0)
    ## WorldArea object reference
    self.world_area = None
    ## all world tile types loaded from the world file
    self.tile_types = {}
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

  ## The active area of the world (the player's close area which
  #  can then be handled in a detailed way). It is a tuple in fomrmat:
  #  (x,y,width,height) where the rectangle must be inside the world
  #  map.

  @property
  def active_area(self):
    return self._active_area

  @active_area.setter
  def active_area(self,value):
    self._active_area = value
    self.__load_active_terrain()

  def __str__(self):
    result = ""
    result += "world width: "
    result += str(self.world_width)
    result += "\nworld height: "
    result += str(self.world_height)
    result += "\ntiles:\n"

    for tile in self.tile_types:
      result += str(tile) + "\n"

    result += "\nactive area:\n"
    result += str(self.world_area)

    return result
