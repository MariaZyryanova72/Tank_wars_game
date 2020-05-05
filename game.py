# coding=utf-8
import time

from sprites import *
from os import *
import sys
from image import load_image


def show_energy_bar(energy):
    color = 2.55 * energy

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -1 * energy))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110), 2)


def show_shooting_bar(shooting):  # Шкала лазеров
    color = 5.1 * shooting

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -1 * shooting * 2))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110), 2)


def lost_game():
    img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)
    show_image(img)


def won_game():
    img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)
    show_image(img)


def exit_game():
    pygame.quit()
    sys.exit()


def pause_game():
    img = load_image(path.join('static', 'img', 'level_1', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img, (0, 0))

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                if event.key == pygame.K_p:
                    pause = False
        pygame.display.update()


def wait_for_keystroke_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return


def show_info():
    img = load_image(path.join('static', 'img', 'level_1', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    show_image(img)


def show_image(img):
    window.blit(img, (0, 0))
    pygame.display.update()
    wait_for_keystroke_menu()


def update_sprites():
    player = Player()
    player_team = pygame.sprite.RenderUpdates(player)
    group_shooting_player = pygame.sprite.RenderUpdates()

    enemy = Enemy()
    enemy_team = pygame.sprite.RenderUpdates()

    return enemy, enemy_team, player, player_team, group_shooting_player


def menu_new_game():
    img = load_image(path.join('static', 'img', 'background', 'background.jpg'), True, DISPLAYMODE)
    show_image(img)


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        menu_new_game()
        self.time = pygame.time.Clock()

    def run(self):
        delay_shooting, fps_shooting = 0, 0
        time_elapsed = time.clock()

        while True:
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            energy = INIT_ENERGY
            try:
                enemy.kill()
                player.kill()
            except Exception:
                pass

            enemy, enemy_team, player, player_team, group_shooting_player = update_sprites()
            background_game = load_image(path.join('static', 'img', 'level_1', 'background', 'background_1.jpg'),
                                         True, DISPLAYMODE)

            group_explosion = pygame.sprite.RenderUpdates()
            kill_enemy = 0
            check_on_press_keys = True
            count_shooting = COUNT_SHOOTING

            # Меню игрока
            score_box = TextBox("Счёт: {}".format(kill_enemy), font_1, 10, 10)
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, 10, 50)
            text_info = TextBox("   Нажмите:", font_2, 10, WINDOW_HEIGHT - 160)
            text_esc = TextBox("+ ESC - Выход из игры", font_2, 10, WINDOW_HEIGHT - 120)
            text_f1 = TextBox("+ F1 - Информация о сражении", font_2, 10, WINDOW_HEIGHT - 80)
            text_p = TextBox("+ P - Пауза, с инфомацией сражения", font_2, 10, WINDOW_HEIGHT - 40)

            group_box = pygame.sprite.RenderUpdates(score_box, time_box, text_esc, text_info,text_f1, text_p)

            while True:
                window.blit(background_game, (0, 0))
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:
                                show_info()
                            if event.key == pygame.K_p:
                                pause_game()
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_SPACE:
                                delay_shooting = 9
                        elif event.type == pygame.KEYUP:
                            player.y_speed = 0

                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:
                        delay_shooting += 1
                        fps_shooting = 0
                        if delay_shooting == 10 and count_shooting - 1 > 0:
                            group_shooting_player.add(PlayerShooting(player.rect.midtop))
                            delay_shooting = 0
                            count_shooting -= 1
                    else:
                        fps_shooting += 1
                        if fps_shooting == 25 and count_shooting < COUNT_SHOOTING:
                            count_shooting += 1
                            fps_shooting = 0

                if len(enemy_team) < MAX_NUMBER_ENEMY:
                    if random.randint(0, 50) == 0:
                        enemy_team.add(Enemy())

                if energy <= 0 and check_on_press_keys:
                    check_on_press_keys = False
                    group_explosion.add(Explosion(player.rect))
                    player.kill()

                # Считаем время
                if not time.clock():
                    time_current = time.perf_counter()
                else:
                    time_current = time.clock()
                # Устонавливаем конечное время
                time_elapsed = time_current - start_time

                check = False
                for enemy in enemy_team:
                    if enemy.rect.right <= 0:
                        check = True
                if check:
                    lost_game()
                    break

                # =========================
                # СПРАЙТ СТОЛКНОВЕНИЯ
                # =========================

                for player in pygame.sprite.groupcollide(player_team, group_shooting_enemy, False, True):
                    energy -= 15

                for enemy in pygame.sprite.groupcollide(enemy_team, group_shooting_player, True, True):
                    group_explosion.add(Explosion(enemy.rect))
                    kill_enemy += 1
                    if kill_enemy >= COUNT_ENEMY:
                        won_game()

                # =============================
                # ОБНОВЛЯЕМ ВСЕ ГРУППЫ
                # =============================

                enemy_team.update()
                player_team.update()
                group_shooting_player.update()
                group_explosion.update()
                group_shooting_enemy.update()
                group_box.update()

                # =======================
                # ОЧИЩАЕМ СПРАЙТЫ
                # =======================

                enemy_team.clear(window, background_game)
                player_team.clear(window, background_game)
                group_shooting_player.clear(window, background_game)
                group_explosion.clear(window, background_game)
                group_shooting_enemy.clear(window, background_game)
                group_box.clear(window, background_game)

                enemy_team.draw(window)
                player_team.draw(window)
                group_shooting_player.draw(window)
                group_explosion.draw(window)
                group_shooting_enemy.draw(window)
                group_box.draw(window)

                # Вносим новые значения в меню игрока
                score_box.text = "Счёт: {}".format(kill_enemy)
                time_box.text = "Время: %.2f" % time_elapsed

                if energy < 0:
                    energy = 0
                show_energy_bar(energy)
                show_shooting_bar(count_shooting)
                pygame.display.update()
                self.time.tick(FPS)
            menu_new_game()
