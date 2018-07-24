#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module is entrance point to minesweeper game."""
import os
import sys

import pygame
from pygame.locals import *

from models import Field, Cell
from view import Renderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minesweeper")
    surface = pygame.display.get_surface()

    clock = pygame.time.Clock()
    field = Field()
    screen = pygame.display.set_mode(field.bound[2:])

    mouse = (0, 0, 0)
    game_over = False
    while 1:
        clock.tick(60)

        surface.fill((255, 255, 255))
        field.render(surface)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_r:
                field = Field()
                game_over = False
            elif event.type == KEYDOWN:
                mx, my = pygame.mouse.get_pos()
                if event.key == K_q:
                    game_over = field.handle_open_left(mx, my)
                elif event.key == K_z:
                    game_over = field.handle_press(mx, my)
            elif game_over:
                continue
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
            elif event.type == MOUSEBUTTONUP:
                mx, my = pygame.mouse.get_pos()
                if mouse[0] and mouse[2]:
                    mouse = (0, 0, 0)
                    game_over = field.handle_open_left(mx, my)
                elif mouse[0]:
                    game_over = field.handle_press(mx, my)
                elif mouse[2]:
                    field.handle_flag(mx, my)


if __name__ == "__main__":
    main()
