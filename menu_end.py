import pygame as pg
import sys


def menu_end(wl: int) -> None:
    WIDTH = 800
    HEIGHT = 600
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    if wl == 1:
        state = "GAME CLEAR"
        TEXT_COL = (255, 255, 255)
    else:
        state = "GAME OVER"
        TEXT_COL = (255, 0, 0)
    pg.display.set_caption(state)
    game_paused = False
    title_font = pg.font.SysFont("arialblack", 120)
    font = pg.font.SysFont("arialblack", 40)
    TITLE_COL = (255, 255, 255)
    SCORE_COL = (157, 204, 224)
    run = True
    while run:
        screen.fill((0, 0, 0))
        if game_paused is True:
            pass
        else:
            img = title_font.render(state, True, TEXT_COL)
            start = font.render("Score saved!", True, TITLE_COL)
            score = font.render("Input your name :", True, SCORE_COL)
            title_spot = img.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            intro_spot = img.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            score_spot = img.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))
            screen.blit(img, title_spot)
            screen.blit(start, intro_spot)
            screen.blit(score, score_spot)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("ゲームスタート")
            if event.type == pg.QUIT:
                run = False
                sys.exit()
            pg.display.update()


if __name__ == "__main__":
    menu_end(0)



