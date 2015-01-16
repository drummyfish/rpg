  ## \file general.py
  #  this file contains general constants and general helper classes and
  #  functions

from enum import Enum
import pygame

TILE_WIDTH = 34
TILE_HEIGHT = 28

RESOURCE_PATH = "../resources"

RACE_HUMAN = 0

GENDER_MALE = 20
GENDER_FEMALE = 21

ANIMATION_IDLE_UP    = 100
ANIMATION_IDLE_RIGHT = 101
ANIMATION_IDLE_DOWN  = 102
ANIMATION_IDLE_LEFT  = 103

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

  def __init__(self,filename):
    self.init()
    self.load_from_file(filename)

  def load_from_file(self,filename):
    image = pygame.image.load(filename)

    self.main_tile[0] = image.subsurface(68,0,34,28)
    self.main_tile[1] = image.subsurface(102,0,34,28)
    self.main_tile[2] = image.subsurface(68,28,34,28)
    self.main_tile[3] = image.subsurface(102,28,34,28)

    self.corner_UL_00 = image.subsurface(51,42,17,14)
    self.corner_UL_01 = image.subsurface(17,42,17,14)
    self.corner_UL_10 = image.subsurface(51,14,17,14)
    self.corner_UL_11 = image.subsurface(17,14,17,14)
    self.corner_UR_00 = image.subsurface(0,42,17,14)
    self.corner_UR_01 = image.subsurface(34,42,17,14)
    self.corner_UR_10 = image.subsurface(0,14,17,14)
    self.corner_UR_11 = image.subsurface(34,14,17,14)
    self.corner_DL_00 = image.subsurface(51,0,17,14)
    self.corner_DL_01 = image.subsurface(17,0,17,14)
    self.corner_DL_10 = image.subsurface(51,28,17,14)
    self.corner_DL_11 = image.subsurface(17,28,17,14)
    self.corner_DR_00 = image.subsurface(0,42,17,14)
    self.corner_DR_01 = image.subsurface(34,0,17,14)
    self.corner_DR_10 = image.subsurface(0,28,17,14)
    self.corner_DR_11 = image.subsurface(34,28,17,14)
