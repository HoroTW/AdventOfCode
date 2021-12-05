class board:
    content: list[list[int]]

    def __init__(self, numbers):
        lines = numbers.strip().splitlines()
        self.content = list(list(map(int, single_line.split())) for single_line in lines)

    def calc_score(self) -> int:
        score = 0
        for row in self.content:
            for val in row:
                if val is None:
                    score += 0
                else:
                    score += val
        return score

    def check_win(self) -> bool:
        for row in self.content:
            if row.count(None) == 5:
                return True

        for col in zip(*self.content):
            if col.count(None) == 5:
                return True

        return False

    def mark(self, number) -> bool:
        for r, row in enumerate(self.content):
            for c, val in enumerate(row):
                if val is number:
                    self.content[r][c] = None
        return self.check_win()


numbers: list[int] = []
boards: list[board] = []
board_count = len(boards)


with open("input.txt", encoding="ascii") as f:
    numbers = map(int, f.readline().split(","))
    boards = list(map(board, f.read().split("\n\n")))

for number in numbers:
    for (i, board) in enumerate(boards):
        if board is None:
            continue
        if board.mark(number):
            score = board.calc_score()
            print(f"WON!! Last number: {number}, Score: {score}, Answer 1: {score * number}")
            boards[i] = None
