import pygame
import time
from random import randint

pygame.init()
WIDTH = 500
HEIGHT = 400

# Визначення кольорів
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
BACK_COLOR = (200, 255, 255)    # колір фону (background)

main_window = pygame.display.set_mode((WIDTH, HEIGHT))   # вікно програми (main window)
main_window.fill((0, 0, 0)) # заповнюємо вікно чорним кольором (fill the window with black color)
back_image = pygame.image.load('images/background.jpg')      # фон програми (background image)
back_image = pygame.transform.scale(back_image, main_window.get_size())  # Масштабування зображення до розмірів вікна
main_window.blit(back_image, (0, 0)) # фон програми (background image)
pygame.display.set_caption("Click faster")          # назва програми (title)
clock = pygame.time.Clock()

# Клас для створення прямокутника
class Area():
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x, y, width, height)   #прямокутник
        self.color = color
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def set_color(self, new_color):
        self.color = new_color

    def fill_rect(self):
        pygame.draw.rect(main_window, self.color, self.rect, border_radius = 20)

    def fill_transparency(self): # якщо не треба заповнювати кольором, то заповнюємо прозорим кольором
        self.surface.fill((255, 255, 255, 0))  # Білий колір із прозорістю
        main_window.blit(self.surface, (self.rect.x, self.rect.y))

    #обведення існуючого прямокутника
    def outline(self, frame_color, thickness):  
        pygame.draw.rect(main_window, frame_color, self.rect, thickness, border_radius = 20)
    
    def collide_point(self, x, y):
        return self.rect.collidepoint(x, y)

# Класс для створення напису
class Label(Area):	
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        if self.color:
            self.fill_rect()
            main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
        else:
            self.fill_transparency()
            main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

cards = []      # масив для карт (array for cards)
num_cards = 4   # кількість карт (number of cards)
space_cards = (WIDTH - num_cards * 100) / 5  # відстань між картами
x = space_cards  # координата x для першої карти 
shift_x = x + 100  # зміщення по x для наступної карти

for i in range(num_cards):
    new_card = Label(x, 170, 100, 120, YELLOW)
    new_card.outline(BLUE, 5)
    new_card.set_text('CLICK', 18)
    cards.append(new_card)
    x = x + shift_x     # координата x для наступної карти
 
time_text = Label(0, 0, 50, 50)
time_text.set_text('Час:', 35, DARK_BLUE)
time_text.draw(20, 20)
 
score_text = Label(WIDTH - 200, 0, 50, 50)
score_text.set_text('Рахунок:', 35, DARK_BLUE)
score_text.draw(20, 20)
 
timer = Label(50, 55, 50, 40)
timer.set_text('0', 30, GREEN)
timer.draw(0, 0)

score = Label(WIDTH - 100, 55, 50, 40)
score.set_text('0', 30, GREEN)
score.draw(0, 0)

wait = 0
running = True
points =0          # лічильник балів
start_time = time.time()

# Основний цикл програми
while running:
    # Перемальовуємо фон кожен кадр
    main_window.blit(back_image, (0, 0))
    time_text.draw(20, 20)
    score_text.draw(20, 20)
    timer.draw(0, 0)
    score.draw(0, 0)
    
    if wait == 0:
        wait = 50
        click = randint (1, num_cards)
        for i in range(num_cards):
            cards[i].set_color(YELLOW)
            if (i+1) == click:
                cards[i].set_text('CLICK', 18)  # Показати "CLICK" лише тут
            else:
                cards[i].set_text('', 18)       # На інших картках текст порожній
    else:
        wait -=1
    
    # Малюємо всі картки
    for i in range(num_cards):
        cards[i].draw(20, 40)
        cards[i].outline(BLUE, 5)   
        
    # Оновлюємо таймер
    new_time = time.time()
    elapsed = int(new_time - start_time)
    timer.set_text(str(elapsed), 30, GREEN)
    timer.draw(0, 0)
    score.set_text(str(points), 30, GREEN)
    score.draw(0, 0)
    
    # Перевірка на перемогу/поразку
    if elapsed >= 11:
        win = Label(0, 0, 500, 500, RED)
        win.set_text("Час вичерпано!!!", 30, DARK_BLUE)
        win.draw(110, 180)
        pygame.display.update()
        pygame.time.wait(4000)  # Показати 4 секунди
        running = False
        continue
    
    if points >= 5:
        win = Label(0, 0, 500, 500, GREEN)
        win.set_text("Ты переміг!!!", 30, DARK_BLUE)
        win.draw(140, 180)
        resul_time = Label(90, 230, 250, 250, GREEN)
        resul_time.set_text("Час проходження: " + str(elapsed) + " секунд", 20, DARK_BLUE)
        resul_time.draw(0, 0)
        pygame.display.update()
        pygame.time.wait(4000)  # Показати 4 секунди
        running = False
        continue
    
    # Обробка кліків по карткам 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    running = False
                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                # шукаємо, в яку карту потрапив клік
                if cards[i].collide_point(x, y):
                    if i + 1 == click:   #якщо на карті є напис - перефарбовуємо в зелений плюс бал
                        cards[i].set_color(GREEN)
                        points +=1
                    else:        #інакше перефарбовуємо в червоний, мінус бал
                        cards[i].set_color(RED)
                        points -=1
                    cards[i].fill_rect()
                    score.set_text(str(points), 30, GREEN)
                    score.draw(0, 0)

    pygame.display.update()
    clock.tick(40)
    
# Завершення роботи pygame
pygame.quit()
