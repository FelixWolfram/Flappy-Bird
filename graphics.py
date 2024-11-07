from pygame import image, transform, mask, Surface
from help import Info
from random import randint


class Tubes:
    def __init__(self):
        self.img = image.load('assets/sprites/pipe-green.png').convert ()
        self.img = transform.smoothscale(self.img, (self.img.get_width() * 1.8, self.img.get_height() * 1.8))
        self.img_bottom = self.img.copy()
        self.img_top = transform.rotate(self.img, 180).copy()
        self.mask_top = mask.from_surface(self.img_top)
        self.mask_bottom = mask.from_surface(self.img_bottom)

        self.gap = 180
        self.offset = randint(130, self.img_top.get_height() - 55)
        self.x_top = Info.WIN_WIDTH + 200
        self.y_top = 0 - self.offset
        self.x_bottom = Info.WIN_WIDTH + 200
        self.y_bottom = self.y_top + self.img_top.get_height() + self.gap

        self.tube_moving_speed = 3.11
        self.enabled = True     # disable tubes when the points for that tube are collected
    

    def move(self):
        self.x_top -= self.tube_moving_speed
        self.x_bottom -= self.tube_moving_speed


class Base:
    def __init__(self, bg_rect, beginning, offset=0):
        self.bg_rect = bg_rect
        self.base_img = image.load('assets/sprites/base.png').convert()
        self.base_img = transform.smoothscale(self.base_img, (Info.WIN_WIDTH, Info.BOTTOM_HEIGHT))
        self.base_rect_mask = mask.from_surface(self.base_img)
        if beginning:
            self.base_rect = self.base_img.get_rect(bottomleft= self.bg_rect.bottomleft)
        else:
            self.base_rect = self.base_img.get_rect(bottomleft = self.bg_rect.bottomright)
            self.base_rect.x -= offset


class Background:
    def __init__(self, game_context):
        self.game_context = game_context
        self.bg = image.load('assets/sprites/background-day.png').convert()
        self.bg = transform.smoothscale(self.bg, (Info.WIN_WIDTH, Info.WIN_HEIGHT))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.topleft = (0, 0)

        self.base = [Base(self.bg.get_rect(), beginning=True)]
        self.bg_surf = Surface((Info.WIN_WIDTH, Info.WIN_HEIGHT))  

        self.tube_distance = 150
        self.tubes = [Tubes()]


    def move(self):
        for tube in self.tubes:
            tube.move()
            if tube.x_top + tube.img_top.get_width() < 0:
                self.tubes.remove(tube)
        self.spawn_new()


    def collect_points(self, birdx):
        self.tubes[0].img_top.get_width()
        for tube in self.tubes:
            if (birdx + self.game_context.bird_width) >= tube.x_top + tube.img_top.get_width() // 2 and tube.enabled:
                self.game_context.score += 1
                tube.enabled = False

    
    def move_base(self):
        for base_part in self.base: # move all base parts
            base_part.base_rect.x -= self.tubes[0].tube_moving_speed
        # if the left base_part goes out of the scree (gap at the right of the screen), append a new base part at the right
        if self.base[-1].base_rect.right <= Info.WIN_WIDTH:
            offset = Info.WIN_WIDTH - self.base[-1].base_rect.right # there could be a gap due to rounding errors -> fix this with the offset
            self.base.append(Base(self.bg.get_rect(), beginning=False, offset=offset))
            if self.base[0].base_rect.right < 0:
                self.base.pop(0)

    
    def spawn_new(self):
        if Info.WIN_WIDTH - self.tubes[-1].x_top > self.tube_distance:
            self.tubes.append(Tubes())


    def draw(self, win):
        self.bg_surf.blit(self.bg, self.bg_rect)
        for tube in self.tubes:
            self.bg_surf.blit(tube.img_top, (tube.x_top, tube.y_top))
            self.bg_surf.blit(tube.img_bottom, (tube.x_bottom, tube.y_bottom))
        for base_part in self.base:
            self.bg_surf.blit(base_part.base_img, (base_part.base_rect.x, base_part.base_rect.y))

        win.blit(self.bg_surf, (0, 0))
