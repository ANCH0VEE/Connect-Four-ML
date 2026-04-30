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

# 4/1/2026
- Group meeting
- Welcome to the group, Nick
- Continue building game state logic:
    - full_board: board is filled when there are 6*7 = 42 chips inserted. Returns if a counter that is incremented with every move played is equal to 42.
    - discussed how we can build method: check_win_state
        - solutions: take last played move. either: 
            a. check all possible groups of 4 around that coordinate, horizontally, vertically, and diagonally.
            b. use a counter to keep track of the number of same colored pieces in a row by expanding outwards in both directions from the last played move.
        - make sure to handle edge-of-board cases. access only existing coordinates.

# 4/8/2026
- Group meeting
- All fundamental game logic finished:
    - check win state method complete: horizontal, vertical, and both diagonals
- Created playable game in terminal, putting all logic together for future convenience.

# 4/15/2026 - 4/16/2026
- Group meeting
- mcts module
- MCTS_Node class
- Slightly generalized Board class method parameters and structure to be used in MCTS_Node class.
- Playable bot, although still misses easy wins and misses blocking player wins. 
- next: organization, add heuristics and neural net.

# 4/16/2026 - ?
- pygame gui
- threading for mcts search (it can be slow)

# 4/29/2026
- Group meeting
- Implemented one move win and block heuristics.
- Replayable game: press r.
- May have suble bugs. Need more testing.
- Started slideshow presentation: presentations and judging next week (Wednesday 5/6/2026).