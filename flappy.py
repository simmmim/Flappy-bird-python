import pygame, random, time
from pygame.locals import *

#VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 8
GRAVITY = 0.7
GAME_SPEED = 5

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect[0] -= GAME_SPEED

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):    
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

# 점수 획득 시스템
def add_score(pipe, score, GAME_SPEED):
    baseSpeed = 5
    if pipe.rect[0] <= SCREEN_WIDHT / 6:
        score += 100 + int(100 * (GAME_SPEED - baseSpeed))
    return score

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

score = 0
highScore = 0

font_score = pygame.font.SysFont(None, 70)
font_highScore = pygame.font.SysFont(None, 100)

# 게임 무한 루프
while 1==1:
    GAME_SPEED = 5
    pass_cnt = 0
    ispassed = False    
    score = 0
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()

    for i in range (2):
        ground = Ground(GROUND_WIDHT * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range (2):
        pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    clock = pygame.time.Clock()

    begin = True

    while begin:    

        clock.tick(60)  

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if (event.type == KEYDOWN and event.key in(K_SPACE, K_UP)) or event.type == pygame.MOUSEBUTTONDOWN:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))    

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])  

            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)    

        bird.begin()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)   

        pygame.display.update() 


    while begin == False:   

        clock.tick(60)  

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if (event.type == KEYDOWN and event.key in(K_SPACE, K_UP)) or event.type == pygame.MOUSEBUTTONDOWN:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()   

        screen.blit(BACKGROUND, (0, 0)) 

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])  

            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)    

        if is_off_screen(pipe_group.sprites()[0]):
            ispassed = False
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])  

            pipes = get_random_pipes(SCREEN_WIDHT * 2)  

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        
        # 파이프를 지나가면 점수를 올려주고, 다음 파이프를 만나기까지 Pass 처리하기
        if not ispassed:
            beforeScore = score
            score = add_score(pipe_group.sprites()[0], score, GAME_SPEED)
        if beforeScore < score and not ispassed:
            pass_cnt += 1 # 통과 횟수 처리
            ispassed = True

        # n 회 통과할 때마다 게임 속도 10% 증가시키기
        if pass_cnt >= 10:
            pass_cnt = 0
            if GAME_SPEED >= 8:
                GAME_SPEED = 8
            else:
                GAME_SPEED *= 1.1
                print("Speed Up!")
            
             
        score_text = font_score.render(str(score), True, (0,0,0))
        score_text_width = score_text.get_rect().size[0]
        score_text_height = score_text.get_rect().size[1]
        x_pos_score = SCREEN_WIDHT/2-score_text_width/2
        y_pos_score= SCREEN_HEIGHT/5-score_text_height/2
        
        bird_group.update()
        ground_group.update()
        pipe_group.update() 

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)   

        screen.blit(score_text, (x_pos_score, y_pos_score))

        pygame.display.update() 


        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            
            highScore = max(highScore, score)
            highScore_text = font_score.render("High Score: "+str(highScore), True, (0,0,255))
            highScore_text_width = highScore_text.get_rect().size[0]
            highScore_text_height = highScore_text.get_rect().size[1]
            x_pos_highScore = SCREEN_WIDHT/2-highScore_text_width/2
            y_pos_highScore= SCREEN_HEIGHT/3-highScore_text_height/2
            screen.blit(highScore_text, (x_pos_highScore, y_pos_highScore))
            pygame.display.update()

            while begin == False:
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    if (event.type == KEYDOWN and event.key in(K_SPACE, K_UP)) or event.type == pygame.MOUSEBUTTONDOWN:
                        bird.bump()
                        begin = True
                        time.sleep(0.5)
                        break

