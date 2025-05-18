import pygame
import time
from random import randint

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
BACK_COLOR = (200, 255, 255)                  # колір фону (background)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)

main_window = pygame.display.set_mode((500, 500))   # вікно програми (main window)
main_window.fill(BACK_COLOR)
clock = pygame.time.Clock()

# Клас для створення прямокутника 
class Area():
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x, y, width, height)   #прямокутник
        self.color = color

    def set_color(self, new_color):
        self.color = new_color

    def fill_color(self):
        pygame.draw.rect(main_window, self.color, self.rect)
    
    #обведення існуючого прямокутника
    def outline(self, frame_color, thickness):     
        pygame.draw.rect(main_window, frame_color, self.rect, thickness)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

# Класс для створення напису
class Label(Area):	
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        self.fill_color()
        main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

cards = []
num_cards = 4
x = 70

for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('CLICK', 18)
    cards.append(new_card)
    x = x + 100

start_time = time.time()
cur_time = start_time
 
time_text = Label(0, 0, 50, 50, BACK_COLOR)
time_text.set_text('Час:', 35, DARK_BLUE)
time_text.draw(20, 20)
 
score_text = Label(380, 0, 50, 50, BACK_COLOR)
score_text.set_text('Рахунок:', 35, DARK_BLUE)
score_text.draw(20, 20)
 
timer = Label(50, 55, 50, 40, BACK_COLOR)
timer.set_text('0', 30, DARK_BLUE)
timer.draw(0, 0)
 
score = Label(430, 55, 50, 40, BACK_COLOR)
score.set_text('0', 30, DARK_BLUE)
score.draw(0, 0)

wait = 0
points = 0
running = True
# Основний цикл програми
while running:
    # Перемальовуємо фон кожен кадр
    main_window.fill(BACK_COLOR) 
    # Перемальовуємо всі елементи

    time_text.draw(20, 20)
    score_text.draw(20, 20)
    timer.draw(0, 0)
    score.draw(0, 0)
    
    if wait == 0:
        # Відмальовування карток
        wait = 40                #стільки тиків напис буде на одному місці
        click = randint(1, num_cards)
        for i in range(num_cards):
                cards[i].set_color(YELLOW)
                if (i + 1) == click:
                    cards[i].set_text('CLICK', 18)
                else:
                    cards[i].set_text('', 18)
    else:
        wait -= 1
    
    # Відмальовування карток
    for i in range(num_cards):
        cards[i].draw(10, 20)
        cards[i].outline(BLUE, 5)

    # Оновлюємо таймер та бали
    new_time = time.time()
    cur_time = int(new_time - start_time)
    timer.set_text(str(cur_time), 30, DARK_BLUE)
    timer.draw(0, 0)
    score.set_text(str(points), 30, DARK_BLUE)
    score.draw(0, 0)

    '''Перемога та поразка'''
    # Перевіряємо умову закінчення часу - більше 10 секунд
    if cur_time >= 11:
        win = Label(0, 0, 500, 500, LIGHT_RED)
        win.set_text("Час вичерпано!!!", 30, DARK_BLUE)
        win.draw(110, 180)
        pygame.display.update()
        pygame.time.wait(4000)  # Показати 4 секунди
        running = False
        continue

    # Перевіряємо умову виграшу - набрано 5 балів  
    if points >= 5:
        win = Label(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text("Ты переміг!!!", 30, DARK_BLUE)
        win.draw(140, 180)
        resul_time = Label(90, 230, 250, 250, LIGHT_GREEN)
        resul_time.set_text("Час проходження: " + str (cur_time) + " секунд", 20, DARK_BLUE)
        resul_time.draw(0, 0)
        pygame.display.update()
        pygame.time.wait(4000)  # Показати 4 секунди
        running = False
        continue
           
    # на кожному тику перевіряємо клік:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
           
            for i in range(num_cards):
                # шукаємо, в яку карту потрапив клік
                    if cards[i].collidepoint(x, y):
                        if i + 1 == click:              #якщо на карті є напис - перефарбовуємо в зелений плюс очко
                            cards[i].set_color(GREEN)
                            points += 1
                        else:                   #інакше перефарбовуємо в червоний, мінус очко
                            cards[i].set_color(RED)
                            points -= 1
                        cards[i].fill_color()

    pygame.display.update()
    clock.tick(40)
    
pygame.quit()