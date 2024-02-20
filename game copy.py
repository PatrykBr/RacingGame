import pygame
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center

pygame.init()

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track3.png"), 1.85)

TRACK_BORDER = scale_image(pygame.image.load("imgs/border2.png"), 1.85)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = scale_image(pygame.image.load("imgs/cars/red_bull.png"), 0.3)
GREEN_CAR = scale_image(pygame.image.load("imgs/cars/mclaren.png"), 0.8)
print(RED_CAR.get_height(), RED_CAR.get_width())

WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()

# Calculate the positions to center the images
grass_x = (WIDTH - GRASS.get_width()) // 2
grass_y = (HEIGHT - GRASS.get_height()) // 2

track_x = (WIDTH - TRACK.get_width()) // 2
track_y = (HEIGHT - TRACK.get_height()) // 2

track_border_x = (WIDTH - TRACK_BORDER.get_width()) // 2
track_border_y = (HEIGHT - TRACK_BORDER.get_height()) // 2

FINISH_POSITION = (WIDTH * 0.6, HEIGHT * 0.86)

pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)
FPS = 60
PATH = [(257, 903), (121, 820), (15, 502), (155, 193), (410, 311), (505, 40), (644, 40), (905, 240), (1446, 255), (1292, 439), 
        (910, 341), (771, 472), (637, 299), (470, 449), (292, 394), (206, 573), (314, 769), (1040, 775), (1272, 529), (1439, 713), (1366, 894), (578, 908)]

class GameInfo:
    LEVELS = 10
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)

        if poi is not None:
            pygame.draw.circle(WIN, (255, 0, 0), poi, 5)
            pygame.display.update()
            
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (WIDTH * 0.45, HEIGHT * 0.86)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.8
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (WIDTH * 0.45, HEIGHT * 0.86)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    #def draw_points(self, win):
    #    for point in self.path:
    #        pygame.draw.circle(win, (255, 0, 0), point, 5)

    #def draw(self, win):
    #    super().draw(win)
    #    self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

def draw(win, images, player_car, computer_car, game_info):
    # Fill the window with a background color (e.g., black)
    win.fill((0, 0, 0))

    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, 10))  # Positioning at the top left

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))  # Positioning at the top right

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))  # Positioning at the bottom left

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()



def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        #print("BOUCNE")
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide is not None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide is not None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)

def play_game(username, sponsor_name):
    run = True
    clock = pygame.time.Clock()

    # Update the images list with the calculated positions
    images = [(GRASS, (grass_x, grass_y)), (TRACK, (track_x, track_y)),
            (FINISH, FINISH_POSITION), (TRACK_BORDER, (track_border_x, track_border_y))]

    player_car = PlayerCar(4, 4)
    computer_car = ComputerCar(2, 4, PATH)
    game_info = GameInfo()

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car, computer_car, game_info)
        while not game_info.started:
            blit_text_center(
                WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():
                #if event.type == pygame.MOUSEBUTTONDOWN:
                #    pos = pygame.mouse.get_pos()
                #    computer_car.path.append(pos)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move_player(player_car)
        computer_car.move()

        handle_collision(player_car, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "You won the game!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()

    #print(computer_car.path)
    pygame.quit()

if __name__ == "__main__":
    play_game("","")