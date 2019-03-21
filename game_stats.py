class GameStats():
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_settings):
        """Initailize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start the game in an inactive state (before pressing play)
        self.game_active = False
    
    def reset_stats(self):
        """Initliaize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
