/*
Parth Krishna Sharma : 2017B3A70907H
Siddhi Burse : 2017B3A70972H
Piyush Phatak : 2017B3A70425H
Keshav Pandya : 2017A3PS0399H
*/


#include<bits/stdc++.h>
using namespace std;
#define int long long int
#define IOS ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
struct soldiers{
    int colour[3];
};
#define N 100
int vis[N][N][N];
vector<string> result;

string get_soldier(int i){
    if(i==0)
        return "Red";
    else if(i==1)
        return "Blue";
    else if(i==2)
        return "Green";
}

int equal(struct soldiers st1, struct soldiers st2){
    if(st1.colour[0]==st2.colour[0] && st1.colour[1]==st2.colour[1] && st1.colour[2]==st2.colour[2]){
        return 1;
    }
    return 0;
}

void DFS(struct soldiers west,struct soldiers east,vector<string> current,char curr_coast,struct soldiers fin_state){

    if(vis[west.colour[0]][west.colour[1]][west.colour[2]]!=0)
        return;
    vis[west.colour[0]][west.colour[1]][west.colour[2]]=1;

    if(equal(west,fin_state)==1){
        if(result.size()==0 || result.size()>current.size()){
            result = current;
        }
    }

    if(curr_coast=='W'){
        for(int i=0; i<2; i++){
            for(int j=i+1; j<3; j++){
                if(west.colour[i]>0 && west.colour[j]>0){
                    west.colour[i]-=1;   
                    west.colour[j]-=1;
                    string s1="West to east: ";
                    string soldier1 = get_soldier(i);
                    string soldier2 = get_soldier(j);
                    s1+=soldier1;
                    s1+=" ";
                    s1+=soldier2;
                    current.push_back(s1);
                    east.colour[i]+=1;
                    east.colour[j]+=1;
                    
                    DFS(west,east,current,'E',fin_state);

                    west.colour[i]+=1;   west.colour[j]+=1;
                    current.pop_back();
                    east.colour[i]-=1;   east.colour[j]-=1;
                }
            }
        }
    }
    if(curr_coast=='E'){
        for(int i=0; i<3; i++){
            if(east.colour[i]){
                east.colour[i]-=1;
                west.colour[i]+=1;

                string s2 = "East to West: ";
                s2+=get_soldier(i);
                current.push_back(s2);
                DFS(west,east,current,'W',fin_state);

                east.colour[i]+=1;
                west.colour[i]-=1;
                current.pop_back();
            }
        }
    }

}

int32_t main(int32_t argc,char* argv[]){
    struct soldiers west_coast;
    //cout<<"Enter initial number of red, blue and green soldiers on west coast:\n";
    //cin>>west_coast.colour[0]>>west_coast.colour[1]>>west_coast.colour[2];
    //cout<<argc<<endl;
    west_coast.colour[0] = atoi(argv[1]);
    west_coast.colour[1] = atoi(argv[2]);
    west_coast.colour[2] = atoi(argv[3]);
    //cout<<"Initial number of soldiers on west coast: \n";
    //cout<<"Red: "<<west_coast.colour[0]<<" Blue: "<<west_coast.colour[1]<<" Green: "<<west_coast.colour[2]<<endl;
    
    struct soldiers east_coast;
    east_coast.colour[0]=0; east_coast.colour[1]=0; east_coast.colour[2]=0;
    
    struct soldiers fin_state;
    fin_state.colour[0]=0; fin_state.colour[1]=0; fin_state.colour[2]=0;
    
    vector<string> current;
    DFS(west_coast,east_coast,current,'W',fin_state);
    //cout<<"Soldier trips:\n";
    for(int i=0; i<result.size(); i++){
        cout<<result[i]<<endl;
    }
    //cout<<"Final number soldiers on east coast: "<<endl;
    //cout<<"Red: "<<west_coast.colour[0]<<" Blue: "<<west_coast.colour[1]<<" Green: "<<west_coast.colour[2]<<endl;
    return 0;
}