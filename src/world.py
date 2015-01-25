  ## \file graphics.py
  #
  #  This file contains classes asociated with game world.

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
    self.filename = ""
    self.identifier = TileType.last_identifier
    TileType.last_identifier += 1

  def __init__(self):
    self.init()

  ## Initialises a new object with given attribute values.
  #
  #  @param priority integer tile priority, this affects how the tiles
  #         overlap
  #  @param filename name of the image for the tile, only the image
  #         name must be given without a path to it, for example:
  #         "grass.png"

  def __init__(self, priority, filename):
    self.init()
    self.priority = priority
    self.filename = filename

  def get_priority(self):
    return self.priority

  def get_filename(self):
    return self.filename

  ## Gets the tile unique integer identifier.
  #
  #  @return unique integer identifier

  def get_identifier(self):
    return self.identifier

#=======================================================================

  ## Represents a part of terrain made of tiles. It is basically a 2D
  #  array of pairs [TileType reference,variant (int)]

class TerrainArray:
  def __init__(self, width, height):
    #initialize the terrain array, it's format is [x][y][tiletype(int),]:

    self.terrain_array = [[[None,0] for i in range(height)] for j in range(width)]

  def get_width(self):
    return len(self.terrain_array)

  def get_height(self):
    return len(self.terrain_array[0])

  ## Sets the tile at given position. If the position is outside the
  #  terrain, nothing happens.

  def set_tile(self, x, y, tile_type, variant):
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
          sys.stdout.write(tile.filename + " " + str(variation) + "    ")
      print("")

#=======================================================================

  ## Represents a concrete tile in game world, consists of tile type
  #  plus objects at the tile.

class TileInfo:

  def __init__(self, tile_type, game_object_list):
    self.tile_type = tile_type
    self.objects = game_object_list

#=======================================================================

  ## Represents the game world as a 2D array of game tiles plus objects
  #  in the world.

class World:

  ## Initialises a new empty world of given size.

  def __init__(self, width, height):
    self.world_array = numpy.empty((width,height),dtype = object)   # using numpy for the large world array, because the standard
                                                                    # Python lists might be too large and not efficient
    for j in range(len(self.world_array[0])):
      for i in range(len(self.world_array)):
        self.world_array[i,j] = TileInfo(None,None)

  def set_tile_type(self, x, y, tile_type):
    try:
      self.world_array[x,y].tile_type = tile_type
    except Exception:
      return

  ## Gets the tile type at given position
  #
  #  @param x x coordinate
  #  @param y y coordinate
  #  @return TileType object representing the tile type, or none if
  #          there was no file at given position or the coordinates
  #          were out of the world

  def get_tile_type(self, x, y):
    try:
      return self.world_array[x,y].tile_type
    except Exception:
      return None

  ## debug purposes method

  def print_out(self):
    print("--------")

    for j in range(len(self.world_array[0])):
      for i in range(len(self.world_array)):
        if self.world_array[i,j].tile_type == None:
          sys.stdout.write("N ")
        else:
          sys.stdout.write(str(self.world_array[i,j].tile_type.get_identifier()) + " ")
      print("")

t1 = TileType(1,"tile_grass.png")

w = World(25,30)
w.set_tile_type(2,1,t1)
w.print_out()
