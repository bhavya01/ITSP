import pygame
import random

WIDTH = 120
HEIGHT = 140
SIZE = (1200,700)
INIT_X = 0
INIT_Y = SIZE[1] - HEIGHT
VEL_X = 6
VEL_Y = 6
FPS = 80
MAX_X = 1200
MIN_X = 0
screen = pygame.display.set_mode(SIZE,0,32)
pygame.display.set_caption('SharpShooter')
COLOR = (255,255,255)


class Bot(pygame.sprite.Sprite):
	bots = pygame.sprite.Group()
	def __init__(self,images,x,y,width,height,state,substate):
		#images is list of states namely idle,run,dead,shoot,jump_and_shoot
		pygame.sprite.Sprite.__init__(self)
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

	def jump_check(self):
		if(self.rect.y > INIT_Y):
			self.vely = 0
			self.rect.y = INIT_Y 
			if self.jump_state_flag == True:
				if self.velx != 0:
					self.state = 2
				else :
					self.state = 0
				self.jump_state_flag = False
		return	
	def collision(self):
		if self.rect.x + self.rect.width > MAX_X +20:
			self.rect.x = MAX_X- self.rect.width
			return  True
		elif self.rect.x < MIN_X -20:
			self.rect.x = MIN_X
			return True

	def update(self):
		if self.health==0:
			self.state = 5
		if not self.collision():
			self.rect.x += self.velx
			self.rect.y += self.vely 

	def tick(self,x,y,width,height):
		Bot.bots.remove(self)
		self.vely += 1
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
			self.rect.y = -100

class Bullet(pygame.sprite.Sprite):
	bullets = pygame.sprite.Group()

	def __init__(self,x,y,width,height,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height
		self.velx = 0
		self.vely = 0

	def collision(self,bot):
		if self.rect.x > MAX_X or self.rect.x < MIN_X:
			return True
		elif pygame.sprite.collide_rect(self,bot):
			if bot.health > 0:
				bot.health -= 10
			return True
		else:
			return False	
	def update(self):
		self.rect.x += self.velx
		self.rect.y += self.vely
 
	def tick(self,x,y,width,height):
		self.rect.x = x
		self.rect.y = y
		self.image = pygame.transform.scale(self.image, (width, height))