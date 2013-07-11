# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")

missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")

explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# initialise game
def init():
    global time, started, soundtrack
    time = 0
    started = False
    soundtrack.pause()
    my_ship.set_position([width/2, height/2])
    for rock in list(rock_group):
        rock_group.remove(rock)    

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.is_ship = True
        
#    def is_ship(self):
#        """ method to tell if sprite is ship or not """
#        return self.is_ship
        
    def draw(self,canvas):
        """ draw method for ship """
        img_center = []
        if self.thrust:
            img_center = [self.image_center[0] + 90,self.image_center[1]]
        else:
            img_center = [self.image_center[0], self.image_center[1]]
        canvas.draw_image(self.image, img_center, self.image_size, self.pos, self.image_size, self.angle)

    def update_angle(self, radians):
        """ method to update angular velocity"""
        self.angle_vel = radians 
        
    def set_thrust(self, on):
        """ method to indicate thrusters are on and to play sound """
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def get_position(self):
        """ method to get position """
        return self.pos
    
    def get_radius(self):
        """ method to get radius """
        return self.radius
    
    def set_position(self, new_pos):
        self.pos = new_pos
    
    def shoot(self):
        """ shoot method for ship"""
        global missile_group
        # get forward vector for ship
        forward = angle_to_vector(self.angle)
        # calculate missile possition based on ship position and a multiple of forward vector
        miss_pos = [self.pos[0]+40*forward[0], self.pos[1]+40*forward[1]]
        # calculate missile velocity using ship's velocity and forward vector
        miss_vel = [self.vel[0] + 5*forward[0], self.vel[1] + 5*forward[1]]
        # create a new missile object
        a_missile = Sprite(miss_pos, miss_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)        

        
    def update(self):
        """ Update position, velocity, angle of ship """
        
        # wrap around ship on the screen
        self.pos[0] = self.pos[0]%width
        self.pos[1] = self.pos[1]%height
        
        # update angle based on angular_velocity
        self.angle += self.angle_vel

        # update position based on velocity	
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        #friction update
        if self.thrust:
            self.vel[0] *= (1 - 0.09)
            self.vel[1] *= (1 - 0.09)
        else:
            self.vel[0] *= (1 - 0.02)
            self.vel[1] *= (1 - 0.02)
        
        # get forward vector and increase velocity when thrusters are on
        fwd_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += fwd_vector[0] 
            self.vel[1] += fwd_vector[1] 
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.is_ship = False
        if sound:
            sound.rewind()
            sound.play()
    
#    def is_ship(self):
#        """ method to tell if sprite is ship or not """
#        return self.is_ship
    
    def get_position(self):
        """ method to get position """
        return self.pos
    
    def get_angle(self):
        """ method to get angle """
        return self.angle
    
    def get_radius(self):
        """ method to get radius """
        return self.radius
    
    def get_velocity(self):
        """ method to get radius """
        return self.vel
    
    def collide(self, other_object):
        """ method to detect collision with other_object """
        result = False
        dist_centers = dist(self.pos,other_object.get_position())
        crit_distance = self.radius + other_object.get_radius()
        if dist_centers < crit_distance:
            result = True
        return result
   
    def draw(self, canvas):
        if self.animated:
            anim_pos = [self.image_center[0] + self.age*self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, anim_pos, self.image_size, self.pos, self.image_size)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        """ Update position, angle of sprite """
        # wrap around ship on the screen
        self.pos[0] = self.pos[0]%width
        self.pos[1] = self.pos[1]%height
            
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.age += 1
        result = True
        if self.age >= self.lifespan:
            result = False
        return result

# Helper function to draw rock group        
def process_sprite_group(sprite_group, canvas):
    for sprite in list(sprite_group):
        if not sprite.update():
            sprite_group.remove(sprite)
        sprite.draw(canvas)

# group collide function between ship and rock or missile and rock        
def group_collide(group, a_sprite):
    num_of_collisions = 0
    for member in list(group):
        if member.collide(a_sprite):
            if a_sprite.is_ship:
                explosion_group.add(Sprite(list(member.get_position()), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            else:
                explosion_group.add(Sprite(list(a_sprite.get_position()), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(member)
            num_of_collisions += 1
    return num_of_collisions

# group group collide function between rocks and missiles
def group_group_collide(rocks, missiles):
    num_of_collisions = 0
    for rock in list(rocks):
        if group_collide(missiles, rock):
            rocks.remove(rock)
            num_of_collisions += 1
    return num_of_collisions
           
def draw(canvas):
    global time, lives, score, started
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])

    # draw group helper function
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    #collision 
    num_of_collisions = group_collide(rock_group, my_ship)
    lives = lives - num_of_collisions
    
    # rock missile collisions
    hits = group_group_collide(rock_group, missile_group)
    score += (hits*10)
    
    if lives == 0:
        canvas.draw_text("GAME OVER!!", [300, 50], 25, "Red")
        init()
    
    #draw score and lives
    canvas.draw_text("Lives", [50, 50], 25, "Red")
    canvas.draw_text(str(lives), [50, 75], 25, "Red")
    canvas.draw_text("Score", [650, 50], 25, "Red")
    canvas.draw_text(str(score), [650, 75], 25, "Red")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())
    
def keydown(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.update_angle(0.05)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.update_angle(-0.05)
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.update_angle(0)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.update_angle(0)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, soundtrack, lives, score
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    rock_pos = [random.randrange(0, width), random.randrange(0, height)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if started:
        if len(rock_group) <= 12:
            if dist(rock_pos, my_ship.get_position()) > (my_ship.get_radius() + a_rock.get_radius() + 20):
                rock_group.add(a_rock)
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)

# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
