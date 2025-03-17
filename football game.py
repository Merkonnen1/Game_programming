import simplegui
import math 

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
BALL_RADIUS = 10

keys = {simplegui.KEY_MAP["w"]: False, simplegui.KEY_MAP["s"]: False,
        simplegui.KEY_MAP["a"]: False, simplegui.KEY_MAP["d"]: False,
        simplegui.KEY_MAP["up"]: False, simplegui.KEY_MAP["down"]: False,
        simplegui.KEY_MAP["left"]: False, simplegui.KEY_MAP["right"]: False}

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def normalize(self):
        mag = (self.x ** 2 + self.y ** 2) ** 0.5
        if mag != 0:
            return Vector(self.x / mag, self.y / mag)
        return Vector(0, 0)

    def reflect(self, normal):
        dot_product = self.x * normal.x + self.y * normal.y
        return Vector(self.x - 2 * dot_product * normal.x, self.y - 2 * dot_product * normal.y)

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def get_p(self):
        return (self.x, self.y)

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
        if self.image_width <= 0 or self.image_height <= 0:
            print(f"Warning: Failed to load image from URL: {url}. Using fallback dimensions.")
            self.image_width = 1
            self.image_height = 1  

        self.frame_width = self.image_width // self.cols
        self.frame_height = self.image_height // self.rows
        self.centres = [[(col * self.frame_width + self.frame_width // 2,
                          row * self.frame_height + self.frame_height // 2)
                         for col in range(self.cols)]
                        for row in range(self.rows)]




    def next_frame(self):
        self.current_col += 1
        if self.current_col == self.cols:
            self.current_col = 0
            self.current_row += 1
            if self.current_row == self.rows:
                self.current_row = 0

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

class Player:
    def __init__(self, position, radius, speed, key_map, sprite_urls):
        self.position = position 
        self.radius = radius      
        self.speed = speed        
        self.velocity = Vector(0, 0) 
        self.key_map = key_map   
        self.sprites = {
            "Idle": Spritesheet(sprite_urls["Idle"], 1, 6, 2),
            "Run": Spritesheet(sprite_urls["Run"], 1, 8, 2),
            "Attack": Spritesheet(sprite_urls["Idle"], 1, 6, 2)  
        }
        self.current = "Idle"  
        self.current_animation = self.sprites[self.current]
        self.clock_obj = Clock()
        self.frame_count = 0

    def update(self):
        self.position.add(self.velocity)
        self.velocity = self.velocity.multiply(0.85)  # Friction factor
        if self.current == "Attack":
            self.frame_count += 1

    def draw(self, canvas):
        if self.current == 'Attack' and self.frame_count >= 6:
            self.current = 'Idle'
            self.frame_count = 0
        self.current_animation = self.sprites[self.current]
        self.clock_obj.tick()

        centre_x, centre_y = self.current_animation.centres[self.current_animation.current_row][
            self.current_animation.current_col]
        canvas.draw_image(self.current_animation.image,
                          (centre_x, centre_y),
                          (self.current_animation.frame_width, self.current_animation.frame_height),
                          self.position.get_p(),
                          (self.current_animation.frame_width, self.current_animation.frame_height))

        if self.clock_obj.transition(self.current_animation.time):
            self.next_frame()

    def next_frame(self):
        self.current_animation.current_col += 1
        if self.current_animation.current_col == self.current_animation.cols:
            self.current_animation.current_col = 0
            self.current_animation.current_row += 1
            if self.current_animation.current_row == self.current_animation.rows:
                self.current_animation.current_row = 0

class Ball:
    def __init__(self, radius):
        self.position = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2) 
        self.velocity = Vector(0, 0) 
        self.radius = radius
        self.friction = 0.98
        self.goal_scored = False
        self.goal_time = 0
        self.moving = False  

    def update(self):
        if self.moving and not self.goal_scored:
            self.position.add(self.velocity)
            self.velocity = self.velocity.multiply(self.friction)

            if self.position.y - self.radius < 0 or self.position.y + self.radius > CANVAS_HEIGHT:
                self.velocity.y *= -1

            if self.position.x - self.radius < 0:
                self.goal_scored = True
                self.goal_time = 180
                game.score_goal(2)
            elif self.position.x + self.radius > CANVAS_WIDTH:
                self.goal_scored = True
                self.goal_time = 180
                game.score_goal(1)

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), self.radius, 2, "White", "White")
        for i in range(5):
            angle = i * 2 * math.pi / 5  
            black_circle = Vector(self.position.x + self.radius * 0.5 * math.cos(angle),
                                self.position.y + self.radius * 0.5 * math.sin(angle))
            canvas.draw_circle(black_circle.get_p(), self.radius * 0.2, 1, "Black", "Black")

        if self.goal_scored:
            self.goal_time -= 1
            if self.goal_time <= 0:
                self.goal_scored = False
                game.reset_positions()

    def check_player_collision(self, player):
        """Checks if the ball collides with a player and reflects its velocity."""
        if self.position.distance(player.position) < self.radius + player.radius:
            normal = Vector(self.position.x - player.position.x, self.position.y - player.position.y).normalize()
            self.velocity = self.velocity.reflect(normal)
            self.moving = True 

class Game:
    def __init__(self):
        self.player1_lives = 3
        self.player2_lives = 3
        self.show_goal_message = False

    def score_goal(self, scorer):
        global ball
        self.show_goal_message = True

        if scorer == 1:
            self.player2_lives -= 1
        else:
            self.player1_lives -= 1

        if self.player1_lives == 0 or self.player2_lives == 0:
            self.end_game()

    def reset_positions(self):
        global ball, player1, player2
        ball = Ball(BALL_RADIUS)
        player1.position = Vector(50, CANVAS_HEIGHT / 2)
        player2.position = Vector(CANVAS_WIDTH - 50, CANVAS_HEIGHT / 2)
        self.show_goal_message = False

    def end_game(self):
        print("Match Ended")

    def update(self):
        
        ball.update()
        player1.update()
        player2.update()
        ball.check_player_collision(player1)
        ball.check_player_collision(player2)

def draw(canvas):
    game.update()
    if game.show_goal_message:
        canvas.draw_text("GOAL!", (CANVAS_WIDTH // 2 - 50, CANVAS_HEIGHT // 2), 50, "Red")
    else:
        ball.draw(canvas)

    player1.draw(canvas)
    player2.draw(canvas)

    canvas.draw_text(f"P1 Lives: {game.player1_lives}", (50, 30), 20, "White")
    canvas.draw_text(f"P2 Lives: {game.player2_lives}", (CANVAS_WIDTH - 150, 30), 20, "White")

def key_down(key):
    if key in keys:
        keys[key] = True

def key_up(key):
    if key in keys:
        keys[key] = False

game = Game()
ball = Ball(BALL_RADIUS)

player1 = Player(
    position=Vector(50, CANVAS_HEIGHT / 2), 
    radius=15, 
    speed=5, 
    key_map={"up": simplegui.KEY_MAP["w"], "down": simplegui.KEY_MAP["s"],
             "left": simplegui.KEY_MAP["a"], "right": simplegui.KEY_MAP["d"]},
    sprite_urls={
        "Idle": "https://i.imgur.com/QEGGeXY.png", 
        "Run": "https://i.imgur.com/DSTxdb0.png", 
        "Attack": "https://i.imgur.com/ND8Mi41.png"  
    }
)

player2 = Player(
    position=Vector(CANVAS_WIDTH - 50, CANVAS_HEIGHT / 2), 
    radius=15, 
    speed=5, 
    key_map={"up": simplegui.KEY_MAP["up"], "down": simplegui.KEY_MAP["down"],
             "left": simplegui.KEY_MAP["left"], "right": simplegui.KEY_MAP["right"]},
    sprite_urls={
        "Idle": "https://i.imgur.com/5F7px4p.png", 
        "Run": "https://i.imgur.com/xY1P0B0.png",  
        "Attack": "https://i.imgur.com/5eD8bnj.png"  
    }
)


frame = simplegui.create_frame("Football Game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

frame.start()
