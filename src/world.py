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

  def init(self):
    self.priority = 0
    self.name = ""
    self.identifier = TileType.last_identifier
    TileType.last_identifier += 1

  def __init__(self):
    self.init()

  ## Initialises a new object with given attribute values.
  #
  #  @param priority integer tile priority, this affects how the tiles
  #         overlap
  #  @param name name of the image for the tile, only the image
  #         name must be given without a path to it, for example:
  #         "grass.png"

  def __init__(self, priority, name):
    self.init()
    self.priority = priority
    self.name = name

  def get_priority(self):
    return self.priority

  def get_name(self):
    return self.name

  ## Gets the tile unique integer identifier.
  #
  #  @return unique integer identifier

  def get_identifier(self):
    return self.identifier

#=======================================================================

## Represents a part of world. It is basically a 2D array of triplets
#  [TileType reference,variant (int),object list] where object list is
#  reference to a list of objects at given tile or None.

class WorldArea:
  def __init__(self, width, height):
    #initialize the terrain array, it's format is [x][y][tiletype(int),]:

    self.terrain_array = numpy.zeros((width,height),dtype=object)

    for j in range(len(self.terrain_array[0])):
      for i in range(len(self.terrain_array)):
        self.terrain_array[i,j] = numpy.array([None,0,None])

    #self.terrain_array = [[[None,0,None] for i in range(height)] for j in range(width)]

  def get_width(self):
    return len(self.terrain_array)

  def get_height(self):
    return len(self.terrain_array[0])

  ## Sets the tile at given position. If the position is outside the
  #  terrain, nothing happens.

  def set_tile(self, x, y, tile_type, variant, object_list):
    try:
      self.terrain_array[x][y][0] = tile_type
      self.terrain_array[x][y][1] = variant
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
    self.tile_type = tile_type
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
    return

  ## Private method, loads the active terrain area from the world file.

  def __load_active_terrain(self):


    return

  ## Private method, initialises the default attribute values

  def __init_attributes(self):
    self.active_area = (0, 0, 0, 0)
    self.world_area = None
    self.width = 0
    self.height = 0

  ## Initialises a new world proxy for given world file.
  #
  #  @param filename name of the world file for which the object will
  #         be proxy

  def __init__(self, filename):
    self.__init_attributes()
    self.__load_non_terrain()
    self.__load_active_terrain()

  ## Gets the world outdoor width.
  #
  #  @return width in tiles

  def get_width(self):
    return self.width

  ## Gets the world outdoor height.
  #
  #  @return height in tiles

  def get_height(self):
    return self.height

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

  ## Gets the tile type at given position of the active area.
  #
  #  @param x x coordinate inside the active_area
  #  @param y y coordinate inside the active_area
  #  @return TileType object representing the tile type, or none if
  #          there was no file at given position or the coordinates
  #          were out of the world

  def get_tile_type(self, x, y):
    return

  ## Makes a terrain array out of the world active area.
  #
  #  @return terrain array representing the active area

  def get_terrain_array(self):
    return

  ## debug purposes method

  def print_active_area(self):
    return
