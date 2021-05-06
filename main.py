import maze_generator

if __name__ == '__main__':
    print("Выберите алгоритм построения: 0 - dfs, 1 - минимальное остовное дерево")
    type = bool(input())
    print("Введите размер лабиринта")
    size = int(input())
    s = maze_generator.MazeGenerator(type, size, size)
    s.print()
    print("Нужно ли сохранить лабиринт?Y/N")
    is_save = input()
    if is_save == "Y":
        print("Введите название файла")
        filename = input()
        s.save(filename)
