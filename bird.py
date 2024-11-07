from pygame import image, transform, mask
from help import Info


class Player:
    def __init__(self, base, tubes, game_context):
        self.game_context = game_context
        self.base = base
        self.tubes = tubes

        self.images = [image.load(f'assets/sprites/yellowbird-{state}.png').convert_alpha() for state in ("midflap", "downflap", "upflap")]
        self.images = [transform.smoothscale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.images]
        self.up_rotation = 30
        self.up_img = [transform.rotate(self.images[i], self.up_rotation).copy() for i in range(len(self.images))]
        self.rotate = 0

        self.game_context.bird_width = self.images[0].get_width()
        self.mask = mask.from_surface(self.images[0])
        self.counter = 0
        self.img_index = 0
        self.x = Info.WIN_WIDTH // 4
        self.y = (Info.WIN_HEIGHT - Info.BOTTOM_HEIGHT) // 2.0
        self.start_vel = 1
        self.max_vel = Info.WIN_HEIGHT // 60
        self.vel = self.start_vel
        self.jump_vel = -(self.start_vel * 11)
        self.ground_collision = False


    def fall(self):
        self.check_for_collision()
        self.y += min(self.max_vel, self.vel)
        self.vel += Info.GRAVITY / Info.FPS
    

    def check_for_collision(self):
        # collision with the ground
        for base_part in self.base:
            if self.mask.overlap(base_part.base_rect_mask, (base_part.base_rect[0] - self.x, base_part.base_rect[1] - self.y)):
                self.game_context.game_over = True
                self.ground_collision = True
        # collision with a tube
        for tube in self.tubes:
            if self.mask.overlap(tube.mask_top, (tube.x_top - self.x, tube.y_top - self.y)) or\
               self.mask.overlap(tube.mask_bottom, (tube.x_bottom - self.x, tube.y_bottom - self.y)):
                self.game_context.game_over = True
        
    
    def draw(self, win):
        if self.vel < self.max_vel * 0.7 and not self.game_context.game_start:
            win.blit(self.up_img[self.img_index], (self.x, self.y))
        else:
            if self.vel >= self.max_vel * 0.7:
                self.rotate = max(self.rotate - self.max_vel // 1.8, -120)
            final_rotate = self.rotate + self.up_rotation if self.vel != self.start_vel else 0    # so the bird is not looking up in the beginning
            win.blit(transform.rotate(self.images[self.img_index], final_rotate), (self.x, self.y))
        self.counter += 1
        if self.counter > Info.FPS / 10:
            self.img_index = (self.img_index + 1) % 3
            self.counter = 0