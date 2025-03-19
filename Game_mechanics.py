class Ball:
    def __init__(self):
        self.pos = Vector(450, 200)
        self.vel = Vector(0, 0)
        self.radius = 15

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.9) 

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "White", "White")

    def kick(self, direction):
        self.vel.add(direction)

class Interaction:
    def __init__(self, player_1, player_2, keyboard, ball):
        self.players = {
            "player_1": player_1,
            "player_2": player_2
        }
        self.keyboard = keyboard
        self.ball = ball

    def update(self):
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]["controls"]
            self.move_player(player, controls, 70, 820, 70, 300)

            if self.is_player_near_ball(player):
                kick_direction = Vector(5, 0) if player_name == 'player_1' else Vector(-5, 0)
                self.ball.kick(kick_direction)

    def move_player(self, player, controls, left_limit, right_limit, up_limit, down_limit):
        if controls["right"] and player.pos.get_p()[0] < right_limit:
            player.vel.add(Vector(1, 0))
        if controls["left"] and player.pos.get_p()[0] > left_limit:
            player.vel.subtract(Vector(1, 0))
        if controls["up"] and player.pos.get_p()[1] > up_limit:
            player.vel.subtract(Vector(0, 1))
        if controls["down"] and player.pos.get_p()[1] < down_limit:
            player.vel.add(Vector(0, 1))

    def is_player_near_ball(self, player):
        return (player.pos.get_p()[0] < self.ball.pos.get_p()[0] + self.ball.radius and
                player.pos.get_p()[0] + 50 > self.ball.pos.get_p()[0] and
                player.pos.get_p()[1] < self.ball.pos.get_p()[1] + self.ball.radius and
                player.pos.get_p()[1] + 50 > self.ball.pos.get_p()[1])

Character_2 = Character(False)
Character = Character(True)
ball = Ball()
keyboard = Keyboard(Character, Character_2)
inter = Interaction(Character, Character_2, keyboard, ball)
