# 🌎 PERS 期刊数据可视分析平台

这是一个针对《Photogrammetric Engineering & Remote Sensing (PERS)》期刊作者发文数据的多维度可视分析控制台。

🔥 **最新更新** (2026-03)：
**全面引入 Elsevier Scopus 官方数据接口！** 实现了长达 **24 年（2003-2026）**、**3000多篇**文献的精确跨库匹配。通过论文匹配机构归属地，100% 攻克了“重名作者难以区分”及“无确切机构国籍无法溯源”的痛点！

👉 **[在线访问最新 Scopus 版控制台 (推荐)](https://tang1693.github.io/PERS-Analysis/)** 👈

---

## 🌟 核心能力

- **100% 精确去歧义**：通过调用 Scopus API 匹配单篇论文特征，即便出现相同的 `Wang B.`，系统也会根据论文抓取其当下任职的准确机构与归属国。
- **动态交互可视化**：所有图表全响应式交互，包含：
  - 🗺️ **全球作者分布图 (Global Map)**：直观展现发文热度
  - 🌍 **国家排名 (Top Countries)**：全球核心贡献国排序
  - 📊 **论文作者深度统计**：多少是一作/通讯等统计指标
  - 🔗 **中外合作态势演变**：年度纯国内与中外合作比例堆叠柱状图
  - ☁️ **标题高频词云**：热点研究主题轮换呈现
- **丝滑体验**：采用最稳定的 ECharts + 阿里高速 CDN，确保无缝秒开。

## 📁 核心文件结构

- `index.html`: **新版主控制台** (基于 Scopus 最新全量数据, 2003-2026)，双击直接运行！
- `index_v1_standalone.html`: **旧版归档** (基于 2019-2026 年姓名启发式推断的归档版本)，可在新版控制台中通过顶部按钮点击切换回顾。
- `ALL_articles_Scopus_Enriched.csv`: 基于原始输入补充了 Scopus 解析的姓名、机构、国家的丰富源数据表。
- `PERS_Authors_Scopus.csv`: **（强烈推荐！）**数据分析专用展平宽表，格式为一行代表一篇论文的一个作者，可以直接用 Tableau/Excel 透视表产出报表。
- `visualization_data_scopus.json` / `scopus_cache_all.json`: 中间爬取及可视化缓存数据。

## 🚀 极速部署

1. clone 或下载此仓库
2. 双击打开 `index.html` 即可直接在本地浏览器完美运行（不需要配置 Web Server 或安装 Python）。
3. 已托管于 GitHub Pages，每次 Push 主分支自动实时更新页面。

---

*由 OpenClaw AI 驱动 | 数据来源：ASPRS (PERS 期刊) & Elsevier Scopus API*
