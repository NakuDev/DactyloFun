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
        self.screen_size = screen

        self.table = lire_donnees_csv("dictout.csv")
        #print(self.table)
        self.mots = []
        for i in range(64):
            self.mots.append(self.table[random.randint(0, len(self.table)-1)]["mot"])

        #print(" ".join([mot for mot in self.mots]))
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font("assets/fonts/LexendDeca-SemiBold.ttf", 50)
        self.font_text = pygame.font.Font("assets/fonts/RobotoMono-VariableFont_wght.ttf", 20)
        self.title = self.font_title.render("DactyloFun", True, WHITE)
        self.text = self.font_text.render(" ".join([mot for mot in self.mots]), True, WHITE)

        

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def blit_text(self, surface, words, pos, font, color=WHITE):
        print(font)
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for word in words:
            print(word)
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


    def display(self):
        
        self.screen.fill(DARKGREY)

        self.screen.blit(self.title, (self.unit*50, self.unit*20))
        self.blit_text(self.screen, self.mots, (20, 300), self.font_text)
        pygame.display.flip()

    def run(self):
        FPS = 30
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handling_events()
            self.update()
            self.display()

game = Main((1000, 600))
game.run()
pygame.quit()