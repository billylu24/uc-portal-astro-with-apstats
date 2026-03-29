UC Portal Astrology: 概率统计与录取预测模型 (UC Portal Astro with AP Stats)


⚠️ 免责声明 / Disclaimer
中文：
本项目仅供娱乐和统计学爱好者交流使用。这不是一项严谨的科学研究，而是作者出于兴趣、为了“好玩”而发起的个人小项目。项目中的“门户玄学”数据均来自申请者的自愿匿名填报，不代表加州大学（UC）官方的招生立场或审核流程。录取预测结果仅基于正态分布模型模拟，具有局限性，请勿将其作为最终录取结果的参考依据。

English:
This project is for entertainment and statistical interest only. It is NOT a formal scientific study but a small personal "just-for-fun" project. The "Portal Astrology" data is sourced from voluntary anonymous submissions and does not represent the official admission policies or procedures of the University of California (UC). Prediction results are based on normal distribution simulations and are subject to limitations; they should not be relied upon as a definitive indicator of admission outcomes.

🚀 项目背景 / Project Background
中文：
每当 UC 录取季临近，申请者群体中总会流传关于门户状态（如 ID 变化、Banner 消失、特定链接登录权限等）的“玄学”预兆。本项目通过收集真实的申请者样本数据，利用贝叶斯定理和倾向评分匹配 (PSM) 等统计手段，试图观察这些玄学现象背后的数据分布，并量化这些“好兆头”与实际学术水平之间的相关性。

English:
As the UC admission season approaches, rumors about "portal astrology" (e.g., ID changes, disappearing banners, specific login permissions) often circulate among applicants. This project collects real applicant sample data and uses statistical methods like Bayesian Theorem and Propensity Score Matching (PSM) to observe the data distribution behind these "omens" and quantify the correlation between these "good signs" and actual academic profiles.

📈 初步发现与示例结果 / Preliminary Findings
(注：以下为基于部分测试样本的示例运行结果，具体数据请以最新样本跑出的结果为准 / Note: The following are sample results based on initial datasets. Please refer to the latest output for actual figures.)

中文：
通过运行 statsanalysis.py 和 expectation.py，我们得出了一些有趣的结论：

UC Berkeley (ID vs Email): 数据显示，门户显示“ID”的群体（Good Omen）在加权 GPA（GPA_W）上的均值略高于显示“Email”的群体。通过 PSM（倾向评分匹配）控制了 PIQ 和课外活动评分后，这种学术差距依然存在。贝叶斯后验概率（Bayes Prob）显示，“ID派”的学术底子强于“Email派”的概率高达 80%+。

UC San Diego (Banner 消失理论): 传言中 #3 Prestige Banner 消失（回答 "No"）是录取的好兆头。模型测算表明，Banner 消失群体的预期录取数（Expected Admits）与实际玄学人数高度重合，且 P-Value 小于 0.05，存在统计学上的显著性差异。

UC Irvine (提前登录链接): 能够成功登入 UCI 特定链接的样本，其学术水平（UW & W GPA）显著分布在官方历年录取的 Q3（前25%）区间内。

English:
By running statsanalysis.py and expectation.py, we found some interesting patterns:

UC Berkeley (ID vs Email): The data shows that the group with "ID" on their portal (Good Omen) has a slightly higher mean Weighted GPA than the "Email" group. After controlling for PIQ and EC ratings using PSM, this academic gap persists. Bayesian posterior probability suggests an 80%+ chance that the "ID" group has a stronger academic profile.

UC San Diego (The Disappearing Banner): Rumor has it that the disappearance of the #3 Prestige Banner (answering "No") is a strong sign of admission. Our model indicates that the "Expected Admits" for this group align closely with the actual astrology count, yielding a P-Value < 0.05, showing statistical significance.

UC Irvine (Early Login Link): Applicants who could successfully log in to the specific UCI link consistently had GPAs distributed within the Q3 (top 25%) range of the official historical admission data.

📂 文件结构 / File Structure
clean.py:

CN: 原始数据清洗引擎，负责处理非结构化文本并标准化 GPA 分数。

EN: Data cleaning engine that processes unstructured text and standardizes GPA scores.

statsanalysis.py:

CN: 核心统计分析工具。包含 T-Test、贝叶斯概率以及 PSM 算法，消除背景差异，评估玄学指标的置信度。

EN: Core statistical analysis tool. Includes T-Tests, Bayesian probabilities, and PSM algorithms to control variables and evaluate astrology indicators.

expectation.py:

CN: 基于官方录取区间拟合正态分布，利用贝叶斯公式 P(Admit|GPA) 计算每个样本的“预期录取概率”。

EN: Fits normal distributions based on official admission ranges to calculate the "expected admission probability" using Bayes' theorem.

majorclarify.py & populationanalysis.py:

CN: 专业类别归纳与样本总体多样性分析。

EN: Major categorization and population diversity analysis.

🛠️ 技术实现 / Technical Implementation
Data Processing: 使用 pandas 进行数据清洗，通过正则表达式提取并标准化 1-10 评分及 GPA（包含百分制到 4.0 分制的转换）。

Probability Modeling: 针对不同校区（UCB, UCSD, UCI）的官方基准数据（基于 Berk.csv 等），利用 scipy.stats 拟合正态分布曲线。

Astrology Validation:

UC Berkeley: 验证 ID 是否比 Email 更具预兆性。

UC San Diego: 验证 #3 Prestige Banner 消失 ("No") 是否为录取信号。

UC Irvine: 验证特定链接的提前登录权限 ("Yes")。

📊 核心指标定义 / Key Metrics
Expected Admits (预期录取数): 基于学术成绩与历史录取分布计算出的理应录取人数。

Actual Astrology (玄学实测数): 实际出现“好兆头”的人数。

Cohen's d: 测量两组样本之间差异大小的效应量（Effect Size）。

Ratio: 玄学实测数与预期录取数的比值。如果实测数远高于预期数，则暗示该玄学预兆具有较强的偏差或特定的相关性。

⚖️ 许可说明 / License
中文：
本项目代码开源，仅供学习交流。严禁用于任何商业用途或误导性宣传。

English:
The code is open-source for educational and exchange purposes only. Commercial use or misleading promotion is strictly prohibited.
