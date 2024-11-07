import pygame
from help import Info, GameContext
from graphics import Background
from bird import Player


class Game:
    def __init__(self, highscore):
        self.game_context = GameContext()
        self.game_end = False
        self.win = pygame.display.set_mode((Info.WIN_WIDTH, Info.WIN_HEIGHT))
        self.background = Background(self.game_context)
        self.bird = Player(self.background.base, self.background.tubes, self.game_context) 
        self.clock = pygame.time.Clock()
        self.game_context.game_start = True
        self.score_imgs = [pygame.image.load(f'assets/sprites/{i}.png').convert_alpha() for i in range(10)]
        self.score_imgs = [pygame.transform.smoothscale(img, (img.get_width() * 1.3, img.get_height() * 1.3)) for img in self.score_imgs]
        self.game_over = False
        self.highscore = highscore

        self.start_gui = pygame.image.load('assets/sprites/message.png').convert_alpha()
        self.start_gui = pygame.transform.smoothscale(self.start_gui, (self.start_gui.get_width() * 2.2, self.start_gui.get_height() * 2.2))
        self.start_gui.set_alpha(1)
        self.start_rect = self.start_gui.get_rect(center=(Info.WIN_WIDTH // 2, (Info.WIN_HEIGHT - Info.BOTTOM_HEIGHT) // 2 + 30))
        self.start_cooldown = True

        self.home_gui = pygame.image.load('assets/sprites/start-message.png').convert_alpha()
        self.home_gui = pygame.transform.smoothscale(self.home_gui, (self.home_gui.get_width() * 1.8, self.home_gui.get_height() * 1.8))
        self.home_rect = self.home_gui.get_rect(center=(Info.WIN_WIDTH // 2, (Info.WIN_HEIGHT - Info.BOTTOM_HEIGHT) // 2))

        self.home_rect.y = 200
        self.home = True
        self.home_move_direct = 1
        self.move_counter = 0
        self.start_button = pygame.image.load('assets/sprites/start.png').convert_alpha()
        self.start_button = pygame.transform.smoothscale(self.start_button, (self.start_button.get_width() * 1.32, self.start_button.get_height() * 1.32))
        self.start_button_rect = self.start_button.get_rect(center = self.win.get_rect().center)
        self.start_button_rect.y = 560

        self.game_over_img = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
        self.game_over_img = pygame.transform.smoothscale(self.game_over_img, (self.game_over_img.get_width() * 1.9, self.game_over_img.get_height() * 1.9))
        self.game_over_img.set_alpha(0)
        self.game_over_rect = self.game_over_img.get_rect(center = self.win.get_rect().center)
        self.game_over_rect.y = 230

        self.score_sheet = pygame.image.load('assets/sprites/score_sheet.png').convert_alpha()
        self.score_sheet = pygame.transform.smoothscale(self.score_sheet, (self.score_sheet.get_width() * 1.7, self.score_sheet.get_height() * 1.7))
        self.score_sheet_rect = self.score_sheet.get_rect(center= self.win.get_rect().center)
        self.score_sheet_rect.y = Info.WIN_HEIGHT + 30
        self.score_sheet_surf = pygame.Surface((self.score_sheet.get_width(), self.score_sheet.get_height()))
        self.increment_score = 0
        self.count_frames_score = 0

        self.ok_button = pygame.image.load('assets/sprites/ok-button.png').convert_alpha()
        self.ok_button = pygame.transform.smoothscale(self.ok_button, (self.ok_button.get_width() * 1.32, self.ok_button.get_height() * 1.32))
        self.ok_button_rect = self.ok_button.get_rect(center= self.win.get_rect().center)
        self.wait_for_ok = 0

        self.medals = {
            "bronze": pygame.image.load('assets/sprites/bronze.png').convert_alpha(),
            "silver": pygame.image.load('assets/sprites/silver.png').convert_alpha(),
            "gold": pygame.image.load('assets/sprites/gold.png').convert_alpha(),
            "platinum": pygame.image.load('assets/sprites/platinum.png').convert_alpha()
        }
        for key in self.medals:
            self.medals[key] = pygame.transform.smoothscale(self.medals[key], (self.medals[key].get_width() * 1.7, self.medals[key].get_height() * 1.7))

    
    def mainloop(self):
        run = True
        while run:
            self.clock.tick(Info.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_end = True
                    return max(self.highscore, self.game_context.score)
                # home screen
                if self.home and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.home = False
                # start screen and during the game
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.home and not self.start_cooldown and not self.game_context.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN or event.key == pygame.K_SPACE:
                        self.bird.vel = self.bird.jump_vel
                        self.bird.rotate = 0
                        self.game_context.game_start = False
                # game over
                if self.game_context.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.ok_button_rect.collidepoint(event.pos):
                        return max(self.highscore, self.game_context.score)
                
            if not self.game_context.game_over:
                if not self.game_context.game_start and not self.home:
                    self.bird.fall()
                    self.background.move()
                self.background.move_base()
                self.background.collect_points(self.bird.x)
            elif self.game_context.game_over and not self.bird.ground_collision:
                self.bird.fall()

            if self.home:
                self.move_counter += 1
                if self.move_counter % 2 == 0:
                    if self.home_move_direct > 0 and self.home_rect.y > 220:
                        self.home_move_direct *= -1  # change direction
                    elif self.home_move_direct < 0 and self.home_rect.y < 180:
                        self.home_move_direct *= -1  # change direction
                    self.home_rect.y += self.home_move_direct

            self.redraw_window()


    def draw_score(self, score):
        score_surf = pygame.Surface((100, 100), pygame.SRCALPHA)    # SRCALPHA so you don't see a 100x100 black box
        text_width = 0
        for digit in str(score):
            text_width += self.score_imgs[int(digit)].get_width()   # sum up all the widths of every digit in the score
        start_x = score_surf.get_width() // 2 - text_width // 2 # starting position for the first digit
        for digit in str(score):
            score_surf.blit(self.score_imgs[int(digit)], (start_x, 0))  # blit the digit to the
            start_x += self.score_imgs[int(digit)].get_width()          # update the starting position for the next digit
        score_pos = score_surf.get_rect(center= self.win.get_rect().center)
        score_pos.y = Info.WIN_HEIGHT // 20
        return score_surf, score_pos, text_width
            

    def redraw_window(self):
        self.win.fill((255, 255, 255))
        self.background.draw(self.win)
        # start screen
        if self.game_context.game_start and not self.home:
            self.win.blit(self.start_gui, self.start_rect)
            new_alpha = self.start_gui.get_alpha() + 4
            if new_alpha >= 255:
                self.start_cooldown = False
            self.start_gui.set_alpha(new_alpha)
        # home screen
        if self.home:
            self.win.blit(self.home_gui, self.home_rect)
            self.win.blit(self.start_button, self.start_button_rect)
        # during game
        elif not self.home:
            score_surf, score_pos, _ = self.draw_score(self.game_context.score)
            self.win.blit(score_surf, score_pos)
            self.bird.draw(self.win)
        # game over
        if self.game_context.game_over:
            self.win.blit(self.game_over_img, self.game_over_rect)
            # animate game over screen first
            if self.game_over_img.get_alpha() < 255:
                new_alpha = self.game_over_img.get_alpha() + 7
                self.game_over_img.set_alpha(new_alpha)
                self.game_over_rect.y -= 1.5
            # then animate the score sheet
            if self.game_over_img.get_alpha() > 180:
                self.score_sheet_surf.blit(self.score_sheet, (0, 0))
                if self.score_sheet_rect.y > self.game_over_rect.bottom + 50:
                    self.score_sheet_rect.y -= 30
                # then animate the score on the score sheet
                else:
                    # score now
                    self.count_frames_score += 1
                    score_surf, _, score_width = self.draw_score(self.increment_score)
                    if self.count_frames_score % 5 == 0 and self.increment_score < self.game_context.score:
                        self.increment_score += 1
                    self.score_sheet_surf.blit(score_surf, ((self.score_sheet.get_width() * 0.79 - score_width / 2, self.score_sheet.get_height() * 0.29)))
                    # highscore
                    score_surf, _, score_width = self.draw_score(max(self.highscore, self.game_context.score))
                    self.score_sheet_surf.blit(score_surf, ((self.score_sheet.get_width() * 0.79 - score_width / 2, self.score_sheet.get_height() * 0.65)))

                    # score counting is done, display "OK" button now to start a new game
                    if self.increment_score == self.game_context.score:
                        # displaying the medal
                        if self.game_context.score >= 10:
                            medal = "bronze"
                        elif self.game_context.score >= 20:
                            medal = "silver"
                        elif self.game_context.score >= 30:
                            medal = "gold"
                        elif self.game_context.score >= 40:
                            medal = "platinum"
                        if self.game_context.score >= 10:   # display the medal
                            self.score_sheet_surf.blit(self.medals[medal], (self.score_sheet.get_width() * 0.1144, self.score_sheet.get_height() * 0.3643))
                        # displaying the "OK" button
                        if self.wait_for_ok > Info.FPS / 2:
                            self.ok_button_rect.y = self.score_sheet_rect.bottom + 30
                            self.win.blit(self.ok_button, self.ok_button_rect)
                        self.wait_for_ok += 1
                self.win.blit(self.score_sheet_surf, self.score_sheet_rect)
        pygame.display.flip()


pygame.init()
pygame.display.set_caption("Flappy Bird")

try:
    with open("highscore.txt", "r") as file:   # with the "with-block" the file is automatically closed after the block is executed
        highscore = int(file.read())
except FileNotFoundError:
    highscore = 0

while True:
    game = Game(highscore)
    score = game.mainloop()
    highscore = max(highscore, score)
    if game.game_end:
        break
    print("was jeht")

with open("highscore.txt", "w") as file:
    file.write(str(highscore))