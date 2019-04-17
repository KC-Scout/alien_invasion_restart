class GameStats():
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_settings):
        """Initailize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        self.high_score = self.retrieve_high_score()
        
        # Start the game in an inactive state (before pressing play)
        self.game_active = False
    
    def reset_stats(self):
        """Initliaize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        
    def retrieve_high_score(self):
        """Retrieve the high score from a json file"""
        try:
            with open("ai_hi_score.txt", "r") as file:
                ai_hi_score = file.read()
        except FileNotFoundError:
            ai_hi_score = 0
            
        return int(ai_hi_score)
        
    def update_high_score(self, score):
        "Update the high score after a new high score has been achieved"
        with open("ai_hi_score.txt", "w") as file:
            file.write(str(score))
            
