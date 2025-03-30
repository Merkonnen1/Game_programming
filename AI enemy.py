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
            if player_name == "player_1":  # Keep player_1 as a human
                controls = self.keyboard.players[player_name]["controls"]
                self.move_player(player, controls, 40, 940, 30, 370)
            else:
                self.move_ai(player)
                
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
        
    def move_ai(self, enemy):
        max_enemy_speed = 7
        base_speed = 3
        reaction_factor = 0.7
    
        difference = self.ball.pos.y - enemy.pos.y

        enemy_speed = base_speed + abs(self.ball.vel.y) * reaction_factor
        enemy_speed = min(enemy_speed, max_enemy_speed)

        if abs(difference) > enemy_speed:
            enemy.pos.y += enemy_speed * (difference / abs(difference))  


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
