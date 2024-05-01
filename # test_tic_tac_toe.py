import pygame
pygame.init()

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

import unittest
from unittest.mock import patch
from io import StringIO
import kryziukai  # Import your main program as kryziukai

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.model = kryziukai.Model()  # Use kryziukai instead of tic_tac_toe
        self.view = kryziukai.View()    # Use kryziukai instead of tic_tac_toe
        self.controller = kryziukai.Controller(self.model, self.view)  # Use kryziukai instead of tic_tac_toe

    def test_reset_board(self):
        self.model.reset_board()
        expected_board = [['' for _ in range(3)] for _ in range(3)]
        self.assertEqual(self.model.board, expected_board)
        self.assertEqual(self.model.player, 'X')
        self.assertIsNone(self.model.winner)

if __name__ == '__main__':
    unittest.main()
