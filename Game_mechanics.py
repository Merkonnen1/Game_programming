class Ball:
    def __init__(self):
        self.pos = Vector(WIDTH / 2, HEIGHT /2)
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
        self.vel.multiply(0.99)
      
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
        self.apply_curve()
    
    def apply_curve(self):
        if abs(self.vel.x) > 0.5:
            curve_strength = abs(self.vel.x) * 0.4  
            self.vel.add(Vector(0, curve_strength if self.vel.x > 0 else -curve_strength))

    def offset_l(self):
        return self.pos.x - self.radius 
    def offset_r(self):
        return self.pos.x + self.radius
    def bounce(self, normal):
        self.vel.reflect(normal)
        
        
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
            self.ball.bounce(self.left_wall.normal)
            self.reset_ball()
            self.reset_char1()
            self.reset_char2()
        elif self.ball.offset_r() >= self.right_wall.pos.x:
            self.score["player_1"] += 1
            self.ball.bounce(self.right_wall.normal)
            self.reset_ball()
            self.reset_char1()
            self.reset_char2()

        if self.score["player_1"] == 3 or self.score["player_2"] == 3:
            self.reset_game()
            return
        self.ball.update()
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]["controls"]
            self.move_player(player, controls, 40, 940, 30, 370)
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
        return (player.pos.get_p()[0] < self.ball.pos.get_p()[0] + self.ball.radius and 
                player.pos.get_p()[0] + 50 > self.ball.pos.get_p()[0] and 
                player.pos.get_p()[1] < self.ball.pos.get_p()[1] + self.ball.radius and 
                player.pos.get_p()[1] + 50 > self.ball.pos.get_p()[1])

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
