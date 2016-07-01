import pygame
import random

WIDTH = 100
HEIGHT = 100
SIZE = (1200,700)
INIT_X = 0
INIT_Y = SIZE[1] - HEIGHT - 10
VEL_X = 6
VEL_Y = 12
FPS = 80
MAX_X = 1200
MIN_X = 0
screen = pygame.display.set_mode(SIZE,0,32)
pygame.display.set_caption('SharpShooter')
COLOR =(255,255,255)

ground= pygame.image.load("png/Tile.png")
ground = pygame.transform.scale(ground,(400,50))
tile= pygame.image.load("png/Tile.png")
tile = pygame.transform.scale(tile,(220,110))
tile1 = pygame.image.load("png/Tile1.png")
tile2 = pygame.image.load("png/Tile2.png")
tile1 = pygame.transform.scale(tile1,(220,110))
tile2 = pygame.transform.scale(tile2,(220,110))
box= pygame.image.load("png/Box.png")
game_over = pygame.image.load("png/game_over.jpg")
winner = pygame.image.load("png/winner.jpg")
box = pygame.transform.scale(box,(140,110))
class Bot(pygame.sprite.Sprite):
	bots = pygame.sprite.Group()
	def __init__(self,images,x,y,width,height,state,substate):
		#images is list of states namely idle,run,dead,shoot,jump_and_shoot
		pygame.sprite.Sprite.__init__(self)
		self.level = None
		self.jump_state_flag = False
		self.bullet_list = []
		self.bullets_available = 20
		self.direction = 0
		self.health = 100
		self.substate = substate
		self.state = state
		self.images = images
		self.image = pygame.image.load(self.images[self.state][self.substate])
		self.image = pygame.transform.scale(self.image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height
		self.velx = 0
		self.vely = 0
		Bot.bots.add(self)
	
	def update(self):
		self.calc_grav()
		self.rect.x += self.velx
		if self.rect.right > MAX_X + 10:
			self.rect.right = MAX_X+10
		if self.rect.left < MIN_X - 10:
			self.rect.left = MIN_X -10
		# See if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# If we are moving right,
			# set our right side to the left side of the item we hit
			if self.velx > 0:
				self.rect.right = block.rect.left
			elif self.velx < 0:
			    # Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right
 
		self.rect.y += self.vely 		
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
		#Collision check
			if self.vely > 0 :
				self.rect.bottom = block.rect.top	
			elif self.vely < 0:
				self.rect.top = block.rect.bottom
			self.vely = 0

			if self.jump_state_flag == True:
	 			if self.velx != 0:
	 				self.state = 2
	 			else :
	 				self.state = 0
	 			self.jump_state_flag = False
	
		if self.health==0:
			self.state = 5
	def calc_grav(self):

		if self.vely == 0:
			self.vely = 1
		else:
			self.vely+= .35
		# See if we are on the ground.
		if self.rect.y >= INIT_Y and self.vely >= 0:
			self.vely = 0
			self.rect.y = INIT_Y
			if self.jump_state_flag == True:
	 			if self.velx != 0:
	 				self.state = 2
	 			else :
	 				self.state = 0
	 			self.jump_state_flag = False

	def jump(self):
		# move down a bit and see if there is a platform below us.
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2
		# If it is ok to jump, set our speed upwards
		if len(platform_hit_list) > 0 or self.rect.bottom >= 680:
		    self.vely = -VEL_Y	    
 
	def tick(self,x,y,width,height):
		Bot.bots.remove(self)
		if not (self.substate == 9 and self.state == 5):		
			self.substate  = (self.substate + 1)%len(self.images[self.state])
		self.image= pygame.image.load(self.images[self.state][self.substate])
		self.image = pygame.transform.scale(self.image, (width, height))
		if (self.direction == 1):
			self.image = pygame.transform.flip(self.image,True, False)
		self.rect=self.image.get_rect()
		
		if not (self.substate == 9 and self.state == 5):
			self.rect.x=x
			self.rect.y=y
			Bot.bots.add(self)
		else :
			self.rect.height = 0

class Bullet(pygame.sprite.Sprite):
	bullets = pygame.sprite.Group()

	def __init__(self,x,y,width,height,image):
		pygame.sprite.Sprite.__init__(self)
		self.level = None
		self.image = pygame.image.load(image)
		self.image = pygame.transform.scale(self.image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height
		self.velx = 0
		self.vely = 0

	def collision(self,bot):
		hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		if self.rect.x > MAX_X or self.rect.x < MIN_X:
			return True
		elif pygame.sprite.collide_rect(self,bot):
			if bot.health > 0:
				bot.health -= 10
			return True
		elif len(hit_list)>0:
			return True

		else:
			return False	
	def update(self):
		self.rect.x += self.velx
		self.rect.y += self.vely
 
	def tick(self,x,y,width,height):
		self.rect.x = x
		self.rect.y = y
		
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
class Level(object):
	#This class contains the background objects
	def __init__(self, player):
		self.platform_list = pygame.sprite.Group()
		self.player = player
	def update(self):
		# Update everything in this level.
		self.platform_list.update()
 
	def draw(self, screen):
		# Draw the background
		screen.fill(COLOR)

		# Draw all the sprite lists that we have
		self.platform_list.draw(screen)
class Level_01(Level):
 
	def __init__(self, player):
		""" Create level 1. """
 
		# Call the parent constructor
		Level.__init__(self, player)
 
		# Array with width, height, x, and y of platform
		level = [[200, 50, 1000, 400],
				 [200, 50, 0, 425],
				 [200, 50, 200, 425],
				 [200, 50, 800, 400],
				 [80,100,550,580],
				 [80,100,30,325],
				 [200,50,310,180],
				 [200,50,850,210]
				 ]
 
		# Go through the array above and add platforms
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block) 

class HealthBar(pygame.sprite.Sprite):
	healthbars = pygame.sprite.Group()
	def __init__(self,x,y,width,height,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height
		HealthBar.healthbars.add(self)
	def tick(self,bot):
		if(bot.health > 0):
			self.rect.width = bot.health
		elif(bot.health == 0):
			image = "png/blank.jpg"
			self.image = pygame.image.load(image)
		
		self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))