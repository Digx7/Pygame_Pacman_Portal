from art import *
from game_math import Map


class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 904
        self.screen_height = 1000
        self.fps = 12

        self.palette = ColorPalette(bg=(0, 0, 0),
                                    header1=(255, 255, 0),
                                    header2=(0, 255, 255),
                                    text=(255, 255, 0),
                                    sub_text=(100, 100, 100),
                                    ui=(0, 0, 0),
                                    pellet=(0, 255, 0),
                                    power_pellet=(0, 255, 0),
                                    fruit=(0, 0, 0),
                                    player=(255, 255, 0),
                                    portal1=(255, 255, 255),
                                    portal2=(255, 255, 255),
                                    inky=(255, 0, 0),
                                    p=(255, 255, 255),
                                    blinky=(0, 0, 255),
                                    clyde=(0, 255, 0),
                                    scatter=(0, 0, 0),
                                    blank=(255, 255, 255))

        self.bg_color = self.palette.bg_color

        self.sprite_sheet = SpriteSheet('images/PacMan Portal Art Assets1_v1.png')
        self.sprites_raw = {"player_move_anim1": self.sprite_sheet.image_at((0, 0, 16, 16)),
                            "player_move_anim2": self.sprite_sheet.image_at((16, 0, 16, 16)),
                            "player_dead_anim1": self.sprite_sheet.image_at((32, 0, 16, 16)),
                            "player_dead_anim2": self.sprite_sheet.image_at((48, 0, 16, 16)),
                            "player_dead_anim3": self.sprite_sheet.image_at((64, 0, 16, 16)),
                            "player_dead_anim4": self.sprite_sheet.image_at((80, 0, 16, 16)),
                            "ghost_move_anim1": self.sprite_sheet.image_at((0, 16, 16, 16)),
                            "ghost_move_anim2": self.sprite_sheet.image_at((16, 16, 16, 16)),
                            "ghost_scatter_anim1": self.sprite_sheet.image_at((32, 16, 16, 16)),
                            "ghost_scatter_anim2": self.sprite_sheet.image_at((48, 16, 16, 16)),
                            "eyes_down": self.sprite_sheet.image_at((64, 16, 16, 16)),
                            "eyes_up": self.sprite_sheet.image_at((80, 16, 16, 16)),
                            "eyes_left": self.sprite_sheet.image_at((96, 16, 16, 16)),
                            "eyes_right": self.sprite_sheet.image_at((112, 16, 16, 16)),
                            "pellet": self.sprite_sheet.image_at((0, 32, 16, 16)),
                            "power_pellet": self.sprite_sheet.image_at((16, 32, 16, 16)),
                            "fruit": self.sprite_sheet.image_at((32, 32, 16, 16)),
                            "portal_bullet": self.sprite_sheet.image_at((32, 48, 16, 16)),
                            "portal_static": self.sprite_sheet.image_at((32, 64, 16, 16)),
                            "portal_gun": self.sprite_sheet.image_at((32, 80, 16, 16))
                            }

        self.sprite_scale_factor = (64, 64)

        self.sprites = {"player_move1": self.get_sprite("player_move_anim1", "player"),
                        "player_move2": self.get_sprite("player_move_anim2", "player"),
                        "player_dead1": self.get_sprite("player_dead_anim1", "player"),
                        "player_dead2": self.get_sprite("player_dead_anim2", "player"),
                        "player_dead3": self.get_sprite("player_dead_anim3", "player"),
                        "player_dead4": self.get_sprite("player_dead_anim4", "player"),
                        "inky_move1": self.get_sprite("ghost_move_anim1", "inky"),
                        "inky_move2": self.get_sprite("ghost_move_anim2", "inky"),
                        "p": self.get_sprite("ghost_move_anim1", "p"),
                        "pinky_move2": self.get_sprite("ghost_move_anim2", "p"),
                        "blinky_move1": self.get_sprite("ghost_move_anim1", "blinky"),
                        "blinky_move2": self.get_sprite("ghost_move_anim2", "blinky"),
                        "clyde_move1": self.get_sprite("ghost_move_anim1", "clyde"),
                        "clyde_move2": self.get_sprite("ghost_move_anim2", "clyde"),
                        "eyes_down": self.get_sprite("eyes_down", "blank"),
                        "eyes_up": self.get_sprite("eyes_up", "blank"),
                        "eyes_left": self.get_sprite("eyes_left", "blank"),
                        "eyes_right": self.get_sprite("eyes_right", "blank"),
                        "pellet": self.get_sprite("pellet", "pellet"),
                        "power_pellet": self.get_sprite("power_pellet", "power_pellet"),
                        "fruit": self.get_sprite("fruit", "fruit"),
                        "portal_bullet1": self.get_sprite("portal_bullet", "portal1"),
                        "portal_bullet2": self.get_sprite("portal_bullet", "portal2"),
                        "portal1": self.get_sprite("portal_static", "portal1"),
                        "portal2": self.get_sprite("portal_static", "portal2"),
                        "portal_gun": self.get_sprite("portal_gun", "blank"),
                        }

        # Scene settings
        self.scenes = {"menu": "_menu",
                       "main": "_main",
                       "end": "_end"}

        self.total_lives = 3

    def get_sprite(self, raw_sprite, color):
        output_sprite = self.sprites_raw[raw_sprite]
        output_sprite.fill(self.palette.color[color], special_flags=pygame.BLEND_MULT)
        output_sprite = pygame.transform.scale(output_sprite, self.sprite_scale_factor)
        output_sprite.set_colorkey(self.palette.color["bg"])
        return output_sprite
