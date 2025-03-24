import streamlit as st
import numpy as np
import time
import random

# Initialize game state
if 'snake' not in st.session_state:
    st.session_state.snake = [(10, 10)]
    st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
    st.session_state.direction = (0, 1)  # Initial direction: right
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.last_move_time = time.time()
    st.session_state.paused = False

# Game constants
GRID_SIZE = 20
CELL_SIZE = 20
SPEED = 0.2  # seconds between moves

# Functions
def generate_food():
    while True:
        food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if food not in st.session_state.snake:
            return food

def move_snake():
    if st.session_state.game_over or st.session_state.paused:
        return
    
    head = st.session_state.snake[0]
    new_head = (head[0] + st.session_state.direction[0], 
                head[1] + st.session_state.direction[1])
    
    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or 
        new_head in st.session_state.snake):
        st.session_state.game_over = True
        return
    
    st.session_state.snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = generate_food()
    else:
        st.session_state.snake.pop()
    
    st.session_state.last_move_time = time.time()

def change_direction(new_dir):
    # Prevent 180-degree turns
    if (new_dir[0] * -1, new_dir[1] * -1) != st.session_state.direction:
        st.session_state.direction = new_dir

def reset_game():
    st.session_state.snake = [(10, 10)]
    st.session_state.food = generate_food()
    st.session_state.direction = (0, 1)
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.last_move_time = time.time()
    st.session_state.paused = False

# UI Layout
st.title("🐍 Snake Game")

col1, col2 = st.columns([3, 1])
with col1:
    game_placeholder = st.empty()
with col2:
    st.metric("Score", st.session_state.score)
    
    if st.button("⏸️ Pause/Resume"):
        st.session_state.paused = not st.session_state.paused
    
    if st.button("🔄 Restart"):
        reset_game()

# Direction buttons
cols = st.columns(4)
with cols[1]:
    if st.button("↑", key="up"):
        change_direction((-1, 0))
with cols[0]:
    if st.button("←", key="left"):
        change_direction((0, -1))
with cols[2]:
    if st.button("→", key="right"):
        change_direction((0, 1))
with cols[3]:
    if st.button("↓", key="down"):
        change_direction((1, 0))

# Game loop
while True:
    # Draw game board
    canvas = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=np.uint8)
    
    # Draw snake
    for i, (x, y) in enumerate(st.session_state.snake):
        color = (0, 255, 0) if i == 0 else (0, 200, 0)  # Head is brighter green
        canvas[x, y] = color
    
    # Draw food
    canvas[st.session_state.food] = (255, 0, 0)
    
    # Display
    game_placeholder.image(canvas, width=400, caption="Snake Game" if not st.session_state.game_over else "Game Over!")
    
    # Handle game over
    if st.session_state.game_over:
        st.error("Game Over! Press Restart to play again.")
        break
    
    # Automatic movement
    if time.time() - st.session_state.last_move_time > SPEED:
        move_snake()
    
    time.sleep(0.05)