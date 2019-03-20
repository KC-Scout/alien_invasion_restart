
class Settings():
    """Define the settings for alien invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3 
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
        
        self.alien_speed_factor = 50
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        
        
