#include "board.hpp"

random_device rd;
mt19937 gen(rd());

array<array<int, M>, M> values = {{
    { 4, -3,  2,  2,  2,  2, -3,  4},
    {-3, -4, -1, -1, -1, -1, -4, -3},
    { 2, -1,  1,  0,  0,  1, -1,  2},
    { 2, -1,  0,  1,  1,  0, -1,  2},
    { 2, -1,  0,  1,  1,  0, -1,  2},
    { 2, -1,  1,  0,  0,  1, -1,  2},
    {-3, -4, -1, -1, -1, -1, -4, -3},
    { 4, -3,  2,  2,  2,  2, -3,  4}
}};

vector<Position> dirs = {Position(0, 1), Position(1, 0), Position(-1, 0), Position(0, -1), Position(1, 1), Position(-1, -1), Position(1, -1), Position(-1, 1)};

Board :: Board()
{
    for (auto& row : B) {
        row.fill(-1);
    }

    B[3][3] = 1;
    B[4][4] = 1;
    B[3][4] = 0;
    B[4][3] = 0;
    
    for(int i = 0; i < M; i++)
        for(int j = 0; j < M; j++)
            if(B[i][j] == -1)   
                fields.insert(Position(j, i));
}

int Board ::get(int x,int y){
    if((0 <= x && x < M) && (0 <= y && y < M))
        return B[y][x];
    return -1;
}

bool Board :: can_beat(int x, int y, Position d, int player)
{ 
    int dx = d.x;
    int dy = d.y;
    x += dx;
    y += dy;
    int cnt = 0;
    while(get(x, y) == 1-player){
        x += dx;
        y += dy;
        cnt += 1;
    }
    return (cnt > 0) && (get(x, y) == player);
}

vector<Position> Board :: moves(int player){
    vector<Position> res;
    for(auto f : fields) {
        for(auto d : dirs) {
            if(can_beat(f.x,f.y,d,player)) {
                res.push_back(f);
                break;
            }
        }
    }

    if(res.empty())
        return {Position(-1,-1)};
    return res;  
}
    

void Board :: do_move(Position move, int player){
    history.push_back(B);
    move_list.push_back(move);
    
    if(move == Position(-1,-1))
        return;

    int x = move.x;
    int y = move.y;
    int x0 = move.x;
    int y0 = move.y;

    B[y][x] = player;
    fields.erase(move);
    
    for(auto d : dirs){
        int dx = d.x;
        int dy = d.y;
        x = x0;
        y = y0;
        vector<Position> to_beat;

        x += dx;
        y += dy;

        while(get(x, y) == 1 - player){
            to_beat.push_back(Position(x, y));
            x += dx;
            y += dy;
        }

        if(get(x, y) == player)
            for(auto n : to_beat)
                B[n.y][n.x] = player;
    }
}

void Board :: undo_move() {
    if (!history.empty()) {
        B = history.back();
        history.pop_back();
        Position last_move = move_list.back();
        move_list.pop_back();
        if (!(last_move == Position(-1,-1))) {
            fields.insert(last_move);
        }
    }
}

Position Board :: random_move(int player){
    auto ms = moves(player);
    if(!ms.empty()){
        uniform_int_distribution<> dist(0,ms.size()-1);
        return ms[dist(gen)]; 
    }
    return Position(-1,-1);
    
}

int Board :: simulation(int player){
    int cnt = 0;
    while (!terminal()) {
        auto move = random_move(player);
        if (move == Position(-1,-1))
            break;
        do_move(move, player);
        player = 1 - player;
        cnt++;
    }
    int winner_result;
    int r = result();
    if (!r) 
        winner_result = 0;
    winner_result = r > 0 ? 1 : -1;

    for (int i = 0; i < cnt; i++)
        undo_move();

    return winner_result;
}

void Board :: draw_board() {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < M; j++) {
            if (B[i][j] == -1)
                cout << ". ";
            else if (B[i][j] == 0)
                cout << "o ";
            else
                cout << "x ";
        }
        cout << endl;
    }
    cout << endl;
}

bool Board :: terminal(){
    if(fields.empty())
        return true;
    if(move_list.size() < 2)
        return false;
    
    int temp = move_list.size();
    if(move_list[temp - 1] == move_list[temp - 2] && move_list[temp - 1] == Position(-1,-1))
        return true;

    return false;
}

bool Board :: result()
{
    int res = 0;
    for(int i = 0; i < M; i++){
        for(int j = 0; j < M; j++){
            int b = B[i][j];           
            if(b == 0)
                res -= 1;
            else if (b == 1)
                res += 1;
        }
    }
    return res;
}