# 3/11/2026
- Club meeting
- Project start
- Create TODO, main.
- Create Board class
- Simple game logic to develop later:
    - find next moves
    - check win states
    - player turns
    - placing moves

# 3/13/2026
- Created board layout: 7x6 pytorch tensor: each row is a connect-four column, because of the way pieces are inserted, and working with one row is easier than working with multiple. Transpose at the final step to make it a proper 6x7 connect-four board.
- Tensor used because we might use neural nets later on.
- Continue developing simple game logic:
    - finding next move in columns
    - finding all possible moves

# 3/22/2026
- Continue developing simple game logic:
    - move placement
    - random move placement
    - a basic idea of how player turns will work
    - some other rough restructuring

# 3/25/2026
- Group meeting
- review and clarification of MCTS