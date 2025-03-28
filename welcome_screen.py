import simplegui

WIDTH = 1000
HEIGHT = 450
game_started = False
button_x = WIDTH / 2 - 50
button_y = HEIGHT * 2 / 3
button_width = 100
button_height = 50

def start_game(position):
    global game_started
    x, y = position
    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
        game_started = True
        print("Game Started!")
        frame.set_canvas_background("lightgreen")

def draw(canvas):
    if not game_started:
        welcome_text = "Welcome to the Football Game!"
        instructions_text = "Click 'Play' to start"

        title_x = (WIDTH - frame.get_canvas_textwidth(welcome_text, 36)) / 2
        instructions_x = (WIDTH - frame.get_canvas_textwidth(instructions_text, 24)) / 2

        title_y = HEIGHT / 4
        instructions_y = title_y + 70

        canvas.draw_text(welcome_text, [title_x, title_y], 36, "White", "monospace")
        canvas.draw_text(instructions_text, [instructions_x, instructions_y], 24, "White", "monospace")
        
        canvas.draw_polygon([(button_x, button_y), 
                             (button_x + button_width, button_y), 
                             (button_x + button_width, button_y + button_height), 
                             (button_x, button_y + button_height)], 
                            1, "Black", "white")
        canvas.draw_text("Play", [button_x + 20, button_y + 30], 24, "Black", "monospace")
        frame.set_canvas_background("green")
    else:
        # ADD ACTUAL GAME HERE
        canvas.draw_text("Game is running...", [150, 100], 36, "Black")

frame = simplegui.create_frame("Welcome Screen", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(start_game)
frame.start()
