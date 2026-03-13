import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# ⚙️ 配置区
# ==========================================
# 确保这里读取的是你用大模型清洗后的文件
INPUT_CSV = "uc_data_final_ai_cleaned.csv"

try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"[错误] 找不到文件 {INPUT_CSV}，请确认文件名！")
    exit()

# 设置图表风格 (英文标签，防止本地电脑缺少中文字体导致乱码)
sns.set_theme(style="whitegrid")

print("=" * 50)
print(f"🎓 UC 申请者样本人群分析报告 (基于 AI 清洗数据)")
print(f"总有效样本数: {len(df)} 人")
print("=" * 50)

# ==========================================
# 1. GPA 分析 (文本 + 图表) - 0.1 颗粒度升级版
# ==========================================
print("\n📊 1. GPA 学术竞争力分析")
gpa_cols = ["GPA(UC UW)?", "GPA(UC W)", "GPA(UC W capped)"]
gpa_stats = df[gpa_cols].describe().round(2).loc[['mean', '50%', 'min', 'max']]
gpa_stats.index = ['平均分 (Mean)', '中位数 (Median)', '最低分 (Min)', '最高分 (Max)']
print(gpa_stats)

# 画图 1：GPA 分布直方图
plt.figure(figsize=(15, 5))
for i, col in enumerate(gpa_cols, 1):
    plt.subplot(1, 3, i)
    # 过滤掉空值画图
    data_to_plot = df[col].dropna()

    # 🌟 核心修改：去掉 bins=15，替换为 binwidth=0.1
    sns.histplot(data_to_plot, kde=True, binwidth=0.1, color="skyblue")

    # 可选优化：让 x 轴的刻度也更细致，方便你对齐查看
    import numpy as np

    min_val = np.floor(data_to_plot.min() * 10) / 10  # 向下取整到 0.1
    max_val = np.ceil(data_to_plot.max() * 10) / 10  # 向上取整到 0.1
    plt.xticks(np.arange(min_val, max_val + 0.1, 0.2))  # 每 0.2 标一个刻度

    plt.title(f'Distribution of {col}')
    plt.xlabel('GPA')
    plt.ylabel('Count')

plt.tight_layout()
plt.savefig("1_GPA_Distribution_Micro.png", dpi=300)
plt.show()
# ==========================================
# 2. 软实力 PIQ & EC 评估分析 (文本 + 图表)
# ==========================================
print("\n📝 2. 软实力自我评估 (PIQ & EC, 1-10分)")
rating_cols = ["Rate your piqs on a scale of 1-10", "Rate your ec's on a scale of 1-10"]
rating_stats = df[rating_cols].describe().round(2).loc[['mean', '50%', 'min', 'max']]
rating_stats.index = ['平均分 (Mean)', '中位数 (Median)', '最低分 (Min)', '最高分 (Max)']
print(rating_stats)

# 画图 2：PIQ & EC 柱状图
plt.figure(figsize=(12, 5))
for i, col in enumerate(rating_cols, 1):
    plt.subplot(1, 2, i)
    # 统计 1-10 分每个分数的频次
    score_counts = df[col].dropna().value_counts().sort_index()
    sns.barplot(x=score_counts.index.astype(int), y=score_counts.values, palette="viridis")

    title = "PIQ Self-Rating" if "piq" in col.lower() else "EC Self-Rating"
    plt.title(f'Distribution of {title}')
    plt.xlabel('Score (1-10)')
    plt.ylabel('Number of Applicants')
plt.tight_layout()
plt.savefig("2_PIQ_EC_Distribution.png", dpi=300)
plt.show()

# ==========================================
# 3. 热门专业 Top 10 (基于 AI 归类) (文本 + 图表)
# ==========================================
print("\n🏫 3. 热门申请专业大类分布 (Top 10)")

# ⚠️ 注意这里使用的是你用 AI 清洗出的新列！
ai_major_cols = {
    "UCB": "UCB major? (AI Categorized)",
    "UCSD": "UCSD major? (AI Categorized)",
    "UCI": "UCI major? (AI Categorized)"
}

plt.figure(figsize=(18, 6))
for i, (school, col) in enumerate(ai_major_cols.items(), 1):
    if col in df.columns:
        print(f"\n--- {school} 申请专业大类 Top 10 ---")

        # 排除 "Other / Unknown"，获取 Top 10
        valid_majors = df[df[col] != "Other / Unknown"][col].dropna()
        top10 = valid_majors.value_counts().head(10)

        for rank, (major, count) in enumerate(top10.items(), 1):
            print(f"{rank}. {major} - {count}人 ({(count / len(valid_majors)) * 100:.1f}%)")

        # 画图 3：各校专业 Top 10 水平柱状图
        plt.subplot(1, 3, i)
        sns.barplot(y=top10.index, x=top10.values, palette="magma")
        plt.title(f'Top 10 Majors for {school}')
        plt.xlabel('Number of Applicants')
        plt.ylabel('')  # 隐藏 y 轴标签让画面更干净
plt.tight_layout()
plt.savefig("3_Top_Majors.png", dpi=300)
plt.show()

print("\n🎉 分析完成！所有图表不仅在屏幕上弹出了，还自动保存在了你代码所在的文件夹里 (高清 PNG 格式)。")