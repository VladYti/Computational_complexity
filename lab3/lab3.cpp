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
#include <unordered_set>
#include <algorithm>
#include <limits.h>

using namespace std;

map<int, vector<int>> P;
vector<vector<int>> AD_m;
vector<int> A;
vector<int> result;


int tmp = INT_MAX;


//template<typename T>
void print(const vector<int>& v)
{
	for (int i : v)
		cout << i << ' ';
	cout << endl;
}


void process(vector<int> & a){
    unordered_set<int> serv(a.begin(), a.end());
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




int main()
{
    
    int n, m;
    cin>>n>>m;
    AD_m.resize(n, vector<int>(n));
    
    int x, y, w;
    for(int i = 0; i<m; i++){
        cin>>x>>y>>w;
        P[x].push_back(y);
        P[y].push_back(x);
        
        AD_m[x-1][y-1] = w;
        AD_m[y-1][x-1] = w;
    }
    

    A.resize(n);
    for (int i = 0; i<n; i++){
        A[i] = 1;
    }

    ps(A, 1);
    
    cout<<"******"<<endl;
    
    print(result);
    cout<<tmp;
    
    return 0;
}
