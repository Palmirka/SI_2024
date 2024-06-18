#ifndef MINIMAX_HPP
#define MINIMAX_HPP 

#include "board.hpp"

struct Result {
    Position move;
    int value;
    Result(Position m, int v) : move(m), value(v) {};
};

class Minimax {
    Board board;
    int player;
    int depth;
    array<array<int, M>, M> heuristics;
    int eval();
    

    public:
    Minimax(Board b, int p, int d, array<array<int, M>, M> h);
    Result minimax(bool max_player, bool player, int depth, int alpha, int beta);
    Position run(int player);
};

#endif