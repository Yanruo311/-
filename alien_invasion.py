import sys
from time import sleep
import pygame
import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlenInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 使用窗口模式（更稳定）
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # 发射控制
        self.firing = False
        self.fire_counter = 0
        self.fire_interval = 15  # 每15帧发射一次

        # 创建外星人
        self._create_random_fleet()

        self.game_active = False
        self.play_button = Button(self, 'Play')

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

                # 持续发射子弹（有间隔）
                if self.firing:
                    self.fire_counter += 1
                    if self.fire_counter >= self.fire_interval:
                        self._fire_bullet()
                        self.fire_counter = 0

            self._update_screen()
            self.clock.tick(60)

    def _create_random_fleet(self):
        """创建随机分布的外星人舰队"""
        self.aliens.empty()

        alien_count = random.randint(8, 15)
        alien_width, alien_height = 0, 0
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        min_distance = 60

        for i in range(alien_count):
            alien = Alien(self)
            if i == 0:
                alien_width, alien_height = alien.rect.size

            max_attempts = 50
            for _ in range(max_attempts):
                alien.rect.x = random.randint(20, screen_width - alien_width - 20)
                alien.rect.y = random.randint(50, screen_height // 2)

                overlap = False
                for existing in self.aliens.sprites():
                    dx = alien.rect.x - existing.rect.x
                    dy = alien.rect.y - existing.rect.y
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    if distance < min_distance:
                        overlap = True
                        break

                if not overlap:
                    break

            alien.speed = random.uniform(0.5, 1.5)
            alien.x = float(alien.rect.x)
            alien.y = float(alien.rect.y)

            self.aliens.add(alien)
    def _update_aliens(self):
        """更新外星人位置"""
        # 检查边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

        # 更新位置
        for alien in self.aliens.sprites():
            alien.x += alien.speed * self.settings.fleet_direction
            alien.rect.x = int(alien.x)

            # 持续向下移动
            alien.y += 0.3
            alien.rect.y = int(alien.y)

            # 随机波动
            if random.random() < 0.03:
                alien.y += random.uniform(-2, 2)
                alien.rect.y = int(alien.y)

        # 检查碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查底部
        self._check_aliens_bottom()

    def _change_fleet_direction(self):
        """改变舰队方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            alien.y = float(alien.rect.y)
            # 随机调整速度
            alien.speed = random.uniform(0.5, 1.5)

        self.settings.fleet_direction *= -1

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    self.stats.save_high_score()
                except:
                    pass
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 重置游戏状态
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的外星人
            self._create_random_fleet()
            self.ship.center_ship()

            # 隐藏鼠标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            try:
                self.stats.save_high_score()
            except:
                pass
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.firing = True
            # 立即发射第一发
            self._fire_bullet()
            self.fire_counter = self.fire_interval

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            self.firing = False

    def _fire_bullet(self):
        """发射子弹 - 无限制"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_random_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _ship_hit(self):
        """处理飞船被撞"""
        if self.stats.ships_left > 0:
            # 减少生命
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空屏幕
            self.bullets.empty()
            self.aliens.empty()

            # 重新开始
            self._create_random_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlenInvasion()
    ai.run_game()