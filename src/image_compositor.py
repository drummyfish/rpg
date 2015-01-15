import os
import pygame
import general
import time

#-----------------------------------------------------------------------

  ## Assembles images out of image resources

class ImageCompositor:

  ## Makes a character image with given body, head, animation type, frame
  #  and gear
  #
  #  @param self object pointer
  #  @param body_name resource name of the body
  #

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

#-----------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((900,600))

done = False

myyy = ImageCompositor()

imgs = []

imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_RIGHT,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_DOWN,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_LEFT,1))
imgs.append(myyy.make_character_image(general.RACE_HUMAN,general.GENDER_MALE,2,general.ANIMATION_IDLE_UP,1))

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


  pygame.display.flip()
