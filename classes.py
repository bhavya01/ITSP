import pygame
import random

WIDTH = 120
HEIGHT = 140
SIZE = (1200,700)
INIT_X = 0
INIT_Y = SIZE[1] - HEIGHT - 10
VEL_X = 6
VEL_Y = 6
FPS = 80
MAX_X = 1200
MIN_X = 0
screen = pygame.display.set_mode(SIZE,0,32)
pygame.display.set_caption('SharpShooter')
COLOR = (255,255,255)
platform_list = [(400,550),(800,400),(50,425)]


class Bot(pygame.sprite.Sprite):
	bots = pygame.sprite.Group()
	def __init__(self,images,x,y,width,height,state,substate):
		#images is list of states namely idle,run,dead,shoot,jump_and_shoot
		pygame.sprite.Sprite.__init__(self)
		self.platform_flag = False
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
	def on_platform(self):
		if self.rect.y == INIT_Y:
			return True
		for item in platform_list:
			print self.rect.y
			if self.rect.x >= item[0] - 60 and self.rect.x <= item[0]+150 :
				if self.rect.y >=  item[1]-self.rect.height - 15  and  self.rect.y <= item[1]-self.rect.height + 15:
					self.platform_flag = True
					return True
			
		return False

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
	def platform_check(self):
		if self.platform_flag:
			if self.rect.x >= 290 and self.rect.x <= 500:
				temp = platform_list[0]
			elif self.rect.x >= 740 and self.rect.x <= 950:
				temp = platform_list[1] 
			else :
				temp = platform_list[2]
			if self.rect.y > temp[1] - 130 and self.rect.x >= temp[0] - 60 and self.rect.x <= temp[0] +150:
				self.vely = 0
				self.rect.y = temp[1] - 130
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
		if not self.collision():
			self.rect.x += self.velx
			self.rect.y += self.vely 
		if self.health==0:
			self.state = 5

	def tick(self,x,y,width,height):
		Bot.bots.remove(self)
		if self.rect.y < INIT_Y and not self.on_platform():
			self.vely += 1
			self.platform_flag = False
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

class Platform(pygame.sprite.Sprite):
	platforms = pygame.sprite.Group()
	def __init__(self,x,y,width,height,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height
		Platform.platforms.add(self)
	def tick(self):
		self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))