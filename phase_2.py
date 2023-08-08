# Phase 2
# Name:
# DING Xiangyuan
# XUE Yayun
# ZHUMANAZAROV Magzhan
# Student ID:
# 4014815
# 4024860
# 4165121
# Course code: CDS2002
# Section: CRN165
# email: xiangyuanding@ln.hk   yayunxue@ln.hk   magzhanzhumanazarov@ln.hk
# Description:
# This file contains test_sovability(), generate_rand_puzzle(), detect_location(), detect_move(), proceed_moves(),
# uniform_cost_search(), print_ucs(), findnumber(), h(), solution_path(), a_star(), showInfo(), getEmptyPos(),
# generateSubStates(), BFS(), print_bfs(), h_tiles, node class, State class, myApp class, button1click, button2click, drawpath():
# ,rightbuttonclick(), leftbuttonclick(), button3click():
#
# test_sovability() is to test the solvability
# generate_rand_puzzle() is to generate a random puzzle
# detect_location() to detect the location of '#'
# detect_move() to find how many possible directions can '#' move to
# proceed_moves() to output a list of all possible moves given the initial state
# uniform_cost_search() conduct the uniform cost search and output a list
# print_ucs() is for printing the result of the uniform cost search
# findnumber(): finds given number in a given state and returns its position
# h(): heuristics function based on manhattan distance
# solution_path(): finds the path from initial state to given state
# a_star(): implements the A* star algorithm
# showInfo() is to print the array in the correct form
# getEmptyPos() is to detect the location of '#'
# generateSubStates() to find possible directions can '#' move to
# BFS() is the best first search
# print_bfs() to conduct BFS and other function
# node class: represents a puzzle state, with its parents, puzzle in the array form and heuristics value
# State class: represents a puzzle state, with its parents, puzzle in the array form, direction which it took and heuristics value
# myApp class: GUI of the program, containing all its processes
# button1click(): function of SOLVE button, solves the puzzle and outputs the running time and steps
# button2click(): function of RANDOM button, generates random solvable puzzle
# drawpath(): takes a puzzle array and displays it
# rightbuttonclick() and leftbuttonclick(): functions for left and right buttons
# button3click(): function of COMPARE button, generates and solves 10 random puzzles, obtaining running time and steps of each algorithm


from random import shuffle
import queue
from copy import deepcopy
import time
import numpy as np
from tkinter import *


# this part is for checking the sovability and generating a random puzzle


def test_sovability(state):
    # to test the sovability
    original_set = []
    rest = []
    inversions = 0

    for i in state:
        for j in i:
            if j != 0:
                original_set.append(j)

    rest = deepcopy(original_set)

    for l in original_set:

        rest.remove(l)
        for k in rest:
            if l > k:
                inversions = inversions + 1

    if inversions % 2 == 0:
        return True
    if inversions % 2 == 1:
        return False


def generate_rand_puzzle():
    # to generate a random puzzle
    c = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    list_1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while True:
        shuffle(list_1)
        for i in range(9):
            c[i // 3][i % 3] = list_1[i]
        if test_sovability(c) is True:
            return c


# this part is for uniform cost search


def detect_location(state):
    # to detect the location of '#'
    for i in state:
        for j in i:
            if j == 0:
                x = i.index(j)
                y = state.index(i)
    return x, y


def detect_move(state):
    # to find how many possible directions can '#' move to
    x, y = detect_location(state)
    up = y - 1
    down = y + 1
    right = x + 1
    left = x - 1

    possible_moves = ['up', 'down', 'right', 'left']

    real_possible = []
    for i in possible_moves:
        if eval(i) >= 0 and eval(i) <= 2:
            real_possible.append(i)

    return real_possible


def proceed_moves(state):
    # to output a list of all possible moves given the initial state
    state_1 = []
    result = []

    for i in detect_move(state):
        if i == "up":
            state_1 = deepcopy(state)
            x, y = detect_location(state_1)
            state_1[y][x] = state_1[y - 1][x]
            y = y - 1
            state_1[y][x] = 0
            result.append(state_1)

        elif i == 'down':
            state_1 = deepcopy(state)
            x, y = detect_location(state_1)
            state_1[y][x] = state_1[y + 1][x]
            y = y + 1
            state_1[y][x] = 0
            result.append(state_1)

        elif i == 'right':
            state_1 = deepcopy(state)
            x, y = detect_location(state_1)
            state_1[y][x] = state_1[y][x + 1]
            x = x + 1
            state_1[y][x] = 0
            result.append(state_1)

        elif i == 'left':
            state_1 = deepcopy(state)
            x, y = detect_location(state_1)
            state_1[y][x] = state_1[y][x - 1]
            x = x - 1
            state_1[y][x] = 0
            result.append(state_1)

    return result


def uniform_cost_search(state, state_2):
    # uniform cost search

    do_list = []
    transfer_list = []
    done_list = []
    key_number = 0
    key_number_list = []
    for i in proceed_moves(state):
        key_number = key_number + 1
        i.insert(0, [key_number])
        do_list.append(i)
        done_list.append(i)

    solved = 0
    key_list = []
    path = []
    count = 0

    while solved == 0:
        if count == 5000:
            return None

        for i in do_list:

            if [i[1], i[2], i[3]] == state_2:
                solved = 1

                return i, done_list

            elif [i[1], i[2], i[3]] != state_2:
                key_number_list = []
                key_number_list = deepcopy(i[0])

                for j in proceed_moves([i[1], i[2], i[3]]):
                    key_number = key_number + 1
                    key_number_list.append(key_number)
                    j.insert(0, key_number_list)
                    transfer_list.append(deepcopy(j))
                    key_number_list.remove(key_number)

        do_list = []
        do_list = deepcopy(transfer_list)
        transfer_list = []
        done_list.append(deepcopy(do_list))
        count += 1


def print_ucs(i_done_list):
    # to print the result
    if i_done_list is None:
        return None
    path_list = []

    i = i_done_list[0]
    done_list = i_done_list[1]
    key_list = []
    key_list_1 = []
    c = 0
    step = 0

    for j in i[0]:
        c = c + 1
        for k in range(c):
            key_list_1.append(i[0][k])
        key_list.append(deepcopy(key_list_1))
        key_list_1 = []

    for l in done_list:
        for j in key_list:
            if l[0] == j:
                path_list.append(l)
            for m in l:
                if m[0] == j:
                    path_list.append(m)

    return path_list


# this part is for a star search


class node:
    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state
        self.h = 0

    def __eq__(self, other):
        return self.state == other.state


def findnumber(state, number):
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == number:
                return i, j


def h(state, goal_state):
    manht = 0
    for i in range(0, 3):
        for j in range(0, 3):
            bij = state[i][j]
            i_b = i
            j_b = j
            i_g, j_g = findnumber(goal_state, bij)

            manht += (abs(i_g - i_b) + abs(j_g - j_b))
    return manht


def solution_path(some_node):
    path = []
    t = some_node
    while t is not None:
        path.append(t.state)
        t = t.parent
    path = path[::-1]
    return path


def a_star(initial, goal):
    initial_state = node(None, list(initial))
    initial_state.h = 0
    goal_state = node(None, list(goal))
    goal_state.h = 0
    not_visited = []
    visited = []

    not_visited.append(initial_state)
    iterations = 0
    max_iterations = 10000

    while len(not_visited) > 0:
        iterations += 1
        current_node = not_visited[0]
        current_index = 0
        for index, item in enumerate(not_visited):
            if item.h < current_node.h:
                current_node = item
                current_index = index

        not_visited.pop(current_index)
        visited.append(current_node)
        if iterations == max_iterations:
            return 0

        if current_node.state == goal_state.state:
            return solution_path(current_node)

        y, x = findnumber(current_node.state, 0)
        children = []
        if x != 0:
            temp = 0
            l = deepcopy(current_node.state)
            temp = l[y][x - 1]
            l[y][x - 1] = l[y][x]
            l[y][x] = temp
            if len([visited_child for visited_child in visited if visited_child.state == l]) == 0:
                children.append(node(current_node, l))
        if x != 2:
            temp = 0
            r = deepcopy(current_node.state)
            temp = r[y][x + 1]
            r[y][x + 1] = r[y][x]
            r[y][x] = temp
            if len([visited_child for visited_child in visited if visited_child.state == r]) == 0:
                children.append(node(current_node, r))
        if y != 2:
            temp = 0
            d = deepcopy(current_node.state)
            temp = d[y + 1][x]
            d[y + 1][x] = d[y][x]
            d[y][x] = temp
            if len([visited_child for visited_child in visited if visited_child.state == d]) == 0:
                children.append(node(current_node, d))
        if y != 0:
            temp = 0
            u = deepcopy(current_node.state)
            temp = u[y - 1][x]
            u[y - 1][x] = u[y][x]
            u[y][x] = temp
            if len([visited_child for visited_child in visited if visited_child.state == u]) == 0:
                children.append(node(current_node, u))

        for child in children:
            child.h = h(child.state, goal)
            if len([i for i in not_visited if child == i]) > 0:
                continue
            not_visited.append(child)


# this part is for the best first search


class State:
    def __init__(self, state, directionFlag=None, parent=None):
        self.state = state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
            # record the possible directions to generate the sub-states
        self.parent = parent
        self.heu = 0

    def showInfo(self):
        for i in range(3):
            print(self.state[i, 0], self.state[i, 1], self.state[i, 2])

        print("\n")
        return

    def getEmptyPos(self):
        postion = np.where(self.state == 0)
        return postion

    def generateSubStates(self):
        if not self.direction:
            return []
        subStates = []
        key_x, key_y = self.getEmptyPos()
        if 'left' in self.direction and key_y > 0:
            s = self.state.copy()
            s[key_x, key_y], s[key_x, key_y - 1] = s[key_x, key_y - 1], s[key_x, key_y]
            news = State(s, directionFlag='right', parent=self)
            subStates.append(news)
        if 'up' in self.direction and key_x > 0:
            s = self.state.copy()
            s[key_x, key_y], s[key_x - 1, key_y] = s[key_x - 1, key_y], s[key_x, key_y]
            news = State(s, directionFlag='down', parent=self)
            subStates.append(news)
        if 'down' in self.direction and key_x < 2:
            s = self.state.copy()
            s[key_x, key_y], s[key_x + 1, key_y] = s[key_x + 1, key_y], s[key_x, key_y]
            news = State(s, directionFlag='up', parent=self)
            subStates.append(news)
        if self.direction.count('right') and key_y < 2:
            s = self.state.copy()
            s[key_x, key_y], s[key_x, key_y + 1] = s[key_x, key_y + 1], s[key_x, key_y]
            news = State(s, directionFlag='left', parent=self)
            subStates.append(news)
        return subStates

    def BFS(self, initState, goalState):
        openTable = []
        closeTable = []
        # append the origin state to the openTable
        openTable.append(self)
        steps = 1
        # start the loop
        while len(openTable) > 0:
            n = openTable[0]
            n_index = 0
            for index, x in np.ndenumerate(openTable):
                if x.heu < n.heu:
                    n = x
                    n_index = index[0]
            openTable.pop(n_index)
            closeTable.append(n)
            subStates = n.generateSubStates()
            path = []
            for s in subStates:
                s.heu = h_tiles(s.state, goalState)
                if (s.state == goalState).all():
                    path.append(initState.state)
                    while s.parent and s != initState:
                        path.append(s.state)
                        s = s.parent
                    path.reverse()
                    return path
                if (s not in closeTable):
                    openTable.append(s)

            steps += 1
            if steps == 10000:
                return None


def h_tiles(state_1, state_2):
    heu = 0
    for i in range(3):
        for j in range(3):
            if state_1[i][j] != state_2[i][j]:
                heu += 1
    return heu


def print_bfs(state_1, state_2):
    # print the result of best first search
    init_state = State(np.array(state_1))
    goal_state = np.array(state_2)
    s1 = State(state=init_state.state)
    solution = s1.BFS(init_state, goal_state)
    if solution is None:
        return 0
    else:
        path = []
        for i in solution:
            path.append(i)
        return path


# this part is for the main function
class MyApp:
    def __init__(self, myParent):
        self.b = [[], [], []]
        self.a = [[], [], []]
        self.c = [[], [], []]
        self.ucs = [[], [], []]
        self.bfs = [[], [], []]
        self.a_star_path = []
        self.a_star_index = 0
        self.ucs_path = []
        self.ucs_index = -1
        self.bfs_path = []
        self.bfs_index = 0
        self.random = 0
        self.a_star_rt = StringVar()
        self.a_star_steps = StringVar()
        self.ucs_rt = StringVar()
        self.ucs_steps = StringVar()
        self.bfs_rt = StringVar()
        self.bfs_steps = StringVar()
        self.rt = []
        self.steps = []

        self.buttonContainer = Frame(myParent)
        self.buttonContainer.grid(row=0, column=0)
        self.button1 = Button(self.buttonContainer, text="SOLVE", background="green", command=self.button1click)
        self.button2 = Button(self.buttonContainer, text="RANDOM", background="yellow", command=self.button2click)
        self.button1.grid(row=3, column=1)
        self.button2.grid(row=3, column=2)
        self.button3 = Button(self.buttonContainer, text="COMPARE", background="cyan", command=self.button3click)
        self.button3.grid(row=3, column=3)

        self.myContainer1 = Frame(myParent)
        self.myContainer1.grid(row=2, column=0)
        self.initlabel = Label(myParent, text="Initial state:")
        self.initlabel.grid(row=1, column=0)
        for i in range(3):
            for j in range(3):
                self.b[i].append(self.entry(self.myContainer1))
                self.b[i][j].grid(row=i, column=j)

        self.myContainer2 = Frame(myParent)
        self.myContainer2.grid(row=2, column=1)
        self.goallabel = Label(myParent, text="Goal state:")
        self.goallabel.grid(row=1, column=1)
        for i in range(3):
            for j in range(3):
                self.a[i].append(self.entry(self.myContainer2))
                self.a[i][j].grid(row=i, column=j)

        self.solutionContainer = Frame(myParent)
        self.solutionContainer.grid(row=3, column=0)
        self.text1 = Label(self.solutionContainer, text="A*")
        self.text1.grid(row=0, column=1, columnspan=2)
        self.leftButton = Button(self.solutionContainer, text="<", command=self.leftButtonclick)
        self.rightButton = Button(self.solutionContainer, text=">", command=self.rightButtonclick)
        self.leftButton.grid(row=1, column=0)
        self.rightButton.grid(row=1, column=4)
        for i in range(3):
            for j in range(3):
                self.c[i].append(self.entry(self.solutionContainer))
                self.c[i][j].grid(row=i + 1, column=j + 1, pady="3")
                self.c[i][j].config(state="readonly")
        self.text11 = Label(self.solutionContainer, textvariable=self.a_star_rt)
        self.text11.grid(row=4, column=0, columnspan=5)
        self.text12 = Label(self.solutionContainer, textvariable=self.a_star_steps)
        self.text12.grid(row=5, column=0, columnspan=5)

        self.text2 = Label(self.solutionContainer, text="UCS")
        self.text2.grid(row=0, column=6, columnspan=2)
        self.leftButton1 = Button(self.solutionContainer, text="<", command=self.leftButton1click)
        self.rightButton1 = Button(self.solutionContainer, text=">", command=self.rightButton1click)
        self.leftButton1.grid(row=1, column=5)
        self.rightButton1.grid(row=1, column=9)
        for i in range(3):
            for j in range(3):
                self.ucs[i].append(self.entry(self.solutionContainer))
                self.ucs[i][j].grid(row=i + 1, column=j + 6, pady="3")
                self.ucs[i][j].config(state="readonly")
        self.text21 = Label(self.solutionContainer, textvariable=self.ucs_rt)
        self.text21.grid(row=4, column=5, columnspan=5)
        self.text22 = Label(self.solutionContainer, textvariable=self.ucs_steps)
        self.text22.grid(row=5, column=5, columnspan=5)

        self.text3 = Label(self.solutionContainer, text="BFS")
        self.text3.grid(row=0, column=11, columnspan=2)
        self.leftButton2 = Button(self.solutionContainer, text="<", command=self.leftButton2click)
        self.rightButton2 = Button(self.solutionContainer, text=">", command=self.rightButton2click)
        self.leftButton2.grid(row=1, column=10)
        self.rightButton2.grid(row=1, column=14)
        for i in range(3):
            for j in range(3):
                self.bfs[i].append(self.entry(self.solutionContainer))
                self.bfs[i][j].grid(row=i + 1, column=j + 11, pady="3")
                self.bfs[i][j].config(state="readonly")
        self.text31 = Label(self.solutionContainer, textvariable=self.bfs_rt)
        self.text31.grid(row=4, column=10, columnspan=5)
        self.text32 = Label(self.solutionContainer, textvariable=self.bfs_steps)
        self.text32.grid(row=5, column=10, columnspan=5)

        self.out = Text(myParent)
        self.out.grid(row=4)

    def entry(self, parent):
        return Entry(parent, width="2")

    def button1click(self):
        self.a_star_index = 0
        self.ucs_index = 0
        self.bfs_index = 0
        init_state = [[], [], []]
        goal_state = [[], [], []]
        for i in range(3):
            for j in range(3):
                init_state[i].append(int(self.b[i][j].get()))
        for i in range(3):
            for j in range(3):
                goal_state[i].append(int(self.a[i][j].get()))
        start_time_1 = time.time()
        self.a_star_path = a_star(init_state, goal_state)
        stop_time_1 = time.time() - start_time_1
        self.a_star_rt.set("Run time:" + str(stop_time_1)[0:10])
        self.a_star_steps.set("Steps: " + str(len(self.a_star_path) - 1))
        if self.random == 0:
            start_time_2 = time.time()
            self.ucs_path = print_ucs(uniform_cost_search(init_state, goal_state))
            stop_time_2 = time.time() - start_time_2
            for i in range(len(self.ucs_path)):
                self.ucs_path[i].pop(0)
            self.ucs_rt.set("Run time:" + str(stop_time_2)[0:10])
            self.ucs_steps.set("Steps: " + str(len(self.ucs_path)))
        else:
            self.ucs_rt.set("UCS has failed")
            self.random = 0
        start_time_3 = time.time()
        self.bfs_path = print_bfs(init_state, goal_state)
        stop_time_3 = time.time() - start_time_3
        self.bfs_rt.set("Run time:" + str(stop_time_3)[0:10])
        self.bfs_steps.set("Steps: " + str(len(self.bfs_path) - 1))
        for i in range(3):
            for j in range(3):
                self.c[i][j].config(state="normal")
                self.ucs[i][j].config(state="normal")
                self.bfs[i][j].config(state="normal")
                self.c[i][j].delete(0)
                self.c[i][j].insert(0, init_state[i][j])
                self.ucs[i][j].delete(0)
                self.ucs[i][j].insert(0, init_state[i][j])
                self.bfs[i][j].delete(0)
                self.bfs[i][j].insert(0, init_state[i][j])
                self.c[i][j].config(state="readonly")
                self.ucs[i][j].config(state="readonly")
                self.bfs[i][j].config(state="readonly")

    def button2click(self):
        state = generate_rand_puzzle()
        self.random = 1
        for i in range(3):
            for j in range(3):
                self.b[i][j].delete(0)
                self.b[i][j].insert(0, state[i][j])

    def drawpath(self, puzzle, display):
        for i in range(3):
            for j in range(3):
                display[i][j].config(state="normal")
                display[i][j].delete(0)
                display[i][j].insert(0, str(puzzle[i][j]))
                display[i][j].config(state="readonly")

    def rightButtonclick(self):
        self.a_star_index += 1
        self.drawpath(self.a_star_path[self.a_star_index], self.c)

    def leftButtonclick(self):
        self.a_star_index -= 1
        self.drawpath(self.a_star_path[self.a_star_index], self.c)

    def rightButton1click(self):
        self.ucs_index += 1
        self.drawpath(self.ucs_path[self.ucs_index], self.ucs)

    def leftButton1click(self):
        self.ucs_index -= 1
        self.drawpath(self.ucs_path[self.ucs_index], self.ucs)

    def rightButton2click(self):
        self.bfs_index += 1
        self.drawpath(self.bfs_path[self.bfs_index], self.bfs)

    def leftButton2click(self):
        self.bfs_index -= 1
        self.drawpath(self.bfs_path[self.bfs_index], self.bfs)

    def button3click(self):

        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        for i in range(11):
            init_state = generate_rand_puzzle()
            start_time_1 = time.time()
            self.a_star_path = a_star(init_state, goal_state)
            stop_time_1 = time.time() - start_time_1
            start_time_3 = time.time()
            self.bfs_path = print_bfs(init_state, goal_state)
            stop_time_3 = time.time() - start_time_3
            self.rt.append([stop_time_1, stop_time_3])
            if self.a_star_path == 0 or self.bfs_path == 0:
                self.steps.append([0, 0])
            else:
                self.steps.append([len(self.a_star_path), len(self.bfs_path)])

        self.out.insert('1.0', ("A* running time: " + str(self.rt[0][0]) + "steps: " + str(self.steps[0][0])))
        self.out.insert('2.0', ("BFS running time " + str(self.rt[0][1]) + "steps: " + str(self.steps[0][1])))
        self.out.insert('3.0', ("A* running time: " + str(self.rt[1][0]) + "steps: " + str(self.steps[1][0])))
        self.out.insert('4.0', ("BFS running time " + str(self.rt[1][1]) + "steps: " + str(self.steps[1][1])))
        self.out.insert('5.0', ("A* running time: " + str(self.rt[2][0]) + "steps: " + str(self.steps[2][0])))
        self.out.insert('6.0', ("BFS running time " + str(self.rt[2][1]) + "steps: " + str(self.steps[2][1])))
        self.out.insert('7.0', ("A* running time: " + str(self.rt[3][0]) + "steps: " + str(self.steps[3][0])))
        self.out.insert('8.0', ("BFS running time " + str(self.rt[3][1]) + "steps: " + str(self.steps[3][1])))
        self.out.insert('9.0', ("A* running time: " + str(self.rt[4][0]) + "steps: " + str(self.steps[4][0])))
        self.out.insert('10.0', ("BFS running time " + str(self.rt[4][1]) + "steps: " + str(self.steps[4][1])))
        self.out.insert('11.0', ("A* running time: " + str(self.rt[5][0]) + "steps: " + str(self.steps[5][0])))
        self.out.insert('12.0', ("BFS running time " + str(self.rt[5][1]) + "steps: " + str(self.steps[5][1])))
        self.out.insert('13.0', ("A* running time: " + str(self.rt[6][0]) + "steps: " + str(self.steps[6][0])))
        self.out.insert('14.0', ("BFS running time " + str(self.rt[6][1]) + "steps: " + str(self.steps[6][1])))
        self.out.insert('15.0', ("A* running time: " + str(self.rt[7][0]) + "steps: " + str(self.steps[7][0])))
        self.out.insert('16.0', ("BFS running time " + str(self.rt[7][1]) + "steps: " + str(self.steps[7][1])))
        self.out.insert('17.0', ("A* running time: " + str(self.rt[8][0]) + "steps: " + str(self.steps[8][0])))
        self.out.insert('18.0', ("BFS running time " + str(self.rt[8][1]) + "steps: " + str(self.steps[8][1])))
        self.out.insert('19.0', ("A* running time: " + str(self.rt[9][0]) + "steps: " + str(self.steps[9][0])))
        self.out.insert('20.0', ("BFS running time " + str(self.rt[9][1]) + "steps: " + str(self.steps[9][1])))
        self.out.insert('21.0', ("A* running time: " + str(self.rt[10][0]) + "steps: " + str(self.steps[10][0])))
        self.out.insert('22.0', ("BFS running time " + str(self.rt[10][1]) + "steps: " + str(self.steps[10][1])))


root = Tk()
myApp = MyApp(root)
root.mainloop()
