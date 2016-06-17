import sys
from time import sleep
from classes import *
from images import *
from PodSixNet.Connection import ConnectionListener, connection

#Initializing Things
class BotGame(ConnectionListener):
	def __init__(self):
		pygame.init()
		self.running=False
		self.clock = pygame.time.Clock()
		self.bot = Bot(images,INIT_X,INIT_Y,WIDTH,HEIGHT,0,0)
		self.bot1 = Bot(images,INIT_X+500,INIT_Y,WIDTH,HEIGHT,0,0)
		self.bot_frame = 0
		self.Connect()
		self.gameid  = None
		self.num = 0
	def Network_startgame(self, data):
		self.running=True
		self.num=data["player"]
		self.gameid=data["gameid"]
		if self.num == 0:
			self.bot.rect.x = INIT_X
		else:
			self.bot.rect.x = MAX_X - WIDTH
			self.bot.direction  = 1

	def Network_botpos(self,data):
		x = data["x"]
		y = data["y"]
		state = data["state"]
		substate = data["substate"]
		direction = data["direction"]
		self.bot1.rect.x = x 
		self.bot1.rect.y = y 
		self.bot1.direction = direction
		self.bot.health = data["health_bot1"]
		if not (self.bot1.state == 5 and self.bot1.substate == 10) :
			self.bot1.state = state
			self.bot1.substate = substate
#Game Loop
	def update(self):
		while not self.running:
			self.Pump()
			connection.Pump()
			sleep(0.01)
		connection.Pump()
		self.Pump()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type== pygame.KEYDOWN:
				if event.key== pygame.K_RIGHT:
					self.bot.velx = VEL_X
					self.bot.state=2
					self.bot.direction = 0
					self.bot.jump_state_flag = False
				if event.key == pygame.K_LEFT:
					self.bot.direction = 1
					self.bot.velx = -VEL_X
					self.bot.state=2
					self.bot.jump_state_flag = False
				if event.key == pygame.K_UP and self.bot.rect.y == INIT_Y:###############Needs to be updated ##############
					self.bot.vely = -VEL_Y
					self.bot.state = 1
					self.bot.jump_state_flag = True
				if event.key == pygame.K_SPACE :
					if self.bot.bullets_available > 0:
						self.bot.bullets_available -= 1
						bullet = Bullet(INIT_X,INIT_Y,30,30,"png/FireBall.png")
						self.bot.bullet_list.append(bullet)
						if self.bot.velx == 0:
							self.bot.state = 3
						else :
							self.bot.state = 4

						if self.bot.direction == 0:
							bullet.velx = 3*VEL_X
							bullet.tick(self.bot.rect.x + self.bot.rect.width/2,self.bot.rect.y+self.bot.rect.height/3,bullet.rect.width,bullet.rect.height)
						else:
							bullet.velx = -3*VEL_X
							bullet.tick(self.bot.rect.x+self.bot.rect.width/4,self.bot.rect.y+self.bot.rect.height/3,bullet.rect.width,bullet.rect.height)
						Bullet.bullets.add(self.bot.bullet_list[len(self.bot.bullet_list)-1])
						self.Send({"action": "bullet", "x": self.bot.rect.x,"y":self.bot.rect.y,"vel" : bullet.velx,"gameid": self.gameid, "num": self.num})	
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					self.bot.velx = 0
					self.bot.state = 0
				if event.key == pygame.K_SPACE:
					if self.bot.velx == 0:
						self.bot.state = 0
					else :
						self.bot.state = 2
				
		self.bot.jump_check()
		self.bot1.jump_check()
				
		
		# Updating the bullets of bot
		for item in list(self.bot.bullet_list):
			if item.collision(self.bot1):
				Bullet.bullets.remove(item)
				self.bot.bullet_list.remove(item)
			item.update()
		for item in list(self.bot1.bullet_list):
			if item.collision(self.bot):
				Bullet.bullets.remove(item)
				self.bot1.bullet_list.remove(item)
			item.update()
		print self.bot1.health,self.bot.health	
		self.Send({"action": "botpos", "x":self.bot.rect.x, "y":self.bot.rect.y, "gameid": self.gameid, "num": self.num,"state": self.bot.state,"substate": self.bot.substate, "direction" : self.bot.direction, "health_bot1" : self.bot1.health})				
	#Updating the bot
		self.bot1.update()
		self.bot.update()	
		self.bot_frame += 1
		if(self.bot_frame == FPS/10):
			self.bot_frame = 0
			self.bot.tick(self.bot.rect.x,self.bot.rect.y,self.bot.rect.width,self.bot.rect.height)
			self.bot1.tick(self.bot1.rect.x,self.bot1.rect.y,self.bot1.rect.width,self.bot1.rect.height)
		#Updating the screen
		screen.fill(COLOR)	
		Bot.bots.draw(screen)
		Bullet.bullets.draw(screen)
		pygame.display.flip()
		self.clock.tick(FPS)

game = BotGame()
while True:
	game.update()