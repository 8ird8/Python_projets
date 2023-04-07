import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

move_right = [pygame.image.load("hero/R1.png"), pygame.image.load("hero/R2.png"), pygame.image.load("hero/R3.png"),
              pygame.image.load("hero/R4.png"),
              pygame.image.load("hero/R5.png"), pygame.image.load("hero/R6.png"), pygame.image.load("hero/R7.png"),
              pygame.image.load("hero/R8.png"),
              pygame.image.load("hero/R9.png")]
move_left = [pygame.image.load("hero/L1.png"), pygame.image.load("hero/L2.png"), pygame.image.load("hero/L3.png"),
             pygame.image.load("hero/L4.png"),
             pygame.image.load("hero/L5.png"), pygame.image.load("hero/L6.png"), pygame.image.load("hero/L7.png"),
             pygame.image.load("hero/L8.png"),
             pygame.image.load("hero/L9.png")]

move_rightE = [pygame.image.load("enemy/R1E.png"), pygame.image.load("enemy/R2E.png"),
               pygame.image.load("enemy/R3E.png"),
               pygame.image.load("enemy/R4E.png"), pygame.image.load("enemy/R5E.png"),
               pygame.image.load("enemy/R6E.png"),
               pygame.image.load("enemy/R7E.png"), pygame.image.load("enemy/R8E.png"),
               pygame.image.load("enemy/R9E.png"),
               pygame.image.load("enemy/R10E.png"), pygame.image.load("enemy/R11E.png")]
move_leftE = [pygame.image.load("enemy/L1E.png"), pygame.image.load("enemy/L2E.png"),
              pygame.image.load("enemy/L3E.png"),
              pygame.image.load("enemy/L4E.png"), pygame.image.load("enemy/L5E.png"),
              pygame.image.load("enemy/L6E.png"),
              pygame.image.load("enemy/L7E.png"), pygame.image.load("enemy/L8E.png"),
              pygame.image.load("enemy/L9E.png"),
              pygame.image.load("enemy/L10E.png"), pygame.image.load("enemy/L10E.png")]

bg = pygame.image.load("Bg.png")
hero = pygame.image.load("hero/standing.png")
score = 0

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)

clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height
        self.step = 5
        self.Left = False
        self.Right = False
        self.speed = 10
        self.health = 10
        self.visible = True
        self.isJumping = False
        self.Moves = 0
        self.Standing = False
        self.box = (self.x + 20, self.y, self.width, self.height + 35)

    def draw(self, screen):
        if self.visible:
            if not self.Standing:
                if self.Left:
                    screen.blit(move_left[self.Moves // 2], (self.x, self.y))
                    self.Moves += 1
                    if self.Moves == 18:
                        self.Moves = 0
                elif self.Right:
                    screen.blit(move_right[self.Moves // 2], (self.x, self.y))
                    self.Moves += 1
                    if self.Moves == 18:
                        self.Moves = 0
            else:
                if self.Right:
                    screen.blit(move_right[0], (self.x, self.y))
                else:
                    screen.blit(move_left[0], (self.x, self.y))
            self.box = (self.x + 20, self.y, self.width, self.height + 35)
            # pygame.draw.rect(screen, RED, self.box, 2)

            pygame.draw.rect(screen, RED, (self.box[0], self.box[1] - 15, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.box[0], self.box[1] - 15, self.health * 5, 10))

    def hit(self):
        global score
        global event
        self.x = self.start_x
        self.y = self.start_y
        self.Moves = 0
        self.health -= 1
        if self.health == 0:
            self.visible = False
            self.box = (0, 0, 0, 0)
            score -= 1
            font1 = pygame.font.SysFont("comicsans", 80)
            text = font1.render("You lose", 1, BLACK)
            screen.blit(text, (900 // 2 - 1, 200))
            pygame.display.update()

        i = 0
        while i < 150:
            i += 1
            pygame.time.delay(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()


class Bullet:

    def __init__(self, x, y, radius, color, direction, step):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.step = step * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Enemy:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.start = x
        self.step = 3
        self.Moves = 0
        self.box = (self.x + 20, self.y, self.width, self.height + 30)
        self.health = 10
        self.visible = True

    def draw(self, screen):
        if self.visible:
            self.move()
            if self.step < 0:
                screen.blit(move_leftE[self.Moves // 2], (self.x, self.y))
                self.Moves += 1
                if self.Moves == 11 * 2:
                    self.Moves = 0
            else:
                screen.blit(move_rightE[self.Moves // 2], (self.x, self.y))
                self.Moves += 1
                if self.Moves == 11 * 2:
                    self.Moves = 0

            pygame.draw.rect(screen, RED, (self.box[0], self.box[1] - 15, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.box[0], self.box[1] - 15, self.health * 5, 10))

    def move(self):
        if self.step > 0:
            if self.x + self.step > self.end:
                self.step *= -1
            else:
                self.x += self.step
        else:
            if self.x - self.step < self.start:
                self.step *= -1
            else:
                self.x += self.step

        self.box = (self.x + 20, self.y, self.width, self.height + 30)
        # pygame.draw.rect(screen, RED, self.box, 2)

    def Hit(self):
        global score
        self.health -= 1
        if self.health == 0:
            self.visible = False
            self.box = (0, 0, 0, 0)
            score += 1
        print("hit")


class Enemy2:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.start = 150
        self.step = 3
        self.Moves = 0
        self.box = (self.x + 20, self.y, self.width, self.height + 30)
        self.health = 10
        self.visible = True

    def Draw(self, screen):
        if self.visible:
            self.move()
            if self.step < 0:
                screen.blit(move_leftE[self.Moves // 2], (self.x, self.y))
                self.Moves += 1
                if self.Moves == 11 * 2:
                    self.Moves = 0
            else:
                screen.blit(move_rightE[self.Moves // 2], (self.x, self.y))
                self.Moves += 1
                if self.Moves == 11 * 2:
                    self.Moves = 0

            pygame.draw.rect(screen, RED, (self.box[0], self.box[1] - 15, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.box[0], self.box[1] - 15, self.health * 5, 10))

    def move(self):
        if self.step > 0:
            if self.x + self.step > self.end:
                self.step *= -1
            else:
                self.x += self.step
        else:
            if self.x - self.step < self.start:
                self.step *= -1
            else:
                self.x += self.step

        self.box = (self.x + 20, self.y, self.width, self.height + 30)

    def Hit(self):
        global score
        self.health -= 1
        if self.health == 0:
            self.visible = False
            self.box = (0, 0, 0, 0)
            score += 1
            print("hit")


man = Player(600, 495, 30, 30)
enemy = Enemy(170, 500, 30, 30, 700)
enemy2 = Enemy2(400, 500, 30, 30, 700)

font = pygame.font.SysFont("comicsans", 35, True)


def start_game():
    text = font.render("Score = " + str(score), True, BLACK)

    screen.blit(bg, (0, 0))
    screen.blit(text, (600, 10))

    man.draw(screen)
    enemy.draw(screen)
    enemy2.Draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


bullets = []

while True:
    clock.tick(30)

    x_mid = (man.box[0] + man.box[0] + man.box[2]) // 2
    y_mid = (man.box[1] + man.box[1] + man.box[3]) // 2
    if enemy.box[0] < x_mid < enemy.box[0] + enemy.box[2]:
        if enemy.box[1] < y_mid < enemy.box[1] + enemy.box[3]:
            man.hit()

    x_mid = (man.box[0] + man.box[0] + man.box[2]) // 2
    y_mid = (man.box[1] + man.box[1] + man.box[3]) // 2
    if enemy2.box[0] < x_mid < enemy2.box[0] + enemy2.box[2]:
        if enemy2.box[1] < y_mid < enemy2.box[1] + enemy2.box[3]:
            man.hit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                if len(bullets) < 10:
                    direction = 0
                    if man.Right:
                        direction = 1
                    else:
                        direction = -1
                    bullets.append(
                        Bullet(round(man.x + man.width // 2), round(man.y + man.height // 2), 4, RED, direction,
                               8))

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        if enemy.box[0] < bullet.x < enemy.box[0] + enemy.box[2]:
            if enemy.box[1] < bullet.y < enemy.box[1] + enemy.box[3]:
                bullets.remove(bullet)
                enemy.Hit()

        if bullet.x >= 800 or bullet.x <= 0:
            bullets.remove(bullet)
        else:
            bullet.x += bullet.step

    for bullet in bullets:
        if enemy2.box[0] < bullet.x < enemy2.box[0] + enemy2.box[2]:
            if enemy2.box[1] < bullet.y < enemy2.box[1] + enemy2.box[3]:
                bullets.remove(bullet)
                enemy2.Hit()

        if bullet.x >= 800 or bullet.x <= 0:
            bullets.remove(bullet)
        else:
            bullet.x += bullet.step

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.step
        man.Left = True
        man.Right = False
        man.Standing = False
    elif keys[pygame.K_RIGHT] and man.x + man.width + man.step <= 780:
        man.x += man.step
        man.Right = True
        man.Left = False
        man.Standing = False

    else:
        man.Standing = True
        man.Moves = 0

    if not man.isJumping:
        # if keys[pygame.K_UP] and y > 0:
        #     y -= step
        # if keys[pygame.K_DOWN] and y + height + step <= 526:
        #     y += step
        if keys[pygame.K_SPACE]:
            man.isJumping = True
    else:
        if man.speed >= -10:
            neg = 1
            if man.speed < 0:
                neg = -1
            man.y -= (man.speed ** 2) * 0.5 * neg
            man.speed -= 1
        else:
            man.speed = 10
            man.isJumping = False

    start_game()
