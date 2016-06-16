import sys
from time import sleep
from classes import *
from images import *
pygame.init()
clock = pygame.time.Clock()

#Initializing Things
WIDTH = 120
HEIGHT = 140
SIZE = (1200,700)
INIT_X = 0
INIT_Y = SIZE[1] - HEIGHT
VEL_X = 6
VEL_Y = 6
FPS = 80
bot_frame = 0
bot = Bot(images,INIT_X,INIT_Y,WIDTH,HEIGHT,0,0)
bot1 = Bot(images,INIT_X+500,INIT_Y,WIDTH,HEIGHT,0,0)
screen = pygame.display.set_mode(SIZE,0,32)
pygame.display.set_caption('SharpShooter')
COLOR = (255,255,255)

def jump_check(bot):
	if(bot.rect.y > INIT_Y):
		bot.vely = 0
		bot.rect.y = INIT_Y 
		if bot.jump_state_flag == True:
			if bot.velx != 0:
				bot.state = 2
			else :
				bot.state = 0
			bot.jump_state_flag = False
	return

#Game Loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type== pygame.KEYDOWN:
			if event.key== pygame.K_RIGHT:
				bot.velx = VEL_X
				bot.state=2
				bot.direction = 0
				bot.jump_state_flag = False
			if event.key == pygame.K_LEFT:
				bot.direction = 1
				bot.velx = -VEL_X
				bot.state=2
				bot.jump_state_flag = False
			if event.key == pygame.K_UP and bot.rect.y == INIT_Y:
				bot.vely = -VEL_Y
				bot.state = 1
				bot.jump_state_flag = True
			if event.key == pygame.K_SPACE :
				if bot.bullets_available > 0:
					bot.bullets_available -= 1
					bullet = Bullet(INIT_X,INIT_Y,30,30,"png/FireBall.png")
					bot.bullet_list.append(bullet)
					if bot.velx == 0:
						bot.state = 3
					else :
						bot.state = 4

					if bot.direction == 0:
						bullet.velx = 3*VEL_X
						bullet.tick(bot.rect.x + bot.rect.width/2,bot.rect.y+bot.rect.height/3,bullet.rect.width,bullet.rect.height)
					else:
						bullet.velx = -3*VEL_X
						bullet.tick(bot.rect.x+bot.rect.width/4,bot.rect.y+bot.rect.height/3,bullet.rect.width,bullet.rect.height)
					Bullet.bullets.add(bot.bullet_list[len(bot.bullet_list)-1])

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				bot.velx = 0
				bot.state = 0
			if event.key == pygame.K_SPACE:
				if bot.velx == 0:
					bot.state = 0
				else :
					bot.state = 2
				

	jump_check(bot)
	jump_check(bot1)
			
	
	# Updating the bullets of bot
	for item in list(bot.bullet_list):
		if item.collision(bot1):
			Bullet.bullets.remove(item)
			bot.bullet_list.remove(item)
		item.update()
		

	#Updating the bot
	bot1.update()
	bot.update()	
	bot_frame += 1
	if(bot_frame == FPS/10):
		bot_frame = 0
		bot.tick(bot.rect.x,bot.rect.y,bot.rect.width,bot.rect.height)
		bot1.tick(bot1.rect.x,bot1.rect.y,bot1.rect.width,bot1.rect.height)
	#Updating the screen
	screen.fill(COLOR)	
	Bot.bots.draw(screen)
	Bullet.bullets.draw(screen)
	pygame.display.flip()
	clock.tick(FPS)