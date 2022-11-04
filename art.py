import pygame
import pygame.font


class Animations():
    def __init__(self, **animations):
        self.animations = animations
        self.current_key = "idle"
        self.current_animation = self.animations[self.current_key]

    def set_current_animation(self, key):
        self.current_animation.current_index = 0

        self.current_key = key
        self.current_animation = self.animations[self.current_key]

    def get_current_animation(self):
        return self.current_animation

    def check_if_fin(self):
        return self.current_animation.check_if_at_end()


class Animation():
    def __init__(self, frames, max_loops=0):
        self.frames = frames
        self.max_loops = max_loops
        self.current_loop = 0
        self.current_index = 0
        self.current_frame = self.frames[self.current_index]

    def update(self):
        self.increment_frame()
        return self.get_current_frame()

    def increment_frame(self):
        self.current_index += 1
        if self.current_index >= len(self.frames) and self.max_loops == 0:
            self.current_index = 0
        elif self.current_index >= len(self.frames) and self.max_loops > 0:
            self.current_loop += 1
            if self.current_loop >= self.max_loops: self.current_index -= 1
            else: self.current_index = 0

    def get_current_frame(self):
        self.current_frame = self.frames[self.current_index]
        return self.current_frame

    def check_if_at_end(self):
        if self.current_loop >= self.max_loops:
            return True
        else:
            return False


class Buttons():
    def __init__(self, settings, screen, **msgs):
        self.settings = settings
        self.screen = screen
        self.msgs = msgs

        self.setup_buttons()

    def setup_buttons(self):
        for key in self.msgs:
            self.msgs[key] = Button(self.settings, self.screen, self.msgs[key])

    def draw_button(self, m):
        self.msgs[m].draw_button()

    def draw_button_absolute(self, m, pos):
        self.msgs[m].draw_button_absolute(pos)

    def draw_button_alignx_center(self, m, y):
        self.msgs[m].draw_button_alignx_center(y)

    def check_button(self, key, mouse_x, mouse_y):
        return self.msgs[key].check_button(mouse_x, mouse_y)


class Button():

    def __init__(self, settings, screen, msg):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimiensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = settings.palette.color["ui"]
        self.text_color = settings.palette.color["text"]
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.msg_image_rect.center = self.rect.center
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_button_absolute(self, pos):
        """Sets the exact position of the button, then draws it"""
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.draw_button()

    def draw_button_alignx_center(self, y):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = y
        self.draw_button()


    def check_button(self, mouse_x, mouse_y):
        """Check to see if the mouse is over the button"""
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True



class ColorPalette():
    def __init__(self, **colors):
        self.color = colors
        self.bg_color = colors["bg"]


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            # self.sheet = pygame.image.load(filename).convert()
            self.sheet = pygame.image.load(filename)
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        # image = pygame.Surface(rect.size).convert()
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)