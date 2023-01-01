import os
import sys
import uuid
import random
import string
from ctypes import cdll
from operator import eq
from math import ceil, sqrt, inf
from typing import List, Any, Callable, Tuple, Optional
from functools import lru_cache
from collections import deque

from pygame.math import Vector2, Vector3, enable_swizzling, disable_swizzling

from ..core.coordinate import CoordinateType, parse, to_pygame, to_opengame
from ..exceptions import OpenGameError

__all__ = ['flatten', 'chunk', 'transpose', 'duplicate_removal', 'distance', 'Vector2',
           'Vector3', 'swizzling', 'mean', 'get_rc_grid', 'get_rc_rect', 'in_row',
           'get_peripheries', 'get_blank_board', 'lighting_game', 'find', 'random_captcha',
           'to_pygame', 'to_opengame', 'deque', 'switch', 'random', 'random_strings',
           'choiceof', 'inv_sqrt', 'integer_log2']


def flatten(array: list):
    """
    碾平列表。
    
    时间复杂度：`O(n^d)`，其中n为列表长度，d为列表嵌套层数
    
    >>> import opengame as og
    >>> og.math.flatten([[1, 2, 3, 4], [5, 6, 7, 8, [9, 10]]])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    if isinstance(array, list):
        return sum(map(flatten, array), [])
    return [array]


def chunk(array: list, step: int):
    """
    切割列表，是opengame.math.flatten(array: list)的反函数。
    
    时间复杂度：`O(nm)`，其中n为列表长度，m为步长
    
    >>> import opengame as og
    >>> og.math.chunk([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 4)
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    >>> og.math.chunk([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)
    [[1, 2, 3, 4, 5], [6, 7, 8, 9]]
    """
    if step == 0:
        return array
    return list(map(lambda x: array[x * step: x * step + step], list(range(ceil(len(array) / step)))))


def transpose(array: List[list]):
    """
    扭转一个二维列表。
    
    时间复杂度：`O(n^2)`，其中n为列表长度
    
    >>> import opengame as og
    >>> og.math.transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    >>> og.math.transpose([[1, 2, 3, 4], [5, 6, 7, 8]])
    [[1, 5], [2, 6], [3, 7], [4, 8]]
    """
    return [list(i) for i in list(zip(*array))]


def _hashable_duplicate_removal(array: list, sort: bool = True):
    res = list(set(array))
    if sort:
        res.sort(key=array.index)
    return res


def _non_hashable_duplicate_removal(array: list):
    res = []
    for i in array:
        if i not in res:
            res.append(i)
    return res
    

def duplicate_removal(array: list, hashable: bool = False, sort: bool = True):
    """
    列表去重。hashable参数表示元素是否为可哈希对象。
    
    时间复杂度：
        当hashable参数为真时：
            sort参数为真：`O(nlogn)`
            
            sort参数为假：`O(n)`
        当hashable参数为假时：`O(n^2)`
    其中n为列表长度
    """
    return _hashable_duplicate_removal(array, sort) if hashable else _non_hashable_duplicate_removal(array)


def distance(point1: CoordinateType, point2: CoordinateType):
    x1, y1 = parse(point1)
    x2, y2 = parse(point2)
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def swizzling(options: bool = True, *args, **kwargs):
    return enable_swizzling(*args, **kwargs) if options else disable_swizzling(*args, **kwargs)


def mean(array: list):
    if not array:
        return 0
    return sum(array) / len(array)


@lru_cache()
def get_rc_grid(x: int, y: int, grid_width: float = 20.0, grid_height: float = 20.0):
    x, y = to_pygame((x, y))
    return round(x / grid_width), round(y / grid_height)


@lru_cache()
def get_rc_rect(x: int, y: int, grid_width: float = 20.0, grid_height: float = 20.0):
    x, y = to_pygame((x, y))
    return x // grid_width, y // grid_height


def in_row(board: List[list], pos: Tuple[int, int], win: int = 5, player: Any = 0,
           judge_hor: bool = True, judge_vert: bool = True, judge_slash: bool = True,
           judge_backslash: bool = True):
    if not any(flatten(board)):
        return None
    hor = vert = slash = backslash = 0
    left = pos[0] - 1
    right = pos[0] + 1
    up = pos[1] - 1
    down = pos[1] + 1
    n = len(board)
    if n != len(board[0]):
        raise OpenGameError('only support n×n board')

    while left > 0 and board[left][pos[1]] == player:
        left -= 1
        hor += 1
    while right < n and board[right][pos[1]] == player:
        right += 1
        hor += 1
    while up > 0 and board[pos[0]][up] == player:
        up -= 1
        vert += 1
    while down < n and board[pos[0]][down] == player:
        down += 1
        vert += 1

    left = pos[0] - 1
    up = pos[1] - 1
    right = pos[0] + 1
    down = pos[1] + 1

    while left > 0 and up > 0 and board[left][up] == player:
        left -= 1
        up -= 1
        backslash += 1
    while right < n and down < n and board[right][down] == player:
        right += 1
        down += 1
        backslash += 1

    right = pos[0] + 1
    up = pos[1] - 1
    left = pos[0] - 1
    down = pos[1] + 1

    while right < n and up > 0 and board[right][up] == player:
        right += 1
        up -= 1
        slash += 1
    while left > 0 and down < n and board[left][down] == player:
        left -= 1
        down += 1
        slash += 1

    if not judge_hor:
        hor = -inf
    if not judge_vert:
        vert = -inf
    if not judge_slash:
        slash = -inf
    if not judge_backslash:
        backslash = -inf
    return max((hor, vert, slash, backslash)) >= win - 1


def get_blank_board(white: Any, width: int, height: Optional[int] = None):
    return [[white] * (height if height else width) for _ in range(width)]


def get_peripheries(x: int, y: int, width: int, height: Optional[int] = None,
                    peripheries: Tuple[Tuple[int, int]] = ((0, 1), (1, 0), (0, -1), (-1, 0))):
    if not height:
        height = width
    res = {(x, y)}
    for tx, ty in peripheries:
        nx, ny = x + tx, y + ty
        if 0 <= nx < width and 0 <= ny < height:
            res.add((nx, ny))
    return res


def lighting_game(board: List[list], white: int = 0, black: int = 1):
    SolveType = List[Tuple[int, int]]
    BoardType = List[List[int]]
    EquationType = List[Tuple[List[Tuple[int, int]], Tuple[int, int]]]
    WIDTH = len(board)
    if WIDTH != len(board[0]):
        raise OpenGameError('only support n×n board')
    
    def equation():
        res = []
        for x in range(WIDTH):
            for y in range(WIDTH):
                peripheries = get_peripheries(x, y, WIDTH)
                res.append((peripheries, (x, y)))
        return res

    def array_to_int(array: SolveType):
        arr = get_blank_board(white, WIDTH)
        for x, y in array:
            arr[x][y] = black
        # flatten = lambda x: [y for L in x for y in flatten(L)] if type(x) is list else [x]
        a = flatten(arr)
        res = [0] * (WIDTH * WIDTH)
        for inx, item in enumerate(a):
            if item == black:
                res[inx] = 1
        res = ''.join(str(i) for i in res)
        return int(res, base=2)
    
    def guassian(equ: EquationType):
        matrix = []
        for xs, pos in equ:
            p = []
            for x, y in xs:
                p.append(x * WIDTH + y)
            a = [0] * (WIDTH * WIDTH)
            for i in p:
                a[i] = 1
            a.append(array_to_int([pos]))
            matrix.append(a)
        return matrix

    def int_to_array(n: int):
        lst = list(bin(n).replace('0b', ''))
        lst = ['0'] * (WIDTH * WIDTH - len(lst)) + lst
        arr = [0] * (WIDTH * WIDTH)
        for inx, item in enumerate(lst):
            if item == '1':
                arr[inx] = black
        arr = chunk(arr, WIDTH)
        return arr
    
    def guass(n: int, matrix: BoardType):
        r = 0
        for c in range(n):
            t = r
            for i in range(r, n):
                if matrix[i][c] == 1:
                    t = i
                    break
        
            if matrix[t][c] == 0:
                continue
            matrix[r], matrix[t] = matrix[t], matrix[r]
        
            for i in range(r + 1, n):
                if matrix[i][c] == 1:
                    for j in range(c, n + 1):
                        matrix[i][j] ^= matrix[r][j]
        
            r += 1
    
        if r < n:
            for i in range(r, n):
                if matrix[i][n] == 1:
                    raise OpenGameError('the equations have no solution')
            raise OpenGameError('the system of equations has multiple sets of solutions')
    
        for i in range(n - 1, -1, -1):
            for j in range(i):
                if matrix[j][i] == 1:
                    matrix[j][n] ^= matrix[i][n]
    
        for i in range(n):
            yield matrix[i][n]
            
    def solve():
        m = guassian(equation())
        res = {}
        for idx, num in enumerate(guass(WIDTH * WIDTH, m)):
            val = int_to_array(num)
            x, y = idx // WIDTH, idx % WIDTH
            res[(x, y)] = val
        return res
    
    def merge(a: BoardType, b: BoardType):
        if not a:
            return b
        if not b:
            return a
        res = get_blank_board(white, WIDTH)
        for x, i in enumerate(a):
            for y, j in enumerate(i):
                k = b[x][y]
                res[x][y] = (white, black)[k == j]
        return res
    
    def get():
        solution = solve()
        res = []
        for x, i in enumerate(board):
            for y, j in enumerate(i):
                if j == black:
                    res.append(solution[(x, y)])
    
        ans = []
        for i in res:
            ans = merge(ans, i)
    
        res = set()
        for x, i in enumerate(ans):
            for y, j in enumerate(i):
                if ans[x][y] == black:
                    res.add((x, y))
        return res
    
    return get()


def find(board: List[list], target: Any):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == target:
                return x, y
    raise OpenGameError(f'{target} not in board')


class switch(object):
    def __init__(self, value: Any, auto_break: bool = False):
        """
        用于替代其他语言的switch-case语法，减少if-elif-else
    
        使用示例：
        >>> import opengame as og
        >>> code = 404
        >>> for case in og.math.switch(code):
        ...     if case(400):
        ...         print('400 Bad Request')
        ...         break
        ...     if case(200):
        ...         print('200 OK')
        ...         break
        ...     if case(404):
        ...         print('404 Not Found')
        ...         break
        ...     print('Error')  # default
        ...
        404 Not Found
    
        :param value: 要匹配的值
        :param auto_break: 匹配到值之后是否默认跳出循环
        """
        self.value = value
        self.auto_break = auto_break
        self.matched = False
        self.to_break = False
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.to_break:
            raise StopIteration
        return self.match
    
    def match(self, *values, is_eq: Callable[[Any, Any], bool] = eq):
        if self.matched:
            return True
        for val in values:
            if is_eq(self.value, val):
                if self.auto_break:
                    self.to_break = True
                self.matched = True
                return True
        return False
    

def random_strings(uuid_no: int = 1, *args, **kwargs):
    if uuid_no not in {1, 3, 4, 5}:
        raise OpenGameError('uuid-no must be 1, 3, 4 or 5')
    functions = [None, uuid.uuid1, None, uuid.uuid3, uuid.uuid4, uuid.uuid5]
    return functions[uuid_no](*args, **kwargs).hex


_DEFAULT_CHARS = string.ascii_letters + string.digits

def random_captcha(length: int = 6, chars: List[str] = _DEFAULT_CHARS):
    return ''.join(random.choice(chars) for _ in range(length))

def choiceof(*items):
    return random.choice(items)


random.randchar = random_strings
random.randcaptcha = random_captcha
random.choiceof = choiceof


def _get_math_dll():
    root = os.path.dirname(__file__)
    name = 'mathc.dll' if sys.platform == 'win32' else 'mathc.so'
    return cdll.LoadLibrary(os.path.join(root, name))


def inv_sqrt(n):
    return _get_math_dll().InvSqrt(n)


def integer_log2(n):
    return _get_math_dll().IntegerLog2(n)
