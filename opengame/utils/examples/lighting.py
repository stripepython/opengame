import opengame as og

GRID_WIDTH = 50
WIDTH = 8

board = [[1] * WIDTH for _ in range(WIDTH)]
window = og.Window('Lighting Game', (GRID_WIDTH * WIDTH, GRID_WIDTH * WIDTH))
black = og.Sprite(og.builtin.sprites.brown, (GRID_WIDTH, GRID_WIDTH))
white = og.Sprite(og.builtin.sprites.white, (GRID_WIDTH, GRID_WIDTH))

@window.when_draw
def draw():
    for row, i in enumerate(board):
        for col, j in enumerate(i):
            if j == 0:
                clone = white.clone()
            else:
                clone = black.clone()
            clone.pos = og.math.to_opengame((row * GRID_WIDTH, col * GRID_WIDTH))
            clone.y -= GRID_WIDTH // 2
            clone.x += GRID_WIDTH // 2
            clone.show()
    if not any(og.math.flatten(board)):
        window.destroy(exit_all=False)
        win()
            
            
@window.when_mouse_down
def mouse_down():
    def reverse(r, c):
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            board[r][c] = 1 - board[r][c]
    
    x, y = og.math.to_pygame(window.mouse.pos)
    x, y = x // GRID_WIDTH, y // GRID_WIDTH
    reverse(x, y)
    reverse(x + 1, y)
    reverse(x - 1, y)
    reverse(x, y - 1)
    reverse(x, y + 1)
    
    
def win():
    new_win = og.Window('Win!', (300, 220))
    og.Label('You win!').pack()
    new_win.show()
    

window.show()
