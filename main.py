# -*- coding: utf-8 -*-
import pygame
import csv
import random
pygame.init()

DARKGREY = (52, 50, 55)
WHITE = (255, 255, 255)

def lire_donnees_csv(chemin):
    fichier = open(chemin, encoding="utf-8")
    table = list(csv.DictReader(fichier))
    fichier.close()
    return table

class Main:

    def __init__(self, screen):
        self.running = True
        self.screen = pygame.display.set_mode(screen)
        self.unit = self.screen.get_height()/1080

        self.table = lire_donnees_csv("dictout.csv")
        print(self.table)
        self.mots = []
        for i in range(20):
            self.mots.append(self.table[random.randint(0, len(self.table)-1)])

        print(" ".join([mot["mot"] for mot in self.mots]))

        self.font_title = pygame.font.Font("assets/fonts/LexendDeca-SemiBold.ttf", 50)
        self.font_text = pygame.font.Font("assets/fonts/RobotoMono-VariableFont_wght.ttf", 20)
        self.title = self.font_title.render("DactyloFun", True, WHITE)
        self.text = self.font_text.render(" ".join([mot["mot"] for mot in self.mots]), True, WHITE)

        

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def display(self):
        
        self.screen.fill(DARKGREY)

        self.screen.blit(self.title, (self.unit*50, self.unit*20))
        self.screen.blit(self.text, (self.screen.get_width()//2 - self.text.get_width()//2, self.screen.get_height()//2 - self.text.get_height()//2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()

game = Main((1000, 600))
game.run()
pygame.quit()