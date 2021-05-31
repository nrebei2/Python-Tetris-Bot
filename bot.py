from board import Board, Tetromino
import random, copy, time
import pyautogui

def generatePositions(piece, board):
    Rotations = [piece, copy.copy(piece).rotate_right(), copy.copy(piece).flip(), copy.copy(piece).rotate_left()]
    returnV = []
    for i in range(len(Rotations)):
        npiece = Rotations[i]
        for j in range(board.WIDTH):
            nboard = board.copy()
            row = nboard.drop(npiece, j)
            if row != "Invalid column":
                attr = nboard.attributes()
                v = {'row': row,
                    'column': j,
                    'piece': npiece,
                    'rotations': i}
                vU = {**attr, **v}
                returnV.append(vU)
    return returnV

def findBestPos(drops):
    # lowest_gaps = min([drop['gaps'] for drop in drops])
    # drops = list(filter(lambda drop: drop['gaps'] == lowest_gaps, drops))

    # lowest_height = min([drop['height'] for drop in drops])
    # drops = list(filter(lambda drop: drop['height'] == lowest_height, drops))

    # lowest_row = max([drop['row'] for drop in drops])
    # drops = list(filter(lambda drop: drop['row'] == lowest_row, drops))
    print(drops)
    bestDrop = min(drops, key=lambda x:(0.83236427*x['gaps'] + 0.47959*x['mean'] + 0.60783124*x['std'] - 0.00558445*x['height diff'] + 0.63778202*x['consec']))
    return [bestDrop['piece'], bestDrop['column'], bestDrop['rotations']]

def waitforPiece():
    while True:
        if get_pixel(mouse) in TETROMINO:
            return

TETROMINO = {
    (184, 133, 0): Tetromino.LTetromino,
    (0, 184, 65): Tetromino.STetromino,
    (184, 168, 0): Tetromino.OTetromino,
    (0, 165, 184): Tetromino.ITetromino,
    (0, 115, 184): Tetromino.JTetromino,
    (156, 0, 184): Tetromino.TTetromino,
    (184, 0, 0): Tetromino.ZTetromino
}

def get_pixel(coordinate):
    return pyautogui.screenshot().getpixel(coordinate)

def get_keystrokes(rotations, column, keys):
    # Move to left side of board

    if rotations == 3:
        pyautogui.press(keys['rotate_left'])
    else:
        for i in range(rotations):
            pyautogui.press(keys['rotate_right'])

    for i in range(5):
        pyautogui.press(keys['move_left'], presses=3)
    for i in range(column):
        pyautogui.press(keys['move_right'])

    

    pyautogui.press(keys['drop'])

if __name__ == '__main__':
    mouse = pyautogui.Point(x=942, y=366)
    print("Mouse coordinates: {}".format(mouse))
    board = Board()

    waitforPiece()

    print("starting!")
    while True:
        waitforPiece()

        tetromino = TETROMINO[get_pixel(mouse)]()
        drops = generatePositions(tetromino, board)
        # Find best combination when dropped ()
        drops = findBestPos(drops)
        # place it down
        
        board.drop(drops[0], drops[1])
        #print("rotations: " + str(drops[2]), "column: " + str(drops[1]))

        get_keystrokes(drops[2], drops[1], {
            'rotate_right': 'up',
            'rotate_left': 'z',
            'move_left': 'left',
            'move_right': 'right',
            'drop': ' '
        })
        board.printBoard()

        
