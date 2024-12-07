import pygame

from trosnoth import data
from trosnoth.const import TEAM_1_COLOUR, TEAM_2_COLOUR
from trosnoth.tools.makeicon import StubbedTheme, draw_one_orb


class TrosnothLogoBuilder:
    def __init__(self, total_width=1024):
        pygame.font.init()
        self.total_width = total_width
        self.font = pygame.font.SysFont('FreeMono', 108, bold=True)

    def build(self):
        pygame.display.init()
        window = pygame.display.set_mode((800, 600))
        result = self.layout_chars([
            self.char('T'),
            self.char('R'),
            self.orb_char('O', TEAM_1_COLOUR),
            self.char('S'),
            self.char('N'),
            self.orb_char('O', TEAM_2_COLOUR),
            self.char('T'),
            self.char('H'),
        ])
        pygame.display.quit()
        return result

    def char(self, letter):
        return self.font.render(letter, True, (0, 0, 0), (255, 255, 255))

    def orb_char(self, letter, colour):
        base = self.char(letter).convert_alpha()

        theme = StubbedTheme()
        orb = draw_one_orb(theme, colour)

        scale_factor = base.get_rect().width / orb.get_rect().width
        current_size = orb.get_size()
        final_size = (round(current_size[0] * scale_factor), round(current_size[1] * scale_factor))
        orb = pygame.transform.smoothscale(orb, final_size)

        rect = orb.get_rect()
        rect.center = base.get_rect().center
        base.blit(orb, rect)
        return base

    def layout_chars(self, chars):
        max_height = max(c.get_rect().height for c in chars)
        result = pygame.Surface((self.total_width, max_height))
        result.fill((255, 255, 255))
        total_rect = result.get_rect()

        left_rect = chars[0].get_rect()
        left_rect.centery = total_rect.centery
        result.blit(chars.pop(0), left_rect)

        right_rect = chars[-1].get_rect()
        right_rect.centery = total_rect.centery
        right_rect.right = total_rect.right
        result.blit(chars.pop(-1), right_rect)

        remaining_width = right_rect.centerx - left_rect.centerx
        for i, char in enumerate(chars):
            rect = char.get_rect()
            rect.centery = total_rect.centery
            rect.centerx = left_rect.centerx + round(remaining_width * (i + 1) / (len(chars) + 1))
            result.blit(char, rect)

        return result


if __name__ == '__main__':
    pygame.image.save(TrosnothLogoBuilder().build(), str(data.base_path / 'welcome' / 'logo.png'))
