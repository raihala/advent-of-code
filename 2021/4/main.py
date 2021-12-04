def score(board, called):
    win = False
    for i in range(5):
        if (all([x in called for x in board[i]]) or
                all([x in called for x in [row[i] for row in board]])):
            win = True
    if win:
        return sum([x for row in board for x in row if x not in called])
    return None


with open('input') as f:
    lines = list(f)

to_call = [int(x) for x in lines[0].strip().split(',')]
board_lines = lines[1:]
num_boards = len(board_lines) // 6

boards = []
for i in range(num_boards):
    board = []
    for row in board_lines[i*6 + 1:i*6 + 6]:
        board.append(tuple(int(x) for x in row.strip().split()))
    boards.append(tuple(board))

called = []
winner_final_score = None
loser_final_score = None

for call in to_call:
    called.append(call)
    scores = {b: score(b, called) for b in boards}
    losers = [b for b, s in scores.items() if s is None]
    winners = [b for b, s in scores.items() if s is not None]

    if len(winners) == 1 and winner_final_score is None:
        winner_final_score = scores[winners[0]] * call
    if len(losers) == 0:
        prev_scores = {b: score(b, called[:-1]) for b in boards}
        prev_winners = [b for b, s in prev_scores.items() if s is not None]
        tardiest_winners = [s for s in winners if s not in prev_winners]
        loser_final_score = scores[tardiest_winners[0]] * call
        break

print(winner_final_score)
print(loser_final_score)
