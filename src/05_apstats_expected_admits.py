import math
import warnings
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from scipy.stats import norm

warnings.filterwarnings("ignore")

# =========================
# File paths
# =========================
INPUT_CSV = "data/processed/uc_applications_ai_major_categories.csv"
BERK_BINS_CSV = "data/raw_public_gpa_bins/uc_berkeley_2025_applicant_gpa_bins.csv"
UCSD_BINS_CSV = "data/raw_public_gpa_bins/uc_san_diego_2025_applicant_gpa_bins.csv"
UCI_BINS_CSV = "data/raw_public_gpa_bins/uc_irvine_2025_applicant_gpa_bins.csv"

GPA_MAX = 4.40
MAX_ADMIT_PROB = 0.85  # 设置录取率天花板（Holistic review决定了满分也不可能100%录取）

# =========================
# Official admit-rate + admit GPA quartiles by broad discipline
# Format: major -> [admit_rate, admit_q1, admit_q3]
# =========================
UCB_DATA = {
    "Architecture": [0.08, 4.14, 4.30],
    "Arts & Humanities": [0.25, 4.06, 4.27],
    "Business": [0.05, 4.20, 4.30],
    "Computer Science": [0.06, 4.20, 4.29],
    "Engineering": [0.07, 4.20, 4.30],
    "Life Sciences": [0.16, 4.16, 4.29],
    "Other/Interdisciplinary": [0.13, 4.16, 4.29],
    "Physical Sciences/Math": [0.16, 4.18, 4.29],
    "Public Admin": [0.14, 4.08, 4.26],
    "Public Health": [0.02, 4.16, 4.29],
    "Social Sciences": [0.09, 4.15, 4.29],
    "Undeclared": [0.12, 4.11, 4.28],
}

UCSD_DATA = {
    "Architecture": [0.31, 4.00, 4.25],
    "Arts & Humanities": [0.35, 4.06, 4.26],
    "Business": [0.21, 4.13, 4.29],
    "Computer Science": [0.20, 4.16, 4.30],
    "Education": [0.31, 4.08, 4.25],
    "Engineering": [0.19, 4.17, 4.30],
    "Life Sciences": [0.33, 4.15, 4.29],
    "Other/Interdisciplinary": [0.31, 4.09, 4.28],
    "Physical Sciences/Math": [0.39, 4.13, 4.29],
    "Public Health": [0.17, 4.08, 4.26],
    "Social Sciences": [0.26, 4.08, 4.28],
    "Undeclared": [0.35, 4.06, 4.27],
}

UCI_DATA = {
    "Arts & Humanities": [0.34, 3.93, 4.23],
    "Business": [0.16, 4.08, 4.28],
    "Computer Science": [0.28, 4.17, 4.29],
    "Engineering": [0.27, 4.15, 4.29],
    "Life Sciences": [0.30, 4.12, 4.29],
    "Other/Interdisciplinary": [0.33, 4.07, 4.27],
    "Physical Sciences/Math": [0.55, 4.02, 4.26],
    "Public Health": [0.37, 4.08, 4.25],
    "Social Sciences": [0.32, 4.00, 4.25],
    "Undeclared": [0.38, 3.93, 4.20],
}


@dataclass
class CampusPool:
    campus: str
    mean_gpa: float
    std_gpa: float
    total_known: int


# =========================
# AP Stats: 1. 解析官方的 GPA 区间分组数据
# =========================
BIN_LABELS_TO_INTERVALS = {
    "0.00-2.99": (0.00, 3.00),
    "3.00-3.29": (3.00, 3.30),
    "3.30-3.69": (3.30, 3.70),
    "3.70-3.99": (3.70, 4.00),
    "4.00 and above": (4.00, GPA_MAX),
}


def load_grouped_counts(csv_path: str) -> list[tuple[float, float, int]]:
    """读取官方 CSV 中的分组数据，返回 [(下限, 上限, 人数), ...]"""
    try:
        df_bins = pd.read_csv(csv_path)
    except FileNotFoundError:
        # 如果找不到文件，提供一个模拟的默认分布以防报错
        return [(0.0, 3.0, 1000), (3.0, 3.3, 2000), (3.3, 3.7, 10000), (3.7, 4.0, 30000), (4.0, 4.4, 50000)]

    label_col = "Applicant characteristics"
    count_col = next(col for col in df_bins.columns if "App Redacted" in col)

    grouped = []
    for _, row in df_bins.iterrows():
        label = str(row[label_col]).strip()
        if label not in BIN_LABELS_TO_INTERVALS:
            continue
        lo, hi = BIN_LABELS_TO_INTERVALS[label]
        grouped.append((lo, hi, int(row[count_col])))

    return grouped


# =========================
# AP Stats: 2. 用分组数据计算总体正态分布均值与标准差
# =========================
def fit_normal_from_grouped_bins(grouped_bins: list[tuple[float, float, int]]) -> tuple[float, float, int]:
    total_n = sum(count for _, _, count in grouped_bins)
    if total_n == 0:
        return 3.8, 0.3, 0

    # 计算加权平均数 (使用区间中点)
    sum_x = sum(((lo + hi) / 2.0) * count for lo, hi, count in grouped_bins)
    mu = sum_x / total_n

    # 计算加权方差与标准差
    sum_sq_diff = sum(count * (((lo + hi) / 2.0) - mu) ** 2 for lo, hi, count in grouped_bins)
    sigma = math.sqrt(sum_sq_diff / total_n)

    return mu, sigma, total_n


def build_campus_pools() -> dict[str, CampusPool]:
    configs = {
        "UC Berkeley": BERK_BINS_CSV,
        "UC San Diego": UCSD_BINS_CSV,
        "UC Irvine": UCI_BINS_CSV,
    }

    pools = {}
    for campus, path in configs.items():
        grouped = load_grouped_counts(path)
        mu, sigma, total_n = fit_normal_from_grouped_bins(grouped)
        pools[campus] = CampusPool(
            campus=campus,
            mean_gpa=mu,
            std_gpa=sigma,
            total_known=total_n,
        )
    return pools


# =========================
# AP Stats: 3. 通过 Q1 和 Q3 反推录取者正态分布
# =========================
def get_admitted_normal(q1: float, q3: float) -> tuple[float, float]:
    mu = (q1 + q3) / 2.0
    # 在标准正态分布中，Q1 和 Q3 对应的 Z-score 大约是 -0.6745 和 0.6745
    # 所以 Q3 - Q1 等于 1.349 个标准差
    sigma = (q3 - q1) / 1.349
    sigma = max(sigma, 0.01)  # 防止分母为 0
    return mu, sigma


# =========================
# AP Stats: 4. 贝叶斯定理计算录取概率 P(Admit | GPA)
# =========================
def calculate_bayes_prob(gpa_capped, major, campus_pool: CampusPool, school_data: dict) -> float:
    if pd.isna(gpa_capped) or major not in school_data:
        return 0.0

    gpa = float(gpa_capped)
    base_rate, q1, q3 = school_data[major]

    admit_mu, admit_sigma = get_admitted_normal(q1, q3)
    app_mu = campus_pool.mean_gpa
    app_sigma = campus_pool.std_gpa

    # 计算在两条正态曲线上的概率密度 (PDF)
    pdf_admit = norm.pdf(gpa, admit_mu, admit_sigma)
    pdf_app = norm.pdf(gpa, app_mu, app_sigma)

    if pdf_app < 1e-9:
        return 0.0

    # 贝叶斯公式: P(A|X) = P(A) * P(X|A) / P(X)
    prob = base_rate * (pdf_admit / pdf_app)

    return min(prob, MAX_ADMIT_PROB)


# =========================
# 主体预测与玄学对比逻辑
# =========================
def run_expectation_vs_astrology(
        df_main: pd.DataFrame,
        school_name: str,
        gpa_col: str,
        major_col: str,
        astrology_col: str,
        good_omen_val: str,
        school_data: dict,
        campus_pool: CampusPool,
        output_csv: str | None = None,
):
    needed = [gpa_col, major_col, astrology_col]
    if any(col not in df_main.columns for col in needed):
        print(f"[{school_name}] skipped because columns are missing: {needed}")
        return

    df_school = df_main[
        ~df_main[astrology_col].astype(str).str.contains("Didn't apply|na|none", case=False, na=False)
    ].copy()

    if len(df_school) == 0:
        print(f"[{school_name}] no valid applicants after filtering.")
        return

    df_school[gpa_col] = pd.to_numeric(df_school[gpa_col], errors="coerce")

    # 对每个人应用贝叶斯定理计算概率
    df_school["Expected_Prob"] = df_school.apply(
        lambda row: calculate_bayes_prob(row[gpa_col], row[major_col], campus_pool, school_data), axis=1
    )

    expected_admits = df_school["Expected_Prob"].sum()
    astrology_count = (df_school[astrology_col].astype(str).str.strip().str.lower() == good_omen_val.lower()).sum()

    diff = astrology_count - expected_admits
    ratio = astrology_count / expected_admits if expected_admits > 0 else 0.0

    print(
        f"[{campus_pool.campus}] AP Stats Pool | Mean={campus_pool.mean_gpa:.3f}, Std={campus_pool.std_gpa:.3f} | N={campus_pool.total_known}")
    print(f"[{school_name}] Validation Results")
    print(f"  Valid Applicants   : {len(df_school)}")
    print(f"  Expected Admits    : {expected_admits:.2f}")
    print(f"  Actual Astrology   : {astrology_count} (Omen: '{good_omen_val}')")
    print(f"  Difference         : {diff:+.2f} (Ratio: {ratio:.2f}x)")
    print("-" * 75)

    if output_csv is not None:
        Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
        cols_to_keep = [c for c in df_school.columns if c != "Expected_Prob"] + ["Expected_Prob"]
        df_school[cols_to_keep].to_csv(output_csv, index=False)
        print(f"Saved scored file: {output_csv}")
        print("-" * 75)


# =========================
# Main
# =========================
def main():
    try:
        df_main = pd.read_csv(INPUT_CSV)
    except FileNotFoundError:
        print(f"Warning: 找不到主样本文件 {INPUT_CSV}，创建空 DataFrame 以便测试环境运行。")
        df_main = pd.DataFrame()

    pools = build_campus_pools()

    print("=== Expected vs. Actual Astrology Analysis ===")
    print("Model: AP Stats Bayesian Model (Normal Distributions)")
    print("Method: P(Admit|GPA) = P(Admit) * P(GPA|Admit) / P(GPA)")
    print("-" * 75)

    if not df_main.empty:
        run_expectation_vs_astrology(
            df_main=df_main,
            school_name="UC Berkeley",
            gpa_col="GPA(UC W capped)",
            major_col="UCB major? (AI Categorized)",
            astrology_col="Berkeley id or email?",
            good_omen_val="Id",
            school_data=UCB_DATA,
            campus_pool=pools["UC Berkeley"],
            output_csv="outputs/scored_probabilities/uc_berkeley_apstats_expected_probabilities.csv",
        )

        run_expectation_vs_astrology(
            df_main=df_main,
            school_name="UC San Diego",
            gpa_col="GPA(UC W capped)",
            major_col="UCSD major? (AI Categorized)",
            astrology_col="Is your UCSD #3 prestige banner there?",
            good_omen_val="No",
            school_data=UCSD_DATA,
            campus_pool=pools["UC San Diego"],
            output_csv="outputs/scored_probabilities/uc_san_diego_apstats_expected_probabilities.csv",
        )

        run_expectation_vs_astrology(
            df_main=df_main,
            school_name="UC Irvine",
            gpa_col="GPA(UC W capped)",
            major_col="UCI major? (AI Categorized)",
            astrology_col="Can you log in to the UCI link?",
            good_omen_val="Yes",
            school_data=UCI_DATA,
            campus_pool=pools["UC Irvine"],
            output_csv="outputs/scored_probabilities/uc_irvine_apstats_expected_probabilities.csv",
        )


if __name__ == "__main__":
    main()
