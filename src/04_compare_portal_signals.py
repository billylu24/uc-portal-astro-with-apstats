import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import warnings

warnings.filterwarnings('ignore')

INPUT_CSV = "data/processed/uc_applications_ai_major_categories.csv"
try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"Error: 找不到文件 {INPUT_CSV}")
    exit()

# 数据列映射与强制数值化
metrics = {
    "GPA_UW": "GPA(UC UW)?",
    "GPA_W": "GPA(UC W)",
    "PIQ": "Rate your piqs on a scale of 1-10",
    "EC": "Rate your ec's on a scale of 1-10"
}
for short_name, original_name in metrics.items():
    if original_name in df.columns:
        df[short_name] = pd.to_numeric(df[original_name], errors='coerce')


def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / pooled_std if pooled_std > 0 else 0


# ==========================================
# 1. 基础数据统计 (Basic Counts)
# ==========================================
print("=== Basic Astrology Status Counts ===")
astrology_cols_raw = {
    "UCB (Berkeley id or email?)": df.get("Berkeley id or email?"),
    "UCSD (Is your UCSD #3 prestige banner there?)": df.get("Is your UCSD #3 prestige banner there?"),
    "UCI (Can you log in to the UCI link?)": df.get("Can you log in to the UCI link?")
}
for name, series in astrology_cols_raw.items():
    if series is not None:
        counts = series.astype(str).str.strip().str.title().value_counts()
        print(f"\n{name}:")
        for k, v in counts.items():
            print(f"  {k}: {v}")
print("\n=======================================================\n")


# ==========================================
# 2. 核心统计引擎 (纯数据输出)
# ==========================================
def run_stats_terse(school_name, ast_col, positive_val, negative_val):
    if ast_col not in df.columns: return

    # 过滤与打标 (1 = 好兆头, 0 = 坏兆头)
    s = df[ast_col].astype(str).str.strip().str.lower()
    df_school = df[s.isin([positive_val.lower(), negative_val.lower()])].copy()
    df_school['Treatment'] = (s == positive_val.lower()).astype(int)

    g1 = df_school[df_school['Treatment'] == 1]
    g0 = df_school[df_school['Treatment'] == 0]

    if len(g1) < 5 or len(g0) < 5:
        print(f"[{school_name}] Insufficient data for {positive_val} vs {negative_val}\n")
        return

    print(f"[{school_name}] Good Omen = '{positive_val}' (N={len(g1)}) | Bad Omen = '{negative_val}' (N={len(g0)})")
    print(
        f"{'Metric':<8} | {'Mean(G)':<8} | {'Mean(B)':<8} | {'Diff':<7} | {'P-Val':<6} | {'Cohen_d':<8} | {'Bayes(G>B)':<10} | {'PSM_Diff':<8}")
    print("-" * 85)

    # PSM 预处理 (控制 PIQ 和 EC)
    df_psm = df_school.dropna(subset=['PIQ', 'EC', 'GPA_UW', 'GPA_W', 'Treatment']).copy()
    psm_valid = len(df_psm[df_psm['Treatment'] == 1]) >= 5 and len(df_psm[df_psm['Treatment'] == 0]) >= 5

    if psm_valid:
        X = df_psm[['PIQ', 'EC']]
        y = df_psm['Treatment']
        lr = LogisticRegression(solver='liblinear').fit(X, y)
        df_psm['PS'] = lr.predict_proba(X)[:, 1]
        t_psm = df_psm[df_psm['Treatment'] == 1]
        c_psm = df_psm[df_psm['Treatment'] == 0]
        nn = NearestNeighbors(n_neighbors=1, metric='euclidean').fit(c_psm[['PS']])
        distances, indices = nn.kneighbors(t_psm[['PS']])
        matched_c = c_psm.iloc[indices.flatten()]

    # 循环计算四个指标
    for var in ['GPA_UW', 'GPA_W', 'PIQ', 'EC']:
        d1, d0 = g1[var].dropna(), g0[var].dropna()
        if len(d1) < 3 or len(d0) < 3:
            continue

        m1, m0 = d1.mean(), d0.mean()
        diff = m1 - m0
        t_stat, p_val = stats.ttest_ind(d1, d0, equal_var=False)
        d_val = cohens_d(d1, d0)

        # 贝叶斯后验概率
        sims = 100000
        s1 = np.random.normal(m1, d1.std() / np.sqrt(len(d1)) if d1.std() > 0 else 0.01, sims)
        s0 = np.random.normal(m0, d0.std() / np.sqrt(len(d0)) if d0.std() > 0 else 0.01, sims)
        bayes_prob = (s1 > s0).mean() * 100

        # PSM 计算纯学术差距 (仅针对 GPA 输出)
        psm_diff_str = "N/A"
        if psm_valid and var in ['GPA_UW', 'GPA_W']:
            t_mean = t_psm[var].mean()
            c_mean = matched_c[var].mean()
            psm_diff_str = f"{t_mean - c_mean:+.3f}"

        print(
            f"{var:<8} | {m1:<8.3f} | {m0:<8.3f} | {diff:<+7.3f} | {p_val:<6.4f} | {d_val:<8.3f} | {bayes_prob:>7.1f}% | {psm_diff_str}")
    print("\n")


# ==========================================
# 3. 批量执行
# ==========================================
run_stats_terse("UC Berkeley", "Berkeley id or email?", "Id", "Email")

# 修正：UCSD Banner 消失（No）才是录取的好兆头，Yes 是坏兆头
run_stats_terse("UC San Diego", "Is your UCSD #3 prestige banner there?", "No", "Yes")

run_stats_terse("UC Irvine", "Can you log in to the UCI link?", "Yes", "No")
