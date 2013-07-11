# implementation of card game - Memory

import simplegui
import random
import math

close_cards = False

# helper function to initialize globals
def init():
    global cards, exposed, click_count, state
    click_count = 0
    l.set_text("Moves = " + str(click_count))
    state = 0
    cards = [i//2 for i in range(16)]
    random.shuffle(cards)
    exposed = [False for i in range(16)]
    close_cards = False

     
# define event handlers
# mouse click is where all the logic of the game is happening
def mouseclick(pos):
    global exposed, click_count, state, prev_card, prev_loc, curr_card, curr_loc, prev_state, close_cards
    card_clicked = pos[0] // 50
            
    if exposed[card_clicked] == False:
        if state == 0:
            prev_state = state
            state = 1
        elif state == 1:
            prev_state = state
            state = 2
        else:
            prev_state = state
            state = 1
        
        #print "State:", state
        exposed[card_clicked] = True
        click_count += 1
        l.set_text("Moves = " + str(click_count))
       
        if state == 1:
            if close_cards:
                exposed[curr_loc] = False
                exposed[prev_loc] = False
            prev_card = cards[card_clicked]
            prev_loc = card_clicked
    
        if state == 2:
            curr_card = cards[card_clicked]
            curr_loc = card_clicked
            if not curr_card == prev_card:
                close_cards = True
            else:
                close_cards = False
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = [12, 75]
    pt1 = 0
    pt2 = 50
    card_pos = 0
    for card in cards:
        if exposed[card_pos]:
            canvas.draw_text(str(card), pos, 50, "White")
        else:
            canvas.draw_polygon([(pt1,0), (pt2, 0), (pt2, 100), (pt1, 100)], 2, "Red", "Green")
        card_pos += 1
        pos[0] += 50
        pt1 += 50
        pt2 += 50
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

# Always remember to review the grading rubric