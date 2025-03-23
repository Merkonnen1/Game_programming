class Ball:
    def __init__(self):
        self.pos = Vector(450, 200)
        self.vel = Vector(0, 0)
        self.radius = 15
    
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.97)  
        
        if self.pos.x - self.radius < 0:  
            self.pos.x = self.radius
            self.vel.x *= -0.8 
            
        if self.pos.x + self.radius > 900:  
            self.pos.x = 900 - self.radius
            self.vel.x *= -0.8  
            
        if self.pos.y - self.radius < 0: 
            self.pos.y = self.radius
            self.vel.y *= -0.8  
            
        if self.pos.y + self.radius > 400:  
            self.pos.y = 400 - self.radius
            self.vel.y *= -0.8  

        
    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, "White", "White")
    
    def kick(self, direction, player_velocity):
        self.vel.add(direction.multiply(0.4))
        self.vel.add(player_velocity.multiply(0.3))  
        self.apply_curve()

    
    def apply_curve(self):
        if abs(self.vel.get_p()[0]) > 0.5:
            curve_strength = abs(self.vel.get_p()[0]) * 0.4  
            self.vel.add(Vector(0, curve_strength if self.vel.get_p()[0] > 0 else -curve_strength))

class Interaction:
    def __init__(self, player_1, player_2, keyboard, ball):
        self.players = {"player_1": player_1, "player_2": player_2}
        self.keyboard = keyboard
        self.ball = ball
    
    def update(self):
        for player_name, player in self.players.items():
            controls = self.keyboard.players[player_name]["controls"]
            self.move_player(player, controls, 50, 860, 35, 320)
            
            if self.is_player_near_ball(player):
                kick_direction = Vector(5, 0) if player_name == 'player_1' else Vector(-5, 0)
                self.ball.kick(kick_direction, player.vel)
    
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
