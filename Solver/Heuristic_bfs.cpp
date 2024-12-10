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
typedef pair<int, int> i2;
typedef pair<i2, int> i3;
typedef pair<i2, i2> i4;

int n, k;
i3 item[maxn];
i4 truck[maxn];

struct Rect
{
    int W, L, x, y;
    Rect(): W(0), L(0), x(0), y(0) {}
    Rect(int W, int L, int x, int y): W(W), L(L), x(x), y(y) {}

    bool operator<(const Rect &x) const
    {
        if (max(W, L) != max(x.W, x.L)) return max(W, L) < max(x.W, x.L);
        return min(W, L) < min(x.W, x.L);
    }
};

bool cmp_truck(const i4 &x, const i4 &y)
{
    return (double)x.se.fi / (x.fi.fi * x.fi.se) < (double)y.se.fi / (y.fi.fi * y.fi.se);
}

bool cmp_item(const i3 &x, const i3 &y)
{
    if(max(x.fi.fi, x.fi.se) != max(y.fi.fi, y.fi.se)) return max(x.fi.fi, x.fi.se) < max(y.fi.fi, y.fi.se);
    return min(x.fi.fi, x.fi.se) < min(y.fi.fi, y.fi.se);
}

int danh_dau_truck, item_queue[maxn], item_cnt, real_item_queue[maxn], real_item_cnt, cant_item_queue[maxn], cant_item_cnt, total_cost = 0, candidate_cost;
i4 ans[maxn];
set<Rect> rect;

int try_to_fill(int id_truck, int save) // save = 1 la update real
{
    //init
    rect.clear();
    rect.insert(Rect(truck[id_truck].fi.fi, truck[id_truck].fi.se, 0, 0));
    //cout << truck[id_truck].fi.fi << " " << truck[id_truck].fi.se << "\n"; // DEBUG
    Rect r, c, cover;
    int id, w, l;
    cant_item_cnt = 0;
    bool in_use = false;
    // xu li
    if(save == 0)
    {
        for_x(i, 1, item_cnt)
        {
            // ###############################
            // LUONG XUAN NGUYEN'S GREEDY BASE
            id = item_queue[i];
            w = item[id].fi.fi, l = item[id].fi.se;
            r = Rect(w, l, 0, 0);
            auto iter = rect.lower_bound(r);
            for (; iter != rect.end(); iter++)
            {
                c = *iter;
                if (max(w, l) <= max(c.W, c.L) && min(w, l) <= min(c.W, c.L)) break;
            }
            if (iter == rect.end())
            {
                cant_item_queue[++cant_item_cnt] = id;
                continue;
            }
            in_use = true; // handle truong hop truck do khong duoc dung
            cover = *iter;
            rect.erase(iter);
            if (cover.W < cover.L)
            {
                if (w < l)
                {
                    if (cover.L - l > 0) rect.insert(Rect(cover.W, cover.L - l, cover.x, cover.y + l));
                    if (cover.W - w > 0) rect.insert(Rect(cover.W - w, l, cover.x + w, cover.y));
                }
                else
                {
                    if (cover.L - w > 0) rect.insert(Rect(cover.W, cover.L - w, cover.x, cover.y + w));
                    if (cover.W - l > 0) rect.insert(Rect(cover.W - l, w, cover.x + l, cover.y));
                }
            }
            else
            {
                if (w < l)
                {
                    if (cover.L - w > 0) rect.insert(Rect(l, cover.L - w, cover.x, cover.y + w));
                    if (cover.W - l > 0) rect.insert(Rect(cover.W - l, cover.L, cover.x + l, cover.y));
                }
                else
                {
                    if (cover.L - l > 0) rect.insert(Rect(w, cover.L - l, cover.x, cover.y + l));
                    if (cover.W - w > 0) rect.insert(Rect(cover.W - w, cover.L, cover.x + w, cover.y));
                }
            }
            // LUONG XUAN NGUYEN'S GREEDY BASE
            // ###############################
        }
        // update queue
        if(in_use)
        {
            item_cnt = cant_item_cnt;
            for_x(i, 1, cant_item_cnt) item_queue[i] = cant_item_queue[i];
            return truck[id_truck].se.fi;
        }
        return 0;
    }
    else // SAVE = 1
    {
        for_x(i, 1, real_item_cnt)
        {
            // ###############################
            // LUONG XUAN NGUYEN'S GREEDY BASE
            id = real_item_queue[i]; // SAVE
            w = item[id].fi.fi, l = item[id].fi.se;
            r = Rect(w, l, 0, 0);
            auto iter = rect.lower_bound(r);
            for (; iter != rect.end(); iter++)
            {
                c = *iter;
                if (max(w, l) <= max(c.W, c.L) && min(w, l) <= min(c.W, c.L)) break;
            }
            if (iter == rect.end())
            {
                cant_item_queue[++cant_item_cnt] = id;
                continue;
            }
            in_use = true; // handle truong hop truck do khong duoc dung
            cover = *iter;
            rect.erase(iter);
            if (cover.W < cover.L)
            {
                if (w < l)
                {
                    ans[item[id].se] = {{truck[id_truck].se.se, cover.x}, {cover.y, 0}};
                    //cout << item[id].se << " " << id_truck << " " << truck[id_truck].se.se << "fck\n"; // DEBUG
                    if (cover.L - l > 0) rect.insert(Rect(cover.W, cover.L - l, cover.x, cover.y + l));
                    if (cover.W - w > 0) rect.insert(Rect(cover.W - w, l, cover.x + w, cover.y));
                }
                else
                {
                    ans[item[id].se] = {{truck[id_truck].se.se, cover.x}, {cover.y, 1}};
                    //cout << item[id].se << " " << id_truck << " " << truck[id_truck].se.se << "fck\n"; // DEBUG
                    if (cover.L - w > 0) rect.insert(Rect(cover.W, cover.L - w, cover.x, cover.y + w));
                    if (cover.W - l > 0) rect.insert(Rect(cover.W - l, w, cover.x + l, cover.y));
                }
            }
            else
            {
                if (w < l)
                {
                    ans[item[id].se] = {{truck[id_truck].se.se, cover.x}, {cover.y, 1}};
                    //cout << item[id].se << " " << id_truck << " " << truck[id_truck].se.se << "fck\n"; // DEBUG
                    if (cover.L - w > 0) rect.insert(Rect(l, cover.L - w, cover.x, cover.y + w));
                    if (cover.W - l > 0) rect.insert(Rect(cover.W - l, cover.L, cover.x + l, cover.y));
                }
                else
                {
                    ans[item[id].se] = {{truck[id_truck].se.se, cover.x}, {cover.y, 0}};
                    //cout << item[id].se << " " << id_truck << " " << truck[id_truck].se.se << "fck\n"; // DEBUG
                    if (cover.L - l > 0) rect.insert(Rect(w, cover.L - l, cover.x, cover.y + l));
                    if (cover.W - w > 0) rect.insert(Rect(cover.W - w, cover.L, cover.x + w, cover.y));
                }
            }
            // LUONG XUAN NGUYEN'S GREEDY BASE
            // ###############################
        }
        // up date queue
        if(in_use)
        {
            real_item_cnt = cant_item_cnt;
            for_x(i, 1, cant_item_cnt) real_item_queue[i] = cant_item_queue[i];
            return truck[id_truck].se.fi;
        }
        return 0;
    }
}

int process(int pos) // xu li ham f()
{
    // init
    item_cnt = real_item_cnt;
    for_x(i, 1, real_item_cnt) item_queue[i] = real_item_queue[i];
    //for_x(i, 1, real_item_cnt) cout << item_queue[i] << " "; // DEBUG
    //cout << "\n"; // DEBUG
    // tinh cost
    int cost = 0;
    for(int i = pos - 1; i <= k && item_cnt && cost < candidate_cost; i++)
    {
        if(danh_dau_truck != i)
        {
            cost += try_to_fill(i, 0); // handle truong hop truck do khong duoc dung
            //cout << truck[i].fi.fi << " " << truck[i].fi.se << " " << truck[i].se.fi << "?\n"; // DEBUG
            //cout << item_cnt << "hle\n"; // DEBUG
        }
    }
    return cost;
}

void best_first_search(int pos)
{
    if(real_item_cnt == 0) return;
    // init
    sort(truck + pos, truck + k + 1, cmp_truck);
    //cout << pos << "wtf\n"; // DEBUG
    //for_x(i, pos, k) cout << truck[i].fi.fi << " " << truck[i].fi.se << " " << truck[i].se.fi << "?\n"; // DEBUG
    int candidate_truck, cost;
    candidate_cost = inf;
    // tim candidate o vi tri dau tien (theo pos)
    for_x(i, pos, k)
    {
        truck[pos - 1] = truck[i], danh_dau_truck = i;
        cost = process(pos);
        if(cost < candidate_cost) candidate_cost = cost, candidate_truck = i;
        //cout << cost << "nihao\n"; // DEBUG
    }
    // xu li real
    truck[pos - 1] = truck[candidate_truck];
    total_cost += try_to_fill(pos - 1, 1);
    for(int i = candidate_truck; i > pos; i--) truck[i] = truck[i - 1];
    //cout << total_cost << " " << candidate_cost << " " << real_item_cnt << "omg\n"; // DEBUG
}

void solve()
{
    // input
    cin >> n >> k;
    for_x(i, 1, n)
    {
        cin >> item[i].fi.fi >> item[i].fi.se;
        item[i].se = i;
    }
    for_x(i, 1, k)
    {
        cin >> truck[i].fi.fi >> truck[i].fi.se >> truck[i].se.fi;
        truck[i].se.se = i;
    }
    // sort item
    sort(item + 1, item + n + 1, cmp_item);
    reverse(item + 1, item + n + 1);
    //for_x(i, 1, n) cout << item[i].fi.fi << " " << item[i].fi.se << " " << item[i].se << "\n"; // DEBUG
    real_item_cnt = n;
    for_x(i, 1, n) real_item_queue[i] = i;
    // tim hoan vi
    for_x(pos, 1, k) best_first_search(pos); // tim candidate cho pos
    //cout << total_cost; // DEBUG
    //cout << real_item_cnt << "\n"; // DEBUG
    for_x(i, 1, n) cout << i << " " << ans[i].fi.fi << " " << ans[i].fi.se << " " << ans[i].se.fi << " " << ans[i].se.se << "\n";
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    //freopen("main.inp", "r", stdin);
    //freopen("main.out", "w", stdout);
    solve();
}
