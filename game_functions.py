import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_key_down_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit hsa not been reached yet."""
    # Create a new bullet and add it to the bullets group
    # No more than 3 bullets at a time bc of ai_settings limits
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def check_key_up_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False



def check_events(ai_settings, screen, stats, play_button, ship, aliens,
    bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, 
                ship, aliens, bullets, mouse_x, mouse_y)
            
        elif event.type == pygame.KEYDOWN: 
            check_key_down_events(event, ai_settings, screen, ship, 
                bullets)
                
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)
            
def check_play_button(ai_settings, screen, stats, play_button, ship, 
    aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # Reset game statistics
        stats.reset_stats()
        stats.game_active = True
        
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
                
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, 
        play_button):
    """Update images on the screen and flip to the new scren."""
    screen.fill(ai_settings.bg_color) # Fill is a method of Surface object
    # Redraw all bullets behind ship and aliens. 
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Draw a play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    # Make the most recently drawn screen visible       
    pygame.display.flip()
    
    
    
def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
    """"Check if a bullet has hit an alien"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
    
def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update the position of bullets and get rid of old bullets."""
    bullets.update()
        
    # Get rid of bullets that have disappeared. 
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows that can fit on the screen"""
    available_space = (ai_settings.screen_height - (3 * alien_height) - 
        ship_height)
    number_rows = available_space / (2 * alien_height)
    return int(number_rows)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that can fit in a row"""
    available_space_x = (ai_settings.screen_width - (2 * alien_width))
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return int(number_aliens_x)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
        
def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)    
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
        alien.rect.height)
    
    # Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
            row_number)
    
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
            
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ships being hit by alien."""
    
    if stats.ships_left > 0:
        # Decrement ships left 
        stats.ships_left -= 1
        
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Pause
        sleep(0.5)
        print(stats.ships_left)
    else:
        stats.game_active = False
    
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            if stats.ships_left > 0:
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                break
                print(stats.ships_left)
            else:
                stats.game_active = False
            
def update_aliens(ai_settings, ship, screen, stats, aliens, bullets):
    """
    Check if the fleet is at an edge, and then update the positions
    of all of the aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    
        

        
        
        
