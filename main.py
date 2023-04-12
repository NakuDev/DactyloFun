# -*- coding: utf-8 -*-
import pygame
import csv
import random
import math

pygame.init()

DARKGREY = (52, 50, 55)
WHITE = (255, 255, 255)


def lire_donnees_csv(chemin):
    fichier = open(chemin, encoding="utf-8")
    table = list(csv.DictReader(fichier))
    fichier.close()
    return table

def ecrire_donnees_csv(table, sortie):
    f = open(sortie, "w")
    w = csv.DictWriter(f, table[0].keys())  # Création d'un "stylo"
    w.writeheader()  # Le stylo écrit dans le fichier les descripteurs
    w.writerows(table)  # Le stylo écrit les données de table
    f.close()

class Main:

    def __init__(self, screen):
        self.running = True
        self.screen = pygame.display.set_mode(screen)
        self.unit = self.screen.get_height() / 1080
        self.screen_size = screen

        self.table = lire_donnees_csv("dictout.csv")
        # print(self.table)
        self.mots = []
        self.nb_mots = 16
        for i in range(self.nb_mots):
            self.mots.append(self.table[random.randint(0, len(self.table) - 1)]["mot"])
        self.text = " ".join([mot for mot in self.mots])

        # print(" ".join([mot for mot in self.mots]))
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font("assets/fonts/LexendDeca-SemiBold.ttf", 100)
        self.font_text = pygame.font.Font("assets/fonts/RobotoMono-VariableFont_wght.ttf", 40)
        self.title = self.font_title.render("DactyloFun", True, WHITE)
        self.text_surface = self.font_text.render(" ".join([mot for mot in self.mots]), True, WHITE)

        self.input_text = ""
        self.full_input_text = ""  # Ajout d'une variable pour stocker l'ensemble du texte saisi
        self.typed_characters = 0  # Ajout d'une variable pour compter le nombre de caractères tapés

        self.timer_started = False
        self.start_time = None
        self.finished = False
        self.wpm = 0
        self.accuracy = 0
        self.errors = 0

        self.on_new_page = False
        self.new_page_button = pygame.Rect(self.screen.get_width() - 60, 10, 50, 50)  # x, y, largeur, hauteur

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and not self.finished:
                if not self.timer_started:
                    self.timer_started = True
                    self.start_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.replay_button.collidepoint(mouse_pos):
                    self.reset_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    self.full_input_text = self.full_input_text[:-1]  # Mettre à jour self.full_input_text
                    self.typed_characters -= 1
                elif event.key == pygame.K_SPACE:
                    self.input_text = ""  # Réinitialiser self.input_text
                    self.full_input_text += " "  # Ajouter un espace à self.full_input_text
                    self.typed_characters += 1
                else:
                    try:
                        self.input_text += event.unicode
                        self.full_input_text += event.unicode  # Mettre à jour self.full_input_text
                        self.typed_characters += 1
                    except:
                        pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.new_page_button.collidepoint(mouse_pos):
                    self.on_new_page = not self.on_new_page

    # ----------------------------- Update ------------------------------------#

    def reset_game(self):
        self.mots = []
        for i in range(self.nb_mots):
            self.mots.append(self.table[random.randint(0, len(self.table) - 1)]["mot"])
        self.text = " ".join([mot for mot in self.mots])
        self.text_surface = self.font_text.render(" ".join([mot for mot in self.mots]), True, WHITE)
        self.input_text = ""
        self.full_input_text = ""
        self.typed_characters = 0
        self.displayed_input_text = ""
        self.complete_input_text = ""
        self.finished = False
        self.start_time = None
        self.timer_started = False
        self.end_time = None
        self.accuracy = 0
        self.errors = 0

    def update(self):
        if not self.finished and self.timer_started and len(self.full_input_text) >= len(self.text):
            self.finished = True
            self.wpm = self.calculate_wpm()
            self.calculate_accuracy()
            self.save_data()

    def calculate_wpm(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000 / 60 # Convertir en minutes
        words = self.typed_characters//5
        wpm = (words / elapsed_time)
        return round(wpm, 1)

    def calculate_accuracy(self):
        for i, char in enumerate(self.full_input_text):
            if i < len(self.text) and char != self.text[i]:
                self.errors += 1
        self.accuracy = round(abs(self.errors/self.typed_characters - 1), 3)

    def check_input_text(self, input_text, original_text):
        checked_text = []
        for i, char in enumerate(input_text):
            if i < len(original_text) and char == original_text[i]:
                checked_text.append((char, (0, 255, 0)))  # Vert
            else:
                checked_text.append((char, (255, 0, 0)))  # Rouge
        return checked_text

    # ----------------------------- Data saving ------------------------------------#

    def save_data(self):
        try: table = lire_donnees_csv("save.csv")
        except: table = []
        table.append({
            "speed": self.wpm,
            "accuracy": self.accuracy
        })
        ecrire_donnees_csv(table, "save.csv")


    # ----------------------------- Display ------------------------------------#

    '''def blit_text(self, surface, words, pos, font):
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = surface.get_size()
            x, y = pos
            for word in words:
                for letter in word:
                    letter_surface = font.render(letter, 0, WHITE)
                    letter_width, letter_height = letter_surface.get_size()
                    if x + letter_width >= max_width:
                        x = pos[0]  # Reset the x.
                        y += letter_height  # Start on new row.
                    surface.blit(letter_surface, (x, y))
                    x += letter_width
                x += space  # Add space between words
            x = pos[0]  # Reset the x.
            y += letter_height  # Start on new row.'''

    def draw_writing_box(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (
        self.screen.get_width() // 2 - self.screen.get_width() * 0.30, self.screen.get_height() * 0.6,
        self.screen.get_width() * 0.6, 80))

    def draw_input_text(self):
        x, y = self.screen.get_width() // 2 - self.font_text.render(self.input_text, True, (0, 0, 0)).get_width()//2, self.screen.get_height() * 0.61
        for char in self.input_text:
            rendered_char = self.font_text.render(char, True, (0, 0, 0))
            char_width, char_height = rendered_char.get_size()
            self.screen.blit(rendered_char, (x, y))
            x += char_width

    def check_input_text(self, full_input_text, original_text):
        checked_text = []
        for i, char in enumerate(full_input_text):
            if i < len(original_text) and char == original_text[i]:
                checked_text.append((char, (0, 255, 0)))  # Vert
            else:
                checked_text.append((char, (255, 0, 0)))  # Rouge

        for i in range(len(full_input_text), len(original_text)):
            checked_text.append((original_text[i], WHITE))  # Blanc

        return checked_text

    def blit_checked_text(self, surface, checked_text, pos, font, max_width):
        x, y = pos
        space_width = font.size(' ')[0]

        words = []
        word = []
        for char, color in checked_text:
            if char == " ":
                words.append(word)
                word = []
            else:
                word.append((char, color))
        words.append(word)

        current_line = []
        current_line_width = 0

        for word in words:
            word_width = sum(font.size(char)[0] for char, _ in word)

            if current_line_width + word_width + space_width > max_width:
                # Render the current line and start a new line
                for line_char, line_color in current_line:
                    char_surface = font.render(line_char, 0, line_color)
                    surface.blit(char_surface, (x, y))
                    x += font.size(line_char)[0]
                x = pos[0]
                y += font.size(char)[1]

                current_line = word
                current_line_width = word_width
            else:
                if current_line:
                    current_line.append((" ", (255, 255, 255)))
                    current_line_width += space_width
                current_line.extend(word)
                current_line_width += word_width

        # Render the remaining characters in the current line
        for line_char, line_color in current_line:
            if line_char == " ":
                x += space_width
            else:
                char_surface = font.render(line_char, 0, line_color)
                surface.blit(char_surface, (x, y))
                x += font.size(line_char)[0]

        return x, y

    def draw_replay_button(self):
        self.replay_button = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() * 0.9, 200, 40)
        pygame.draw.rect(self.screen, (200, 200, 200), self.replay_button)
        replay_text = self.font_text.render("Replay", True, (0, 0, 0))
        self.screen.blit(replay_text, (self.replay_button.x + (self.replay_button.width - replay_text.get_width()) // 2,
                                       self.replay_button.y + (
                                                   self.replay_button.height - replay_text.get_height()) // 2))

    def display_new_page(self):
        self.screen.fill(DARKGREY)

        pygame.draw.rect(self.screen, WHITE, self.new_page_button)

        # afficher les stats
        try:
            table = lire_donnees_csv("save.csv")
        except:
            table = None
        if table == None or len(table) == 0:
            none_text = self.font_text.render("Il n'y a aucune données enregistrées", True, WHITE)
            self.screen.blit(none_text, (self.screen.get_width() // 2 - none_text.get_width() // 2,
                                         self.screen.get_height() // 2 - none_text.get_height() // 2))
        else:
            last10 = table[len(table) - 10:]
            moy1_speed = round(sum(float(i["speed"]) for i in table) / len(table), 1)
            moy1_acc = round(sum(float(i["accuracy"]) for i in table) / len(table)*100, 3)
            moy2_speed = round(sum(float(i["speed"]) for i in last10) / len(table), 1)
            moy2_acc = round(sum(float(i["accuracy"]) for i in last10) / len(table)*100, 3)

            titre1 = "Moyenne générale :"
            titre1_render = self.font_text.render(titre1, True, WHITE)
            self.screen.blit(titre1_render, (
                self.screen.get_width() // 2 - titre1_render.get_width() // 2,
                self.screen.get_height() * 0.2 - titre1_render.get_height() // 2))
            stats_text1 = f"Vitesse: {moy1_speed}   Précision: {moy1_acc}%"
            stats_render1 = self.font_text.render(stats_text1, True, WHITE)
            self.screen.blit(stats_render1, (
                self.screen.get_width() // 2 - stats_render1.get_width() // 2,
                self.screen.get_height() * 0.3 - stats_render1.get_height() // 2))
            titre2 = "Moyenne des 10 derniers essais :"
            titre2_render = self.font_text.render(titre2, True, WHITE)
            self.screen.blit(titre2_render, (
                self.screen.get_width() // 2 - titre2_render.get_width() // 2,
                self.screen.get_height() * 0.5 - titre2_render.get_height() // 2))
            stats_text2 = f"Vitesse: {moy1_speed}   Précision: {moy1_acc}%"
            stats_render2 = self.font_text.render(stats_text2, True, WHITE)
            self.screen.blit(stats_render1, (
                self.screen.get_width() // 2 - stats_render2.get_width() // 2,
                self.screen.get_height() * 0.6 - stats_render2.get_height() // 2))

    def display(self):
        self.screen.fill(DARKGREY)

        if not self.on_new_page:
            self.screen.blit(self.title, (self.unit * 50, self.unit * 20))

            checked_text = self.check_input_text(self.full_input_text, self.text)
            self.blit_checked_text(self.screen, checked_text, (20, 300), self.font_text, self.screen.get_width() - 40)

            self.draw_writing_box()
            self.draw_input_text()

            self.draw_replay_button()

            if self.finished:
                wpm_text = f"Vitesse: {self.wpm} MPM   Précision: {round(self.accuracy*100,1)}%"
                wpm_render = self.font_text.render(wpm_text, True, WHITE)
                self.screen.blit(wpm_render, (
                    self.screen.get_width() // 2 - wpm_render.get_width() // 2, self.screen.get_height() * 0.8))

            pygame.draw.rect(self.screen, WHITE, self.new_page_button)
        else:
            self.display_new_page()

        pygame.display.flip()

    # ----------------------------- Running Function ------------------------------------#

    def run(self):
        FPS = 60
        while self.running:
            self.clock.tick(FPS)
            self.handling_events()
            self.update()
            self.display()


game = Main((1920, 1080))
game.run()
pygame.quit()
