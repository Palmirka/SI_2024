#include "minimax.hpp"


Minimax :: Minimax(Board b, int p, int d, array<array<int, M>, M> h) : board(b), player(p), depth(d), heuristics(h) {}

int Minimax :: eval(){
    int result = 0;

    for(int i = 0; i < M; i++){
        for(int j = 0; j < M; j++){
            int b = board.get(i, j);           
            if(b == 0)
                result -= values[i][j];
            else if (b == 1)
                result += values[i][j];
        }
    }

    return result;
}

Result Minimax :: minimax(bool max_player, bool player, int depth, int alpha, int beta){
    if(depth == 0 || board.terminal() || board.moves(max_player)[0] == Position(-1,-1))
        return {Position(-1, -1), eval()};

    vector<Position> next_moves = board.moves(max_player);
    Result best_move = {Position(-1, -1), max_player ? INT32_MIN : INT32_MAX};
    if(max_player){
        for(auto move : next_moves){
            board.do_move(move, 1);
            Result result = minimax(0, 1 - player, depth-1, alpha, beta);
            if (result.value > best_move.value)
                best_move = {move, result.value};
            board.undo_move();
            alpha = max(alpha, result.value);
            if(alpha >= beta)
                break;
        }
    }else{
        for(auto move : next_moves){
            board.do_move(move, 0);
            Result result = minimax(1, 1 - player, depth-1, alpha, beta);
            if (result.value < best_move.value)
                best_move = {move, result.value};
            board.undo_move();
            beta = min(beta, result.value);
            if(alpha >= beta)
                break;
        }
    }
    return best_move;
}
Position Minimax :: run(int player){
    return minimax(true, player, depth, INT32_MIN, INT32_MAX).move;
}