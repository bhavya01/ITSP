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
		self.healthbar = HealthBar(20,20,100,30,"png/healthbar.png") 
		self.healthbar1 = HealthBar(1080,20,100,30,"png/healthbar.png")
	# Create all the levels
		self.level_list = []
		self.level_list.append( Level_01(self.bot) )
 
    # Set the current level
		self.current_level_no = 0
		self.current_level = self.level_list[self.current_level_no]
		self.bot.level = self.current_level
		self.bot1.level = self.current_level
		self.bot_frame = 0
	#Initiating the music	
		self.initSound()
	#Address of the server
		address=raw_input("Address of Server: ")
		try:
			if not address:
				host, port="localhost", 8000
			else:
				host,port=address.split(":")
			self.Connect((host, int(port)))
		except:
			print "Error Connecting to Server"
			print "Usage:", "host:port"
			print "e.g.", "localhost:31425"
			exit()
		print "Boxes client started"
		self.gameid  = None
		self.num = 0

	#Setting up the sound
	def initSound(self):
		pygame.mixer.music.load("sound/background.wav")
		self.bulletSound = pygame.mixer.Sound("sound/bullet.wav")

	#Function called when startgame signal is recieved
	def Network_startgame(self, data):
		try :
			pygame.mixer.music.play(-1)
		except:
			print "Could not load music"
		self.running=True
		self.num=data["player"]
		self.gameid=data["gameid"]
		if self.num == 0:
			self.bot.rect.x = INIT_X
		else:
			self.bot.rect.x = MAX_X - WIDTH
			self.bot.direction  = 1
	#Function called when botpos signal is recieved		
	def Network_botpos(self,data):
		x = data["x"]
		y = data["y"]
		state = data["state"]
		substate = data["substate"]
		direction = data["direction"]
		self.bot1.rect.x = x 
		self.bot1.rect.y = y 
		self.bot1.direction = direction
		if not (self.bot1.state == 5 and self.bot1.substate == 10) :
			self.bot1.state = state
			self.bot1.substate = substate
	#Function called when bullet signal is recieved
	def Network_bullet(self,data):		
		if self.bot1.bullets_available > 0:
			pygame.mixer.music.pause()
			self.bulletSound.play()
			pygame.mixer.music.unpause()
			self.bot1.bullets_available -= 1
			bullet = Bullet(INIT_X,INIT_Y,20,20,"png/FireBall.png")
			bullet.level = self.current_level
			self.bot1.bullet_list.append(bullet)
			if self.bot1.direction == 0:
				bullet.velx = 3*VEL_X
				bullet.tick(self.bot1.rect.x + self.bot1.rect.width/2,self.bot1.rect.y+self.bot1.rect.height/3,bullet.rect.width,bullet.rect.height)
			else:
				bullet.velx = -3*VEL_X
				bullet.tick(self.bot1.rect.x+self.bot1.rect.width/4,self.bot1.rect.y+self.bot1.rect.height/3,bullet.rect.width,bullet.rect.height)
			Bullet.bullets.add(self.bot1.bullet_list[len(self.bot1.bullet_list)-1])	
	#GameOver Screens
	def finished(self):
		if(self.bot.health == 0 and self.bot1.health > 0):
			game_over_screen = pygame.transform.scale(game_over,(500,500))
			screen.blit(game_over_screen,(350,100))
		elif(self.bot.health > 0 and self.bot1.health == 0):
			winning_screen = pygame.transform.scale(winner,(500,500))
			screen.blit(winning_screen,(350,100))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()
	#Game Loop
	def update(self):
		#Till the player finds a partner screen will be black
		if  self.bot.state == 5 and self.bot.substate == 9:
			return 0
		elif  self.bot1.state == 5 and self.bot1.substate == 9:
			return 1
		while not self.running:
			self.Pump()
			connection.Pump()
			sleep(0.01)
		connection.Pump()
		self.Pump()
		#Event management
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
				if event.key == pygame.K_UP:
					self.bot.jump()
					self.bot.state = 1
					self.bot.jump_state_flag = True
				if event.key == pygame.K_SPACE :
					if self.bot.bullets_available > 0 and self.bot.health > 0:
						pygame.mixer.music.pause()
						self.bulletSound.play()
						pygame.mixer.music.unpause()
						self.bot.bullets_available -= 1
						bullet = Bullet(INIT_X,INIT_Y,20,20,"png/FireBall.png")
						bullet.level = self.current_level
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
						self.Send({"action": "bullet","gameid": self.gameid, "num": self.num})	

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT  and self.bot.velx <0:
					self.bot.velx = 0
					self.bot.state = 0
				if event.key == pygame.K_RIGHT and self.bot.velx>0:
					self.bot.velx = 0
					self.bot.state =0 
				if event.key == pygame.K_SPACE:
					if self.bot.velx == 0:
						self.bot.state = 0
					else :
						self.bot.state = 2
				
		# Updating the bullets of bot
		for item in list(self.bot.bullet_list):
			item.update()
			if item.collision(self.bot1):
				Bullet.bullets.remove(item)
				self.bot.bullet_list.remove(item)
			
		for item in list(self.bot1.bullet_list):
			item.update()
			if item.collision(self.bot):
				Bullet.bullets.remove(item)
				self.bot1.bullet_list.remove(item)
		
		#Updating the bot
		self.bot1.update()
		self.bot.update()
		if(self.num == 0):
			self.healthbar.tick(self.bot)
			self.healthbar1.tick(self.bot1)	
		else:
			self.healthbar.tick(self.bot1)
			self.healthbar1.tick(self.bot)
		self.bot_frame += 1
		if(self.bot_frame == FPS/10):
			self.bot_frame = 0
			self.bot.tick(self.bot.rect.x,self.bot.rect.y,self.bot.rect.width,self.bot.rect.height)
			self.bot1.tick(self.bot1.rect.x,self.bot1.rect.y,self.bot1.rect.width,self.bot1.rect.height)

		#Sending the data of player to the server
		self.Send({"action": "botpos", "x":self.bot.rect.x, "y":self.bot.rect.y, "gameid": self.gameid, "num": self.num,"state": self.bot.state,"substate": self.bot.substate, "direction" : self.bot.direction})	
		#Updating the screen
		self.current_level.draw(screen)
		screen.blit(ground,(0,680))
		screen.blit(ground,(400,680))
		screen.blit(ground,(800,680))
		screen.blit(tile,(0,415))
		screen.blit(tile2,(220,415))		
		screen.blit(tile,(980,390))
		screen.blit(tile1,(780,390))
		screen.blit(box,(520,570))
		screen.blit(box,(0,315))
		screen.blit(tile,(300,170))
		screen.blit(tile,(840,200))
		Bot.bots.draw(screen)
		Bullet.bullets.draw(screen)
		HealthBar.healthbars.draw(screen)
		pygame.display.flip()
		self.clock.tick(FPS)

game = BotGame()
while True:
	if game.update() == 1 or game.update()==0:
		break
game.finished()