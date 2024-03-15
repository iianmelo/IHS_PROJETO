import pygame, sys, random
from pygame.math import Vector2
import assets

class BULLET:
    def __init__(self, car_pos_x):
        #posicoes iniciais da bala
        self.bullet_pos_X = car_pos_x + 21
        self.bullet_pos_Y = 570
        self.velocity = 5
        #vetor da posicao da bala
        self.position = Vector2(self.bullet_pos_X, self.bullet_pos_Y)
        #retangulo para checar colisao da bala
        self.bullet_rect = pygame.Rect(self.position.x,self.position.y, assets.bullet_width_adjust*0.9,assets.bullet_height_adjust)    
    def draw_bullet(self):
        #centro do retangulo da bala
        self.bullet_rect.center = [self.position.x+0.5*assets.bullet_width_adjust,self.position.y+0.5*assets.bullet_height_adjust]
        #desenhando uma bala
        screen.blit(assets.bullet_asset_center, self.position)
        
class CAR:
    def __init__(self):
        #posicoes iniciais do carro
        self.car_pos_x = screen.get_width() / 1.9
        self.car_pos_y = 570
        #vetor da posicao do carro
        self.position = Vector2(self.car_pos_x, self.car_pos_y)
        #direcao do carro (para fazer a angulacao da imagem) #0=meio, 1= direita e -1 = esquerda
        self.direction = 0 
        #retangulo para checar colisao do carro
        self.car_rect = pygame.Rect(self.position.x+5,self.position.y+3, assets.car_width_adjust*0.9,assets.car_height_adjust)
    #desenhando o carro de acordo com sua direcao para a angulacao
    def draw_car(self):
        if self.direction == 0:
            screen.blit(assets.car_asset_center,self.position)
        elif self .direction == 1:
            screen.blit(assets.car_to_right,self.position)
        elif self.direction == -1:
            screen.blit(assets.car_to_left,self.position)
        
class OBSTACULO:
    def __init__(self):
        #criando as vidas do zumbi
        self.life = 3
        #gerando um x aleatorio para a posicao do zumbi 
        self.randomize()
        #retangulo para checar colisao do zumbi
        self.zombie_rect = pygame.Rect(self.pos.x, self.pos.y, assets.zombie_width_adjust*0.8, assets.zombie_height_adjust*0.5)
        
    def draw_obstaculo(self):
        #centro do retangulo do zumbi
        self.zombie_rect.center = [self.pos.x+35 , self.pos.y+30]
        #contador para animacao da imagem do zumbi
        assets.image_counter += 1
        if assets.image_counter >= assets.image_delay:
            assets.image_index = (assets.image_index + 1) % len(assets.move_zombie)
            assets.image_counter = 0
        #desenhando o sprite do zumbi
        current_image = assets.move_zombie[assets.image_index]
        screen.blit(current_image, self.pos)

    def randomize(self):
        self.x = random.randint(125, 405)
        self.y = 5
        self.pos = pygame.math.Vector2(self.x, self.y) #vetor de posições
    
    #movendo sempre o obstaculo para baixo
    def move_obstaculo(self):
        self.pos.y += 8
        self.zombie_rect.y += 8

class MAIN():

    def __init__(self):
        self.car = CAR()
        #inciciando vetor de zumbis
        self.obst_vector = []
        #iniciando vetor de balas
        self.bullet_vector = []
        self.obst_vector.append(OBSTACULO()) #OBSTACULO INICIAL P/ TESTES 
        self.obst_vector.append(OBSTACULO())

    #funcao para desenhar elementos
    def draw_elements(self):
        self.car.draw_car()
        for obst in self.obst_vector:
            #desenhando cada obstaculo
            obst.draw_obstaculo()
            #removendo o obstaculo caso passe do final
            if(obst.pos.y>=650):
                self.obst_vector.remove(obst)
        for bullet in self.bullet_vector:
            #desenhando cada bala
            bullet.draw_bullet()
            #removendo a bala caso passe do final
            if(bullet.position.y <= 0):
                self.bullet_vector.remove(bullet)
        
    def update(self):
        self.check_collision()
        self.car.direction = 0
        for obst in self.obst_vector:
            obst.move_obstaculo()
        for bullet in self.bullet_vector:
            #movendo cada bala
            bullet.position.y -= bullet.velocity
        
    def game_over(self):
        pygame.quit()
        sys.exit()
    

    def check_collision(self):
        for obst in self.obst_vector:
            if((self.car.car_rect).colliderect(obst.zombie_rect)):
                obst.life -= 1      
                #print(obst.life)
                if obst.life <= 0:
                    obst.life = 3
                    obst.randomize()
            for bullet in self.bullet_vector:
                if((bullet.bullet_rect).colliderect(obst.zombie_rect)):
                    obst.life -= 1
                    self.bullet_vector.remove(bullet) 
                    #print(obst.life)
                    if obst.life <= 0:
                        obst.life = 3
                        obst.randomize()

pygame.init()
screen_height = 700
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock() # para garantir que o jogo não mude de velocidade de pc para pc

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 16)

main_game = MAIN() 

while True: # loop game
    # desenhar todos o elementos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over() #garante que vai fechar o jogo
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game.bullet_vector.append(BULLET(main_game.car.position.x))

    press = pygame.key.get_pressed()
    if press[pygame.K_LEFT] and main_game.car.position.x > 130:
        main_game.car.direction = -1
        main_game.car.position.x -= 10
        main_game.car.car_rect.x -=10  
    if press[pygame.K_RIGHT] and main_game.car.position.x < 407:
        main_game.car.direction = 1
        main_game.car.position.x += 10
        main_game.car.car_rect.x += 10 
    if press[pygame.K_UP]:
        main_game.car.position.y -= 5
        main_game.car.car_rect.y -= 5 
    if press[pygame.K_DOWN]:
        main_game.car.position.y += 5
        main_game.car.car_rect.y += 5

    screen.blit(assets.background_correct_size, (0,0)) 
    main_game.draw_elements()
    pygame.display.flip()
    clock.tick(60) # garante que o jogo rode a 60 fps