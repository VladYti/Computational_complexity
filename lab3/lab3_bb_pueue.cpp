#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <limits.h>
#include <set>
#include <map>


using namespace std;

map<int, vector<int>> P;
vector<vector<int>> AD_m;
int record = INT_MAX;
vector<int> record_sol;
set<int> WEIGHTS;

int N;

struct Pair{
    int first;
    vector<int> second;
};

//template<typename T>
void print(const vector<int>& v)
{
	for (int i : v)
		cout << i << ' ';
	cout << endl;
}


auto cmp = [](const Pair& l, const Pair& r)
{
	double c1 = l.first, c2 = r.first;
	return c1 >= c2;
};

priority_queue<Pair, vector<Pair>, decltype(cmp)> q(cmp);


bool check(vector<int> & a){
    set<int> sv(a.begin(), a.end());
    if (a.size() != sv.size()) return false;
    
    if (a.size() == N){
        if (find(P[1].begin(), P[1].end(), a.back()) == P[1].end()){
            return false;
        }
    }
    return true;
}


int bound(vector<int> & a){
    int cur_value = 0;
    set<int> cur_weights;
    set<int> serv;
    
    for (int i = 0; i<a.size()-1; i++){
        cur_value += AD_m[a[i]][a[i+1]];
        cur_weights.insert(AD_m[a[i]][a[i+1]]);
    }
    set_difference(WEIGHTS.begin(), WEIGHTS.end(),
                    cur_weights.begin(), cur_weights.end(),
                    inserter(serv, serv.end()));
    int tmp1 = *min_element(serv.begin(), serv.end());
    cur_value += (N-a.size())*tmp1;
    if (a.size() == N){
        cur_value += AD_m[a.back()][a.front()];
    }
    
    return cur_value;
}


void put_in_queue(vector<int> & a){
    int ind = a.back();
    for (auto item:P[ind]){
        a.push_back(item);
        if (check(a)){
            q.push({bound(a), a});
        }
        a.pop_back();
    }
}


void process(vector<int> & a){
    put_in_queue(a);
    
    while (!q.empty()){
        auto serv = q.top();
        q.pop();
        if (serv.first < record && serv.second.size() == N){
            record = serv.first;
            record_sol = serv.second;
        }
        put_in_queue(serv.second);
    }
}

int main(){
    
    int n, m;
    cin>>n>>m;
    AD_m.resize(n+1, vector<int>(n+1));
    N = n;
    
    int x, y, w;
    for(int i = 0; i<m; i++){
        cin>>x>>y>>w;
        P[x].push_back(y);
        P[y].push_back(x);
        
        AD_m[x][y] = w;
        AD_m[y][x] = w;
        WEIGHTS.insert(w);
        
    }
    vector<int> A;
    A.push_back(1);
    process(A);
    
    print(record_sol);
    cout<<record;
    
    
    return 0;
}


