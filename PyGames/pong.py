# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [4,  -2]
paddle1_pos = [0, HEIGHT/2-PAD_HEIGHT/2]
paddle2_pos = [WIDTH, HEIGHT/2-PAD_HEIGHT/2]
paddle1_vel = [0, 0]
paddle2_vel = [WIDTH, 0]
paddle_speed = 10
score1 = 0
score2 = 0


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel_x = -1 * random.randrange(120, 240)
    ball_vel_y = -1 * random.randrange(60, 180)
    ball_vel = [ball_vel_x / 60,  ball_vel_y / 60]
    if right:
        ball_vel[0] = -1 * ball_vel[0]
    pass

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, paddle_speed  # these are floats
    global score1, score2  # these are ints
    ball_init(False)
    paddle1_pos = [0, HEIGHT/2-PAD_HEIGHT/2]
    paddle2_pos = [WIDTH, HEIGHT/2-PAD_HEIGHT/2]
    paddle1_vel = [0, 0]
    paddle2_vel = [WIDTH, 0]
    paddle_speed = 10
    score1 = 0
    score2 = 0
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, player1_score, player2_score
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vel[1] > 0 and paddle1_pos[1] > 0:
        paddle1_pos[1] -= paddle1_vel[1]
    if paddle1_vel[1] < 0 and paddle1_pos[1] < (HEIGHT - PAD_HEIGHT):
        paddle1_pos[1] -= paddle1_vel[1]
    if paddle2_vel[1] > 0 and paddle2_pos[1] > 0:
        paddle2_pos[1] -= paddle2_vel[1]
    if paddle2_vel[1] < 0 and paddle2_pos[1] < (HEIGHT - PAD_HEIGHT):
        paddle2_pos[1] -= paddle2_vel[1]
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line(paddle1_pos, (paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT), 17, "White")
    c.draw_line(paddle2_pos, (paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT), 17, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off left paddle, 
    # increase velocity after each successful hit
    # if ball misses paddle, other player score increases
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1] >= paddle1_pos[1]) and (ball_pos[1] <= (paddle1_pos[1]+PAD_HEIGHT)):
            ball_vel[0] = - (ball_vel[0] * 1.1)
        else:
            ball_init(True)
            score2 += 1            
    
    # collide and reflect off right paddle, 
    # increase velocity after each successful hit
    # if ball misses paddle, other player score increases
    if ball_pos[0] >= (WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH):
        if (ball_pos[1] >= paddle2_pos[1]) and (ball_pos[1] <= (paddle2_pos[1]+PAD_HEIGHT)):
            ball_vel[0] = - (ball_vel[0] * 1.1)
        else:
            ball_init(False)
            score1 += 1

    # collide and reflect off top side of canvas    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # collide and reflect off bottom side of canvas
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1] 
        
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text(str(score1), (WIDTH / 4, HEIGHT/4), 40, "White")
    c.draw_text(str(score2), ((WIDTH / 2)+(WIDTH / 4), HEIGHT/4), 40, "White")
    
# capture w, s for moving left paddle and up and down key for moving right paddle         
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle_speed
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = paddle_speed
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = -1 * paddle_speed
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = paddle_speed
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = -1 * paddle_speed
        
# keyup on w, s, up and down should stop moving the paddles   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
     


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()

