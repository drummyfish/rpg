  ## \file graphics.py
  #
  #  This file contains classes asociated with game world.

import os
import pygame
import general
import time

#-----------------------------------------------------------------------

  ## Represents a game file type. I.e. not a single tile but rather
  #  a type of tile, such as grass, road etc.

class TileType:
  priority = 0         #< tile priority, this affects how the tiles' borders overlap
  image_filename = ""  #< name of the resource image file in which the tile is saved
  is_animated = False
