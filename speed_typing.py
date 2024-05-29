import pygame
from pygame.locals import *
import sys
import time
import random
import requests

# URL API
BASE_URL = "http://localhost:5000/api/statistics"

class Game:

    def __init__(self):
        self.w = 900
        self.h = 600
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))


        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed test')

    def draw_text(self, screen, msg, y, fsize, color, max_width=None):
        font = pygame.font.Font(None, fsize)
        lines = self.wrap_text(font, msg, max_width) if max_width else [msg]
        for line in lines:
            text = font.render(line, 1, color)
            text_rect = text.get_rect(center=(self.w / 2, y))
            screen.blit(text, text_rect)
            y += fsize  # Move to the next line
        pygame.display.update()

    def wrap_text(self, font, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if not self.end:
            # Расчет времени
            self.total_time = time.time() - self.time_start

            # Расчет точности
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Расчет количества слов в минуту
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # Загрузка иконки
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

            # Функция для добавления статистики
            def add_statistic(time, accuracy, wpm):
                payload = {
                    "time": time,
                    "accuracy": accuracy,
                    "wpm": wpm
                }
                response = requests.post(f"{BASE_URL}/add", json=payload)
                if response.status_code == 201:
                    print("Statistic added successfully")
                else:
                    print(f"Failed to add statistic: {response.text}")

            add_statistic(self.total_time,self.accuracy,self.wpm)
            

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 800, 75))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 800, 75), 2)
            # Обновление текста пользовательского ввода
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250), 650)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # Расположение окна ввода
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    # Расположение кнопки сброса
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.reset_game()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 420, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = time.time()
        self.total_time = 0
        self.wpm = 0

        # Получаем случайное предложение
        self.word = self.get_sentence()
        if not self.word:
            self.reset_game()
        # Загрузка окна
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        # Отрисовка поля ввода
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # Отрисовка строки предложения
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()

Game().run()