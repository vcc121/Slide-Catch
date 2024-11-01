import pygame, simpleGE, random

class Frog(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("froggy.png")
        self.setSize(50,50)
        self.position = (320, 400)
        self.moveSpeed = 5
        
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
            
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("pond background.jpg")
        self.frog = Frog(self)
        self.fly = Fly(self)
        self.blip = simpleGE.Sound("blip sound.wav")
        self.sprites = [self.frog,
                        self.fly]
        
    def process(self):
        if self.frog.collidesWith(self.fly):
            self.blip.play()
            self.fly.reset()

def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()