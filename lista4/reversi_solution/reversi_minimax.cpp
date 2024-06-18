#include "minimax.hpp"

using namespace std::chrono;

void basic(int all){
    auto start = high_resolution_clock::now();
    int wins = 0;
    auto minimax_time = 0;
    auto random_time = 0;

    int depth = 2;
    for(int i = 0; i < all; i++){
        Board B = Board();
        int player = 0;
        while(!B.terminal()){
            if(player == 0){
                auto random_start = high_resolution_clock::now();
                Position m = B.random_move(player);
                auto random_stop = high_resolution_clock::now();
                random_time += duration_cast<microseconds>(random_stop - random_start).count();
                B.do_move(m, player);
            }else{
                auto minimax_start = high_resolution_clock::now();
                Position m = Minimax(B, player, depth, values).run(player);
                auto minimax_stop = high_resolution_clock::now();
                minimax_time += duration_cast<microseconds>(minimax_stop - minimax_start).count();
                B.do_move(m, player);  
            }
            player = 1 - player;
        } 
        if(B.result() > 0)
            wins++;
    }
    auto stop = high_resolution_clock::now();
    cout << "   Wins: " << wins << "," << endl;
    cout << "   Loses: " << all - wins << endl;
    cout << "   Time: " << duration_cast<milliseconds>(stop - start).count() << "ms" << endl;
    cout << "   Average minimax time: " << minimax_time / all << "μs" << endl;
    cout << "   Average random time: " << random_time / all << "μs" << endl;
}

int main(){
    cout << "NOVICE / BASIC / STANDARD: " << endl;
    basic(1000);
    return 0;
}

