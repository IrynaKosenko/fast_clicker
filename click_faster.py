import pygame
import time
from random import randint

pygame.init()
WIDTH = 800
HEIGHT = 500

# Визначення кольорів
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
BACK_COLOR = (200, 255, 255)    # колір фону (background)

main_window = pygame.display.set_mode((WIDTH, HEIGHT))   # вікно програми (main window)
main_window.fill(BACK_COLOR)
back_image = pygame.image.load('images/background.jpg')      # фон програми (background image)
back_image = pygame.transform.scale(back_image, main_window.get_size())  # Масштабування зображення до розмірів вікна
main_window.blit(back_image, (0, 0)) # фон програми (background image)
pygame.display.set_caption("Click faster")          # назва програми (title)
clock = pygame.time.Clock()

transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
transparent_surface.fill((255, 255, 255, 0))  # Білий колір із прозорістю
main_window.blit(transparent_surface, (0, 0))

# Клас для створення прямокутника 
class Area():
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x, y, width, height)   #прямокутник
        self.color = color
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def set_color(self, new_color):
        self.color = new_color

    def fill_color(self):
        pygame.draw.rect(main_window, self.color, self.rect, border_radius = 20)

    def fill_transparency(self): # якщо не треба заповнювати кольором, то заповнюємо прозорим кольором
        self.surface.fill((255, 255, 255, 0))  # Білий колір із прозорістю
        main_window.blit(self.surface, (self.rect.x, self.rect.y))

    #обведення існуючого прямокутника
    def outline(self, frame_color, thickness):  
        pygame.draw.rect(main_window, frame_color, self.rect, thickness, border_radius = 20)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

# Класс для створення напису
class Label(Area):	
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        if self.color:
            self.fill_color()
            main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
        else:
            self.fill_transparency()
            main_window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

cards = []
num_cards = 4
x = (WIDTH - num_cards * 100) / 5
shift_x = x + 100

for i in range(num_cards):
    new_card = Label(x, 170, 100, 120, YELLOW)
    new_card.outline(BLUE, 5)
    new_card.set_text('CLICK', 18)
    cards.append(new_card)
    x = x + shift_x     # координата x для наступної карти

start_time = time.time()
old_time = time.time()
 
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
while running:
    if wait == 0:
        wait = 20
        click = randint (1, num_cards)
        for i in range(num_cards):
            cards[i].set_color(YELLOW)
            if (i+1) == click:
                cards[i].draw(20, 40)
                cards[i].outline(BLUE, 5)  # Малюємо обведення
            else:
                cards[i].fill_color()
                cards[i].outline(BLUE, 5)  # Малюємо обведення
    else:
        wait -=1
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    running = False
                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                #шукаємо, в яку карту потрапив клік
                    if cards[i].collidepoint(x,y):
                        if i + 1 == click:              #якщо на карті є напис - перефарбовуємо в зелений плюс очко
                            cards[i].set_color(GREEN)
                        else:                          #інакше перефарбовуємо в червоний, мінус очко
                            cards[i].set_color(RED)
                        cards[i].fill_color()

    pygame.display.update()
    clock.tick(40)
    
# Завершення роботи pygame
pygame.quit()
