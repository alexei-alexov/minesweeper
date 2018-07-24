# -*- coding: utf-8 -*-
import pygame


class Renderer(object):

    def __init__(self, conf):
        self.cellw = conf.get('cellw', 30)
        self.cellh = conf.get('cellh', 30)

        self.f = pygame.font.Font(pygame.font.get_default_font(), self.cellh)

        # TOP RIGHT BOTTOM LEFT
        self.padding = conf.get('padding', (10, 10, 10, 10))

        # V H
        self.spacing = conf.get('spacing', (5, 5))

        self.c_hidden = conf.get('c_hidden', (14, 14, 14))


    def render_field(self, field, surface):
        cell_rect = pygame.Rect(self.padding[0], self.padding[1],
                                self.cellw, self.cellh)

        field.field[0][0].hidden = True
        for y, row in enumerate(field.field):
            for x, cell in enumerate(row):
                # render cell part...
                if cell.hidden:
                    pygame.draw.rect(surface, (144, 144, 144), cell_rect)
                else:
                    pygame.draw.rect(surface, (190, 190, 190), cell_rect)
                    self.f.render(str(cell.cell_type), 0, (0, 0, 0,))

                cell_rect.move_ip(self.spacing[0] + self.cellw, 0)

            cell_rect.move_ip(0, self.cellh + self.spacing[1])
            cell_rect.x = self.padding[0]
