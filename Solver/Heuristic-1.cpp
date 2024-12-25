// Heuristic Basic Greedy - Group 9

#include <bits/stdc++.h>
using namespace std;

struct Rect {
    int W, L, x, y;
    Rect(): W(0), L(0), x(0), y(0) {}
    Rect(int W, int L, int x, int y): W(W), L(L), x(x), y(y) {}

    bool operator<(const Rect &x) const {
        if (max(W, L) != max(x.W, x.L)) return max(W, L) < max(x.W, x.L);
        return min(W, L) < min(x.W, x.L);
    }
};
struct Item {
    int w, l, i;
    Item(): w(0), l(0), i(0) {}
    Item(int w, int l, int i): w(w), l(l), i(i) {}

    bool operator<(const Item &x) {
        if (max(w, l) != max(x.w, x.l)) return max(w, l) < max(x.w, x.l);
        return min(w, l) < min(x.w, x.l);
    }
};
struct ItemAns {
    int t, i, x, y, o;
    ItemAns(): t(0), i(0), x(0), y(0), o(0) {}
    ItemAns(int t, int i, int x, int y, int o): t(t), i(i), x(x), y(y), o(o) {}

    bool operator<(const ItemAns &x) {
        return i < x.i;
    }
};

const int N = 1e4 + 5;
int n, k;
Item it[N];
vector<ItemAns> ans;

struct Truck {
    int W, L, c, i;
    set<Rect> rect;
    Truck(): W(0), L(0), c(0), i(0) {
        rect.insert(Rect(W, L, 0, 0));
    }
    Truck(int W, int L, int c, int i): W(W), L(L), c(c), i(i) {
        rect.insert(Rect(W, L, 0, 0));
    }

    bool operator<(const Truck &x) {
        if (max(W, L) != max(x.W, x.L)) return max(W, L) < max(x.W, x.L);
        return min(W, L) < min(x.W, x.L);
    }

    vector<ItemAns> itemStore;
    vector<int> putItemsIntoTruck(vector<int> it_id, int clear) {
        vector<int> ret;

        for (int id : it_id) {
            int w, l;
            w = it[id].w; l = it[id].l;
            Rect r = Rect(w, l, 0, 0);
            auto iter = rect.lower_bound(r);
            for (; iter != rect.end(); iter++) {
                Rect c = *iter;
                if (max(w, l) <= max(c.W, c.L) && min(w, l) <= min(c.W, c.L)) break;
            }
            if (iter == rect.end()) {
                ret.push_back(id);
                continue;
            }
            Rect cover = *iter;
            Rect rect1, rect2;

            if (cover.W < cover.L) {
                if (w < l) {
                    itemStore.push_back(ItemAns(i, it[id].i, cover.x, cover.y, 0));
                    if (cover.L - l > 0) rect1 = Rect(cover.W, cover.L - l, cover.x, cover.y + l);
                    if (cover.W - w > 0) rect2 = Rect(cover.W - w, l, cover.x + w, cover.y);
                } else {
                    itemStore.push_back(ItemAns(i, it[id].i, cover.x, cover.y, 1));
                    if (cover.L - w > 0) rect1 = Rect(cover.W, cover.L - w, cover.x, cover.y + w);
                    if (cover.W - l > 0) rect2 = Rect(cover.W - l, w, cover.x + l, cover.y);
                }
            } else {
                if (w < l) {
                    itemStore.push_back(ItemAns(i, it[id].i, cover.x, cover.y, 1));
                    if (cover.L - w > 0) rect1 = Rect(l, cover.L - w, cover.x, cover.y + w);
                    if (cover.W - l > 0) rect2 = Rect(cover.W - l, cover.L, cover.x + l, cover.y);
                } else {
                    itemStore.push_back(ItemAns(i, it[id].i, cover.x, cover.y, 0));
                    if (cover.L - l > 0) rect1 = Rect(w, cover.L - l, cover.x, cover.y + l);
                    if (cover.W - w > 0) rect2 = Rect(cover.W - w, cover.L, cover.x + w, cover.y);
                }
            }
            rect.erase(iter);
            rect.insert(rect1);
            rect.insert(rect2);
        }
        if (clear) {
            rect.clear();
            itemStore.clear();
            rect.insert(Rect(W, L, 0, 0));
        }
        return ret;
    }
};

Truck tr[N];

bool cmp1(const Truck &x, const Truck &y) {
    return x.c < y.c;
}

bool cmp2(const Truck &x, const Truck &y) {
    return x.W * x.L > y.W * y.L;
}

bool cmp3(const Truck &x, const Truck &y) {
    return double(x.c) / (x.W * x.L) < double(y.c) / (y.W * y.L);
}

int minCost = int(1e9);

void processCurrentState() {
    vector<int> itemIdx(n);
    int cost = 0;
    iota(itemIdx.begin(), itemIdx.end(), 1);
    int maxk = k;

    for (int i = 1; i <= k; ++i) {
        if (itemIdx.size() == 0) {
            maxk = i;
            break;
        }
        vector<int> newItemIdx;
        for (int idx : itemIdx) {
            vector<int> ret = tr[i].putItemsIntoTruck({idx}, 0);
            if (ret.size() == 1) newItemIdx.push_back(ret[0]);
        }
        if (itemIdx.size() > newItemIdx.size()) cost += tr[i].c;
        itemIdx = newItemIdx;
    }

    if (cost < minCost) {
        minCost = cost;
        ans.clear();
        for (int i = 1; i <= maxk; ++i) 
            for (ItemAns it : tr[i].itemStore)
                ans.push_back(it);
    }

    for (int i = 1; i <= maxk; ++i)
        tr[i].putItemsIntoTruck({}, 1);
}

int main() {
    // freopen("text.inp", "r", stdin);
    // freopen("text.out", "w", stdout);

    cin >> n >> k;
    for (int i = 1; i <= n; ++i) {
        int w, l; cin >> w >> l;
        it[i] = Item(w, l, i);
    }
    for (int i = 1; i <= k; ++i) {
        int W, L, c; cin >> W >> L >> c;
        tr[i] = Truck(W, L, c, i);
    }

    sort(it + 1, it + n + 1);
    reverse(it + 1, it + n + 1);

    sort(tr + 1, tr + k + 1);
    reverse(tr + 1, tr + k + 1);
    processCurrentState();

    sort(tr + 1, tr + k + 1, cmp1);
    processCurrentState();

    sort(tr + 1, tr + k + 1, cmp2);
    processCurrentState();

    sort(tr + 1, tr + k + 1, cmp3);
    processCurrentState(); 

    sort(ans.begin(), ans.end());
    for (ItemAns i : ans)
        cout << i.i << ' ' << i.t << ' ' << i.x << ' ' << i.y << ' ' << i.o << '\n';
    return 0;
}

/*
5 5
90 70
10 70
80 30 
100 60
20 90 
180 120 8 
20 100 10 
160 50 6
120 140 11
180 30 7 
*/