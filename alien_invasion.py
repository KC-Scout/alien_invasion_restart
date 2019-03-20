from settings import Settings
import pygame
from pygame.sprite import Group
from ship import Ship
import game_functions as gf
from game_stats import GameStats

def run_game():
    """ Initialize game and create a screen object."""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height )
            ) # Returns Surface
    
    # Make a ship, a group of aliens and a group of bullets
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    # Create an instance of game statistics
    stats = GameStats(ai_settings)
    
    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    pygame.display.set_caption("Alien Invasion")

    # Start the main loop of the game:
    while True:
        
        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        gf.update_aliens(ai_settings, ship, screen, stats, aliens, bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        
        


run_game()

