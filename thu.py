# Staff scheduling – 6:00→24:00 (18 giờ)
# FT: 5h làm – 1h nghỉ – 4h làm, $189/ca; PT: 5h liên tục, $65/ca
# Q1: tối thiểu chi phí. Q2: thêm ràng buộc ≥1 FT mỗi giờ & tổng FT ≥ 6.

import numpy as np, math

HOURS = 18
labels = [f"{6+i}:00-{7+i}:00" if 7+i < 24 else f"{6+i}:00-Midnight" for i in range(HOURS)]
req = np.array([3,4,6,7,8,9,8,9,8,7,6,5,4,4,3,3,2,2 ], dtype=int)
FT_COST, PT_COST = 189, 65

def ft_cov(start):
    c = np.zeros(HOURS, int)
    c[start:start+5] = 1
    c[start+6:start+10] = 1  # nghỉ 1h ở (start+5)
    return c[:HOURS]

def pt_cov(start):
    c = np.zeros(HOURS, int)
    c[start:start+5] = 1
    return c[:HOURS]

FT_STARTS = range(0, 9)   # start+9 <= 18
PT_STARTS = range(0, 14)  # start+5 <= 18
FT_COV = np.stack([ft_cov(s) for s in range(HOURS)])  # [start, hour]
PT_COV = np.stack([pt_cov(s) for s in range(HOURS)])

def greedy_pt(deficit):
    """Thêm PT greedily để phủ deficit."""
    deficit = deficit.copy()
    cnt = np.zeros(HOURS, int)
    while (deficit > 0).any():
        # chọn start PT phủ được nhiều deficit nhất
        best_gain, best_s = 0, None
        for s in PT_STARTS:
            gain = int(np.minimum(deficit, PT_COV[s]).sum())
            if gain > best_gain:
                best_gain, best_s = gain, s
        if best_gain == 0:  # không cải thiện thêm
            break
        cnt[best_s] += 1
        deficit = np.maximum(0, deficit - PT_COV[best_s])
    return cnt, deficit

def summarize(ft, pt):
    cover_ft = (ft[:, None] * FT_COV).sum(0)
    cover_pt = (pt[:, None] * PT_COV).sum(0)
    cover = cover_ft + cover_pt
    return dict(
        ok = bool((cover >= req).all()),
        cost = int(ft.sum())*FT_COST + int(pt.sum())*PT_COST,
        ft_shifts = int(ft.sum()),
        pt_shifts = int(pt.sum()),
        cover=cover, cover_ft=cover_ft, cover_pt=cover_pt
    )

# Q1 – PT-only optimal (vì rẻ hơn/h)
def solve_q1():
    pt, rem = greedy_pt(req)
    assert not (rem>0).any(), "Input không phủ đủ bằng PT."
    ft = np.zeros(HOURS, int)
    return ft, pt, summarize(ft, pt)

# Q2 – ≥1 FT mỗi giờ & tổng FT ≥ 6 (branch&bound + PT greedy)
def solve_q2(min_ft_total=6, min_ft_each_hr=1):
    best = {"cost": 10**9, "ft": None, "pt": None}
    MAX_FT_PER_START = 6

    def branch(i, cover_ft, ft_cnt, ft_sum):
        deficit = np.maximum(0, req - cover_ft)
        lb = ft_sum*FT_COST + math.ceil(deficit.sum()/5)*PT_COST
        if lb >= best["cost"]:
            return
        if i == 9:
            if ft_sum < min_ft_total: return
            if (cover_ft < min_ft_each_hr).any(): return
            pt_cnt, rem = greedy_pt(np.maximum(0, req - cover_ft))
            if (rem>0).any(): return
            cost = ft_sum*FT_COST + int(pt_cnt.sum())*PT_COST
            if cost < best["cost"]:
                best.update(cost=cost, ft=ft_cnt.copy(), pt=pt_cnt.copy())
            return

        cov = FT_COV[i]
        for k in range(0, MAX_FT_PER_START+1):
            new_cover = cover_ft + k*cov
            # ✅ Đổi 3 dòng dưới cho đúng:
            new_ft = ft_cnt.copy()
            new_ft[i] = k
            branch(i+1, new_cover, new_ft, ft_sum+k)

    branch(0, np.zeros(HOURS, int), np.zeros(HOURS, int), 0)
    return best["ft"], best["pt"], summarize(best["ft"], best["pt"])


def print_solution(tag, ft, pt, s):
    print(f"\n== {tag} ==")
    print(f"Cost = ${s['cost']} | FT = {s['ft_shifts']} | PT = {s['pt_shifts']} | Feasible = {s['ok']}")
    # In các start times khác 0
    ft_starts = [(i, int(ft[i])) for i in FT_STARTS if ft[i]>0]
    pt_starts = [(i, int(pt[i])) for i in PT_STARTS if pt[i]>0]
    if ft_starts:
        print("FT starts (hour index from 0=6:00):", ft_starts)
    if pt_starts:
        print("PT starts (hour index from 0=6:00):", pt_starts)
    # Kiểm tra phủ theo giờ
    print("Hour-by-hour  Required | FT_on | PT_on | Total")
    cover_ft = s['cover_ft']; cover_pt = s['cover_pt']
    for t in range(HOURS):
        print(f"{labels[t]:<16} {req[t]:>3}        {cover_ft[t]:>3}     {cover_pt[t]:>3}     {cover_ft[t]+cover_pt[t]:>3}")

if __name__ == "__main__":
    ft1, pt1, s1 = solve_q1()
    print_solution("Q1 (min-cost)", ft1, pt1, s1)

    ft2, pt2, s2 = solve_q2(min_ft_total=6, min_ft_each_hr=1)
    print_solution("Q2 (≥1 FT/hr & ≥6 FT total)", ft2, pt2, s2)
