import pygame


def main():
    ...
    while running:
        for event in pygame.event.get():
            ...

        if state == "menu":
            # update
            # draw
        elif state == "game":
            # update(Entityの情報を更新)
            # draw(描画)
        ...

        clock.tick(60)
