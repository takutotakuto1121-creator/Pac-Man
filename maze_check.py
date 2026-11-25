from mazegenerator import MazeGenerator

# 1. インスタンスの作成（引数はすべて省略可）
mg = MazeGenerator(
    size=(15, 15),
    perfect=False,
    entry_cell=(0, 0),
    exit_cell=(-1, -1),
    seed=42,
)

# 2. 迷路の生成
mg.generate(seed=41)

# 3. print
print("Entry:", mg.maze_entry)
print("Exit:", mg.maze_exit)
print("Shortest path:", mg.shortest_path)
print("Maze:", mg.maze)
