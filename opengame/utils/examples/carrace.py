import opengame as og


window = og.Window('Car Race', size=(400, 710))
car = og.random.choice([og.builtin.sprites.car17, og.builtin.sprites.car18, og.builtin.sprites.car16])
player = og.Sprite(car, (80, 158))
player.y -= 260
track_idx = og.random.randint(0, 2)
player.x += (track_idx - 1) * 115

bomb = og.Sprite(og.builtin.sprites.bomb, (25, 38))
bombs = []

@window.when_draw
def draw():
    window.fill((44, 252, 226))
    player.show()
    for i in bombs:
        i.y -= og.random.randint(0, 5)
        i.show()
        if i.collide_bottom_edge():
            bombs.remove(i)
        if player.collide(i):
            og.play_sound(og.builtin.sounds.bomb)
            window.screenshot('temp.png')
            game_over(i.pos)
    if window.rates(30):
        s = bomb.clone()
        s.pos = og.random.choice((-135, 0, 135)), og.random.randint(160, 350)
        bombs.append(s)
    if window.rates(45):
        if bombs:
            del bombs[og.random.randint(0, len(bombs) - 1)]
    og.play_sound(og.builtin.sounds.ding)
    
@window.when_key_down
def key_down():
    global track_idx
    if window.event.is_down('left') and track_idx != 0:
        track_idx -= 1
        player.x -= 115
    if window.event.is_down('right') and track_idx != 2:
        track_idx += 1
        player.x += 115
        
def game_over(pos):
    window.destroy(exit_all=False)
    new_win = og.Window('Game Over', (400, 710))
    back = og.Background('temp.png')
    back.pack()
    over = og.Sprite(og.builtin.sprites.gameover1)
    over.pack()
    boom = og.Sprite(og.builtin.sprites.boom)
    boom.pack()
    boom.pos = pos
    new_win.show()


if __name__ == '__main__':
    window.show()
