#include <bits/stdc++.h>
#define inf            1000000007
#define maxn           1005
#define for_x(i,a,b)   for(int i = a; i <= b; i++)
#define for_n(i,a,b)   for(int i = a; i >= b; i--)
#define fi             first
#define se             second
#define p_b            push_back
#define mod            1000000007

using namespace std;
typedef long long LL;

int n, k, item_w[maxn], item_l[maxn], truck_w[maxn], truck_l[maxn], truck_c[maxn];

int randlr(int l, int r)
{
    return l + (LL)rand() * rand() % (r - l + 1);
}

bool check_test()
{
    system("main.exe");
    ifstream rfile;
    rfile.open("main.out");
    string s;
    getline(rfile, s);
    if(s == "0") return true;
    return false;
}

void make_test(int x, int y)
{
    n = k = max(11, x * 10 + y);
    for_x(i, 1, n)
    {
        item_w[i] = randlr(50, 250)/10 * 10;
        item_l[i] = randlr(50, 250)/10 * 10;
    }
    for_x(i, 1, k)
    {
        truck_w[i] = randlr(100, 400)/10 * 10;
        truck_l[i] = randlr(100, 400)/10 * 10;
        truck_c[i] = randlr(100, 500);
    }
    ofstream wfile;
    wfile.open("main.inp");
    wfile << n << " " << k << "\n";
    for_x(i, 1, n) wfile << item_w[i] << " " << item_l[i] << "\n";
    for_x(i, 1, k) wfile << truck_w[i] << " " << truck_l[i] << " " << truck_c[i] << "\n";
    wfile.close();
}

void viet_test(int x, int y)
{
    string str_prefix = "D:\\window\\codeblock\\main\\Phase_1\\input"; // thay doi cai nay thanh folder chua test
    ofstream wfile;
    string path = str_prefix + to_string(x) + to_string(y) + ".txt";
    cout << path << "\n";
    wfile.open(path);
    wfile << n << " " << k << "\n";
    for_x(i, 1, n) wfile << item_w[i] << " " << item_l[i] << "\n";
    for_x(i, 1, k) wfile << truck_w[i] << " " << truck_l[i] << " " << truck_c[i] << "\n";
    wfile.close();
}

int main()
{
    srand(time(0));
    for_x(i, 0, 5)
    {
        for_x(j, 0, 9)
        {
            bool ok = false;
            while(!ok)
            {
                make_test(i, j);
                ok = check_test();
            }
            viet_test(i, j);
        }
    }
}
