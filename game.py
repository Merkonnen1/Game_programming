try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from user304_rsf8mD0BOQ_1 import Vector
class Spritesheet:
    def __init__(self, url, rows, cols,time):
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
        self.centres = [[(col * self.frame_width + self.frame_width//2,
                          row * self.frame_height + self.frame_height//2)
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
class Character:
    def __init__(self, boolean):
        if boolean:
            self.pos = Vector(150, 200)
            self.player = {
                "Idle": Spritesheet("https://i.imgur.com/QEGGeXY.pngg", 1, 6, 2),
                "Run": Spritesheet("https://i.imgur.com/DSTxdb0.png", 1, 8, 2),
                "Attack": Spritesheet("https://i.imgur.com/ND8Mi41.png", 1, 6, 2)}
        else:
            self.player = {
                "Idle": Spritesheet("https://i.imgur.com/5F7px4p.png", 1, 6, 2),
                "Run": Spritesheet("https://i.imgur.com/xY1P0B0.png", 1, 8, 2),
                "Attack": Spritesheet("https://i.imgur.com/5eD8bnj.png", 1, 6, 2)}
            self.pos = Vector(750, 200)
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

class Keyboard:
    def __init__(self, player_1, player_2):
        self.players = {
            "player_1": {"instance": player_1, "right": False, "left": False, "up": False, "down": False},
            "player_2": {"instance": player_2, "right": False, "left": False, "up": False, "down": False}
        }
        self.key_map = {
            "player_1": {"right": "d", "left": "a", "up": "w", "down": "s"},
            "player_2": {"right": "right", "left": "left", "up": "up", "down": "down"}
        }

    def keyDown(self, key):
        for player, controls in self.key_map.items():
            for action, key_name in controls.items():
                if key == simplegui.KEY_MAP[key_name]:
                    self.players[player][action] = True
                    self.players[player]["instance"].current = 'Run'
    def keyUp(self, key):
        for player, controls in self.key_map.items():
            idle = True
            for action, key_name in controls.items():
                if key == simplegui.KEY_MAP[key_name]:
                    self.players[player][action] = False
                if self.players[player][action] == True:
                    idle=False
            if idle:
                self.players[player]["instance"].current = 'Idle'

class Interaction:
    def __init__(self, player_1, player_2, keyboard):
        self.players = {
            "player_1": player_1,
            "player_2": player_2
        }
        self.keyboard = keyboard

    def update(self):
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]
            if player_name=='player_1':
                if controls["right"] and player.pos.get_p()[0]<350:
                    player.vel.add(Vector(1, 0))
                if controls["left"] and player.pos.get_p()[0]>100:
                    player.vel.subtract(Vector(1, 0))
                if controls["up"] and player.pos.get_p()[1]>70:
                    player.vel.subtract(Vector(0, 1))
                if controls["down"] and player.pos.get_p()[1]<290:
                    player.vel.add(Vector(0, 1))
            else:
                if controls["right"] and player.pos.get_p()[0]<800:
                    player.vel.add(Vector(1, 0))
                if controls["left"] and player.pos.get_p()[0]>550:
                    player.vel.subtract(Vector(1, 0))
                if controls["up"] and player.pos.get_p()[1]>70:
                    player.vel.subtract(Vector(0, 1))
                if controls["down"] and player.pos.get_p()[1]<290:
                    player.vel.add(Vector(0, 1))
Character_2 = Character(False)
Character = Character(True)
keyboard = Keyboard(Character,Character_2)
inter = Interaction(Character,Character_2,keyboard)
def draw(canvas):
    inter.update()
    Character.update()
    Character_2.update()
    Character.draw(canvas)
    Character_2.draw(canvas)
frame = simplegui.create_frame('Game',900,400)
frame.set_canvas_background('blue')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()
