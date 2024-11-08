import pygame, simpleGE, random


class Frog(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("froggy.png")
        self.setSize(50,50)
        self.position = (320, 400)
        self.moveSpeed = 6
        
    def process(self):
        if self.isKeyPressed(pygame.K_a):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_d):
            self.x += self.moveSpeed

class Fly(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("fly.png")
        self.setSize(50,50)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.x = random.randint(0, self.screenWidth)
        self.y = 0
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Intro(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        
        self.setImage("pond background.jpg")
        self.status = "quit"
        self.score = score
        
        self.lblInstructions = simpleGE.MultiLabel()
        self.lblInstructions.textLines = [
            "You are a frog, and you're hungry.",
            "Lucky for you, it is raining flies!",
            "Using the A and D keys,",
            "move left and right to catch them!"]
        self.lblInstructions.center = (320, 240)
        self.lblInstructions.size = (350, 200)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320, 100)
        self.lblScore.size = (350, 30)
        self.lblScore.text = f"Previous Score: {self.score}"
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (150, 400)
        self.btnPlay.text = "Play"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (500, 400)
        self.btnQuit.text = "Quit"
        
        self.sprites = [
            self.lblScore,
            self.lblInstructions,
            self.btnPlay,
            self.btnQuit
            ]

    def process(self):
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.status = "quit"
            self.stop()
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100,30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500,30)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("pond background.jpg")
        self.frog = Frog(self)
        self.numFlies = 10
        self.blip = simpleGE.Sound("blip sound.wav")
        self.score = 0
        self.lblScore = LblScore()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.lblTime = LblTime()
        self.flies = []
        for i in range(self.numFlies):
            self.flies.append(Fly(self))
        self.sprites = [self.frog,
                        self.flies,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for fly in self.flies:
            if fly.collidesWith(self.frog):
                fly.reset()
                self.blip.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
            
        self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            self.stop()

def main():
    
    keepGoing = True
    score = 0
    
    while keepGoing:
        intro = Intro(score)
        intro.start()
        if intro.status == "quit":
            keepGoing = False
        else:
            game = Game()
            game.start()
            score = game.score

if __name__ == "__main__":
    main()
    