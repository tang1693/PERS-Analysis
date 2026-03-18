# PERS分析 - CSV文件使用指南

**生成日期**: 2026-03-19  
**数据范围**: 2019-2026年  
**总论文数**: 383篇  
**总作者数**: 1,757人次（1,423位唯一作者）

---

## 📁 文件清单

### 1️⃣ authors_detailed.csv
**作者详细信息表** - 每位作者的完整记录

| 字段 | 说明 | 示例 |
|------|------|------|
| Author Name | 作者姓名 | Shao, Zhenfeng |
| Nationality | 判定国籍 | China |
| Paper Count | 论文数量 | 12 |

**用途**:
- 查找特定作者信息
- 按论文数排序查看高产作者
- 筛选特定国籍的作者

**统计**: 1,423位唯一作者，按论文数降序排列

---

### 2️⃣ nationality_summary.csv
**国籍汇总统计表** - 各国作者总体分布

| 字段 | 说明 | 示例 |
|------|------|------|
| Nationality | 国家/地区 | China |
| Unique Authors | 唯一作者数 | 859 |
| Percentage (Unique) | 占唯一作者比例 | 60.37% |
| Total Contributions | 总贡献次数 | 1,104 |
| Percentage (Total) | 占总贡献比例 | 62.83% |

**用途**:
- 快速了解各国作者分布
- 对比唯一作者数vs总贡献数
- 识别主要贡献国家

**统计**: 14个国家/地区，按唯一作者数降序排列

**关键发现**:
- 🇨🇳 China: 91.0% (已识别作者中)
- 🌐 Unknown: 33.7% (未识别)

---

### 3️⃣ yearly_trends.csv
**年度趋势表** - 按年份统计的核心指标

| 字段 | 说明 | 示例 |
|------|------|------|
| Year | 年份 | 2025 |
| Total Papers | 论文总数 | 45 |
| Total Authors | 作者总数 | 245 |
| China Authors | 中国作者数 | 168 |
| China Percentage | 中国占比 | 68.6% |
| Unknown Authors | 未识别作者数 | 70 |
| Unknown Percentage | 未识别占比 | 28.6% |
| Other Authors | 其他国家作者数 | 7 |

**用途**:
- 观察年度变化趋势
- 分析中国作者占比变化
- 评估数据完整性（Unknown占比）

**统计**: 8年数据（2019-2026）

**趋势亮点**:
- 2021年作者数最多（319人）
- 中国作者占比2021年达峰值（68.7%）
- 2023年出现异常低值（51.6%）

---

### 4️⃣ yearly_nationality_breakdown.csv
**年度国籍详细分布表** - 各年各国作者数矩阵

| 字段 | 说明 |
|------|------|
| Year | 年份 |
| China, Unknown, Arab, Turkey, Germany... | 各国作者数（Top 14国家） |

**用途**:
- 制作时间序列图表
- 对比各国发展趋势
- Excel数据透视表分析

**统计**: 8年 × 14国家的矩阵数据

**适用场景**:
- 可视化（折线图、堆叠柱状图）
- 国家间对比分析
- 识别新兴研究力量

---

### 5️⃣ top_authors.csv
**高产作者排名表** - Top 100作者详细排名

| 字段 | 说明 | 示例 |
|------|------|------|
| Rank | 排名 | 1 |
| Author Name | 作者姓名 | Shao, Zhenfeng |
| Nationality | 国籍 | China |
| Paper Count | 论文数 | 12 |

**用途**:
- 识别领域核心作者
- 学术合作分析
- 引用关系研究

**统计**: Top 100作者，按论文数排名

**Top 5**:
1. Shao, Zhenfeng (12篇) 🇨🇳
2. Huang, Xiao (9篇) 🇨🇳
3. Qin, Rongjun (8篇) 🇨🇳
4. Cheng, Qimin (8篇) 🇨🇳
5. Zhu, Qing (7篇) 🇨🇳

---

### 6️⃣ papers_detailed.csv
**论文详细信息表** - 每篇论文的作者构成

| 字段 | 说明 | 示例 |
|------|------|------|
| Year | 年份 | 2025 |
| Month | 月份（issue编号） | 3 |
| Title | 论文标题（截断至100字符） | Integration of Near-Proximal... |
| Total Authors | 总作者数 | 7 |
| China Authors | 中国作者数 | 2 |
| Unknown Authors | 未识别作者数 | 5 |
| Other Authors | 其他国家作者数 | 0 |
| Access Type | 访问类型 | Open Access content |

**用途**:
- 分析论文合作模式
- 识别国际合作论文
- 按访问类型筛选论文

**统计**: 383篇论文，按年份月份降序排列

**分析维度**:
- 合作强度（作者数分布）
- 国际化程度（Other Authors占比）
- 开放获取比例

---

### 7️⃣ top_authors_by_country.csv
**各国高产作者表** - 按国家分组的Top 5作者

| 字段 | 说明 | 示例 |
|------|------|------|
| Country | 国家 | China |
| Rank in Country | 国内排名 | 1 |
| Author Name | 作者姓名 | Shao, Zhenfeng |
| Paper Count | 论文数 | 12 |

**用途**:
- 按国家查找核心作者
- 跨国对比研究实力
- 学术交流目标识别

**统计**: 13个国家 × Top 5作者 = 54条记录

**覆盖国家**:
- China, Arab, Turkey, Germany, USA
- Korea, Japan, India, Saudi Arabia
- Netherlands, France, Spain, Canada

---

## 📊 数据使用建议

### Excel/WPS使用
```
1. 使用 UTF-8-sig 编码，Excel可直接打开
2. 推荐使用数据透视表分析
3. 条件格式化可视化关键指标
```

### Python分析
```python
import pandas as pd

# 读取CSV
df = pd.read_csv('authors_detailed.csv', encoding='utf-8-sig')

# 按国籍分组统计
country_stats = df.groupby('Nationality').agg({
    'Author Name': 'count',
    'Paper Count': 'sum'
})
```

### R分析
```r
library(tidyverse)

# 读取CSV
authors <- read_csv('authors_detailed.csv')

# 可视化
ggplot(authors, aes(x = Nationality, y = `Paper Count`)) +
  geom_bar(stat = 'identity')
```

---

## 🔍 常见分析场景

### 场景1: 寻找潜在合作者
**使用文件**: `top_authors_by_country.csv`
1. 筛选目标国家
2. 查看Top作者
3. 交叉参考 `authors_detailed.csv` 确认专业

### 场景2: 分析研究趋势
**使用文件**: `yearly_trends.csv` + `yearly_nationality_breakdown.csv`
1. 制作时间序列图
2. 识别增长最快的国家
3. 预测未来趋势

### 场景3: 评估国际化程度
**使用文件**: `papers_detailed.csv`
1. 计算 `Other Authors > 0` 的论文比例
2. 按年份分析国际合作变化
3. 识别典型国际合作案例

### 场景4: 作者影响力排名
**使用文件**: `top_authors.csv`
1. 直接查看排名
2. 可结合引用数据进一步分析
3. 追踪作者发表规律

---

## ⚠️ 数据使用注意事项

### 1. 国籍判断准确性
- **高置信度**: China, Korea, Japan, Turkey（姓名特征明显）
- **中置信度**: India, USA, Germany（姓氏重叠）
- **低置信度**: 欧洲国家（姓氏跨国普遍）
- **未识别**: 33.7%的作者（主要是欧美作者）

### 2. 数据完整性
- 2026年数据仅包含前3个月（61人）
- 建议等待全年数据后重新分析年度趋势
- 历史数据（2019-2025）较完整

### 3. 统计偏差
- 基于姓名判断，非实际国籍/机构隶属
- 华裔/移民背景作者可能误判
- 国际合作中作者归属可能不准确

### 4. 字符编码
- 所有CSV使用 **UTF-8-sig** 编码
- Excel可直接打开，避免乱码
- Python/R读取时注意指定编码

---

## 📈 推荐可视化

### 1. 国籍分布饼图
**数据源**: `nationality_summary.csv`
- 展示Top 5国家 + Others
- 突出中国的主导地位

### 2. 年度趋势折线图
**数据源**: `yearly_trends.csv`
- X轴：年份
- Y轴：中国作者占比 / 总作者数
- 双Y轴展示两个指标

### 3. 各国作者数热力图
**数据源**: `yearly_nationality_breakdown.csv`
- X轴：年份
- Y轴：国家
- 颜色深度：作者数

### 4. 高产作者Top 20柱状图
**数据源**: `top_authors.csv`
- 按论文数排序
- 颜色区分国籍

---

## 🔗 相关文件

- `EXECUTIVE_SUMMARY.md` - 分析执行摘要
- `author_nationality_report_enhanced.txt` - 完整文本报告
- `author_nationality_analysis_enhanced.json` - 原始JSON数据
- `batch_nationality_rules.py` - 数据处理脚本

---

## 📞 联系方式

**项目维护**: 虾总  
**分析日期**: 2026-03-19  
**数据更新**: 如需更新或定制分析，请联系维护者

---

**备注**: 本数据集仅用于学术研究和统计分析，基于公开发表的论文数据。
