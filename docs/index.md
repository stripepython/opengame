OpenGame is a Python3 module that can help you build a game faster.  
Document is writing, this is the dev version.

![Favicon](https://article.biliimg.com/bfs/article/8393f6fcdd2ac4e5d9eaaba6fc6dee3b1fd10bcb.png)

# Theory
OpenGame built on `pygame2`. Many features of `pygame` are retained.   
Therefore, it has good compatibility with `pygame`.

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

# Write the First OpenGame Program
After installing, we'll use OpenGame to write our first game.

First, Import it:
```python
import opengame as og
```
> Note: `og` is our recommended alias, you can use other.  

Then, Create a `Window`:
```python
import opengame as og
window = og.Window('Hello, OpenGame!')  # Create a window
```

After that, Create a `Label` and show it:
```python
import opengame as og
window = og.Window('Hello, OpenGame!')  # Create a window
label = og.Label('Hello, OpenGame!')   # Create a label
label.pack()  # This is really user-friendly, isn't it?
```

Finally, show the window:
```python
import opengame as og
window = og.Window('Hello, OpenGame!')  # Create a window
label = og.Label('Hello, OpenGame!')   # Create a label
label.pack()  # This is really user-friendly, isn't it?
window.show()
```

# Quick Start
If you want to start using `OpenGame` quickly, I think that you should see some examples.

Now, We will try to explain the examples provided by OpenGame.  
These are in `opengame.utils.examples`

## Gluttonous Snake
Source Code:
```python
import opengame as og

def create_food():
    x, y = og.random.randint(-18, 18) * 20, og.random.randint(-13, 13) * 20
    while (x, y) in body:
        x, y = og.random.randint(-18, 18) * 20, og.random.randint(-13, 13) * 20
    return [x, y]


def move(func):
    body.pop()
    head = body[0]
    body.appendleft(func(head))
    
    
def game_over():
    return (
        body[0][0] < -400 or body[0][0] > 400
        or body[0][1] < -300 or body[0][1] > 300
    ) or (body.count(body[0]) > 1 and window.counter > 10 and flag)


def show_over():
    win = og.Window('Game Over', (800, 600))
    og.Background('temp.png').pack()
    win.show()


window = og.Window('Snake', (800, 600), fps=30)

pen = og.Pen()
text = og.Label('Score: 0', font=og.Font(None, 40))
text.pack()

body = og.math.deque([[0, -20], [0, 0], [0, 20]])
food = create_food()

angle = 'up'
score = 0
flag = True

@window.when_draw
def draw():
    global score, food, flag
    
    pen.rect((0, 128, 0), food, (20, 20))
    for i in body:
        pen.rect((128, 0, 0), i, (20, 20))
    
    if window.rates(6):
        if angle == 'up':
            move(lambda pos: [pos[0], pos[1] + 20])
        elif angle == 'down':
            move(lambda pos: [pos[0], pos[1] - 20])
        elif angle == 'left':
            move(lambda pos: [pos[0] - 20, pos[1]])
        elif angle == 'right':
            move(lambda pos: [pos[0] + 20, pos[1]])
        flag = True
    
    if food in body:
        score += 1
        text.set_text(f'Score: {score}')
        food = create_food()
        body.appendleft(body[0])
        flag = False
            
    if game_over():
        window.screenshot('temp.png')
        window.destroy(exit_all=False)
        
        show_over()
    

@window.when_key_down
def key_down():
    global angle
    if window.event.is_down('up') and angle != 'down':
        angle = 'up'
    elif window.event.is_down('down') and angle != 'up':
        angle = 'down'
    elif window.event.is_down('left') and angle != 'right':
        angle = 'left'
    elif window.event.is_down('right') and angle != 'left':
        angle = 'right'
    

if __name__ == '__main__':
    window.show()

```

The explanation is writing...
