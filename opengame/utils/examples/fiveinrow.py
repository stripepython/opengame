import opengame as og

WIDTH = 720
GRID_WIDTH = WIDTH // 20   # WIDTH // (19 + 1)
LINES = [
    ((WIDTH // 2 - GRID_WIDTH, WIDTH // 2 - GRID_WIDTH), (WIDTH // 2 - GRID_WIDTH, -WIDTH // 2 + GRID_WIDTH)),
    ((-WIDTH // 2 + GRID_WIDTH, -WIDTH // 2 + GRID_WIDTH), (WIDTH // 2 - GRID_WIDTH, -WIDTH // 2 + GRID_WIDTH)),
    ((-WIDTH // 2 + GRID_WIDTH, WIDTH // 2 - GRID_WIDTH), (WIDTH // 2 - GRID_WIDTH, WIDTH // 2 - GRID_WIDTH)),
    ((-WIDTH // 2 + GRID_WIDTH, WIDTH // 2 - GRID_WIDTH), (-WIDTH // 2 + GRID_WIDTH, -WIDTH // 2 + GRID_WIDTH))
]
CIRCLES = [
    (GRID_WIDTH * 4 - WIDTH // 2, -GRID_WIDTH * 4 + WIDTH // 2),
    (WIDTH - GRID_WIDTH * 4 - WIDTH // 2, -GRID_WIDTH * 4 + WIDTH // 2),
    (WIDTH - GRID_WIDTH * 4 - WIDTH // 2, -(WIDTH - GRID_WIDTH * 4) + WIDTH // 2),
    (GRID_WIDTH * 4 - WIDTH // 2, -(WIDTH - GRID_WIDTH * 4) + WIDTH // 2),
    (GRID_WIDTH * 10 - WIDTH // 2, -GRID_WIDTH * 10 + WIDTH // 2),
    (GRID_WIDTH * 10 - WIDTH // 2, -GRID_WIDTH * 4 + WIDTH // 2),
    (GRID_WIDTH * 4 - WIDTH // 2, -GRID_WIDTH * 10 + WIDTH // 2),
    (GRID_WIDTH * 10 - WIDTH // 2, -GRID_WIDTH * 16 + WIDTH // 2),
    (GRID_WIDTH * 16 - WIDTH // 2, -GRID_WIDTH * 10 + WIDTH // 2)
]
BLACK = og.Color(0, 0, 0)
WHITE = og.Color(255, 255, 255)

window = og.Window('Five In Row', size=(WIDTH, WIDTH))
background = og.Background(og.builtin.backgrounds.weiqi)
background.pack()
pen = og.Pen()
board = [[None] * 20 for _ in range(20)]
player = BLACK

def destroy(tips):
    update()
    window.screenshot()
    window.destroy(exit_all=False)
    new_win = og.Window('Game Over', (WIDTH, WIDTH))
    bg = og.Background('screenshot.png')
    bg.pack()
    label = og.Label(tips, font=og.Font.from_system('msmincho', 52, True), color=(0, 255, 0))
    label.pack()
    og.play_sound(og.builtin.sounds.win)
    new_win.show()
    

def update():
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j:
                pen.circle(j, (x * GRID_WIDTH - WIDTH // 2, -y * GRID_WIDTH + WIDTH // 2), GRID_WIDTH // 2)


@window.when_draw
def draw():
    for line in LINES:
        pen.line(BLACK, line[0], line[1], 4)
    for cnt in range(19):
        pen.line(
            BLACK,
            (GRID_WIDTH * (2 + cnt) - WIDTH // 2, -GRID_WIDTH + WIDTH // 2),
            (GRID_WIDTH * (2 + cnt) - WIDTH // 2, GRID_WIDTH - WIDTH + WIDTH // 2)
        )
        pen.line(
            BLACK,
            (GRID_WIDTH - WIDTH // 2, -GRID_WIDTH * (2 + cnt) + WIDTH // 2),
            (WIDTH - GRID_WIDTH - WIDTH // 2, -GRID_WIDTH * (2 + cnt) + WIDTH // 2)
        )
    for circle in CIRCLES:
        pen.circle(BLACK, circle, 8)
        
    update()
        
        
@window.when_mouse_down
def mouse_down():
    global player
    row, column = og.math.get_rc_grid(*window.mouse.pos, GRID_WIDTH, GRID_WIDTH)
    if 1 <= row < 20 and 1 <= column < 20:
        if not board[row][column]:
            board[row][column] = player
            og.play_sound(og.builtin.sounds.stone)
            win = og.math.in_row(board, (row, column), player=player)
            if win is None:
                destroy('Withdraw')
                return
            if win:
                destroy(('White' if player == WHITE else 'Black') + ' wins')
                return
            player = WHITE if player == BLACK else BLACK


if __name__ == '__main__':
    window.show()
