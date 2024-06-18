#include "mcts.hpp"

/* MCTS */

Position MCTS :: run(int player) {
    MCTSNode node = MCTSNode(board, Position(-1, -1));
    for (int i = 0; i < iterations; i++){
        node.expand(player);
    }
    return node.best_move();
}

/* MCTS node */

float MCTSNode :: selection(int parent) {
    if (n == 0)
        return INF;
    return x / n + C * sqrt(log(parent) / n);
}

float MCTSNode :: value() {
    if (n == 0)
        return 0;
    return x / n;
}

Position MCTSNode :: best_move() {
    auto best_node = max_element(children.begin(), children.end(), 
                                 [](MCTSNode& a, MCTSNode& b) {
                                    return a.value() <= b.value();
                                 });
    return best_node->move;
}

MCTSNode MCTSNode :: best_child() {
    auto best_node = max_element(children.begin(), children.end());
    return *best_node;
}

int MCTSNode :: expand(int player) {
    if (n == 0 || board.terminal()) {
        int r = board.simulation(player);
        n += 1;
        if (r == 0) {
            r = 0.5;
        } else if (r == 1 && player == 1) {
            r = 1;
        } else if (r == -1 && player == 0) {
            r = 1;
        } else {
            r = 0;
        }
        x += r;

        if (!board.terminal()) {
            auto moves = board.moves(player);
            for (const auto& move : moves) {
                MCTSNode child = MCTSNode(board, move);
                children.push_back(child);
            }
        }
        return r;
    }

    MCTSNode node = best_child();
    board.do_move(node.move, player);
    double r = node.expand(1 - player);
    n += 1;
    x += r;
    board.undo_move();
    return r;
}