# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player = None
dealer = None
deck = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        result = ''
        for card in self.hand:
            result += str(card) + ','
        return result

    def add_card(self, card):
        self.hand.append(card)
        
    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        for card in self.hand:
            #print card.get_rank(), VALUES[card.get_rank()]
            if card.get_suit() == 'A':
                value += 1
                if (value + 10) <= 21:
                    value += 10
            else:
                value += VALUES[card.get_rank()]
        return value
            

    def busted(self):
        pass	# replace with your code
    
    def draw(self, canvas, p):
        pass	# replace with your code
 
        
# define deck class
class Deck:
    def __init__(self):
        self.deck = []

    # add cards back to deck and shuffle
    def shuffle(self):
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        result = ''
        for card in self.deck:
            result += str(card) + ','
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck

    print ""
    print "Fresh Deal"
    deck.shuffle()
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    print "Player: ", str(player), " Value: ", player.get_value()
    print "Dealer: ", str(dealer), " Value: ", dealer.get_value()
    
    in_play = True

def hit():
    global in_play
    print
    print "Player hit"
 
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card()) 
    
    # if busted, assign an message to outcome, update in_play and score
    
    print "Player: ", str(player), " Value: ", player.get_value()
    print "Dealer: ", str(dealer), " Value: ", dealer.get_value()
       
def stand():
    pass	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deck = Deck()
deal()

# get things rolling
frame.start()


# remember to review the gradic rubric