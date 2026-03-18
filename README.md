# PERS作者国籍分析 (2019-2026)

[![识别率](https://img.shields.io/badge/识别率-68.4%25-success)](https://github.com)
[![论文数](https://img.shields.io/badge/论文数-383-blue)](https://github.com)
[![作者数](https://img.shields.io/badge/作者数-1%2C757-orange)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Photogrammetric Engineering & Remote Sensing (ASPRS期刊) 作者国籍深度分析与可视化**

[📊 在线查看可视化](https://你的GitHub用户名.github.io/PERS-Analysis/) | [📥 下载数据](https://github.com/你的GitHub用户名/PERS-Analysis/releases) | [📖 使用指南](CSV_FILES_GUIDE.md)

---

## 🌟 项目亮点

- 📊 **完整数据集**: 383篇论文，1,757位作者，1,423位唯一作者
- 🌍 **68.4%识别率**: 基于高级启发式算法 + 手动增强
- 📈 **8年趋势分析**: 2019-2026年完整时间序列
- 🗺️ **交互式可视化**: ECharts地图、趋势图、统计图表
- 💾 **10个CSV数据表**: 完整原始数据，可直接用于Excel/Python/R分析

---

## 📊 核心发现

### 国籍分布（已识别作者）

| 排名 | 国家 | 作者数 | 占比（已识别） |
|------|------|--------|----------------|
| 🥇 | 🇨🇳 China | 866 | **88.9%** |
| 🥈 | 🇺🇸 USA | 16 | 1.6% |
| 🥉 | 🇹🇷 Turkey | 15 | 1.5% |
| 4 | 🕌 Arab | 14 | 1.4% |
| 5 | 🇩🇪 Germany | 13 | 1.3% |
| ... | 其他 | 50 | 5.1% |

### 年度趋势

```
2019: China 52.9% ━━━━━━━━━━━━━━━━━━━━━━━━
2020: China 64.2% ▲ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2021: China 68.7% ▲ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2022: China 65.7% ▼ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2023: China 51.6% ▼ ━━━━━━━━━━━━━━━━━━━━━━━
2024: China 65.3% ▲ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2025: China 68.6% ▲ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2026: China 67.2% ▼ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Top 10 高产作者

| 排名 | 作者 | 论文数 | 国籍 |
|------|------|--------|------|
| 1 | Shao, Zhenfeng | 12 | 🇨🇳 China |
| 2 | Huang, Xiao | 9 | 🇨🇳 China |
| 3 | Qin, Rongjun | 8 | 🇨🇳 China |
| 4 | Cheng, Qimin | 8 | 🇨🇳 China |
| 5 | Zhu, Qing | 7 | 🇨🇳 China |
| 6 | Ge, Xuming | 7 | 🇨🇳 China |
| 7 | Wu, Bo | 6 | 🇨🇳 China |
| 8 | Ahmad, Muhammad Nasar | 6 | 🕌 Arab |
| 9-10 | 多位作者 | 5 | 🇨🇳 China |

---

## 🚀 快速开始

### 在线查看可视化

1. **直接打开HTML**（推荐）
   ```bash
   # 克隆仓库
   git clone https://github.com/你的GitHub用户名/PERS-Analysis.git
   cd PERS-Analysis
   
   # 用浏览器打开 index.html
   open index.html  # macOS
   start index.html # Windows
   xdg-open index.html # Linux
   ```

2. **在线访问**
   - GitHub Pages: [https://你的GitHub用户名.github.io/PERS-Analysis/](https://你的GitHub用户名.github.io/PERS-Analysis/)

### 使用CSV数据

#### Excel/WPS
```
1. 下载 PERS_Master_Data_2019_2026.csv
2. 双击打开（UTF-8编码，无乱码）
3. 使用数据透视表分析
```

#### Python
```python
import pandas as pd

# 读取主数据表
df = pd.read_csv('PERS_Master_Data_2019_2026.csv', encoding='utf-8-sig')

# 按国籍统计
country_stats = df.groupby('Author_Nationality').agg({
    'Author_Name': 'nunique',
    'Paper_Title': 'count'
})
print(country_stats)

# 筛选中国作者
china_authors = df[df['Author_Nationality'] == 'China']
print(f"中国作者论文数: {len(china_authors)}")
```

#### R
```r
library(tidyverse)

# 读取数据
df <- read_csv('PERS_Master_Data_2019_2026.csv')

# 按年份和国籍统计
yearly_stats <- df %>%
  group_by(Year, Author_Nationality) %>%
  summarise(count = n())

# 可视化
ggplot(yearly_stats, aes(x = Year, y = count, fill = Author_Nationality)) +
  geom_bar(stat = 'identity', position = 'stack')
```

---

## 📁 文件结构

```
PERS-Analysis/
├── index.html                              # 🌐 交互式可视化页面
├── visualization_data.json                  # 📊 可视化数据
├── README.md                                # 📖 项目说明
├── CSV_FILES_GUIDE.md                       # 📋 CSV使用指南
├── EXECUTIVE_SUMMARY.md                     # 📄 执行摘要
│
├── 🗂️ CSV数据表 (10个)
│   ├── PERS_Master_Data_2019_2026.csv      # 主数据表 (1,757条)
│   ├── PERS_Yearly_Country_Analysis.csv    # 年度国家分析
│   ├── PERS_Analysis_Summary.csv           # 汇总统计
│   ├── authors_detailed.csv                # 作者详情
│   ├── nationality_summary.csv             # 国籍汇总
│   ├── yearly_trends.csv                   # 年度趋势
│   ├── yearly_nationality_breakdown.csv    # 年度国籍矩阵
│   ├── top_authors.csv                     # 高产作者Top 100
│   ├── papers_detailed.csv                 # 论文详情
│   └── top_authors_by_country.csv          # 各国高产作者
│
├── 🔧 分析脚本
│   ├── analyze_author_nationality.py       # 基础分析
│   ├── batch_nationality_rules.py          # 高级识别算法
│   └── manual_nationality_rules.py         # 手动增强规则
│
└── 📦 打包文件
    └── PERS_Analysis_Final_Package.tar.gz  # 完整数据包 (113KB)
```

---

## 🛠️ 技术栈

- **数据处理**: Python 3.6+
- **可视化**: ECharts 5.4.3
- **前端**: HTML5 + CSS3 + JavaScript (ES6)
- **数据格式**: CSV (UTF-8-sig), JSON
- **分析方法**: 
  - 高级启发式算法（姓名特征 + 文化背景）
  - 手动增强识别（高产作者）
  - 统计分析（时间序列、分布分析）

---

## 📊 数据说明

### 数据来源
- **期刊**: Photogrammetric Engineering & Remote Sensing (ASPRS)
- **时间范围**: 2019年 - 2026年3月
- **论文数量**: 383篇
- **来源URL**: https://www.ingentaconnect.com/content/asprs/pers

### 识别方法
本分析采用多层次启发式算法：

1. **字符检测** (Unicode中文、特殊字符)
2. **姓氏数据库匹配** (20+国家，500+姓氏)
3. **名字模式识别** (拼音、罗马字、阿拉伯结构)
4. **评分系统** (完全匹配2.0分，模式匹配1.0分)
5. **手动增强** (高产作者专家识别)

### 准确性评估

| 置信度 | 国家 | 准确率估计 |
|--------|------|------------|
| **高** | China, Korea, Japan, Turkey | ~90% |
| **中** | India, USA, Germany | ~75% |
| **低** | 欧洲国家 | ~60% |

---

## 📈 可视化功能

### 交互式HTML页面特性

✅ **地图可视化** - 全球作者分布地图（ECharts Geo）  
✅ **年份筛选** - 点击年份查看该年论文和作者  
✅ **趋势分析** - 中国作者占比时间序列  
✅ **国家排名** - Top 15国家作者数排名  
✅ **论文详情** - 完整论文列表，作者国籍标注  
✅ **响应式设计** - 支持桌面和移动设备  

### 使用示例

1. **查看全局分布**
   - 打开 `index.html`
   - 地图上查看各国作者分布
   - 圆圈大小代表作者数量

2. **按年份筛选**
   - 点击年份按钮（如"2025年"）
   - 自动更新论文列表
   - 显示该年度统计

3. **查看作者详情**
   - 论文卡片显示所有作者
   - 鼠标悬停查看国籍
   - 点击论文标题访问原文

---

## 🔍 使用场景

### 学术研究
- 📚 文献综述与研究趋势分析
- 🤝 寻找国际合作伙伴
- 🏆 识别领域核心作者

### 机构管理
- 📊 评估研究国际化程度
- 🎯 制定学术发展策略
- 🌏 分析全球研究格局

### 个人学习
- 📖 了解遥感领域研究现状
- 🔗 追踪高产作者发表规律
- 💡 发现研究热点和方向

---

## ⚠️ 限制与注意事项

### 数据局限
- ⚠️ 2026年数据仅包含前3个月（不完整）
- ⚠️ 31.6%作者未识别（主要是欧美作者）
- ⚠️ 基于姓名判断，非官方国籍数据

### 算法局限
- 华裔/移民背景作者可能误判
- 跨文化姓名难以准确识别
- 国际合作作者归属可能不准确

### 建议
- 将本数据作为**参考**，而非绝对标准
- 结合其他数据源进行交叉验证
- 对关键结论进行人工审核

---

## 🤝 贡献指南

欢迎贡献！以下是几种贡献方式：

### 1. 数据改进
- 🔍 纠正错误的国籍识别
- 📝 补充未识别作者的国籍
- 🆕 添加新的识别规则

### 2. 功能增强
- 🌐 改进可视化效果
- 📊 添加新的分析维度
- 🎨 优化用户界面

### 3. 文档完善
- 📖 补充使用案例
- 🌍 添加多语言支持
- 📋 改进代码注释

### 提交方式
```bash
# Fork本仓库
# 创建特性分支
git checkout -b feature/your-feature

# 提交更改
git commit -am "添加新功能"

# 推送到分支
git push origin feature/your-feature

# 创建Pull Request
```

---

## 📝 更新日志

### v1.0.0 (2026-03-19)
- ✨ 初始版本发布
- 📊 完成383篇论文分析
- 🌍 识别率达68.4%
- 🗺️ 交互式可视化页面
- 💾 10个CSV数据表

### 计划功能 (v1.1.0)
- [ ] 机构分析（提取作者单位）
- [ ] 合作网络图（作者/机构关系）
- [ ] 主题分析（结合关键词）
- [ ] 引用分析（作者影响力）

---

## 📞 联系方式

**项目维护**: 虾总  
**分析时间**: 2026-03-19  
**问题反馈**: [GitHub Issues](https://github.com/你的GitHub用户名/PERS-Analysis/issues)  
**讨论交流**: [GitHub Discussions](https://github.com/你的GitHub用户名/PERS-Analysis/discussions)

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)

```
Copyright (c) 2026 虾总

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 致谢

- **ASPRS** - 提供高质量的遥感学术论文
- **ECharts** - 强大的数据可视化库
- **OpenClaw** - 项目开发平台
- **所有贡献者** - 感谢你们的支持和建议

---

## 📚 相关资源

- [ASPRS官网](https://www.asprs.org/)
- [PERS期刊](https://www.ingentaconnect.com/content/asprs/pers)
- [ECharts官方文档](https://echarts.apache.org/)
- [数据科学最佳实践](https://github.com)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star！**

Made with ❤️ by 虾总 | Powered by 🦞 OpenClaw

</div>
