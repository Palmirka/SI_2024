#ifndef MCTS_HPP
#define MCTS_HPP

#include <algorithm>
#include "board.hpp"

#define C 1.41421
#define INF INT32_MAX

class MCTS {
    int iterations;
    Board board;
    public:
    MCTS(Board b, int iters) : board(b), iterations(iters) {};
    Position run(int player);
};

class MCTSNode {
    Board board;
    Position move;
    float x;
    float n;
    float selection(int parent);
    float value();
    vector<MCTSNode> children;

    public:
    MCTSNode(Board b, Position m) : 
        board(b),
        move(m), 
        x(0), 
        n(0){};
        
    bool operator<(MCTSNode& other) {
        return selection(n) < other.selection(other.n);
    }

    int expand(int player);
    Position best_move();
    MCTSNode best_child();
};

#endif