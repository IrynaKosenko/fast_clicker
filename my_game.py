#Підключення потрібних модулів
import pygame
from random import randint

pygame.init()
clock = pygame.time.Clock()  
#кольори
TEXT_COLOR = (0,0,0)
AREA_COLOR = (51, 255, 153)
BACK = (255,255,0)        #колір фону (background)

#створення вікна гри
main_window = pygame.display.set_mode((500,500))    #Вікно програми (main window)
main_window.fill(BACK)

class TextArea():
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = None):
         #запам'ятовуємо прямокутник:
        self.rect = pygame.Rect(x, y, width, height)
        # колір заливки - або переданий параметр, або загальний колір тла
        self.fill_color = color
        self.titles = []

    #додати текст до списку можливих написів
    def add_text(self, text):
        self.titles.append(text)

    #Встановити текст
    def set_text(self, number = 0, font_size = 12, text_color = TEXT_COLOR):
        self.text = self.titles[number]
        self.image = pygame.font.Font(None, font_size).render(self.text, True, text_color)

    # Опис прямокутника з текстом
    def draw(self, shift_x = 0, shift_y = 0):
        pygame.draw.rect(main_window, self.fill_color, self.rect)
        main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


#створення карток
quest_card = TextArea(120, 100, 290, 70, AREA_COLOR)
quest_card.add_text('Питання')
quest_card.add_text('Що вивчаєш в Алгоритміку?')
quest_card.add_text('Якою мовою говорять у Франції?')
quest_card.add_text('Що росте на яблуні?')
quest_card.set_text(0, 75)

ans_card = TextArea(120, 240, 290, 70, AREA_COLOR)
ans_card.add_text('Відповідь')
ans_card.add_text('Python')
ans_card.add_text('Французька')
ans_card.add_text('Яблука')
ans_card.set_text(0, 75)

quest_card.draw(10, 10)
ans_card.draw(10, 10)

running = True
while running:
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  
                num = randint (1, len(quest_card.titles) - 1)
                quest_card.set_text(num, 25)
                main_window.fill(BACK)
                quest_card.draw(10, 20)
                ans_card.draw(10, 20)
                
            if event.key == pygame.K_a:
                num = randint (1, len(ans_card.titles) - 1)
                ans_card.set_text(num, 25)
                main_window.fill(BACK)
                quest_card.draw(10, 20)
                ans_card.draw(10, 20)
                
            if event.key == pygame.K_ESCAPE:
                running = False
                
    pygame.display.flip()        # оновлення вікна            
    clock.tick(60)               # обмеження частоти кадрів (60 FPS)

# Завершення роботи pygame
pygame.quit()