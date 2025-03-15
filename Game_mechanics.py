import simplegui

CANVAS_WIDTH = 600 #change it to whatever is ok with u
CANVAS_HEIGHT = 400 # change as suited
BALL_RADIUS = 10 #also

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


class Ball:
    def __init__(self, radius):
        self.position = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
        self.velocity = Vector(3, -2)
        self.radius = radius
        self.friction = 0.98
        self.goal_scored = False
        self.goal_time = 0

    def update(self):
        if not self.goal_scored:
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
        if not self.goal_scored:
            canvas.draw_circle(self.position.get_p(), self.radius, 2, "White", "White")
        else:
            self.goal_time -= 1
            if self.goal_time <= 0:
                self.goal_scored = False
                game.reset_positions()

    def check_player_collision(self, player):
        """Checks if ball collides with a player and reflects its velocity"""
        if self.position.distance(player.position) < self.radius + player.radius:
            normal = Vector(self.position.x - player.position.x, self.position.y - player.position.y).normalize()
            self.velocity = self.velocity.reflect(normal)


class Player:
    def __init__(self, position, radius, speed, key_map):
        self.position = position
        self.radius = radius
        self.speed = speed
        self.velocity = Vector(0, 0)
        self.key_map = key_map

    def update(self):
        move_direction = Vector(0, 0)

        if keys[self.key_map["up"]]:
            move_direction.y -= 1
        if keys[self.key_map["down"]]:
            move_direction.y += 1
        if keys[self.key_map["left"]]:
            move_direction.x -= 1
        if keys[self.key_map["right"]]:
            move_direction.x += 1

        move_direction = move_direction.normalize()
        self.velocity = move_direction.multiply(self.speed)
        self.position.add(self.velocity)

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), self.radius, 2, "Blue", "Blue")


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


def update():
    ball.update()
    player1.update()
    player2.update()

    ball.check_player_collision(player1)
    ball.check_player_collision(player2)


def key_down(key):
    if key in keys:
        keys[key] = True


def key_up(key):
    if key in keys:
        keys[key] = False


game = Game()
ball = Ball(BALL_RADIUS)
player1 = Player(Vector(50, CANVAS_HEIGHT / 2), 15, 5, {"up": simplegui.KEY_MAP["w"], "down": simplegui.KEY_MAP["s"],
                                                        "left": simplegui.KEY_MAP["a"], "right": simplegui.KEY_MAP["d"]})
player2 = Player(Vector(CANVAS_WIDTH - 50, CANVAS_HEIGHT / 2), 15, 5, {"up": simplegui.KEY_MAP["up"], "down": simplegui.KEY_MAP["down"],
                                                                      "left": simplegui.KEY_MAP["left"], "right": simplegui.KEY_MAP["right"]})

frame = simplegui.create_frame("Football Game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

# Start game
frame.start()
