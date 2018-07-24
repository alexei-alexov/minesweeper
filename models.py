# -*- coding: utf-8 -*-
"""This module contains all game model classes."""
from collections import deque

import pygame

from res import f


DIRS = (-1, 0, +1)


class Cell(object):

    W = 20
    H = 20
    C_HIDDEN = (155, 155, 155)
    C_OPEN = (200, 200, 200)
    C_BOMB = (255, 100, 100)
    CS = ((0, 50, 150), ) + tuple((75 + 20*i, 100 - i*5, 50) for i in range(9)) + ((0, 0, 0),)


    def __init__(self, coords, cell_type=0, hidden=False):
        self.cell_type = cell_type
        self.hidden = hidden
        self.flagged = False
        self.x = coords[0]
        self.y = coords[1]
        self.bounds = pygame.Rect(coords, (self.W, self.H))

    def check_press(self, x, y):
        return self.bounds.collidepoint(x, y)

    def render(self, surface):
        if self.hidden:
            pygame.draw.rect(surface, self.C_HIDDEN, self.bounds)
            if self.flagged:
                text = f.render("f", 1, (0, 0, 0))
                textpos = text.get_rect(centerx=self.x + self.W / 2, centery=self.y + self.H/2)
                surface.blit(text, textpos)
        else:
            if self.cell_type != -1:
                pygame.draw.rect(surface, self.C_OPEN, self.bounds)
            else:
                pygame.draw.rect(surface, self.C_BOMB, self.bounds)
            if self.cell_type != 0:
                if self.cell_type == -1:
                    text = f.render("*", 1, self.CS[self.cell_type])
                else:
                    text = f.render(str(self.cell_type), 1, self.CS[self.cell_type])
                textpos = text.get_rect(centerx=self.x + self.W / 2, centery=self.y + self.H/2)
                surface.blit(text, textpos)

    def press(self):
        if self.hidden:
            self.hidden = False
            self.flagged = False

    def __repr__(self):
        return "[%s] %s,%s %s" % (self.hidden, self.x, self.y, self.cell_type, )


class Field(object):

    # padding
    TOP_P = 1
    LEFT_P = 1

    # spacing
    VSP = 1
    HSP = 1

    def __init__(self, size=(60, 20), mine_amount=180):
        self.m_left = mine_amount
        self.cells_left = size[0] * size[1]
        self.size = size
        import random as r
        self.field = []
        sx, sy = self.LEFT_P, self.TOP_P
        for y in range(size[1]):
            row = []
            sx = self.LEFT_P
            for x in range(size[0]):
                row.append(Cell((sx, sy), 0, True))
                sx += Cell.W + self.VSP
            self.field.append(row)
            sy += Cell.H + self.HSP
        mines = set()
        while mine_amount:
            new_mine = (r.randint(0, self.size[1]-1), r.randint(0, self.size[0]-1))
            if new_mine not in mines:
                mines.add(new_mine)
                self.field[new_mine[0]][new_mine[1]].cell_type = -1
                mine_amount -= 1

        dirs = (-1, 0, 1)
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell.cell_type == -1: continue
                count = 0
                for dir_x in dirs:
                    for dir_y in dirs:
                        if not dir_x and not dir_y: continue
                        fx, fy = x + dir_x, y + dir_y
                        if 0 <= fx < self.size[0] and 0 <= fy < self.size[1]:
                            if self.field[fy][fx].cell_type == -1: count += 1
                self.field[y][x].cell_type = count

        self.bound = pygame.Rect(self.LEFT_P, self.TOP_P, sx, sy)

    def render(self, surface):
        for row in self.field:
            for cell in row:
                cell.render(surface)

    def handle_press(self, x, y):
        ind_x, ind_y = -1, -1
        for iy, row in enumerate(self.field):
            for ix, cell in enumerate(row):
                if cell.check_press(x, y):
                    ind_x, ind_y = ix, iy
        if ind_x == -1: return False
        cell = self.field[ind_y][ind_x]
        if cell.flagged: return False
        if not cell.hidden:
            return self.handle_open_left(x, y)

        if cell.cell_type == -1:
            cell.hidden = False
            return True
        if cell.cell_type == 0:
            self.handle_empty_open(ind_x, ind_y)
        else:
            self.cells_left -= 1
            cell.hidden = False

        print(self.cells_left)
        if self.cells_left == self.m_left:
            return True
        return False

    def handle_flag(self, x, y):
        ind_x, ind_y = -1, -1
        for iy, row in enumerate(self.field):
            for ix, cell in enumerate(row):
                if cell.check_press(x, y):
                    ind_x, ind_y = ix, iy
        if ind_x == -1: return
        cell = self.field[ind_y][ind_x]
        if cell.hidden:
            cell.flagged = not cell.flagged

    def handle_open_left(self, x, y):
        """When you click on opened cell it can reveal neighbour cells."""
        ind_x, ind_y = -1, -1
        for iy, row in enumerate(self.field):
            for ix, cell in enumerate(row):
                if cell.check_press(x, y):
                    ind_x, ind_y = ix, iy
        if ind_x == -1: return
        cell = self.field[ind_y][ind_x]
        print('cell: ', cell)
        if cell.hidden:
            return
        neighbour_cells = []
        flagged = 0
        closed = 0
        # import ipdb; ipdb.set_trace()
        for dir_x in DIRS:
            for dir_y in DIRS:
                if not dir_x and not dir_y: continue
                fx, fy = ind_x + dir_x, ind_y + dir_y
                if 0 <= fx < self.size[0] and 0 <= fy < self.size[1]:
                    tmp_cell = self.field[fy][fx]
                    if tmp_cell.hidden and not tmp_cell.flagged:
                        neighbour_cells.append((tmp_cell, fx, fy))
                        closed += 1
                    if tmp_cell.flagged:
                        flagged += 1
        print("ng cells: %s. flagged: %s. closed: %s" % (neighbour_cells, flagged, closed, ))
        if flagged == cell.cell_type:
            boom = False
            for cell, ix, iy in neighbour_cells:
                cell.hidden = False
                if cell.cell_type == -1:
                    boom = True
                if not cell.cell_type:
                    self.handle_empty_open(ix, iy)
            if boom:
                return True


    def handle_empty_open(self, ix, iy):
        bounds = deque()
        bounds.appendleft((ix,iy))
        while bounds:
            x, y = bounds.pop()
            self.field[y][x].hidden = False
            self.cells_left -= 1
            if self.field[y][x].cell_type: continue
            for dir_x in DIRS:
                for dir_y in DIRS:
                    if not dir_x and not dir_y: continue
                    fx, fy = x + dir_x, y + dir_y
                    if 0 <= fx < self.size[0] and 0 <= fy < self.size[1]:
                        if self.field[fy][fx].hidden:
                            self.field[fy][fx].hidden = False
                            bounds.appendleft((fx, fy))




