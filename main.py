import pygame
import sys, time, random
pygame.init()

DARKGREY = (52, 50, 55)
WHITE = (255, 255, 255)

class Main:

    def __init__(self, screen):
        self.running = True
        self.screen = pygame.display.set_mode(screen)
        self.unit = self.screen.get_height()//1080

        self.font_title = pygame.font.Font("assets/fonts/LexendDeca-SemiBold.ttf", 50)
        self.title = self.font_title.render("DactyloFun", True, WHITE)

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def display(self):
        
        self.screen.fill(DARKGREY)

        self.screen.blit(self.title, (self.unit*200, self.unit*200))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()


game = Main((1000, 600))
game.run()
pygame.quit()