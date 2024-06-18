#include <sstream>
#include "minimax.hpp"

using namespace std;
using namespace std::chrono;

Board board = Board();
int player = 1;

void send_rdy() {
    cout << "RDY" << endl;
}

void send_ido(int x, int y) {
    cout << "IDO " << x << " " << y << endl;
}

void handle_ugo(float move_time, float game_time) {
    player = 0;
    Position m = Minimax(board, player, 1, values).run(player);
    board.do_move(m, player);
    send_ido(m.x, m.y);
}

void handle_hedid(float move_time, float game_time, int x, int y) {
    //cerr << "move_description: " << x << " " << y << endl;
    board.do_move(Position(x, y), 1 - player);
    Position m = Minimax(board, player, 1, values).run(player);
    board.do_move(m, player);
    send_ido(m.x, m.y);
}

void handle_onemore() {
    player = 1;
    board = Board();
    send_rdy();
}

int main() {
    string line;
    send_rdy();
    while(getline(cin, line)) {
        istringstream ss(line);
        string command;
        ss >> command;
        if(command == "UGO") {
            float move_time, game_time;
            ss >> move_time >> game_time;
            handle_ugo(move_time, game_time);
        } else if(command == "HEDID") {
            float move_time, game_time;
            int x, y;
            ss >> move_time >> game_time >> x >> y;
            handle_hedid(move_time, game_time, x, y);
        } else if(command == "ONEMORE") {
            handle_onemore();
        } else if(command == "BYE") {
            break;
        }

    }

    return 0;
}
