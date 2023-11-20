/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
#include <vector>
#include <map>
#include <list>
#include <typeinfo>
#include <set>
#include <algorithm>
#include <limits.h>

using namespace std;

map<int, vector<int>> P;
vector<vector<int>> AD_m;
vector<int> A;
vector<int> result;
set<int> WEIGHTS;


int tmp = INT_MAX;
int N;
int best_bound = INT_MAX;

vector<vector<int>> bb_res;


//template<typename T>
void print(const vector<int>& v)
{
	for (int i : v)
		cout << i << ' ';
	cout << endl;
}


void process(vector<int> & a){
    set<int> serv(a.begin(), a.end());
    int s = 0;
    if (a.size() != serv.size()) return;
    if (find(P[1].begin(), P[1].end(), a[a.size()-1]) == P[1].end()){
        return;
    }

    for (int i = 0; i<a.size()-1; i++){
        s += AD_m[a[i]-1][a[i+1]-1];
    }
    
    s += AD_m[a[a.size()-1]-1][a[0]-1];
    
    if (s < tmp)
    {
        tmp = s;
        result = a;
    }
}

void ps(vector<int> & a, int k){
    if (k==a.size()){
        process(a);
    }
    else{
        int ind=a[k-1];
        for (auto item:P[ind]){
            a[k] = item;
            ps(a, k+1);
        }
        
    }
}


bool bound(vector<int> & a){
    
    set<int> sv(a.begin(), a.end());
    if (a.size() != sv.size()) return false;
    
    int cur_value = 0;
    set<int> cur_weights;
    set<int> serv;
    
    for (int i = 0; i<a.size()-2; i++){
        cur_value += AD_m[a[i]][a[i+1]];
        cur_weights.insert(AD_m[a[i]][a[i+1]]);
    }
    set_difference(WEIGHTS.begin(), WEIGHTS.end(),
                    cur_weights.begin(), cur_weights.end(),
                    inserter(serv, serv.end()));
    int tmp1 = *min_element(serv.begin(), serv.end());
    cur_value += (N-a.size())*tmp1;
    
    
    if (cur_value < best_bound){
        return true;
    }
    
    return false;
}

void new_bound(vector<int> & a){
    int cur_value;
    for (int i = 0; i<a.size()-1; i++){
        cur_value += AD_m[a[i]][a[i+1]];
    }
    cur_value += AD_m[a.back()][a[0]];
    
    if (cur_value <= best_bound){
        best_bound = cur_value;
    }
}

void process_bb(vector<int> & a){
    bb_res.push_back(a);
}


void branch(vector<int> & a){
    if (a.size() == N){
        
        new_bound(a);
        process_bb(a);
    }
    else{
        for (auto item:P[a.back()]){
            a.push_back(item);
            if (bound(a)){
                branch(a);
            }
            a.pop_back();
        }
    }
}

int main()
{
    
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
    

    // A.resize(n);
    // for (int i = 0; i<n; i++){
    //     A[i] = 1;
    // }
    

    vector<int> B;
    B.push_back(1);
    branch(B);

    result = bb_res.back();
    int res = 0;
    for (int i = 0; i<result.size()-1; i++){
        res += AD_m[result[i]][result[i+1]];
    }
    
    res += AD_m[result.back()][result.front()];
    
    for (auto i: result){
        cout<<i<<" ";
    }
    cout<<endl;
    cout<<res;

    
    
    // process string call
    // ps(A, 1);
    
    // cout<<"******"<<endl;
    
    // print(result);
    // cout<<tmp;
    
    
    
    
    return 0;
}
