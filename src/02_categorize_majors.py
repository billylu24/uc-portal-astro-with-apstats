import pandas as pd
import ollama

# ==========================================
# ⚙️ 配置区 (请确认这里的输入文件名)
# ==========================================
INPUT_CSV = "data/processed/uc_application_data_cleaned.csv"
OUTPUT_CSV = "data/processed/uc_applications_ai_major_categories.csv"
MODEL_NAME = "qwen2.5:3b"  # 使用的本地 AI 模型

# ==========================================
# 📊 定义 UC 官方 12 个专业大类
# ==========================================
CATEGORIES = [
    "Architecture",
    "Arts & Humanities",
    "Business",
    "Computer Science",
    "Engineering",
    "Life Sciences",
    "Other/Interdisciplinary",
    "Physical Sciences/Math",
    "Public Admin",
    "Public Health",
    "Social Sciences",
    "Undeclared"
]
category_list_str = "\n".join([f"- {c}" for c in CATEGORIES])


def classify_major_with_llm(major_name):
    """调用本地 Ollama 模型进行分类"""
    if pd.isna(major_name) or str(major_name).strip() == '':
        return "Undeclared" # 遇到空缺直接归类为未定

    prompt = f"""
    Classify the following college major into EXACTLY ONE of the official University of California categories below. 
    Categories:
    {category_list_str}

    Major to classify: "{major_name}"
    Output ONLY the exact category name. No extra words, no explanations.
    """

    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt}
        ])

        ai_answer = response['message']['content'].strip()
        # 兜底验证：如果 AI 话痨了，强行匹配这 12 个官方分类
        for cat in CATEGORIES:
            if cat.lower() in ai_answer.lower():
                return cat
        return "Other/Interdisciplinary"
    except Exception as e:
        print(f"  [报错] 分类失败 '{major_name}': {e}")
        return "Other/Interdisciplinary"


# ==========================================
# 🚀 主运行程序
# ==========================================
if __name__ == "__main__":

    print(f"1. 正在检查并准备本地大模型 {MODEL_NAME}...")
    try:
        ollama.pull(MODEL_NAME)
        print("   模型准备就绪！\n")
    except Exception as e:
        print(f"   [警告] 模型拉取失败，请确保你的电脑右下角有 Ollama 小羊驼图标在运行！错误：{e}\n")

    print(f"2. 正在读取表格: {INPUT_CSV}")
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"   成功读取数据，共 {len(df)} 行。\n")
    except FileNotFoundError:
        print(f"   [错误] 找不到文件 {INPUT_CSV}，请确认你第一步生成的文件是不是这个名字！")
        exit()

    major_columns = ["UCB major?", "UCSD major?", "UCI major?"]
    print("3. 正在提取需要清洗的唯一专业名称...")

    all_majors = pd.concat([df[col] for col in major_columns if col in df.columns]).dropna().unique()
    print(f"   发现 {len(all_majors)} 个不重复的专业名称。准备让 AI 按照 UC 官方大类重新批阅！\n")

    print("4. 开始 AI 全自动官方分类...")
    ai_major_mapping = {}
    for i, major in enumerate(all_majors):
        print(f"   [{i + 1}/{len(all_majors)}] {major} ", end="", flush=True)
        category = classify_major_with_llm(major)
        ai_major_mapping[major] = category
        print(f"-> {category}")

    print("\n5. 正在把 AI 分类结果填回表格...")
    for col in major_columns:
        if col in df.columns:
            df[col + ' (AI Categorized)'] = df[col].map(ai_major_mapping)

    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"🎉 搞定！带有【UC 官方分类】的新表格已保存至: {OUTPUT_CSV}")
