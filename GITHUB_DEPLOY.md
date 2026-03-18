# GitHub 部署指南

## 📦 准备推送到GitHub

### 1️⃣ 创建GitHub仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建新仓库:
   - **仓库名**: `PERS-Analysis` (推荐)
   - **描述**: `PERS作者国籍分析与可视化 (2019-2026)`
   - **可见性**: Public (推荐) 或 Private
   - **不要**初始化README、.gitignore或LICENSE（已有）

### 2️⃣ 推送本地代码

```bash
cd /root/.openclaw/workspace/PERS分析

# 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的GitHub用户名/PERS-Analysis.git

# 推送到GitHub
git push -u origin master

# 或使用main分支
git branch -M main
git push -u origin main
```

### 3️⃣ 启用GitHub Pages（在线访问）

1. 进入仓库 Settings
2. 左侧菜单选择 **Pages**
3. **Source** 选择 `Deploy from a branch`
4. **Branch** 选择 `master` (或 `main`)，目录选择 `/ (root)`
5. 点击 **Save**
6. 等待几分钟，访问：`https://你的GitHub用户名.github.io/PERS-Analysis/`

---

## 🔐 使用SSH推送（推荐）

如果你配置了SSH密钥：

```bash
git remote add origin git@github.com:你的GitHub用户名/PERS-Analysis.git
git push -u origin master
```

---

## 🌐 本地测试HTML

推送前测试可视化：

```bash
# macOS
open index.html

# Windows
start index.html

# Linux
xdg-open index.html

# 或使用Python启动本地服务器
python3 -m http.server 8000
# 然后访问 http://localhost:8000/index.html
```

---

## 📝 更新README中的链接

推送后，替换 `README.md` 中的占位符：

```bash
# 全局替换
sed -i 's/你的GitHub用户名/YOUR_USERNAME/g' README.md

# 然后提交
git add README.md
git commit -m "更新README链接"
git push
```

---

## 🔄 后续更新

```bash
# 修改文件后
git add .
git commit -m "更新描述"
git push
```

---

## ⚠️ 常见问题

### Q: 推送失败 (403 Forbidden)
**A**: 使用Personal Access Token替代密码
1. GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. 选择 `repo` 权限
4. 复制token
5. 推送时使用token作为密码

### Q: GitHub Pages显示404
**A**: 
- 确保`index.html`在仓库根目录
- 等待5-10分钟构建完成
- 检查Settings → Pages是否启用

### Q: HTML打开后没有数据
**A**: 
- 确保`visualization_data.json`在同目录
- 使用HTTP服务器打开（非file://协议）
- 检查浏览器控制台错误

---

## 📊 项目结构

```
PERS-Analysis/
├── index.html              ← GitHub Pages入口
├── visualization_data.json ← 数据文件
├── README.md              ← 项目说明
├── LICENSE                ← MIT许可证
├── CSV_FILES_GUIDE.md     ← CSV使用指南
├── *.csv                  ← 10个数据表
└── *.py                   ← 分析脚本
```

---

## 🎯 发布检查清单

- [ ] Git仓库初始化
- [ ] 所有文件已提交
- [ ] 远程仓库已添加
- [ ] 代码已推送
- [ ] GitHub Pages已启用
- [ ] README链接已更新
- [ ] 在线页面可访问
- [ ] CSV数据可下载

---

**完成后通知我，我帮你验证部署！** 🦞
