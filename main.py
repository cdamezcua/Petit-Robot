import os
import time

NL_CODE_FILE_PATH = "input.txt"
ASC_FILE_PATH = "build/output.asm"
BOARD_FILE_PATH = "assets/board.txt"
DELAY = 0.2


class Simulator:
    def __init__(self, board_file_path, asc_file_path):
        self.board_file_path = board_file_path
        self.asc_file_path = asc_file_path
        self.gui = GUI(board_file_path)

    def run(self):
        with open(self.asc_file_path, "r") as f:
            for line in f:
                try:
                    self.line_run(line.strip())
                except Exception as e:
                    print()
                    print(e)
                    print()
                    exit()
            print()
            print("[!] execution completed successfully!")
            print()

    def line_run(self, line):
        line = line.split(",")
        if line[0] == "MOV":
            try:
                self.gui.move_robot(int(line[1]))
            except Exception as e:
                print()
                print(e)
                print()
                exit()
        elif line[0] == "TURN":
            self.gui.turn_robot(int(line[1]))
        else:
            raise Exception("[!] Invalid instruction!")


class GUI:
    def __init__(self, board_file):
        self.light_to_dark_corners = {
            ("┼", (-1, -1)): "╆",
            ("├", (-1, -1)): "┢",
            ("┬", (-1, -1)): "┲",
            ("┌", (-1, -1)): "┏",
            ("─", (-1, 0)): "━",
            ("┼", (-1, 1)): "╅",
            ("┤", (-1, 1)): "┪",
            ("┬", (-1, 1)): "┱",
            ("┐", (-1, 1)): "┓",
            ("│", (0, 1)): "┃",
            ("┼", (1, 1)): "╃",
            ("┴", (1, 1)): "┹",
            ("┤", (1, 1)): "┩",
            ("┘", (1, 1)): "┛",
            ("─", (1, 0)): "━",
            ("┼", (1, -1)): "╄",
            ("┴", (1, -1)): "┺",
            ("├", (1, -1)): "┡",
            ("└", (1, -1)): "┗",
            ("│", (0, -1)): "┃",
        }
        self.light_to_dark = {
            "─": "━",
            "│": "┃",
        }
        self.ROWS = 10
        self.COLUMNS = 10
        self.ROW_B = 2
        self.ROW_M = 2
        self.COLUMN_B = 4
        self.COLUMN_M = 4
        self.robot = Robot()
        self.empty_matrix = []
        with open(board_file, "r") as f:
            for line in f:
                self.empty_matrix.append(list(line.strip("\n")))
        self.full_matrix = []
        self.render_gui()
        self.print_gui()

    def move_robot(self, steps):
        for i in range(steps):
            self.robot.move()
            if (
                self.robot.get_row() < 0
                or self.robot.get_row() >= self.ROWS
                or self.robot.get_column() < 0
                or self.robot.get_column() >= self.COLUMNS
            ):
                raise Exception("[!] Robot has hit a wall!")
            self.render_gui()
            self.print_gui()

    def turn_robot(self, degrees):
        turns = degrees // 90
        for i in range(turns):
            self.robot.turn()
            self.render_gui()
            self.print_gui()

    def render_gui(self):
        self.render_background()
        #self.render_trail()
        self.render_robot()
        self.render_target()

    def render_trail(self):
        for i in range(len(self.robot.get_trail_positions())):
            self.full_matrix[
                self.ROW_B + self.ROW_M * self.robot.get_trail_positions()[i][0]
            ][
                self.COLUMN_B + self.COLUMN_M * self.robot.get_trail_positions()[i][1]
            ] = self.robot.get_trail_icon(
                i
            )

    def render_background(self):
        self.full_matrix = [i[:] for i in self.empty_matrix]

    def render_robot(self):
        self.full_matrix[self.ROW_B + self.ROW_M * self.robot.get_row()][
            self.COLUMN_B + self.COLUMN_M * self.robot.get_column()
        ] = self.robot.get_icon()

    def render_target(self):
        self.render_target_corners()
        self.render_target_lines()

    def render_target_corners(self):
        for i in self.robot.get_relative_target_corners_positions():
            self.full_matrix[
                self.ROW_B
                + self.ROW_M * self.robot.get_row()
                + (self.ROW_M // 2) * i[0]
            ][
                self.COLUMN_B
                + self.COLUMN_M * self.robot.get_column()
                + (self.COLUMN_M // 2) * i[1]
            ] = self.light_to_dark_corners[
                (
                    self.full_matrix[
                        self.ROW_B
                        + self.ROW_M * self.robot.get_row()
                        + (self.ROW_M // 2) * i[0]
                    ][
                        self.COLUMN_B
                        + self.COLUMN_M * self.robot.get_column()
                        + (self.COLUMN_M // 2) * i[1]
                    ],
                    i,
                )
            ]

    def render_target_lines(self):
        for i in range(4):
            self.render_targer_line(
                self.ROW_B
                + self.ROW_M * self.robot.get_row()
                + (self.ROW_M // 2)
                * self.robot.get_relative_target_corners_positions()[i][0],
                self.COLUMN_B
                + self.COLUMN_M * self.robot.get_column()
                + (self.COLUMN_M // 2)
                * self.robot.get_relative_target_corners_positions()[i][1],
                self.ROW_B
                + self.ROW_M * self.robot.get_row()
                + (self.ROW_M // 2)
                * self.robot.get_relative_target_corners_positions()[(i + 1) % 4][0],
                self.COLUMN_B
                + self.COLUMN_M * self.robot.get_column()
                + (self.COLUMN_M // 2)
                * self.robot.get_relative_target_corners_positions()[(i + 1) % 4][1],
            )

    def render_targer_line(self, row1, column1, row2, column2):
        if row1 == row2:
            for i in range(min(column1, column2) + 1, max(column1, column2)):
                self.full_matrix[row1][i] = self.light_to_dark[
                    (self.full_matrix[row1][i])
                ]
        elif column1 == column2:
            for i in range(min(row1, row2) + 1, max(row1, row2)):
                self.full_matrix[i][column1] = self.light_to_dark[
                    (self.full_matrix[i][column1])
                ]

    def print_gui(self):
        os.system("clear")
        for i in self.full_matrix:
            print("".join(i))
        time.sleep(DELAY)


class Robot:
    def __init__(self):
        self.row = 0
        self.column = 0
        self.direction = 0
        self.movements = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.icons = ["⇧", "⇨", "⇩", "⇦"]
        self.relative_target_corners_positions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        self.trail_maximun_length = 5
        self.trail_icons = ["□"]

        self.trail_positions = []

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_icon(self):
        return self.icons[self.direction]

    def get_relative_target_corners_positions(self):
        return self.relative_target_corners_positions

    def get_trail_positions(self):
        return self.trail_positions

    def get_trail_icon(self, index):
        if index >= len(self.trail_icons):
            return self.trail_icons[-1]
        return self.trail_icons[index]

    def move(self):
        if len(self.trail_positions) >= self.trail_maximun_length:
            # remove from end
            self.trail_positions.pop()
        # insert al begining
        self.trail_positions.insert(0, (self.row, self.column))
        self.row += self.movements[self.direction][0]
        self.column += self.movements[self.direction][1]

    def turn(self):
        self.direction = (self.direction + 1) % 4


def main():
    os.system("mkdir build")
    os.system("yacc -d compiler.y && mv y.tab.c y.tab.h ./build")
    os.system("lex compiler.l && mv lex.yy.c ./build")
    os.system("gcc ./build/y.tab.c ./build/lex.yy.c -ly -ll -o compiler && mv compiler ./build")
    os.system("./build/compiler " + NL_CODE_FILE_PATH + " > " + ASC_FILE_PATH)
    simulator = Simulator(BOARD_FILE_PATH, ASC_FILE_PATH)
    simulator.run()


if __name__ == "__main__":
    main()
