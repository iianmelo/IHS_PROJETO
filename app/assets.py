import pygame

# Asset do cone (obstaculo 1)
cone_asset = pygame.image.load('sprites/traffic-cone.png')
escala_cone = 0.05
cone_width_adjust = int(cone_asset.get_width() * escala_cone)
cone_height_adjust = int(cone_asset.get_height() * escala_cone)
cone_asset_center = pygame.transform.scale(cone_asset, (cone_width_adjust, cone_height_adjust))

# Asset da bala
bullet_asset = pygame.image.load('sprites/bullet3.png')
escala_bala = 0.05
bullet_width_adjust = int(bullet_asset.get_width() * escala_bala)
bullet_height_adjust = int(bullet_asset.get_height() * escala_bala)
bullet_asset_center = pygame.transform.scale(bullet_asset, (bullet_width_adjust, bullet_height_adjust))

# Asset pista
background = pygame.image.load('sprites/pista.png')
background_correct_size = pygame.transform.scale(background, (600, 700))

# Asset do carro
car_asset = pygame.image.load('sprites/Car.png')
escala = 0.05
car_width_adjust = int(car_asset.get_width() * escala)
car_height_adjust = int(car_asset.get_height() * escala)
car_asset_center = pygame.transform.scale(car_asset, (car_width_adjust, car_height_adjust))
car_to_left = pygame.transform.rotate(car_asset_center,11) #asset de movimento para esquerda
car_to_right = pygame.transform.rotate(car_asset_center,-11) #asset de movimento para direita

# Assets zombie
zombie_scale = 0.27
zombie_asset = pygame.image.load('sprites/zombie_movement/skeleton-move_0.png')
zombie_width_adjust = int(zombie_asset.get_width()* zombie_scale)
zombie_height_adjust = int (zombie_asset.get_height()* zombie_scale)
zombie_asset_adjust = pygame.transform.scale(zombie_asset,(zombie_width_adjust, zombie_height_adjust))
zombie_adjust_rotate = pygame.transform.rotate(zombie_asset_adjust, -90)
zombie_move_0 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_0.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_1.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_2.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_3 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_3.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_4 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_4.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_5 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_5.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_6 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_6.png'),(zombie_width_adjust, zombie_height_adjust)),-90) 
zombie_move_7 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_7.png'),(zombie_width_adjust, zombie_height_adjust)),-90) 
zombie_move_8 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_8.png'),(zombie_width_adjust, zombie_height_adjust)),-90) 
zombie_move_9 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_9.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_10 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_10.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_11 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_11.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_12 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_12.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_13 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_13.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_14 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_14.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_15 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_15.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
zombie_move_16 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('sprites/zombie_movement/skeleton-move_16.png'),(zombie_width_adjust, zombie_height_adjust)),-90)
move_zombie= [zombie_move_0,zombie_move_1,zombie_move_2,zombie_move_3,zombie_move_4,zombie_move_5,zombie_move_6,zombie_move_7,zombie_move_8,zombie_move_9,zombie_move_10,zombie_move_11,zombie_move_12,zombie_move_13,zombie_move_14,zombie_move_15,zombie_move_16]

#indices para animação do zombie
image_index = 0
image_delay = 5
image_counter = 0