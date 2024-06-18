#ifndef BOARD_HPP
#define BOARD_HPP 

#include <iostream>
#include <array>
#include <utility>
#include <vector>
#include <random>
#include <set>
#include <chrono>

#define M 8
using namespace std;
using namespace std::chrono;

extern random_device rd;
extern mt19937 gen;

extern array<array<int, M>, M> values;

struct Position {
    int x;
    int y;
    Position(int x, int y) : x(x), y(y) {}

    bool operator==(const Position& other) const {
        return x == other.x && y == other.y;
    }
    bool operator<(const Position& other) const {
        return x < other.x || (x == other.x && y < other.y);
    }
};

extern vector<Position> dirs;

class Board {
    array<array<int, M>, M> B;
    set<Position> fields;
    vector<Position> move_list;
    vector<array<array<int, M>, M>> history;
    
    public:
        Board();
        int get(int x,int y);
        bool can_beat(int x, int y, Position d, int player);
        vector<Position> moves(int player);
        void do_move(Position pos, int player);
        void undo_move();
        int simulation(int player);
        Position random_move(int player);
        void draw_board();
        bool terminal();
        bool result();
};

#endif