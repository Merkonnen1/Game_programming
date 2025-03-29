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
        speed = 4  
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
