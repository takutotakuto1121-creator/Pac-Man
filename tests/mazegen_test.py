from mazegenerator import MazeGenerator

mazegen = MazeGenerator()
maze = mazegen.maze
path = mazegen.shortest_path
entry = mazegen.maze_entry
exit = mazegen.maze_exit

print("== mazegenerator test ==")
print("= maze =")
print(maze)
print("= path =")
print(path)
print("= entry =")
print(entry)
print("= exit =")
print(exit)
