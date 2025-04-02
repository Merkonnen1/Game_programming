try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from user304_rsf8mD0BOQ_1 import Vector

import math
import time

WIDTH = 1000
HEIGHT = 450
game_started = False
game_frame = None
button_x = WIDTH / 2 - 50
button_y = HEIGHT * 2 / 3
button_width = 100
button_height = 60


class Spritesheet:
    def __init__(self, url, rows, cols, time):
        self.clock_obj = Clock()
        self.image = simplegui.load_image(url)
        self.rows = rows
        self.cols = cols
        self.current_row = 0
        self.current_col = 0
        self.time = time
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.frame_width = self.image_width // self.cols
        self.frame_height = self.image_height // self.rows
        self.centres = [[(col * self.frame_width + self.frame_width // 2,
                          row * self.frame_height + self.frame_height // 2)
                         for col in range(self.cols)]
                        for row in range(self.rows)]


class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def transition(self, frame_duration):
        if self.time > frame_duration:
            self.time = 0
            return True
        return False


class Character:
    def __init__(self, is_player_one):
        self.pos = Vector(WIDTH / 8, 200) if is_player_one else Vector(WIDTH * 7 / 8, 200)
        self.player = {
            "Idle": Spritesheet("https://i.imgur.com/QEGGeXY.png", 1, 6, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/5F7px4p.png", 1, 6, 2),
            "Run": Spritesheet("https://i.imgur.com/DSTxdb0.png", 1, 8, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/xY1P0B0.png", 1, 8, 2),
            "Attack": Spritesheet("https://i.imgur.com/ND8Mi41.png", 1, 6, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/5eD8bnj.png", 1, 4, 2)
        }
        self.current_state = "Idle"
        self.current_animation = self.player[self.current_state]
        self.vel = Vector(0, 0)
        self.frame_count = 0
        self.clock_obj = Clock()
        self.is_attacking = False

    def set_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.current_animation = self.player[self.current_state]
            self.frame_count = 0

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.75)
        print(self.vel)
        if self.is_attacking and self.frame_count > self.current_animation.cols:
           
            self.is_attacking = False
            if self.vel.x == 0:
                self.set_state("Idle")
            else:
                self.set_state("Run")
            self.frame_count = 0

        self.current_animation = self.player[self.current_state]

    def draw(self, canvas):
        self.clock_obj.tick()
        centre_x, centre_y = self.current_animation.centres[self.current_animation.current_row][
            self.current_animation.current_col]
        canvas.draw_image(self.current_animation.image,
                          (centre_x, centre_y),
                          (self.current_animation.frame_width, self.current_animation.frame_height),
                          self.pos.get_p(), (self.current_animation.frame_width, self.current_animation.frame_height))

        if self.clock_obj.transition(self.current_animation.time):
            self.frame_count+=1
            self.next_frame()

    def next_frame(self):
        self.current_animation.current_col += 1
        if self.current_animation.current_col == self.current_animation.cols:
            self.current_animation.current_col = 0

    def attack(self):
        if not self.is_attacking:
            self.set_state("Attack")
            self.is_attacking = True
            self.frame_count = 0

class Keyboard:
    def __init__(self, player_1, player_2):
        self.players = {
            "player_1": {"instance": player_1,
                        "controls": {"right": False, "left": False, "up": False, "down": False}},
            "player_2": {"instance": player_2,
                        "controls": {"right": False, "left": False, "up": False, "down": False}}
                }
        self.key_map = {
                "player_1": {"right": "d", "left": "a", "up": "w", "down": "s"},
                "player_2": {"right": "right", "left": "left", "up": "up", "down": "down"}
            }


    def keyDown(self, key):
        for player, controls in self.key_map.items():
            for action, key_name in controls.items():
                if key == simplegui.KEY_MAP[key_name]:
                    self.players[player]["controls"][action] = True
                    self.players[player]["instance"].set_state("Run")


    def keyUp(self, key):
        for player, controls in self.key_map.items():
            idle = True
            for action, key_name in controls.items():
                if key == simplegui.KEY_MAP[key_name]:
                    self.players[player]["controls"][action] = False
                if self.players[player]["controls"][action]:
                    idle = False
            if idle:
                self.players[player]["instance"].set_state('Idle')


class Ball:
    def __init__(self):
        self.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.vel = Vector(0, 0)
        self.radius = 15
        self.spots = self.generate_even_spots()
        self.kick_time = None
        self.kicked = False

    def generate_even_spots(self):
        spots = []
        num_spots = 5
        for i in range(num_spots):
            angle = (2 * math.pi / num_spots) * i
            x_offset = self.radius * 0.6 * math.cos(angle)
            y_offset = self.radius * 0.6 * math.sin(angle)
            spots.append(Vector(x_offset, y_offset))
        return spots

    def update(self):
        if not self.kicked:
            return

        self.pos.add(self.vel)
        self.vel.multiply(0.99)

        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -0.7
        if self.pos.x + self.radius > WIDTH:
            self.pos.x = WIDTH - self.radius
            self.vel.x *= -0.7
        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -0.7
        if self.pos.y + self.radius > HEIGHT:
            self.pos.y = HEIGHT - self.radius
            self.vel.y *= -0.7

        if self.kick_time and time.time() - self.kick_time > 0.3:
            self.curve_toward_goal()

        self.rotate_spots()

    def rotate_spots(self):
        rotation_angle = self.vel.get_p()[0] * 0.05
        for i, spot in enumerate(self.spots):
            x = spot.x
            y = spot.y
            rotated_x = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
            rotated_y = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
            self.spots[i] = Vector(rotated_x, rotated_y)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "Black", "White")
        for spot in self.spots:
            spot_pos = self.pos.copy().add(spot)
            canvas.draw_circle(spot_pos.get_p(), self.radius // 4, 1, "Black", "Black")

    def kick(self, direction, player_velocity):
        self.vel.add(direction)
        self.vel.add(player_velocity.multiply(0.4))
        self.kick_time = time.time()
        self.kicked = True

    def curve_toward_goal(self):

        target_x = WIDTH - 50 if self.vel.x > 0 else 50
        target_y = HEIGHT // 2

        goal_direction = Vector(target_x - self.pos.x, target_y - self.pos.y)
        goal_direction.normalize()

        curve_intensity = 0.05
        self.vel.add(goal_direction.multiply(curve_intensity))

    def reset(self):
        self.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.vel = Vector(0, 0)
        self.kicked = False
        self.kick_time = None

    def offset_l(self):
        return self.pos.x - self.radius

    def offset_r(self):
        return self.pos.x + self.radius


class Interaction:
    def __init__(self, player_1, player_2, keyboard, ball, left_wall, right_wall):
        self.players = {"player_1": player_1, "player_2": player_2}
        self.keyboard = keyboard
        self.ball = ball
        self.left_wall = left_wall
        self.right_wall = right_wall
        self.score = {"player_1": 0, "player_2": 0}

    def update(self):
        if self.ball.offset_l() <= self.left_wall.pos.x:
            self.score["player_2"] += 1
            self.reset_ball()
            self.reset_char1()
            self.reset_char2()
        elif self.ball.offset_r() >= self.right_wall.pos.x:
            self.score["player_1"] += 1
            self.reset_ball()
            self.reset_char1()
            self.reset_char2()

        if self.score["player_1"] == 3 or self.score["player_2"] == 3:
            self.reset_game()
            return
        self.ball.update()
        for player_name, player in self.players.items():
            if player_name == "player_1":
                controls = self.keyboard.players[player_name]["controls"]
                self.move_player(player, controls, 120, 450, 30, 370)
            else:
                self.move_ai(player)

        if self.is_player_near_ball(player):
            kick_direction = Vector(5, 0) if player_name == 'player_1' else Vector(-5, 0)
            self.ball.kick(kick_direction, player.vel)

    def move_player(self, player, controls, left_limit, right_limit, up_limit, down_limit):
        if controls["right"] and player.pos.x < right_limit:
            player.vel.add(Vector(1, 0))
        if controls["left"] and player.pos.x > left_limit:
            player.vel.subtract(Vector(1, 0))
        if controls["up"] and player.pos.y > up_limit:
            player.vel.subtract(Vector(0, 1))
        if controls["down"] and player.pos.y < down_limit:
            player.vel.add(Vector(0, 1))

    def is_player_near_ball(self, player):
        calculation = (player.pos.get_p()[0] < self.ball.pos.get_p()[0] + self.ball.radius and
                       player.pos.get_p()[0] + 50 > self.ball.pos.get_p()[0] and
                       player.pos.get_p()[1] < self.ball.pos.get_p()[1] + self.ball.radius and
                       player.pos.get_p()[1] + 50 > self.ball.pos.get_p()[1])
        if calculation:
            player.attack()
        return calculation

    def move_ai(self, enemy):
        max_enemy_speed = 7
        base_speed = 3
        reaction_factor = 0.7

        difference = self.ball.pos.y - enemy.pos.y

        enemy_speed = base_speed + abs(self.ball.vel.y) * reaction_factor
        enemy_speed = min(enemy_speed, max_enemy_speed)

        if abs(difference) > enemy_speed:
            enemy.pos.y += enemy_speed * (difference / abs(difference))

    def reset_game(self):
        self.score = {"player_1": 0, "player_2": 0}
        self.reset_ball()
        self.reset_char1()
        self.reset_char2()
        global game_started
        game_started = False

    def reset_ball(self):
        self.ball.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.ball.vel = Vector(0, 0)

    def reset_char1(self):
        self.players["player_1"].pos = Vector(WIDTH / 8, 200)

    def reset_char2(self):
        self.players["player_2"].pos = Vector(WIDTH * 7 / 8, 200)

    def draw(self, canvas):
        canvas.draw_text(f"Player 1: {self.score['player_1']}", (70, 55), 20, "Black", "monospace")
        canvas.draw_text(f"Player 2: {self.score['player_2']}", (WIDTH - 200, 55), 20, "Black", "monospace")
        self.left_wall.draw(canvas)
        self.right_wall.draw(canvas)
        self.ball.draw(canvas)


class Goal:
    def __init__(self, x, y, border, color):
        self.pos = Vector(x, y)
        self.x = x
        self.y = y
        self.border = border
        self.normal = Vector(x, 0)
        self.color = color

    def hit(self, ball):
        if ball.offset_r() >= self.pos.x:
            return True
        elif ball.offset_l() <= self.pos.x + self.width:
            return True
        return False

    def draw(self, canvas):
        canvas.draw_line(
            (self.x, HEIGHT / 4),
            (self.x, HEIGHT * 3 / 4),
            self.border * 2 + 1,
            self.color)


def draw_game(canvas):
    bg_image = simplegui.load_image('https://www.cs.rhul.ac.uk/home/zmac220/cs1822/pitch.png')
    if bg_image.get_width() > 0 and bg_image.get_height() > 0:
        canvas.draw_image(bg_image,
                          (bg_image.get_width() / 2, bg_image.get_height() / 2),
                          (bg_image.get_width(), bg_image.get_height()),
                          (WIDTH / 2, HEIGHT / 2),
                          (WIDTH, HEIGHT))
    inter.update()
    Character.update()
    Character_2.update()
    ball.update()
    inter.draw(canvas)
    Character.draw(canvas)
    Character_2.draw(canvas)
    ball.draw(canvas)
    left_goal.draw(canvas)
    right_goal.draw(canvas)


def start_game(position):
    global game_started

    x, y = position
    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
        game_started = True


def draw(canvas):
    global game_started
    if not game_started:
        welcome_txt = "Welcome to the Football Game!"
        instructions_txt = "click 'Play' to start"
        comment_txt = "first player to score 3 goals wins!"

        canvas.draw_text(welcome_txt, [120, HEIGHT / 4], 45, "White", "monospace")
        canvas.draw_text(comment_txt, [(WIDTH - 500) / 2, 170], 25, "White", "monospace")
        canvas.draw_text(instructions_txt, [(WIDTH - 300) / 2, 270], 25, "White", "monospace")

        canvas.draw_polygon([(button_x, button_y),
                             (button_x + button_width, button_y),
                             (button_x + button_width, button_y + button_height),
                             (button_x, button_y + button_height)],
                            1, "Black", "white")
        canvas.draw_text("Play", [button_x + 20, button_y + 35], 24, "Black", "monospace")
        frame.set_canvas_background("green")
    else:
        draw_game(canvas)


left_goal = Goal(20, 20, 5, "White")
right_goal = Goal(WIDTH - 20, 20, 5, "White")
Character_2 = Character(False)
Character = Character(True)
ball = Ball()
keyboard = Keyboard(Character, Character_2)
inter = Interaction(Character, Character_2, keyboard, ball, left_goal, right_goal)
frame = simplegui.create_frame("Game", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(start_game)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()
