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

    def update(self, players):
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
        global game_finished, two_player, player_1_won
        if self.ball.offset_l() <= self.left_wall.pos.x:
            self.score["player_2"] += 1
            self.reset_ball("player_1")  
            self.reset_char1()
            self.reset_char2()
        elif self.ball.offset_r() >= self.right_wall.pos.x:
            self.score["player_1"] += 1
            self.reset_ball("player_2") 
            self.reset_char1()
            self.reset_char2()

        
        if self.score["player_1"] == 3:
            self.reset_game()
            game_finished = True
            player_1_won = True
            return
        elif self.score["player_2"] == 3:
            self.reset_game()
            game_finished = True
            return

        
        self.ball.update(list(self.players.values()))
        
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]["controls"]
            if player_name == "player_1":
                self.move_player(player, controls, 120, WIDTH / 2, 30, 370)
            else:
                if two_player:
                    self.move_player(player, controls, WIDTH / 2, WIDTH - 50, 30, 370)
                else:
                    self.move_ai(player)
            
            if self.is_player_near_ball(player):
                if not self.ball.kicked:
                    self.ball.kicked = True  
                kick_direction = Vector(5, 0) if player_name == "player_1" else Vector(-5, 0)
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
        ball_target_x = self.ball.pos.x
        ball_target_y = self.ball.pos.y

        
        if enemy.pos.x > WIDTH / 2:  
            difference_y = ball_target_y - enemy.pos.y  
            if abs(difference_y) > max_enemy_speed:
                direction_y = difference_y / abs(difference_y)  
                enemy.pos.y += direction_y * max_enemy_speed
            else:
                enemy.pos.y += difference_y
            enemy.pos.y = max(30, min(370, enemy.pos.y))


    def reset_game(self):
        self.score = {"player_1": 0, "player_2": 0}
        self.reset_ball("center")
        self.reset_char1()
        self.reset_char2()
        global game_started
        game_started = False

    def reset_ball(self, scored_on_player_name):
        if scored_on_player_name == "player_1":
            self.ball.pos = Vector(self.players["player_1"].pos.x + 50, self.players["player_1"].pos.y)
        elif scored_on_player_name == "player_2":
            self.ball.pos = Vector(self.players["player_2"].pos.x - 50, self.players["player_2"].pos.y)
        elif scored_on_player_name == "center":  
            self.ball.pos = Vector(WIDTH / 2, HEIGHT / 2)

        self.ball.vel = Vector(0, 0)
        self.ball.kicked = False



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


