import pygame
import random

screen = pygame.display.set_mode((1000,700))
class Bot(pygame.sprite.Sprite):
	bots = pygame.sprite.Group()
	def __init__(self,images,x,y,width,height,state,substate):
		#images is list of states namely idle,run,dead,shoot,jump_and_shoot
		pygame.sprite.Sprite.__init__(self)
		self.direction = 0
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
		self.rect.x += self.velx
		self.rect.y += self.vely 

	def tick(self,x,y,width,height):
		Bot.bots.remove(self)
		self.vely += 1
		self.substate  = (self.substate + 1)%len(self.images[self.state])
		self.image= pygame.image.load(self.images[self.state][self.substate])
		self.image = pygame.transform.scale(self.image, (width, height))
		if (self.direction == 1):
			self.image = pygame.transform.flip(self.image,True, False)
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		# self.rect.width=width
		# self.rect.height=height
		Bot.bots.add(self)