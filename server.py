import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
	def Network(self, data):
		pass
	def Network_botpos(self,data):
		x = data["x"]
		y = data["y"]
		state = data["state"]
		substate = data["substate"]
		self.gameid = data["gameid"]
		num = data["num"]
		direction = data["direction"]
		# health = data["health"]
		self._server.placeBot(x, y, state, substate, direction, self.gameid, num ,data)
 
class myServer(PodSixNet.Server.Server):
	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.games = []
		self.queue = None
		self.currentIndex=0

	def placeBot(self, x, y, state, substate, direction, gameid, num, data):
		game = [a for a in self.games if a.gameid==gameid]
		if len(game)==1:
			game[0].placeBot(x, y, state, substate,direction, gameid, num, data)
	
	channelClass = ClientChannel

	def Connected(self, channel, addr):
		print 'new connection:', channel
		if self.queue==None:
			self.currentIndex+=1
			channel.gameid=self.currentIndex
			self.queue=Game(channel, self.currentIndex)
		else:
			channel.gameid=self.currentIndex
			self.queue.player1=channel
			self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
			self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
			self.games.append(self.queue)
			self.queue=None
 
class Game:
	def __init__(self, player0, currentIndex):
		#initialize the players including the one who started the game
		self.player0=player0
		self.player1=None
		#gameid of game
		self.gameid=currentIndex 

	def placeBot(self, x, y, state, substate, direction, gameid, num, data):
		if num == 0:
			self.player1.Send(data)
		else:
			self.player0.Send(data)
print "STARTING SERVER ON LOCALHOST"
boxesServe=myServer()
while True:
	boxesServe.Pump()


