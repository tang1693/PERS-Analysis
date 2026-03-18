# 🚀 快速开始指南

## 1️⃣ 本地测试HTML可视化

### 方法1: 直接打开（推荐）
```bash
# 下载这两个文件到同一文件夹:
# - index.html
# - visualization_data.json

# 然后双击 index.html 即可
```

### 方法2: 使用HTTP服务器（更稳定）
```bash
# Python 3
python3 -m http.server 8000

# 然后访问: http://localhost:8000/index.html
```

### 方法3: 使用Node.js
```bash
npx http-server -p 8000

# 访问: http://localhost:8000/index.html
```

---

## 2️⃣ 分析CSV数据

### Excel/WPS
1. 打开 `PERS_Master_Data_2019_2026.csv`
2. 使用筛选功能选择年份/国籍
3. 创建数据透视表统计

### Python快速分析
```python
import pandas as pd

# 读取数据
df = pd.read_csv('PERS_Master_Data_2019_2026.csv', encoding='utf-8-sig')

# 按年份统计中国作者
china_by_year = df[df['Author_Nationality'] == 'China'].groupby('Year').size()
print(china_by_year)

# 高产作者Top 20
top_authors = df.groupby('Author_Name').size().sort_values(ascending=False).head(20)
print(top_authors)
```

---

## 3️⃣ 推送到GitHub

```bash
# 1. 创建GitHub仓库 (网页操作)
https://github.com/new

# 2. 推送代码
cd /root/.openclaw/workspace/PERS分析
git remote add origin https://github.com/YOUR_USERNAME/PERS-Analysis.git
git branch -M main
git push -u origin main

# 3. 启用GitHub Pages
# Settings → Pages → Source: main branch → Save

# 4. 访问
https://YOUR_USERNAME.github.io/PERS-Analysis/
```

---

## 📋 检查清单

- [ ] 本地HTML可以正常打开
- [ ] 图表显示正常
- [ ] 年份筛选功能工作
- [ ] 论文列表显示完整
- [ ] CSV数据可以用Excel打开
- [ ] GitHub仓库已创建
- [ ] 代码已推送
- [ ] GitHub Pages已启用

---

## ⚠️ 常见问题

**Q: HTML打开后一片空白**
A: 确保 `visualization_data.json` 在同一目录

**Q: 图表不显示**
A: 使用HTTP服务器打开，不要直接用file://协议

**Q: CSV有乱码**
A: 用UTF-8编码打开，或用记事本另存为UTF-8

**Q: 推送失败**
A: 使用Personal Access Token代替密码

---

**有问题随时问我！** 🦞
