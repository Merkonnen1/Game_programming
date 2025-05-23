try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from user304_rsf8mD0BOQ_1 import Vector


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
        self.pos = Vector(150, 200) if is_player_one else Vector(750, 200)
        self.player = {
            "Idle": Spritesheet("https://i.imgur.com/QEGGeXY.png", 1, 6, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/5F7px4p.png", 1, 6, 2),
            "Run": Spritesheet("https://i.imgur.com/DSTxdb0.png", 1, 8, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/xY1P0B0.png", 1, 8, 2),
            "Attack": Spritesheet("https://i.imgur.com/ND8Mi41.png", 1, 6, 2) if is_player_one else Spritesheet(
                "https://i.imgur.com/5eD8bnj.png", 1, 6, 2)
        }
        self.current = 'Idle'
        self.current_animation = self.player[self.current]
        self.vel = Vector(0, 0)
        self.frame_count = 0
        self.clock_obj = Clock()

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        if self.current == "Attack":
            self.frame_count += 1

    def draw(self, canvas):
        if self.current == 'Attack' and self.frame_count >= 6:
            self.current = 'Idle'
            self.frame_count = 0
        self.current_animation = self.player[self.current]
        self.clock_obj.tick()

        centre_x, centre_y = self.current_animation.centres[self.current_animation.current_row][
            self.current_animation.current_col]
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
    def __init__(self, goal):
        self.pos = Vector(250, 200)
        self.vel = Vector(0, 0)
        self.radius = 15
        self.target_pos = Vector(0, 100)
        self.radius = 10
        self.hit = False

    def update(self):
        global ball_pos, ball_vel

        direction = self.target_pos - self.pos
        distance = direction.length()

        if distance > 1 and self.hit:
            direction = direction.get_normalized()
            self.vel += direction * 0.05

        self.pos.add(self.vel)

        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > 900:
            self.vel.x = -self.vel.x

        if self.pos.y - self.radius < 0 or self.pos.y + self.radius > 400:
            self.vel.y = -self.vel.y

    def draw(self, canvas):
        self.update()
        canvas.draw_circle(self.pos.get_p(), self.radius, 2, "Red", "Red")

    def kick(self, direction, target_pos):
        self.target_pos = target_pos
        self.hit = True
        self.vel.add(direction)


class Interaction:
    def __init__(self, player_1, player_2, keyboard, ball, goal):
        self.players = {
            "player_1": player_1,
            "player_2": player_2
        }
        self.keyboard = keyboard
        self.ball = ball
        self.goal = goal
        self.kick_power = 2

    def update(self):
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]['controls']
            if player_name == 'player_1':
                if controls["right"] and player.pos.get_p()[0] < 350:
                    player.vel.add(Vector(1, 0))
                if controls["left"] and player.pos.get_p()[0] > 100:
                    player.vel.subtract(Vector(1, 0))
                if controls["up"] and player.pos.get_p()[1] > 70:
                    player.vel.subtract(Vector(0, 1))
                if controls["down"] and player.pos.get_p()[1] < 290:
                    player.vel.add(Vector(0, 1))
            else:
                if controls["right"] and player.pos.get_p()[0] < 800:
                    player.vel.add(Vector(1, 0))
                if controls["left"] and player.pos.get_p()[0] > 550:
                    player.vel.subtract(Vector(1, 0))
                if controls["up"] and player.pos.get_p()[1] > 70:
                    player.vel.subtract(Vector(0, 1))
                if controls["down"] and player.pos.get_p()[1] < 290:
                    player.vel.add(Vector(0, 1))
            print(controls)
            if self.is_player_near_ball(player):
                self.kick_power += 0.5

                if player_name == 'player_1':
                    if controls['down']:
                        self.ball.kick(Vector(self.kick_power, 0), Vector(900, 300))
                    elif controls['up']:
                        self.ball.kick(Vector(self.kick_power, 0), Vector(900, 100))
                    else:
                        self.ball.kick(Vector(self.kick_power, 0), Vector(900, 200))
                else:
                    if controls['down']:
                        self.ball.kick(Vector(-self.kick_power, 0), Vector(0, 300))
                    elif controls['up']:
                        self.ball.kick(Vector(-self.kick_power, 0), Vector(0, 100))
                    else:
                        self.ball.kick(Vector(-self.kick_power, 0), Vector(0, 200))

    def is_player_near_ball(self, player):
        return (player.pos.get_p()[0] < self.ball.pos.get_p()[0] + self.ball.radius and
                player.pos.get_p()[0] + 50 > self.ball.pos.get_p()[0] and
                player.pos.get_p()[1] < self.ball.pos.get_p()[1] + self.ball.radius and
                player.pos.get_p()[1] + 50 > self.ball.pos.get_p()[1])


class Goal:
    def __init__(self, goal_1_start, goal_1_end, goal_2_start, goal_2_end):
        self.goal_1 = [goal_1_start, goal_1_end]
        self.goal_2 = [goal_2_start, goal_2_end]

    def draw(self, canvas):
        canvas.draw_line(self.goal_1[0], self.goal_1[1], 12, 'red')
        canvas.draw_line(self.goal_2[0], self.goal_2[1], 12, 'red')


Character_2 = Character(False)
Character = Character(True)
goal = Goal([0, 100], [0, 300], [900, 100], [900, 300])
ball = Ball(goal)
keyboard = Keyboard(Character, Character_2)
inter = Interaction(Character, Character_2, keyboard, ball, goal)


def draw(canvas):
    inter.update()
    Character.update()
    Character_2.update()
    ball.update()
    Character.draw(canvas)
    Character_2.draw(canvas)
    ball.draw(canvas)
    goal.draw(canvas)


frame = simplegui.create_frame('Game', 900, 400)
frame.set_canvas_background('green')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()
