from designer import *
from random import *
from math import *

Ship = {
    'image': DesignerObject,
    'velocity': float,
    'rotation_velocity': int,
    'acceleration': float,
    'lives': int
    }

def make_ship (file: str) -> Ship:
    '''
    Initiates the ship to load with the following
    keys when created in the make_world function.
    '''
    
    return {'image': image(file, 400, 450),
            'velocity': 0.0,
            'rotation_velocity': 0,
            'acceleration': 0.0,
            'lives': 999
            }

'''
Rather than give an asteroid random integers for their x and y coordinates within the
window (e.g. randint(0, get_width()), the y position is dependent updon the randomized
x position. This should make it so that an asteroid will not spawn directly upon the
space ship and only come from the window borders.
'''
    
def set_y_pos (x: int) -> int:
    '''
    Returns a y value dependent upon the x value
    so that an asteroid will only spawn only the borders of the window.
    '''

    if x > 1 and x < get_width()-1:
        random_chance = randint(1,2)
        if random_chance == 1:
            return 1
        else:
            return get_height()-1
    else:
        return randint(1, get_height()-1)
    
Asteroid = {
    'body': DesignerObject,
    'velocity': int,
    'set_angle': int,
    'size': int
    }

def make_asteroid (asteroid_size: int, x_pos, y_pos) -> Asteroid:
    '''
    Creates an asteroid object with the following keys.
    '''
    
    return {'body': rectangle('brown', set_asteroid_scale(asteroid_size), set_asteroid_scale(asteroid_size), x_pos, y_pos),
            'velocity': randint(1,4),
            'set_angle': randint(0,350),
            'size': asteroid_size
            }

def set_asteroid_scale (asteroid_size: int) -> int:
    if asteroid_size == 3:
        return 60
    elif asteroid_size == 2:
        return 40
    elif asteroid_size == 1:
        return 20

Missile = {
    'body': DesignerObject,
    'velocity': int,
    'fixed_angle': float,
    'timer': float
    }

def make_missile (x_pos: float, y_pos: float, ship_angle: float) -> Missile:
    '''
    Creates a missile with the follow keys.
    '''
    
    return {'body': rectangle('black', 5, 20, x_pos, y_pos),
            'velocity': 13,
            'fixed_angle': ship_angle,
            'timer': 0
            }

Item = {
    'image': DesignerObject,
    'velocity': int,
    'set_angle': float
    }

def make_item () -> Item:
    '''
    Creates an item with the following keys.
    '''
    
    return {'image': image("item"+str(randint(0,2))+".png", randint(0, get_width()), randint(0, get_height())),
            'velocity': 1,
            'set_angle': randint(0,360)
            }

World = {
    'ship': Ship,
    'timer': float,
    'message': str,
    'instructions': str,
    'score': int,
    'asteroids': [Asteroid],
    'missiles': [Missile],
    'items': [Item]
    }
    
def make_world() -> World:
    '''
    Initiates the basic world instance.
    '''
    
    return {
        'ship': make_ship('ship.png'),
        'asteroids': [],
        'timer': 0.0,
        'score': 0,
        'message': text('black', ''),
        'instructions': text('black', ''),
        'missiles': [],
        'items': []
        }

def move_ship (w: World):
    '''
    Triangulates the ships position based on it's angle and
    continously moves the ship based on its velocity.
    '''
    
    w['ship']['velocity'] += w['ship']['acceleration']    
    w['ship']['image']['x'] += (w['ship']['velocity']*sin(radians(w['ship']['image']['angle'])))
    w['ship']['image']['y'] += (w['ship']['velocity']*cos(radians(w['ship']['image']['angle'])))
    
ACCELERATION = 0.25

def accelerate_ship (w: World, key: str):
    '''
    Sets ship acceleration to the acceleration
    global constant.
    '''
    
    if key == 'up':
        w['ship']['acceleration'] = ACCELERATION
  
def release_acceleration (w: World, key: str):
    '''
    Acceleration of the ship is stopped when the 'up'
    key is released.
    '''
    
    if key == 'up':
        w['ship']['acceleration'] = 0
  
DECELERATION =  0.07

def decelerate_ship (w: World):
    '''
    Function will continously decelerate the ship
    by deceleration global constant value
    every update where the ship is greater than 0.
    '''
    
    if w['ship']['velocity'] > 0:
        w['ship']['velocity'] -= DECELERATION
        
    if w['ship']['velocity'] < 0:
        w['ship']['velocity'] = 0
    
def limit_ship_speed (w: World):
    '''
    Prohibits the ship from accelerating past a
    velocity of 8.
    '''
    
    if w['ship']['velocity'] >= 8:
        w['ship']['velocity'] = 8

def rotate_ship (w: World, key: str):
    '''
    Rotiation velocity of the ship is set according to
    the key pressed.
    '''
    
    if key == 'left':
        w['ship']['rotation_velocity'] = 8
    elif key == 'right':
        w['ship']['rotation_velocity'] = -8
        
def release_rotation (w: World, key: str):
    '''
    Rotation velocity is set to 0 as soon as the
    key is released.
    '''
    
    if key == 'left':
        w['ship']['rotation_velocity'] = 0
    elif key == 'right':
        w['ship']['rotation_velocity'] = 0
      
def ship_rotation_handler (w: World):
    '''
    Angle of the ship is continuously rotated based on the
    rotation velocity determined by user key input.
    '''
    
    w['ship']['image']['angle'] += w['ship']['rotation_velocity']    

def move_asteroids (w: World):
    '''
    Gives each asteroid movement based on their assigned
    random velocities and angles.
    '''
    
    for asteroid in w['asteroids']:
        asteroid['body']['x'] += (asteroid['velocity']*cos(radians(asteroid['body']['angle'])))
        asteroid['body']['y'] += (asteroid['velocity']*sin(radians(asteroid['body']['angle'])))
        
def make_asteroid_list (w: World):
    '''
    Makes sure there are only ever a certain amount of large asteroids
    on screen at the same time. Also creates them based on a 5% chance each update.
    '''
    not_max_asteroids = len(w['asteroids']) < 5
    random_chance = randint(1, 20) == 20
    if not_max_asteroids and random_chance:
        x = randint(0, 365)
        w['asteroids'].append(make_asteroid(3, x, set_y_pos(x))) 
        
def move_items (w: World):
    '''
    Allows items to move freely based on their assigned angle.
    '''
    
    for item in w['items']:
        item['image']['x'] += (item['velocity']*cos(radians(item['image']['angle'])))
        item['image']['y'] += (item['velocity']*sin(radians(item['image']['angle'])))
   
def set_item_angle (w: World):
    '''
    Sets each item to have it's own angle.
    '''
    
    for item in w['items']:
        item['image']['angle'] = item['set_angle']

def make_item_list (w: World):
    '''
    Makes sure there are only ever a max of 3 items
    on screen at the same time. Also creates them based on a 2% chance each update.
    '''
    
    not_max_items = len(w['items']) < 3
    random_chance = randint(1, 50) == 2
    if not_max_items and random_chance:
        w['items'].append(make_item())
    
def set_asteroid_angle (w: World):
    '''
    Sets each asteroid to have their own randomized angle.
    '''
    
    for asteroid in w['asteroids']:
        asteroid['body']['angle'] = asteroid['set_angle']

def collide_ship_asteroid (w: World):
    '''
    Asteroids are destroyed upon collision with the ship, while
    the ship is reset (instructed by TAs to not destroy ship).
    '''
    
    destroyed_asteroids = []
    
    for asteroid in w['asteroids']:
        if colliding(w['ship']['image'], asteroid['body']) and asteroid['size'] == 3:
            destroyed_asteroids.append(asteroid)
            reset_ship(w)
            w['asteroids'].append(make_asteroid(2, asteroid['body']['x'], asteroid['body']['y']))
            w['asteroids'].append(make_asteroid(2, asteroid['body']['x'], asteroid['body']['y']))
            
        elif colliding(w['ship']['image'], asteroid['body']) and asteroid['size'] == 2:
            destroyed_asteroids.append(asteroid)
            reset_ship(w)
            w['asteroids'].append(make_asteroid(1, asteroid['body']['x'], asteroid['body']['y']))
            w['asteroids'].append(make_asteroid(1, asteroid['body']['x'], asteroid['body']['y']))
            
        elif colliding(w['ship']['image'], asteroid['body']) and asteroid['size'] == 1:
            destroyed_asteroids.append(asteroid)
            reset_ship(w)
    w['asteroids'] = filter_from(w['asteroids'], destroyed_asteroids)
    
def collide_missile_asteroid (w: World):
    '''
    Missile collides with a small asteroid and both are destroyed; player
    gets points.
    '''
    
    destroyed_asteroids = []
    destroyed_missiles = []
    for asteroid in w['asteroids']:
        for missile in w['missiles']:
            if colliding(missile['body'], asteroid['body']) and asteroid['size'] == 3:
                destroyed_asteroids.append(asteroid)
                destroyed_missiles.append(missile)
                w['asteroids'].append(make_asteroid(2, asteroid['body']['x'], asteroid['body']['y']))
                w['asteroids'].append(make_asteroid(2, asteroid['body']['x'], asteroid['body']['y']))
                
            elif colliding(missile['body'], asteroid['body']) and asteroid['size'] == 2:
                destroyed_asteroids.append(asteroid)
                destroyed_missiles.append(missile)
                w['asteroids'].append(make_asteroid(1, asteroid['body']['x'], asteroid['body']['y']))
                w['asteroids'].append(make_asteroid(1, asteroid['body']['x'], asteroid['body']['y']))
                
            elif colliding(missile['body'], asteroid['body']) and asteroid['size'] == 1:
                destroyed_asteroids.append(asteroid)
                destroyed_missiles.append(missile)
                w['score'] += 50
    w['asteroids'] = filter_from(w['asteroids'], destroyed_asteroids)            
    w['missiles'] = filter_from(w['missiles'], destroyed_missiles)

def collide_ship_item (w: World):
    '''
    When the ship touches an item, the item is destroyed
    and the player's score increases.
    '''
    
    destroyed_items = []
    for item in w['items']:
        if colliding(w['ship']['image'], item['image']):
            destroyed_items.append(item)
            w['score'] += 25
    w['items'] = filter_from(w['items'], destroyed_items)
                
def reset_ship (w: World):
    '''
    Ship will not actually be deleted (as instructed by TAs), but reset and a live
    will be lost upon collision with asteroid.
    '''
    
    w['ship']['image']['x'] = 400
    w['ship']['image']['y'] = 450
    w['ship']['velocity'] = 0
    w['ship']['rotation_velocity'] = 0
    w['ship']['lives'] -= 1

def filter_from(old_list: list, elements_to_not_keep: list) -> list:
    '''
    Helper function which checks if an element in a given list
    is not already in a certain list. Filters these elements
    into a new list.
    '''
    
    new_values = []
    for item in old_list:
        if item not in elements_to_not_keep:
            new_values.append(item)
    return new_values

def shoot_missile (w: World, key: str):
    '''
    When the space key is pressed, a missile is generated
    at the ship's coordinates and faces the angle in which
    the ship is facing.
    '''
    
    if key == 'space':
        w['missiles'].append(make_missile(w['ship']['image']['x'], w['ship']['image']['y'], w['ship']['image']['angle']))

def delete_missile (w: World):
    '''
    A missile is deleted two seconds after being
    shot.
    '''
    
    destroyed_missiles = []
    for missile in w['missiles']:
        if round(missile['timer']) == 2:
            destroyed_missiles.append(missile)
    w['missiles'] = filter_from(w['missiles'], destroyed_missiles) 
 
def missile_update_timer (w: World):
    '''
    Adds 1/30 to an individual missile's timer every update, where 30 updates
    equal one second, thus giving a timer in seconds.
    '''
    
    for missile in w['missiles']:
        missile['timer'] += 1/30 
        
def set_missile_angle (w: World):
    '''
    Makes it so that the missile's angle does not continuously
    update according to the ship's angle after it is created.
    '''
    
    for missile in w['missiles']:
        missile['body']['angle'] = missile['fixed_angle']

def move_missile (w: World):
    '''
    Gives the missiles movement based on their
    angle and velocity (constant).
    '''
    
    for missile in w['missiles']:
        missile['body']['x'] += (missile['velocity']*sin(radians(missile['body']['angle'])))
        missile['body']['y'] += (missile['velocity']*cos(radians(missile['body']['angle'])))

def wrap_around_ship (w: World):
    '''
    Makes the ship wrap around the screen and appear
    on the opposite side should it be flown out of
    view. Works for both height and width of the screen.
    '''
    
    if w['ship']['image']['x'] >= get_width():
        w['ship']['image']['x'] %= get_width()
        
    if w['ship']['image']['y'] >= get_height():
        w['ship']['image']['y'] %= get_height()
        
    if w['ship']['image']['y'] <= get_height():
        w['ship']['image']['y'] %= get_height()
        
    if w['ship']['image']['x'] <= get_width():
        w['ship']['image']['x'] %= get_width()
        
def wrap_around_object (objects: [dict], body: str):
    '''
    Auxillary function allowing a list of objects
    to wrap around the screen.
    '''
    
    for an_object in objects:
        if an_object[body]['x'] >= get_width():
            an_object[body]['x'] %= get_width()
        
        if an_object[body]['y'] >= get_height():
            an_object[body]['y'] %= get_height()
        
        if an_object[body]['y'] <= get_height():
            an_object[body]['y'] %= get_height()
        
        if an_object[body]['x'] <= get_width():
            an_object[body]['x'] %= get_width()
            
def wrap_around(w: World):
    '''
    Calls the wrap_around_objects function in order
    to allow the following list of objects to wrap around
    the screen.
    '''
    
    wrap_around_object(w['asteroids'], 'body')
    wrap_around_object(w['missiles'], 'body')
    wrap_around_object(w['items'], 'image')
    
def update_timer (w: World):
    '''
    Adds 1/30 to the timer every update, where 30 updates
    equal one second, thus giving a timer in seconds.
    '''
    
    w['timer'] += 1/30
    
def check_no_lives (w: World) -> bool:
    '''
    Checks if the user has run out of lives.
    '''
    
    return w['ship']['lives'] == 0

def flash_game_over (w: World):
    '''
    Displays the final game over message.
    '''
    
    w['message']['text'] = ("FINAL SCORE: " + str(w['score']),
                            "You survived for " + str(round(w['timer'])) + " seconds!")
    
def show_instructions (w: World):
    '''
    Displays instructions on how to control the ship at the top
    of the screen.
    '''
    
    w['instructions']['text'] = "'up' to accelerate ship; arrow keys to rotate; 'space' to shoot"
    w['instructions']['y'] = 10
    
def show_general_message (w: World):
    '''
    Primitive UI which displays lives remaining, score, time elapsed,
    and current speed of the ship.
    '''
    
    w['message']['text'] = ("Lives: " + str(w['ship']['lives']),
                            "Score: " + str(w['score']),
                            "Time: " + str(round(w['timer'])),
                            "Speed: " + str(round(w['ship']['velocity'])))
    w['message']['y'] = 30
    
    
when('starting', make_world)

when('updating', update_timer, show_general_message, show_instructions, wrap_around) # General world handlers

when('updating', move_ship, ship_rotation_handler, wrap_around_ship, decelerate_ship, limit_ship_speed) # Ship handlers

when('updating', make_asteroid_list, move_asteroids, set_asteroid_angle) # Asteroid handlers

when('updating', move_missile, set_missile_angle, delete_missile, missile_update_timer) # Missile handlers

when('updating', move_items, make_item_list, set_item_angle) # Item Handlers

when('updating', collide_ship_asteroid, collide_missile_asteroid, collide_ship_item) # Collision handlers

when('typing', rotate_ship, accelerate_ship, shoot_missile) # Typing Handlers

when('done typing', release_rotation, release_acceleration) # Release Key Handlers

when(check_no_lives, flash_game_over, pause) # Game Over handlers

start()