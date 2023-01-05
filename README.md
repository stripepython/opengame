OpenGame is a Python3 module that can help you build a game faster.  
Document is writing, this is the dev version.

![Favicon](https://article.biliimg.com/bfs/article/8393f6fcdd2ac4e5d9eaaba6fc6dee3b1fd10bcb.png)

Version: 1.0.2beta

# New
1.0.2alpha: passed the test on `Windows 10` and `Ubuntu`.      
1.0.2beta: deleted `opengame.utils.builtin.builtin` module

# Theory
OpenGame built on `pygame2`. Many features of `pygame` are retained.   
Therefore, it has good compatibility with `pygame`.

# Why do you use OpenGame?
Let's see an example, we'll show a label "Hello World" on the screen. And let it follow the mouse.

If we use `opengame`, we should:
```python
import opengame as og
win = og.Window('Demo', (800, 600))
text = og.Label('Hello World')
text.pack()
@win.when_draw
def draw():
    text.pos = win.mouse.pos
win.show()
```

If we use `pygame`, we should:
```python
import sys
import pygame as pg
pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Demo')
font = pg.font.Font(None, 26)
while True:
    screen.fill((255, 255, 255))
    text = font.render('Hello World', True, (0, 0, 0))
    rect = text.get_rect()
    rect.x, rect.y = pg.mouse.get_pos()
    screen.blit(text, rect)
    for event in pg.event.get():
        if event == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
```

Really easy?

Although using `pyglet` and `opengame` is similar, `opengame` has other reason why you should use it.  
> Note: In large projects, you should still use other packages because `opengame` designed for small projects.

## The Advantages
1. Simple API, callback system;
2. A perfect resource library;
3. Great encapsulation, more functions;
4. Lots of humanity design.

## The Inferiority
1. Instability;
2. Not applicable to large projects.

# Install
Use `pip` install it:
```shell
pip install -U opengame
```
Use `git`:
```shell
git clone https://github.com/stripepython/opengame/
cd opengame
pip install -r requirements.txt
python setup.py install
```

# Where can I see OpenGame?
- PYPI: [https://pypi.org/project/opengame/](https://pypi.org/project/opengame/)
- Github: [https://github.com/stripepython/opengame/](https://github.com/stripepython/opengame/)
- Document: [https://stripepython.github.io/opengame/](https://stripepython.github.io/opengame/)
- CSDN: [https://blog.csdn.net/weixin_38805653?type=blog](https://blog.csdn.net/weixin_38805653?type=blog)

# Document
See [https://github.com/stripepython/opengame/](https://github.com/stripepython/opengame/) or `/docs/index.md`
