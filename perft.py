#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A test set of more than 6000 positions. The perft node count for a given depth
# is the number of legal move sequences from that position. This can be used
# to check correctness and speed of the legal move generator.
#
# The original test suite was created by Marcel van Kervinck and found at
# http://marcelk.net/rookie/nostalgia/v3/perft-random.epd

from __future__ import print_function

import chess
import unittest
import sys


def perft(board, depth):
    if depth > 1:
        count = 0

        for move in board.legal_moves:
            board.push(move)
            count += perft(board, depth - 1)
            board.pop()

        return count
    elif depth == 1:
        return len(board.legal_moves)
    else:
        return 1


def into_check_perft(board, depth):
    if depth >= 1:
        count = 0

        for move in board.pseudo_legal_moves:
            if board.is_into_check(move):
                continue

            board.push(move)
            count += into_check_perft(board, depth - 1)
            board.pop()

        return count
    else:
        return 1


def debug_perft(board, depth):
    assert board.is_valid()

    if depth >= 1:
        count =  0

        for move in board.pseudo_legal_moves:
            assert move in board.pseudo_legal_moves, (move, board)

            if board.is_into_check(move):
                assert move not in board.legal_moves, (move, board)
                continue

            assert move in board.legal_moves, (move, board)
            assert move == board.parse_san(board.san(move))

            board.push(move)
            count += debug_perft(board, depth - 1)
            board.pop()

        return count
    else:
        return 1


class PerftTestCase(unittest.TestCase):

    def execute_test(self, method, maxnodes):
        current_id = None
        board = chess.Board()

        with open("data/perft-random.epd") as data:
            for line in data:
                s = line.split()
                if not s:
                    pass
                elif s[0] == "id":
                    current_id = s[1]
                    sys.stdout.write(".")
                    sys.stdout.flush()
                elif s[0] == "epd":
                    board.set_epd(" ".join(s[1:]))
                elif s[0] == "perft":
                    depth = int(s[1])
                    nodes = int(s[2])
                    if nodes < maxnodes:
                        self.assertEqual(method(board, depth), nodes, current_id)

        sys.stdout.write("\n")
        sys.stdout.flush()

    def test_into_check(self):
        self.execute_test(into_check_perft, 1000)

    def test_debug(self):
        self.execute_test(debug_perft, 100)

    def test_speed(self):
        self.execute_test(perft, 10000)

    def test_chess960(self):
        # Source: http://www.talkchess.com/forum/viewtopic.php?t=55274

        # XFEN 00
        board = chess.Board("r1k1r2q/p1ppp1pp/8/8/8/8/P1PPP1PP/R1K1R2Q w KQkq - 0 1 ")
        self.assertEqual(perft(board, 1), 23)
        self.assertEqual(perft(board, 2), 522)
        self.assertEqual(perft(board, 3), 12333)
        self.assertEqual(perft(board, 4), 285754)
        sys.stdout.write(".")
        sys.stdout.flush()

        # XFEN 01
        board = chess.Board("r1k2r1q/p1ppp1pp/8/8/8/8/P1PPP1PP/R1K2R1Q w KQkq - 0 1")
        self.assertEqual(perft(board, 1), 28)
        self.assertEqual(perft(board, 2), 738)
        self.assertEqual(perft(board, 3), 20218)
        self.assertEqual(perft(board, 4), 541480)
        sys.stdout.write(".")
        sys.stdout.flush()

        # XFEN 02
        board = chess.Board("8/8/8/4B2b/6nN/8/5P2/2R1K2k w Q - 0 1")
        self.assertEqual(perft(board, 1), 34)
        self.assertEqual(perft(board, 2), 318)
        self.assertEqual(perft(board, 3), 9002)
        self.assertEqual(perft(board, 4), 118388)
        sys.stdout.write(".")
        sys.stdout.flush()

        # XFEN 03
        board = chess.Board("2r5/8/8/8/8/8/6PP/k2KR3 w K - 0 1")
        self.assertEqual(perft(board, 1), 17)
        self.assertEqual(perft(board, 2), 242)
        self.assertEqual(perft(board, 3), 3931)
        self.assertEqual(perft(board, 4), 57700)
        sys.stdout.write(".")
        sys.stdout.flush()

        # XFEN 04
        board = chess.Board("4r3/3k4/8/8/8/8/6PP/qR1K1R2 w KQ - 0 1")
        self.assertEqual(perft(board, 1), 19)
        self.assertEqual(perft(board, 2), 628)
        self.assertEqual(perft(board, 3), 12858)
        self.assertEqual(perft(board, 4), 405636)
        sys.stdout.write(".\n")
        sys.stdout.flush()


if __name__ == "__main__":
    unittest.main()
