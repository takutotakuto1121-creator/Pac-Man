import pygame as pg
import sys


def menu_end(WIDTH: int, HEIGHT: int, win: bool) -> None:
    # winが１以外ならゲームオーバーの処理
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    if win is True:
        state = "GAME CLEAR"
        TEXT_COL = (255, 255, 255)
    else:
        state = "GAME OVER"
        TEXT_COL = (255, 0, 0)
    pg.display.set_caption(state)
    game_paused = False
    title_font = pg.font.SysFont("arialblack", 120)
    font = pg.font.SysFont("arialblack", 40)
    SCORE_COL = (157, 204, 224)

    name = ""
    confirmed_name = ""
    run = True
    while run:
        screen.fill((0, 0, 0))
        if game_paused is True:
            pass
        else:
            img = title_font.render(state, True, TEXT_COL)
            score = font.render("Input your name :", True, SCORE_COL)
            input_box = font.render(name + "|", True, (255, 220, 100))

            title_spot = img.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            score_spot = score.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            input_spot = input_box.get_rect(
                center=(WIDTH / 2, HEIGHT / 2 + 70))

            screen.blit(img, title_spot)
            screen.blit(score, score_spot)
            screen.blit(input_box, input_spot)

            if confirmed_name:
                saved = font.render(f"Score saved!  {confirmed_name}!",
                                    True, (120, 255, 160))
                saved_spot = saved.get_rect(
                    center=(WIDTH / 2, HEIGHT / 2 + 150))
                screen.blit(saved, saved_spot)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    confirmed_name = name
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pg.K_SPACE:
                    name += "_"
                else:
                    if len(name) < 10 and (event.unicode.isalnum()):
                        name += event.unicode

        pg.display.update()


if __name__ == "__main__":
    menu_end(800, 600, True)
