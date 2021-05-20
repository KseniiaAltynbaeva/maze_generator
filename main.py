import maze_generator
import sys
while True:
    print("Выберите способ построение лабиринта: \n  0 - импортировать \n  1 - сгененрировать новый")
    choice = int(input())
    if choice:
        print("Введите количество строк в лабиринте:")
        height = int(input())
        print("Введите количество столбцов в лабиринте:")
        width = int(input())
        print("Выберите алгоритм построения лабиринта: \n 0 - алгоритм Прима \n 1 - алгоритм Крускала"
                " \n 2 - алгоритм поиска в глубину")
        algorithm = int(input())
        maze = maze_generator.Maze(height, width, algorithm)
    else:
        maze = maze_generator.Maze(0, 0, -1)
        print("Введите название файла, из которого нужно считать лабиринт.")
        filename = input()
        maze.read(filename)

    maze.print()
    print("Хотите сохранить лабиринт?Да/Нет")
    agreement = input()
    if agreement == 'Да':
        print("Укажите полный путь до файла. Файл должен иметь расширение .txt")
        filename = input()
        try:
            maze.save(filename)
        except Exception:
            print("Oops! Something went wrong.")
    print("Хотите пройти лабиринт?")
    agreement = input()
    if agreement == 'Да':
        maze.play()
    print("Показать решение?Да/Нет")
    agreement = input().strip().strip()
    print(agreement)
    if agreement[-2:] == 'Да':
        maze.print_solution()
    print("Сгенерировать новый лабиринт? Да/Нет")
    agreement = input()
    if agreement != 'Да':
        break

