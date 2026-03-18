# 📖 使用指南

## 🚀 方式1: 自包含版本（推荐）⭐

**最简单的方式！**

### 步骤
1. 下载 `index-standalone.html`（365KB）
2. 双击打开
3. 完成！✨

### 优点
- ✅ 无需额外文件
- ✅ 数据已内嵌
- ✅ 无跨域问题
- ✅ 离线可用

---

## 🌐 方式2: 分离版本（在线部署）

**适合GitHub Pages等在线环境**

### 步骤
1. 下载 `index.html` (26KB)
2. 下载 `visualization_data.json` (340KB)
3. 放在同一文件夹
4. 使用HTTP服务器打开

### HTTP服务器
```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx http-server -p 8000

# 访问
http://localhost:8000/index.html
```

### 优点
- ✅ 文件更小
- ✅ 数据可单独更新
- ✅ 适合在线部署

---

## ⚠️ 常见问题

### Q: 为什么双击index.html显示"数据加载失败"？

**A**: 因为浏览器的跨域安全限制（CORS）

**解决方案**:
1. 使用 `index-standalone.html`（推荐）
2. 或用HTTP服务器打开（见上面命令）

### Q: 两个版本有什么区别？

| 特性 | index.html | index-standalone.html |
|------|------------|------------------------|
| 文件大小 | 26KB | 365KB |
| 需要JSON | ✅ 需要 | ❌ 不需要 |
| 双击打开 | ❌ 不行 | ✅ 可以 |
| 在线部署 | ✅ 更好 | ✅ 也可以 |
| 离线使用 | ❌ 不行 | ✅ 可以 |
| 推荐场景 | GitHub Pages | 本地查看 |

### Q: GitHub Pages用哪个？

**A**: 两个都可以，推荐用分离版本（index.html）
- 文件小，加载快
- 数据可缓存
- 但自包含版本也完全能用

---

## 📊 功能列表

两个版本功能完全一致：

✅ 世界地图（ECharts）  
✅ 年份筛选（2019-2026）  
✅ 国家分布图（Top 15 + Unknown）  
✅ 年度趋势分析  
✅ 论文详细列表  
✅ 作者国籍标注  
✅ 响应式设计（支持手机）  

---

## 🎯 推荐使用场景

### 本地查看/演示
👉 下载 `index-standalone.html`，双击打开

### GitHub Pages部署
👉 使用 `index.html` + `visualization_data.json`

### 分享给别人
👉 发送 `index-standalone.html`（单文件）

### 数据经常更新
👉 使用分离版本，只需更新JSON

---

## 🔧 技术说明

### 自包含版本原理
```javascript
// 数据直接嵌入HTML
const embeddedData = {
  "papers": [...],
  "countries": {...},
  ...
};
```

### 分离版本原理
```javascript
// 从外部加载JSON
const response = await fetch('visualization_data.json');
const data = await response.json();
```

---

**有问题随时问我！** 🦞
