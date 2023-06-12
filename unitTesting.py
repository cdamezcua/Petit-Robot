import unittest
from unittest.mock import patch, mock_open
from main import Simulator, GUI, Robot

class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator("assets/board.txt", "output.asm")
            
    def test_run(self):
        # Prueba la ejecución de una línea con una instrucción MOV válida.
        with patch.object(self.simulator.gui, 'move_robot') as mock_move_robot:
            self.simulator.line_run('TURN,90')
            self.simulator.line_run('MOV,1')
            mock_move_robot.assert_called_once_with(1)
            

    def test_line_run_invalid(self):
        # Prueba la ejecución de una línea con una instrucción inválida.
        with self.assertRaises(Exception):
            self.simulator.line_run('INVALID,1')

class TestGUI(unittest.TestCase):
    def setUp(self):
        with open('assets/board.txt', 'r') as f:
            file_contents = f.read()
        with patch('builtins.open', mock_open(read_data=file_contents)), patch.object(GUI, "render_robot"):
            self.gui = GUI("assets/board.txt")

    def test_move_robot(self):
        # Prueba mover el robot una posición hacia adelante.
        initial_col = self.gui.robot.get_column()
        initial_row = self.gui.robot.get_row()
        self.gui.turn_robot(90)
        self.gui.move_robot(8)
        self.gui.turn_robot(90)
        self.gui.move_robot(6)
        self.gui.turn_robot(90)
        self.gui.move_robot(3)
        self.gui.turn_robot(270)
        self.gui.move_robot(3)
        self.gui.turn_robot(270)
        self.gui.move_robot(3)
        self.gui.turn_robot(270)
        self.gui.move_robot(9)
        self.gui.turn_robot(270)
        self.gui.move_robot(8)
        self.assertEqual(self.gui.robot.get_column(), initial_col )
        self.assertEqual(self.gui.robot.get_row(), initial_row)

    def test_move_robot(self):
        # Prueba mover el robot una posición hacia adelante.
        initial_col = self.gui.robot.get_column()
        initial_row = self.gui.robot.get_row()
        self.gui.turn_robot(90)
        self.gui.move_robot(10)
        self.assertEqual(self.gui.robot.get_column(), initial_col )
        self.assertEqual(self.gui.robot.get_row(), initial_row)

    def test_turn_robot(self):
        # Prueba girar el robot 90 grados.
        initial_direction = self.gui.robot.direction
        self.gui.turn_robot(90)
        self.assertEqual(self.gui.robot.direction, (initial_direction + 1) % 4)

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Robot()

    def test_move(self):
        # Prueba mover el robot una posición hacia adelante.
        initial_row = self.robot.get_row()
        initial_column = self.robot.get_column()
        self.robot.move()
        self.assertEqual(self.robot.get_row(), initial_row - 1)
        self.assertEqual(self.robot.get_column(), initial_column)

    def test_turn(self):
        # Prueba girar el robot 90 grados.
        initial_direction = self.robot.direction
        self.robot.turn()
        self.assertEqual(self.robot.direction, (initial_direction + 1) % 4)

if __name__ == '__main__':
    unittest.main()
