class Ball:
    def __init__(self):
        self.pos = Vector(450, 200)
        self.vel = Vector(0, 0)
        self.radius = 15
        self.curving = False
        self.target = None
        self.max_speed = 20
        self.time_in_air = 0
        self.gravity = 0.15
        self.initial_speed_y = -10
        self.initial_speed_x = 15
        self.homing_factor = 0.1
        self.last_kicked_by = None

    def update(self):
        self.pos.add(self.vel)

        if self.curving:
            self.time_in_air += 1
            self.vel.y += self.gravity

        self.homing()

        if self.vel.length() > self.max_speed:
            self.vel.normalize()
            self.vel.multiply(self.max_speed)

        self.vel.multiply(0.97)

        if self.pos.x < 0 or self.pos.x > 900:
            self.reset()

    def reset(self):
        self.pos = Vector(450, 200)
        self.vel = Vector(0, 0)
        self.curving = False
        self.target = None
        self.time_in_air = 0

    def homing(self):
        if self.last_kicked_by == "player_1":
            goal_pos = Vector(900, 200)
        elif self.last_kicked_by == "player_2":
            goal_pos = Vector(0, 200)
        else:
            return

        direction_to_goal = Vector(goal_pos.x - self.pos.x, goal_pos.y - self.pos.y)
        direction_to_goal.normalize()

        self.vel.x += direction_to_goal.x * self.homing_factor
        self.vel.y += direction_to_goal.y * self.homing_factor

    def kick(self, player_name):
        self.last_kicked_by = player_name

        if player_name == "player_1":
            goal_pos = Vector(900, 200)
        else:
            goal_pos = Vector(0, 200)

        direction = Vector(goal_pos.x - self.pos.x, 0)
        direction.normalize()
        direction.multiply(self.initial_speed_x)

        self.vel = direction

        self.vel.y = self.initial_speed_y

        self.vel.multiply(1.5)

        self.curving = True
        self.time_in_air = 0

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 2, "white", "white")


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
                self.ball.kick(player_name)

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
