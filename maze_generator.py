import random
import sys
from colorama import Fore, Style
import os
import keyboard
os.system('cls' if os.name == 'nt' else 'clear')
sys.setrecursionlimit(20000)


class Edge:
    def __init__(self, start, finish):
        self.start = min(start, finish)
        self.finish = max(start, finish)

    def __lt__(self, other):
        if min(self.start, self.finish) == min(other.start, other.finish):
            if max(self.finish, self.start) < max(other.finish, other.start):
                return True
        elif min(self.start, self.finish) < min(other.start, other.finish):
            return True
        return False

    def __eq__(self, other):
        if (min(self.start, self.finish) == min(other.start, other.finish)
                and max(self.start, self.finish) == max(other.start, other.finish)):
            return True
        return False

    def __hash__(self):
        return hash(self.start * + self.finish)


class Maze:
    def __init__(self, height, width, algorithm):
        self.edges = list()
        self.height = height
        self.width = width
        self.choose_algorithm(algorithm)

    def choose_algorithm(self, algorithm):
        if algorithm == 0:
            self.prims_algorithm()
        elif algorithm == 1:
            self.kruskal_algorithm()
        elif algorithm == 2:
            self.recursive_backtracker()

    def get_neighbours(self, vertex):
        line = vertex // self.width
        column = vertex % self.width
        possible_neighbors = list()
        possible_neighbors.append([line + 1, column])
        possible_neighbors.append([line - 1, column])
        possible_neighbors.append([line, column + 1])
        possible_neighbors.append([line, column - 1])
        neighbours = list()
        for neighbour in possible_neighbors:
            if 0 <= neighbour[0] < self.height and 0 <= neighbour[1] < self.width:
                neighbours.append(neighbour)
        return neighbours

    def prims_algorithm(self):
        visited = [False] * (self.width * self.height)
        visited[0] = True
        queue = self.get_neighbours(0)
        edges = list()
        for vertex in queue:
            edges.append(Edge(0, vertex[0] * self.width + vertex[1]))
        while len(edges) != 0:
            random.shuffle(edges)
            edge = edges.pop()
            if visited[edge.finish]:
                continue
            visited[edge.finish] = True
            self.edges.append(edge)
            queue = self.get_neighbours(edge.finish)
            for vertex in queue:
                edges.append(Edge(edge.finish, vertex[0] * self.width + vertex[1]))
            random.shuffle(edges)
        self.edges.sort()

    def kruskal_algorithm(self):
        def get(vertex, prev):
            if prev[vertex] == -1:
                return vertex
            else:
                prev[vertex] = get(prev[vertex], prev)
                return prev[vertex]

        def unite(u, v, size, prev):
            u = get(u, prev)
            v = get(v, prev)
            if u == v:
                return
            if size[u] < size[v]:
                u, v = v, u
            prev[v] = u
            size[u] += size[v]

        prev = [-1] * (self.width * self.height)
        size = [1] * (self.width * self.height)
        possible_edges = set()
        for i in range(self.width * self.height):
                queue = self.get_neighbours(i)
                for vertex in queue:
                    possible_edges.add(Edge(i, vertex[0] * self.width + vertex[1]))
        edges = list(possible_edges)
        random.shuffle(edges)
        while len(edges):
            front = edges.pop()
            if get(front.start, prev) != get(front.finish, prev):
                self.edges.append(front)
                unite(front.start, front.finish, size, prev)
        self.edges.sort()

    def recursive_backtracker(self):
        def dfs(used, prev, vertex):
            used[vertex] = True
            if prev != -1:
                self.edges.append(Edge(prev, vertex))
            neighbours = self.get_neighbours(vertex)
            random.shuffle(neighbours)
            for neighbour in neighbours:
                if not used[neighbour[0] * self.width + neighbour[1]]:
                    dfs(used, vertex, neighbour[0] * self.width + neighbour[1])
        used = [False] * (self.width * self.height)
        dfs(used, -1, 0)

    def solve(self):
        def dfs(used, prev, prev_vert, matrix, vertex):
            used[vertex] = True
            prev[vertex] = prev_vert
            for neighbour in matrix[vertex]:
                if not used[neighbour]:
                    dfs(used, prev, vertex, matrix, neighbour)

        start = 0
        finish = self.width * self.height - 1
        prev = [-1] * self.width * self.height
        matrix = [[0] for _ in range(self.width * self.height)]
        used = [False] * self.width * self.height
        for edge in self.edges:
            matrix[edge.start].append(edge.finish)
            matrix[edge.finish].append(edge.start)
        used[start] = True
        dfs(used, prev, -1,  matrix, start)
        current = finish
        solution = []
        while current != start:
            solution.append(Edge(current, prev[current]))
            current = prev[current]
        return sorted(solution)

    def print_solution(self):
        sys.stdout.flush()
        solution = self.solve()
        visualisation = self.build_maze()
        for edge in solution:
            prev_start_column = edge.start % self.width
            prev_start_line = edge.start // self.width
            prev_finish_column = edge.finish % self.width
            prev_finish_line = edge.finish // self.width
            new_start_column = prev_start_column * 2 + 1
            new_start_line = prev_start_line * 2 + 1
            new_finish_column = prev_finish_column * 2 + 1
            new_finish_line = prev_finish_line * 2 + 1
            wall_column = (new_start_column + new_finish_column) // 2
            wall_line = (new_start_line + new_finish_line) // 2
            visualisation[wall_line][wall_column] = '*'
            visualisation[new_start_line][new_start_column] = '*'
            visualisation[new_finish_line][new_finish_column] = '*'
            visualisation[1][0] = '*'
            visualisation[2 * self.height - 1][2 * self.width] = '*'
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if visualisation[i][j] == '*':
                    print(Fore.GREEN + visualisation[i][j], end=' ')
                    print(Style.RESET_ALL, end='')
                else:
                    print(visualisation[i][j], end=' ')
            print()
        sys.stdout.flush()

    def save(self, filename):
        visualisation = self.build_maze()
        file = open(filename, 'w')
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                file.write(visualisation[i][j]+" ")
            file.write('\n')
        file.close()

    def read(self, filename):
        file = open(filename, 'r')
        lines = file.read().split('\n')
        for j in range(len(lines)):
            newline = str()
            for i in range(len(lines[j])):
                if i % 2:
                    continue
                newline += lines[j][i]
            lines[j] = newline
        lines.pop()
        self.height = (len(lines) - 1) // 2
        self.width = (len(lines[0]) - 1) // 2
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if (i % 2 == 0 or j % 2 == 0) and (i != 2 * self.height - 1 or j != 2*self.width) and j != 0:
                    if lines[i][j] == ' ':
                        if i % 2 != 0:
                            vis_line = (i - 1) // 2
                            vis_column_left = (j - 1 - 1) // 2
                            vis_column_right = (j - 1 + 1) // 2
                            start = self.width * vis_line + vis_column_left
                            finish = self.width * vis_line + vis_column_right
                            self.edges.append(Edge(start, finish))
                        if j % 2 != 0:
                            vis_column = (j - 1) // 2
                            vis_line_left = (i - 1 - 1) // 2
                            vis_line_right = (i - 1 + 1) // 2
                            start = self.width * vis_line_left + vis_column
                            finish = self.width * vis_line_right + vis_column
                            self.edges.append(Edge(start, finish))
        file.close()

    def build_maze(self):
        visualisation = [['$'] * (2 * self.width + 1) for _ in range(1 + 2 * self.height)]
        for edge in self.edges:
            prev_start_column = edge.start % self.width
            prev_start_line = edge.start // self.width
            prev_finish_column = edge.finish % self.width
            prev_finish_line = edge.finish // self.width
            new_start_column = prev_start_column * 2 + 1
            new_start_line = prev_start_line * 2 + 1
            new_finish_column = prev_finish_column * 2 + 1
            new_finish_line = prev_finish_line * 2 + 1
            wall_column = (new_start_column + new_finish_column) // 2
            wall_line = (new_start_line + new_finish_line) // 2
            visualisation[wall_line][wall_column] = ' '
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if i % 2 == 1 and j % 2 == 1:
                    visualisation[i][j] = ' '
        visualisation[1][0] = ' '
        visualisation[2 * self.height - 1][2 * self.width] = ' '
        return visualisation

    def print(self):
        visualisation = self.build_maze()
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                print(visualisation[i][j], end=' ')
            print()

    def play(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Используйте стрелочки для игры! Нажмите ctrl, чтобы выйти.")
        visualisation = self.build_maze()
        visualisation[1][0] = '*'
        current_position = [1, 0]
        possible_coord = current_position[:]
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                print(visualisation[i][j], end=' ')
            print()
        sys.stdout.flush()

        while current_position != [2 * self.height - 1, 2 * self.width]:
            key = keyboard.read_key()
            if key == "ctrl":
                break
            if key == "up":
                possible_coord = [current_position[0] - 1, current_position[1]]
            if key == "right":
                possible_coord = [current_position[0], current_position[1] + 1]
            if key == "down":
                possible_coord = [current_position[0] + 1, current_position[1]]
            if key == "left":
                possible_coord = [current_position[0], current_position[1] - 1]
            if visualisation[possible_coord[0]][possible_coord[1]] == "$":
                print("Здесть пройти нельзя!")
                sys.stdout.flush()
                continue
            visualisation[current_position[0]][current_position[1]] = ' '
            current_position = possible_coord[:]
            visualisation[current_position[0]][current_position[1]] = '*'
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Используйте стрелочки для игры!Нажмите ctrl, чтобы выйти.")
            for i in range(2 * self.height + 1):
                for j in range(2 * self.width + 1):
                    print(visualisation[i][j], end=' ')
                print()
            sys.stdout.flush()
