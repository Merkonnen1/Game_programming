try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from user304_rsf8mD0BOQ_1 import Vector
import math



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
        self.pos = Vector(100, 225) if is_player_one else Vector(900, 225)
        self.player = {
            "Idle": Spritesheet("https://i.imgur.com/QEGGeXY.png", 1, 6, 2) if is_player_one else Spritesheet("https://i.imgur.com/5F7px4p.png", 1, 6, 2),
            "Run": Spritesheet("https://i.imgur.com/DSTxdb0.png", 1, 8, 2) if is_player_one else Spritesheet("https://i.imgur.com/xY1P0B0.png", 1, 8, 2),
            "Attack": Spritesheet("https://i.imgur.com/ND8Mi41.png", 1, 6, 2) if is_player_one else Spritesheet("https://i.imgur.com/5eD8bnj.png", 1, 6, 2)
        }
        self.current = 'Idle'
        self.current_animation = self.player[self.current]
        self.vel = Vector(0, 0)
        self.frame_count = 0
        self.clock_obj = Clock()

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.75)
        if self.current == "Attack":
            self.frame_count += 1

    def draw(self, canvas):
        if self.current == 'Attack' and self.frame_count >= 6:
            self.current = 'Idle'
            self.frame_count = 0
        self.current_animation = self.player[self.current]
        self.clock_obj.tick()

        centre_x, centre_y = self.current_animation.centres[self.current_animation.current_row][self.current_animation.current_col]
        canvas.draw_image(self.current_animation.image,
                          (centre_x, centre_y),
                          (self.current_animation.frame_width, self.current_animation.frame_height),
                          self.pos.get_p(), (self.current_animation.frame_width, self.current_animation.frame_height))

        if self.clock_obj.transition(self.current_animation.time):
            self.next_frame()

    def next_frame(self):
        self.current_animation.current_col += 1
        if self.current_animation.current_col == self.current_animation.cols:
            self.current_animation.current_col = 0
            self.current_animation.current_row += 1
            if self.current_animation.current_row == self.current_animation.rows:
                self.current_animation.current_row = 0

class Keyboard:
    def __init__(self, player_1, player_2):
        self.players = {
            "player_1": {"instance": player_1, "controls": {"right": False, "left": False, "up": False, "down": False}},
            "player_2": {"instance": player_2, "controls": {"right": False, "left": False, "up": False, "down": False}}
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
                    self.players[player]["instance"].current = 'Run'

    def keyUp(self, key):
        for player, controls in self.key_map.items():
            idle = True
            for action, key_name in controls.items():
                if key == simplegui.KEY_MAP[key_name]:
                    self.players[player]["controls"][action] = False
                if self.players[player]["controls"][action]:
                    idle = False
            if idle:
                self.players[player]["instance"].current = 'Idle'   

class Ball:
    def __init__(self):
        self.pos = Vector(500, 225)
        self.vel = Vector(0, 0)
        self.radius = 15
        self.spots = self.generate_even_spots()

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
        self.pos.add(self.vel)
        self.vel.multiply(0.97)
      
        if self.pos.x - self.radius < 0:  
            self.pos.x = self.radius
            self.vel.x *= -0.7  
            
        if self.pos.x + self.radius > 1000: 
            self.pos.x = 1000 - self.radius
            self.vel.x *= -0.7  
            
        if self.pos.y - self.radius < 0: 
            self.pos.y = self.radius
            self.vel.y *= -0.7 
            
        if self.pos.y + self.radius > 450:  
            self.pos.y = 450 - self.radius
            self.vel.y *= -0.7

        self.rotate_spots()

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "White", "White")
        for spot in self.spots:
            spot_pos = self.pos.copy().add(spot)
            canvas.draw_circle(spot_pos.get_p(), self.radius // 4, 1, "Black", "Black")

    def kick(self, direction, player_velocity):
        self.vel.add(direction)
        self.vel.add(player_velocity.multiply(0.9))  
        self.apply_curve()

    def apply_curve(self):
        if abs(self.vel.get_p()[0]) > 0.5:
            curve_strength = abs(self.vel.get_p()[0]) * 0.4  
            self.vel.add(Vector(0, curve_strength if self.vel.get_p()[0] > 0 else -curve_strength))

    def rotate_spots(self):
        rotation_angle = self.vel.get_p()[0] * 0.05
        for i, spot in enumerate(self.spots):
            x = spot.x
            y = spot.y
            rotated_x = x * math.cos(rotation_angle) - y * math.sin(rotation_angle)
            rotated_y = x * math.sin(rotation_angle) + y * math.cos(rotation_angle)
            self.spots[i] = Vector(rotated_x, rotated_y)
class Interaction:
    def __init__(self, player_1, player_2, keyboard, ball):
        self.players = {"player_1": player_1, "player_2": player_2}
        self.keyboard = keyboard
        self.ball = ball

    def update(self):
        for player_name, player in self.players.items():
            other_player = self.get_other_player(player_name)
            controls = self.keyboard.players[player_name]["controls"]

            self.move_player(player, controls, other_player, 30, 970, 15, 390)

            if self.is_player_near_ball(player):
                kick_direction = self.get_kick_direction(player_name)
                self.ball.kick(kick_direction, player.vel)

    def get_other_player(self, player_name):
        return self.players["player_2"] if player_name == "player_1" else self.players["player_1"]

    def get_kick_direction(self, player_name):
        return Vector(5, 0) if player_name == 'player_1' else Vector(-5, 0)

    def move_player(self, player, controls, other_player, left_limit, right_limit, up_limit, down_limit):
        speed = 3  
        new_pos = player.pos.copy()
        
        if controls["right"] and player.pos.get_p()[0] < right_limit:
            new_pos.add(Vector(speed, 0))
        if controls["left"] and player.pos.get_p()[0] > left_limit:
            new_pos.subtract(Vector(speed, 0))
        if controls["up"] and player.pos.get_p()[1] > up_limit:
            new_pos.subtract(Vector(0, speed))
        if controls["down"] and player.pos.get_p()[1] < down_limit:
            new_pos.add(Vector(0, speed))

        if not self.is_collision(new_pos, other_player.pos):
            player.pos = new_pos

    def is_player_near_ball(self, player):
        buffer = 15 
        return (
            player.pos.get_p()[0] < self.ball.pos.get_p()[0] + self.ball.radius + buffer and
            player.pos.get_p()[0] + 50 > self.ball.pos.get_p()[0] - buffer and
            player.pos.get_p()[1] < self.ball.pos.get_p()[1] + self.ball.radius + buffer and
            player.pos.get_p()[1] + 50 > self.ball.pos.get_p()[1] - buffer
        )

    def is_collision(self, pos1, pos2, buffer=50):
        return (
            abs(pos1.get_p()[0] - pos2.get_p()[0]) < buffer and
            abs(pos1.get_p()[1] - pos2.get_p()[1]) < buffer
        )


Character_2 = Character(False)
Character = Character(True)
ball = Ball()
keyboard = Keyboard(Character, Character_2)
inter = Interaction(Character, Character_2, keyboard, ball)

def draw(canvas):
    inter.update()
    Character.update()
    Character_2.update()
    ball.update()
    Character.draw(canvas)
    Character_2.draw(canvas)
    ball.draw(canvas)

frame = simplegui.create_frame('Game', 1000, 450)
frame.set_canvas_background('green')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()
