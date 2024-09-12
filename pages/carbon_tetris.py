import streamlit as st
import random
import time

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
        self.current_block_x = 0
        self.current_block_y = 0
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
        self.current_block_x = self.width // 2 - len(self.current_block.shape[0]) // 2
        self.current_block_y = 0

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

def visualize_game(game):
    st.write(f"Score: {game.score}")
    st.write(f"Carbon Balance: {game.carbon_balance}")
    
    # 게임 그리드를 HTML 테이블로 표현
    html = "<table style='border-collapse: collapse;'>"
    for i, row in enumerate(game.grid):
        html += "<tr>"
        for j, cell in enumerate(row):
            color = "lightblue" if cell else "white"
            # 현재 블록 위치 표시
            if game.current_block and game.current_block_y <= i < game.current_block_y + len(game.current_block.shape) and \
               game.current_block_x <= j < game.current_block_x + len(game.current_block.shape[0]):
                if game.current_block.shape[i - game.current_block_y][j - game.current_block_x]:
                    color = "blue"
            html += f"<td style='width: 20px; height: 20px; border: 1px solid gray; background-color: {color};'></td>"
        html += "</tr>"
    html += "</table>"
    
    st.markdown(html, unsafe_allow_html=True)

def main():
    st.title("Carbon Neutral Tetris")

    # 세션 상태 초기화
    if 'game' not in st.session_state:
        st.session_state.game = CarbonTetris(10, 20)
        st.session_state.game.new_block()
    
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    # 게임 컨트롤
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Left") and not st.session_state.game_over:
            st.session_state.game.move('left')
    with col2:
        if st.button("Right") and not st.session_state.game_over:
            st.session_state.game.move('right')
    with col3:
        if st.button("Rotate") and not st.session_state.game_over:
            st.session_state.game.rotate()
    with col4:
        if st.button("Drop") and not st.session_state.game_over:
            st.session_state.game.drop()

    # 게임 상태 업데이트
    if not st.session_state.game_over:
        status = update_game_state(st.session_state.game)
        if status == "Game Over":
            st.session_state.game_over = True

    # 게임 시각화
    visualize_game(st.session_state.game)

    # 게임 오버 체크
    if st.session_state.game_over:
        st.error("Game Over!")
        if st.button("Restart"):
            st.session_state.game = CarbonTetris(10, 20)
            st.session_state.game.new_block()
            st.session_state.game_over = False
            st.rerun()

    # 게임이 진행 중일 때만 자동 리프레시
    if not st.session_state.game_over:
        time.sleep(0.5)  # 게임 속도 조절
        st.rerun()

if __name__ == "__main__":
    main()
