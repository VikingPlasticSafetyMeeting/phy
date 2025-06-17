import pygame
import random
import math
import sys
import os
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon World Explorer")

# Load fonts
title_font = pygame.font.Font(None, 60)
dialog_font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 28)

# Create a directory for our assets
if not os.path.exists('assets'):
    os.makedirs('assets')

# Create game assets programmatically
def create_assets():
    # Create player sprite
    player_img = pygame.Surface((40, 60), pygame.SRCALPHA)
    pygame.draw.rect(player_img, (50, 150, 200), (5, 0, 30, 40))
    pygame.draw.circle(player_img, (250, 200, 150), (20, 15), 8)
    pygame.draw.rect(player_img, (80, 180, 80), (0, 40, 40, 20))
    pygame.image.save(player_img, 'assets/player.png')
    
    # Create NPC sprites
    npc_colors = [(200, 50, 50), (50, 200, 50), (200, 50, 200), (200, 200, 50)]
    for i, color in enumerate(npc_colors):
        npc_img = pygame.Surface((40, 60), pygame.SRCALPHA)
        pygame.draw.rect(npc_img, color, (5, 0, 30, 40))
        pygame.draw.circle(npc_img, (250, 200, 150), (20, 15), 8)
        pygame.draw.rect(npc_img, (100, 100, 200), (0, 40, 40, 20))
        pygame.image.save(npc_img, f'assets/npc_{i}.png')
    
    # Create Pokémon sprites
    pokemon_data = [
        ("Pikachu", (255, 215, 0), (255, 165, 0)),
        ("Bulbasaur", (50, 205, 50), (144, 238, 144)),
        ("Charmander", (255, 69, 0), (255, 165, 0)),
        ("Squirtle", (30, 144, 255), (135, 206, 250)),
        ("Jigglypuff", (255, 182, 193), (255, 105, 180)),
        ("Geodude", (160, 82, 45), (205, 133, 63)),
    ]
    
    for name, color1, color2 in pokemon_data:
        pokemon_img = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(pokemon_img, color1, (30, 30), 25)
        pygame.draw.circle(pokemon_img, color2, (30, 30), 20)
        
        # Draw eyes
        pygame.draw.circle(pokemon_img, (0, 0, 0), (20, 25), 5)
        pygame.draw.circle(pokemon_img, (0, 0, 0), (40, 25), 5)
        
        # Draw mouth
        pygame.draw.arc(pokemon_img, (0, 0, 0), (15, 20, 30, 30), 0, math.pi, 3)
        
        pygame.image.save(pokemon_img, f'assets/{name.lower()}.png')
    
    # Create gym sprite
    gym_img = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.rect(gym_img, (200, 30, 30), (0, 0, 80, 80))
    pygame.draw.rect(gym_img, (240, 200, 30), (10, 10, 60, 60))
    pygame.draw.circle(gym_img, (30, 30, 200), (40, 40), 20)
    pygame.draw.circle(gym_img, (200, 200, 255), (40, 40), 15)
    pygame.image.save(gym_img, 'assets/gym.png')
    
    # Create grass tile
    grass_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(grass_img, (34, 139, 34), (0, 0, 50, 50))
    for _ in range(20):
        x, y = random.randint(0, 50), random.randint(0, 50)
        pygame.draw.line(grass_img, (0, 100, 0), (x, y), (x, y-10), 2)
    pygame.image.save(grass_img, 'assets/grass.png')
    
    # Create water tile
    water_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(water_img, (30, 144, 255), (0, 0, 50, 50))
    for _ in range(15):
        x, y = random.randint(0, 50), random.randint(0, 50)
        pygame.draw.arc(water_img, (135, 206, 250), (x, y, 15, 10), 0, math.pi, 2)
    pygame.image.save(water_img, 'assets/water.png')
    
    # Create path tile
    path_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(path_img, (210, 180, 140), (0, 0, 50, 50))
    pygame.draw.rect(path_img, (180, 150, 110), (0, 0, 50, 50), 3)
    pygame.image.save(path_img, 'assets/path.png')
    
    # Create tree sprite
    tree_img = pygame.Surface((50, 70), pygame.SRCALPHA)
    pygame.draw.rect(tree_img, (139, 69, 19), (20, 30, 10, 40))
    pygame.draw.circle(tree_img, (0, 100, 0), (25, 20), 25)
    pygame.draw.circle(tree_img, (34, 139, 34), (25, 20), 20)
    pygame.image.save(tree_img, 'assets/tree.png')

# Create assets if they don't exist
if not os.path.exists('assets/player.png'):
    create_assets()

# Load assets
def load_image(name):
    return pygame.image.load(f'assets/{name}').convert_alpha()

player_img = load_image('player.png')
npc_imgs = [load_image(f'npc_{i}.png') for i in range(4)]
gym_img = load_image('gym.png')
grass_img = load_image('grass.png')
water_img = load_image('water.png')
path_img = load_image('path.png')
tree_img = load_image('tree.png')

pokemon_imgs = {
    'pikachu': load_image('pikachu.png'),
    'bulbasaur': load_image('bulbasaur.png'),
    'charmander': load_image('charmander.png'),
    'squirtle': load_image('squirtle.png'),
    'jigglypuff': load_image('jigglypuff.png'),
    'geodude': load_image('geodude.png'),
}

# Game states
WORLD_MAP = 0
DIALOG = 1
BATTLE = 2
MENU = 3
GYM_BATTLE = 4

# Game classes
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = 0  # 0: down, 1: up, 2: left, 3: right
        self.pokemon = [
            {'name': 'Pikachu', 'type': 'Electric', 'level': 12, 'hp': 45, 'max_hp': 45, 'img': 'pikachu'},
            {'name': 'Bulbasaur', 'type': 'Grass', 'level': 10, 'hp': 42, 'max_hp': 42, 'img': 'bulbasaur'},
            {'name': 'Charmander', 'type': 'Fire', 'level': 11, 'hp': 39, 'max_hp': 39, 'img': 'charmander'}
        ]
        self.active_pokemon = 0
        self.badges = 0
        self.pokedex = 15
        self.money = 1750

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check boundaries
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            # Check collision with obstacles (trees, water, etc.)
            tile_x, tile_y = int(new_x // 50), int(new_y // 50)
            if world.map[tile_y][tile_x] in ['.', '~']:
                self.x = new_x
                self.y = new_y
                
                # Set direction for animation
                if dx > 0:
                    self.direction = 3
                elif dx < 0:
                    self.direction = 2
                elif dy > 0:
                    self.direction = 0
                elif dy < 0:
                    self.direction = 1
                
                # Check for wild Pokémon encounter in grass
                if world.map[tile_y][tile_x] == '~' and random.random() < 0.01:
                    return True
        return False

    def draw(self, screen, camera_x, camera_y):
        screen.blit(player_img, (self.x - camera_x, self.y - camera_y))
        
        # Draw direction indicator
        indicator_color = (255, 0, 0)
        indicator_pos = [(self.x - camera_x + 20, self.y - camera_y + 60),
                         (self.x - camera_x + 20, self.y - camera_y - 10),
                         (self.x - camera_x - 10, self.y - camera_y + 20),
                         (self.x - camera_x + 50, self.y - camera_y + 20)]
        pygame.draw.circle(screen, indicator_color, indicator_pos[self.direction], 5)

class NPC:
    def __init__(self, x, y, name, dialogues):
        self.x = x
        self.y = y
        self.name = name
        self.dialogues = dialogues
        self.img = random.choice(npc_imgs)
        self.walk_timer = 0
        self.direction = random.randint(0, 3)
        self.walking = False

    def update(self):
        # NPC random movement
        self.walk_timer += 1
        if self.walk_timer > 120:
            self.walking = not self.walking
            if self.walking:
                self.direction = random.randint(0, 3)
            self.walk_timer = 0
            
        if self.walking:
            speed = 2
            if self.direction == 0:  # Down
                self.y += speed
            elif self.direction == 1:  # Up
                self.y -= speed
            elif self.direction == 2:  # Left
                self.x -= speed
            elif self.direction == 3:  # Right
                self.x += speed
                
            # Boundary check
            self.x = max(50, min(950, self.x))
            self.y = max(50, min(650, self.y))

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))
        
        # Draw name tag
        name_surf = small_font.render(self.name, True, (255, 255, 0))
        screen.blit(name_surf, (self.x - camera_x - name_surf.get_width()//2 + 20, 
                              self.y - camera_y - 30))

class World:
    def __init__(self):
        self.width = 2000
        self.height = 2000
        self.map = self.generate_map()
        self.gyms = [
            (300, 250, "Brock", "Rock"),
            (1500, 300, "Misty", "Water"),
            (400, 1600, "Lt. Surge", "Electric"),
            (1700, 1700, "Erika", "Grass")
        ]
        self.npcs = [
            NPC(500, 400, "Youngster Joey", [
                "My Rattata is in the top percentage of Rattata!",
                "I've been training since I was 4 years old.",
                "Have you collected any gym badges yet?",
                "Legend says there's a rare Pokémon in the forest!"
            ]),
            NPC(1200, 600, "Lass Emily", [
                "I love cute Pokémon! What's your favorite?",
                "The water gym leader is really tough. Bring grass types!",
                "If you see my Jigglypuff, please let me know.",
                "I heard Team Rocket is causing trouble near the power plant."
            ]),
            NPC(800, 1500, "Poké Prof", [
                "Hello, trainer! How is your Pokédex coming along?",
                "Remember to catch Pokémon to complete your Pokédex!",
                "Different Pokémon appear in different areas.",
                "Strong trainers have a balanced team of different types."
            ]),
            NPC(1600, 800, "Hiker Bob", [
                "I've been climbing mountains for 40 years!",
                "Rock-type Pokémon are the toughest, I tell ya!",
                "I once saw a giant Onix deep in this mountain.",
                "Always carry potions when exploring caves!"
            ])
        ]
        
    def generate_map(self):
        # Create a base map (grass everywhere)
        game_map = [['~' for _ in range(self.width // 50)] for _ in range(self.height // 50)]
        
        # Add paths
        for i in range(10, 30):
            game_map[i][15] = '.'
            game_map[i][16] = '.'
            
        for i in range(15, 25):
            game_map[20][i] = '.'
            game_map[21][i] = '.'
            
        # Add water areas
        for i in range(5, 15):
            for j in range(5, 15):
                game_map[i][j] = 'w'
                
        for i in range(25, 35):
            for j in range(25, 35):
                game_map[i][j] = 'w'
        
        # Add trees
        for _ in range(100):
            x = random.randint(0, (self.width // 50) - 1)
            y = random.randint(0, (self.height // 50) - 1)
            if game_map[y][x] == '~':
                game_map[y][x] = 'T'
                
        return game_map
    
    def draw(self, screen, camera_x, camera_y):
        # Draw tiles
        start_x = max(0, int(camera_x // 50))
        end_x = min(self.width // 50, int((camera_x + SCREEN_WIDTH) // 50) + 1)
        start_y = max(0, int(camera_y // 50))
        end_y = min(self.height // 50, int((camera_y + SCREEN_HEIGHT) // 50) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_x = x * 50
                tile_y = y * 50
                
                if self.map[y][x] == '~':
                    screen.blit(grass_img, (tile_x - camera_x, tile_y - camera_y))
                elif self.map[y][x] == '.':
                    screen.blit(path_img, (tile_x - camera_x, tile_y - camera_y))
                elif self.map[y][x] == 'w':
                    screen.blit(water_img, (tile_x - camera_x, tile_y - camera_y))
                elif self.map[y][x] == 'T':
                    screen.blit(grass_img, (tile_x - camera_x, tile_y - camera_y))
                    screen.blit(tree_img, (tile_x - camera_x, tile_y - camera_y - 20))
        
        # Draw gyms
        for gym in self.gyms:
            x, y, _, _ = gym
            screen.blit(gym_img, (x - camera_x, y - camera_y))
            
            # Draw gym name
            gym_name = small_font.render(f"{gym[2]}'s Gym", True, (255, 215, 0))
            screen.blit(gym_name, (x - camera_x - gym_name.get_width()//2 + 40, 
                                  y - camera_y - 30))
        
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(screen, camera_x, camera_y)

class Battle:
    def __init__(self, player, opponent_pokemon=None, is_gym=False):
        self.player = player
        self.is_gym = is_gym
        self.state = "SELECT_ACTION"
        
        if opponent_pokemon:
            self.opponent = opponent_pokemon
        else:
            # Random wild Pokémon
            wild_pokemon = random.choice([
                {'name': 'Pikachu', 'type': 'Electric', 'level': random.randint(5, 10), 'hp': 35, 'max_hp': 35, 'img': 'pikachu'},
                {'name': 'Bulbasaur', 'type': 'Grass', 'level': random.randint(5, 10), 'hp': 32, 'max_hp': 32, 'img': 'bulbasaur'},
                {'name': 'Charmander', 'type': 'Fire', 'level': random.randint(5, 10), 'hp': 30, 'max_hp': 30, 'img': 'charmander'},
                {'name': 'Squirtle', 'type': 'Water', 'level': random.randint(5, 10), 'hp': 33, 'max_hp': 33, 'img': 'squirtle'},
                {'name': 'Jigglypuff', 'type': 'Normal', 'level': random.randint(5, 10), 'hp': 40, 'max_hp': 40, 'img': 'jigglypuff'},
                {'name': 'Geodude', 'type': 'Rock', 'level': random.randint(5, 10), 'hp': 28, 'max_hp': 28, 'img': 'geodude'},
            ])
            self.opponent = wild_pokemon.copy()
            self.opponent['hp'] = self.opponent['max_hp']
        
        self.message = f"Wild {self.opponent['name']} appeared!" if not is_gym else f"Gym Leader sent out {self.opponent['name']}!"
        self.message_timer = 0
        self.player_action = None
        self.opponent_action = None
        
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
            return
            
        if self.state == "SELECT_ACTION":
            return
            
        elif self.state == "PLAYER_ACTION":
            # Resolve player action
            player_pokemon = self.player.pokemon[self.player.active_pokemon]
            
            if self.player_action == "FIGHT":
                damage = random.randint(10, 20)
                self.opponent['hp'] = max(0, self.opponent['hp'] - damage)
                self.message = f"{player_pokemon['name']} used Tackle! It dealt {damage} damage!"
                
            elif self.player_action == "POKEMON":
                self.state = "SELECT_POKEMON"
                return
                
            elif self.player_action == "ITEM":
                self.message = "You used a Potion!"
                player_pokemon['hp'] = min(player_pokemon['max_hp'], player_pokemon['hp'] + 20)
                
            elif self.player_action == "RUN":
                self.message = "Got away safely!"
                self.message_timer = 60
                return "END_BATTLE"
            
            self.state = "OPPONENT_ACTION"
            self.player_action = None
            
        elif self.state == "OPPONENT_ACTION":
            # Opponent's turn
            player_pokemon = self.player.pokemon[self.player.active_pokemon]
            
            # 20% chance to use special move
            if random.random() < 0.2:
                damage = random.randint(15, 25)
                move_name = "Hyper Beam" if not self.is_gym else "Gym Special"
            else:
                damage = random.randint(8, 15)
                move_name = "Scratch"
                
            player_pokemon['hp'] = max(0, player_pokemon['hp'] - damage)
            self.message = f"Opponent's {self.opponent['name']} used {move_name}! It dealt {damage} damage!"
            
            self.state = "SELECT_ACTION"
            self.opponent_action = None
            
        # Check for battle end
        if player_pokemon['hp'] <= 0:
            self.message = f"{player_pokemon['name']} fainted!"
            self.message_timer = 60
            return "LOSE"
            
        if self.opponent['hp'] <= 0:
            if self.is_gym:
                self.message = "You defeated the Gym Leader! You earned a badge!"
                self.player.badges += 1
            else:
                self.message = f"You defeated the wild {self.opponent['name']}!"
                
            self.message_timer = 60
            return "WIN"
            
        return None
            
    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, (70, 130, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (50, 50, 50), (0, 400, SCREEN_WIDTH, 300))
        
        # Draw opponent Pokémon
        opponent_img = pokemon_imgs.get(self.opponent['img'].lower(), None)
        if opponent_img:
            screen.blit(pygame.transform.scale(opponent_img, (200, 200)), (600, 150))
        
        # Draw player Pokémon
        player_pokemon = self.player.pokemon[self.player.active_pokemon]
        player_img = pokemon_imgs.get(player_pokemon['img'].lower(), None)
        if player_img:
            screen.blit(pygame.transform.scale(player_img, (200, 200)), (200, 250))
        
        # Draw health bars
        # Opponent health
        pygame.draw.rect(screen, (100, 100, 100), (450, 100, 300, 30))
        health_width = 300 * self.opponent['hp'] / self.opponent['max_hp']
        pygame.draw.rect(screen, (220, 60, 60), (450, 100, health_width, 30))
        pygame.draw.rect(screen, (200, 200, 200), (450, 100, 300, 30), 2)
        opponent_text = small_font.render(f"{self.opponent['name']} Lv.{self.opponent['level']}", True, (255, 255, 255))
        screen.blit(opponent_text, (455, 75))
        
        # Player health
        pygame.draw.rect(screen, (100, 100, 100), (50, 350, 300, 30))
        health_width = 300 * player_pokemon['hp'] / player_pokemon['max_hp']
        pygame.draw.rect(screen, (60, 220, 60), (50, 350, health_width, 30))
        pygame.draw.rect(screen, (200, 200, 200), (50, 350, 300, 30), 2)
        player_text = small_font.render(f"{player_pokemon['name']} Lv.{player_pokemon['level']}", True, (255, 255, 255))
        screen.blit(player_text, (55, 325))
        hp_text = small_font.render(f"HP: {player_pokemon['hp']}/{player_pokemon['max_hp']}", True, (255, 255, 255))
        screen.blit(hp_text, (55, 385))
        
        # Draw message box
        pygame.draw.rect(screen, (30, 30, 50), (50, 450, 900, 150))
        pygame.draw.rect(screen, (100, 100, 150), (50, 450, 900, 150), 3)
        message_text = dialog_font.render(self.message, True, (255, 255, 255))
        screen.blit(message_text, (70, 480))
        
        # Draw action menu
        if self.state == "SELECT_ACTION":
            pygame.draw.rect(screen, (80, 80, 120), (550, 450, 400, 150))
            pygame.draw.rect(screen, (150, 150, 200), (550, 450, 400, 150), 3)
            
            actions = ["FIGHT", "POKEMON", "ITEM", "RUN"]
            for i, action in enumerate(actions):
                action_text = menu_font.render(action, True, (255, 255, 255))
                x = 570 + (i % 2) * 180
                y = 470 + (i // 2) * 60
                screen.blit(action_text, (x, y))
                
        elif self.state == "SELECT_POKEMON":
            pygame.draw.rect(screen, (80, 80, 120), (50, 450, 900, 150))
            pygame.draw.rect(screen, (150, 150, 200), (50, 450, 900, 150), 3)
            
            title = menu_font.render("Choose a Pokémon:", True, (255, 255, 255))
            screen.blit(title, (70, 470))
            
            for i, pokemon in enumerate(self.player.pokemon):
                status = "FNT" if pokemon['hp'] <= 0 else f"HP: {pokemon['hp']}/{pokemon['max_hp']}"
                color = (200, 60, 60) if pokemon['hp'] <= 0 else (255, 255, 255)
                pokemon_text = small_font.render(f"{i+1}. {pokemon['name']} ({status})", True, color)
                screen.blit(pokemon_text, (70, 510 + i * 30))

# Main game class
class PokemonGame:
    def __init__(self):
        self.world = World()
        self.player = Player(500, 500)
        self.camera_x = 0
        self.camera_y = 0
        self.game_state = WORLD_MAP
        self.current_dialog = None
        self.battle = None
        self.current_gym = None
        
        # For dialog system
        self.dialog_index = 0
        self.dialog_timer = 0
        
        # Create a simple title screen image
        self.title_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_screen.fill((30, 50, 100))
        pygame.draw.rect(self.title_screen, (70, 130, 180), (100, 100, SCREEN_WIDTH-200, SCREEN_HEIGHT-200))
        title = title_font.render("Pokémon World Explorer", True, (255, 215, 0))
        subtitle = menu_font.render("Press SPACE to start your adventure!", True, (255, 255, 255))
        self.title_screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
        self.title_screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 300))
        
        # Draw Pokémon on title screen
        for i, name in enumerate(['pikachu', 'bulbasaur', 'charmander', 'squirtle']):
            img = pokemon_imgs[name]
            self.title_screen.blit(img, (200 + i*150, 400))
        
        self.show_title = True
    
    def update_camera(self):
        # Center camera on player
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        
        # Clamp camera to world boundaries
        self.camera_x = max(0, min(self.camera_x, self.world.width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.world.height - SCREEN_HEIGHT))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            if self.show_title:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.show_title = False
                continue
                
            if event.type == KEYDOWN:
                if self.game_state == WORLD_MAP:
                    if event.key == K_m:
                        self.game_state = MENU
                
                elif self.game_state == DIALOG:
                    if event.key == K_SPACE:
                        self.dialog_index += 1
                        if self.dialog_index >= len(self.current_dialog):
                            self.game_state = WORLD_MAP
                            self.current_dialog = None
                
                elif self.game_state == BATTLE or self.game_state == GYM_BATTLE:
                    if self.battle.state == "SELECT_ACTION":
                        if event.key == K_1:
                            self.battle.player_action = "FIGHT"
                            self.battle.state = "PLAYER_ACTION"
                        elif event.key == K_2:
                            self.battle.player_action = "POKEMON"
                            self.battle.state = "PLAYER_ACTION"
                        elif event.key == K_3:
                            self.battle.player_action = "ITEM"
                            self.battle.state = "PLAYER_ACTION"
                        elif event.key == K_4:
                            self.battle.player_action = "RUN"
                            self.battle.state = "PLAYER_ACTION"
                    
                    elif self.battle.state == "SELECT_POKEMON":
                        if event.key == K_1:
                            self.player.active_pokemon = 0
                            self.battle.state = "SELECT_ACTION"
                        elif event.key == K_2:
                            self.player.active_pokemon = 1
                            self.battle.state = "SELECT_ACTION"
                        elif event.key == K_3:
                            self.player.active_pokemon = 2
                            self.battle.state = "SELECT_ACTION"
                        elif event.key == K_ESCAPE:
                            self.battle.state = "SELECT_ACTION"
                
                elif self.game_state == MENU:
                    if event.key == K_ESCAPE or event.key == K_m:
                        self.game_state = WORLD_MAP
        
        return True
    
    def update(self):
        if self.show_title:
            return
        
        # Update NPCs
        for npc in self.world.npcs:
            npc.update()
        
        if self.game_state == WORLD_MAP:
            # Handle player movement
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[K_UP] or keys[K_w]:
                dy = -self.player.speed
            if keys[K_DOWN] or keys[K_s]:
                dy = self.player.speed
            if keys[K_LEFT] or keys[K_a]:
                dx = -self.player.speed
            if keys[K_RIGHT] or keys[K_d]:
                dx = self.player.speed
                
            if dx != 0 or dy != 0:
                encounter = self.player.move(dx, dy, self.world)
                if encounter:
                    self.battle = Battle(self.player)
                    self.game_state = BATTLE
                    
                self.update_camera()
                
            # Check for NPC interaction
            if keys[K_SPACE]:
                for npc in self.world.npcs:
                    distance = math.sqrt((npc.x - self.player.x)**2 + (npc.y - self.player.y)**2)
                    if distance < 60:
                        self.current_dialog = npc.dialogues
                        self.dialog_index = 0
                        self.game_state = DIALOG
                        break
                        
                # Check for gym interaction
                for gym in self.world.gyms:
                    x, y, name, _ = gym
                    distance = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
                    if distance < 80:
                        self.current_gym = gym
                        self.battle = Battle(
                            self.player, 
                            {'name': 'Geodude', 'type': 'Rock', 'level': 15, 'hp': 50, 'max_hp': 50, 'img': 'geodude'},
                            True
                        )
                        self.game_state = GYM_BATTLE
                        break
                        
        elif self.game_state in [BATTLE, GYM_BATTLE]:
            result = self.battle.update()
            if result == "END_BATTLE" or result == "WIN" or result == "LOSE":
                if self.battle.message_timer <= 0:
                    self.game_state = WORLD_MAP
                    self.battle = None
    
    def draw(self):
        if self.show_title:
            screen.blit(self.title_screen, (0, 0))
            pygame.display.flip()
            return
            
        # Draw world
        screen.fill((100, 100, 150))
        self.world.draw(screen, self.camera_x, self.camera_y)
        self.player.draw(screen, self.camera_x, self.camera_y)
        
        # Draw HUD
        pygame.draw.rect(screen, (30, 30, 50, 200), (10, 10, 250, 80))
        pygame.draw.rect(screen, (100, 100, 150), (10, 10, 250, 80), 3)
        
        name_text = small_font.render(f"Trainer: Ash", True, (255, 255, 255))
        badge_text = small_font.render(f"Badges: {self.player.badges}/8", True, (255, 255, 255))
        money_text = small_font.render(f"Money: ₽{self.player.money}", True, (255, 255, 255))
        
        screen.blit(name_text, (20, 20))
        screen.blit(badge_text, (20, 45))
        screen.blit(money_text, (20, 70))
        
        # Draw controls info
        controls = small_font.render("SPACE: Interact | M: Menu | Arrow Keys: Move", True, (200, 200, 255))
        screen.blit(controls, (SCREEN_WIDTH - controls.get_width() - 20, SCREEN_HEIGHT - 30))
        
        # Draw dialog if active
        if self.game_state == DIALOG:
            pygame.draw.rect(screen, (30, 30, 50), (100, 500, 800, 150))
            pygame.draw.rect(screen, (100, 100, 150), (100, 500, 800, 150), 3)
            
            dialog_text = dialog_font.render(self.current_dialog[self.dialog_index], True, (255, 255, 255))
            screen.blit(dialog_text, (120, 530))
            
            prompt = small_font.render("Press SPACE to continue", True, (200, 200, 255))
            screen.blit(prompt, (120, 580))
        
        # Draw battle if active
        elif self.game_state in [BATTLE, GYM_BATTLE]:
            self.battle.draw(screen)
            
        # Draw menu
        elif self.game_state == MENU:
            pygame.draw.rect(screen, (30, 30, 50, 200), (200, 100, 600, 500))
            pygame.draw.rect(screen, (100, 100, 150), (200, 100, 600, 500), 3)
            
            title = title_font.render("Pokémon Menu", True, (255, 215, 0))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 130))
            
            # Draw player Pokémon
            pygame.draw.rect(screen, (50, 50, 80), (230, 200, 540, 250))
            pygame.draw.rect(screen, (100, 100, 150), (230, 200, 540, 250), 2)
            
            for i, pokemon in enumerate(self.player.pokemon):
                img = pokemon_imgs.get(pokemon['img'].lower())
                if img:
                    screen.blit(pygame.transform.scale(img, (80, 80)), (250, 220 + i*80))
                
                status = f"HP: {pokemon['hp']}/{pokemon['max_hp']}"
                color = (200, 60, 60) if pokemon['hp'] <= 0 else (255, 255, 255)
                pokemon_text = menu_font.render(f"{pokemon['name']} Lv.{pokemon['level']} ({status})", True, color)
                screen.blit(pokemon_text, (350, 240 + i*80))
            
            # Draw badges
            badge_title = menu_font.render("Gym Badges:", True, (255, 255, 255))
            screen.blit(badge_title, (250, 470))
            
            for i in range(8):
                color = (255, 215, 0) if i < self.player.badges else (100, 100, 100)
                pygame.draw.circle(screen, color, (450 + i*40, 500), 15)
                pygame.draw.circle(screen, (200, 200, 200), (450 + i*40, 500), 15, 2)
                badge_text = small_font.render(str(i+1), True, (30, 30, 50))
                screen.blit(badge_text, (450 + i*40 - badge_text.get_width()//2, 500 - badge_text.get_height()//2))
            
            prompt = small_font.render("Press ESC to return", True, (200, 200, 255))
            screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 550))
        
        pygame.display.flip()

# Main game loop
def main():
    game = PokemonGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()