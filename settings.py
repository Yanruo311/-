class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 99999999999
        self.fleet_drop_speed = 25
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        #1表示向右移动，-1表示向左移动
        self.ship_limit = 3
        self.alien_min_count = 5
        self.alien_max_count = 15
        self.alien_min_speed = 1.0
        self.alien_max_speed = 4.0
        self.alien_spawn_area_top = 50
        self.alien_spawn_area_bottom = 400
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 3.0
        self.bullet_speed = 5.0
        self.alien_speed = 3.0
        self.fleet_direction = 1
        self.alien_points = 50


    def increase_speed(self):
        if self.ship_speed >=6.0:
            self.ship_speed = 6.0
        if self.bullet_speed >= 10:
            self.bullet_speed = 10
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
        print(self.alien_points)
