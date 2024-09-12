import random

class CarbonBlock:
    def __init__(self, shape, carbon_value):
        self.shape = shape
        self.carbon_value = carbon_value  # 양수: 배출, 음수: 흡수

class CarbonTetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_block = None
        self.score = 0
        self.carbon_balance = 0

    def new_block(self):
        shapes = [
            [[1, 1], [1, 1]],  # 공장 (높은 배출)
            [[1, 1, 1]],       # 자동차 (중간 배출)
            [[1], [1], [1]],   # 빌딩 (낮은 배출)
            [[0, 1, 0], [1, 1, 1]],  # 나무 (흡수)
            [[1, 1, 1, 1]]     # 태양 전지판 (높은 흡수)
        ]
        carbon_values = [10, 5, 2, -3, -8]
        shape = random.choice(shapes)
        carbon_value = carbon_values[shapes.index(shape)]
        self.current_block = CarbonBlock(shape, carbon_value)

    def move(self, direction):
        if self.current_block:
            dx = -1 if direction == "left" else 1 if direction == "right" else 0
            new_x = self.current_block_x + dx
            if self.is_valid_position(self.current_block.shape, new_x, self.current_block_y):
                self.current_block_x = new_x
                return True
        return False

    def rotate(self):
        if self.current_block:
            rotated_shape = list(zip(*self.current_block.shape[::-1]))
            if self.is_valid_position(rotated_shape, self.current_block_x, self.current_block_y):
                self.current_block.shape = rotated_shape
                return True
        return False

    def drop(self):
        if self.current_block:
            while self.is_valid_position(self.current_block.shape, self.current_block_x, self.current_block_y + 1):
                self.current_block_y += 1
            self.place_block()
            return True
        return False

    def check_lines(self):
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(self.width)])
        return len(full_lines)

    def update_carbon_balance(self):
        self.carbon_balance += self.current_block.carbon_value
        if self.carbon_balance == 0:
            self.score += 100  # 탄소 중립 보너스
        self.score += 10  # 기본 점수

    def game_over(self):
        return any(self.grid[0])  # 가장 위 줄에 블록이 있으면 게임 오버

    def is_valid_position(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if (x + j < 0 or x + j >= self.width or
                        y + i >= self.height or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True

    def place_block(self):
        for i, row in enumerate(self.current_block.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_block_y + i][self.current_block_x + j] = cell
        self.update_carbon_balance()
        lines_cleared = self.check_lines()
        self.score += lines_cleared * 100  # 줄 제거 보너스
        self.new_block()

    def new_block(self):
        # ... (이전 코드 유지)
        self.current_block_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_block_y = 0

# 게임 상태 업데이트 함수
def update_game_state(game):
    if game.current_block is None:
        game.new_block()
    
    game.current_block_y += 1
    if not game.is_valid_position(game.current_block.shape, game.current_block_x, game.current_block_y):
        game.current_block_y -= 1
        game.place_block()
        if game.game_over():
            return "Game Over"
    
    return "Continue"
