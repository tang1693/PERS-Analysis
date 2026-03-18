#!/usr/bin/env python3
"""
PERS作者国籍分析工具
批量分析2019-2026年论文作者的国籍分布
"""
import json
import re
from collections import defaultdict, Counter
import time

def parse_authors(author_string):
    """解析作者字符串，返回作者列表"""
    if not author_string:
        return []
    
    # 按分号分隔
    authors = re.split(r';', author_string)
    
    # 清理每个作者名字
    parsed_authors = []
    for author in authors:
        author = author.strip()
        if author:
            parsed_authors.append(author)
    
    return parsed_authors

def guess_nationality_by_name(name):
    """
    根据名字特征初步判断国籍
    这是一个启发式方法，用于批量处理前的初步分类
    """
    # 检查是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', name):
        return 'China'
    
    # 检查常见的姓氏模式
    common_patterns = {
        'China': ['Wang', 'Zhang', 'Li', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou', 
                  'Xu', 'Sun', 'Ma', 'Zhu', 'Hu', 'Guo', 'He', 'Lin', 'Gao', 'Luo'],
        'Japan': ['Yamamoto', 'Tanaka', 'Suzuki', 'Watanabe', 'Takahashi', 'Sato', 'Ito', 'Nakamura'],
        'Korea': ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang'],
        'India': ['Kumar', 'Singh', 'Sharma', 'Patel', 'Gupta', 'Reddy', 'Verma', 'Jain'],
        'USA': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Wilson'],
        'Germany': ['Mueller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner'],
        'France': ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit'],
    }
    
    # 提取姓氏（通常是逗号前的部分）
    lastname = name.split(',')[0].strip() if ',' in name else name.split()[-1]
    
    for country, surnames in common_patterns.items():
        if lastname in surnames:
            return country
    
    # 检查名字的字母特征
    if re.search(r'[āáǎàēéěèīíǐìōóǒòūúǔù]', name.lower()):
        return 'China'  # 拼音特征
    
    return 'Unknown'

def analyze_authors_batch(papers):
    """批量分析作者"""
    
    all_authors = []
    paper_author_map = defaultdict(list)
    
    print("📝 提取所有作者...")
    for paper in papers:
        authors = parse_authors(paper['Authors'])
        paper_id = f"{paper['year']}-{paper.get('month', 0):02d}"
        
        for author in authors:
            all_authors.append(author)
            paper_author_map[paper_id].append(author)
    
    print(f"   总作者数: {len(all_authors)}")
    
    # 统计唯一作者
    unique_authors = list(set(all_authors))
    print(f"   唯一作者数: {len(unique_authors)}")
    
    # 批量判断国籍（使用启发式方法）
    print("\n🌍 分析作者国籍...")
    nationality_map = {}
    
    for i, author in enumerate(unique_authors):
        nationality = guess_nationality_by_name(author)
        nationality_map[author] = nationality
        
        if (i + 1) % 100 == 0:
            print(f"   已处理: {i+1}/{len(unique_authors)}")
    
    # 统计国籍分布
    nationality_counts = Counter(nationality_map.values())
    
    # 统计每个作者的出现次数
    author_counts = Counter(all_authors)
    
    # 按国籍统计论文贡献
    nationality_paper_counts = defaultdict(int)
    for author, count in author_counts.items():
        nationality = nationality_map.get(author, 'Unknown')
        nationality_paper_counts[nationality] += count
    
    return {
        'total_authors': len(all_authors),
        'unique_authors': len(unique_authors),
        'nationality_map': nationality_map,
        'nationality_counts': dict(nationality_counts),
        'nationality_paper_counts': dict(nationality_paper_counts),
        'author_counts': dict(author_counts),
        'paper_author_map': dict(paper_author_map)
    }

def generate_report(papers, analysis_results):
    """生成分析报告"""
    
    report = []
    report.append("=" * 80)
    report.append("PERS 作者国籍分析报告 (2019-2026)")
    report.append("=" * 80)
    
    # 基本统计
    report.append(f"\n📊 基本统计:")
    report.append(f"  论文总数: {len(papers)}")
    report.append(f"  作者总数: {analysis_results['total_authors']}")
    report.append(f"  唯一作者: {analysis_results['unique_authors']}")
    report.append(f"  平均每篇: {analysis_results['total_authors']/len(papers):.1f} 人")
    
    # 按年份统计
    year_stats = defaultdict(int)
    for paper in papers:
        year_stats[paper['year']] += 1
    
    report.append(f"\n📅 年份分布:")
    for year in sorted(year_stats.keys(), reverse=True):
        report.append(f"  {year}: {year_stats[year]:3d} 篇")
    
    # 国籍分布（按唯一作者）
    report.append(f"\n🌍 国籍分布（唯一作者）:")
    nationality_counts = analysis_results['nationality_counts']
    sorted_nationalities = sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)
    
    total_known = sum(count for nat, count in sorted_nationalities if nat != 'Unknown')
    
    for nationality, count in sorted_nationalities[:20]:  # Top 20
        percentage = count / analysis_results['unique_authors'] * 100
        if nationality != 'Unknown':
            of_known = count / total_known * 100 if total_known > 0 else 0
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}% | {of_known:5.1f}% of known)")
        else:
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 国籍分布（按总贡献）
    report.append(f"\n📈 国籍分布（按总论文贡献）:")
    nationality_paper_counts = analysis_results['nationality_paper_counts']
    sorted_paper_contributions = sorted(nationality_paper_counts.items(), key=lambda x: x[1], reverse=True)
    
    total_contributions = analysis_results['total_authors']
    for nationality, count in sorted_paper_contributions[:20]:
        percentage = count / total_contributions * 100
        report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 高产作者
    report.append(f"\n🏆 高产作者 (Top 20):")
    author_counts = analysis_results['author_counts']
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (author, count) in enumerate(sorted_authors[:20], 1):
        nationality = analysis_results['nationality_map'].get(author, 'Unknown')
        report.append(f"  {i:2d}. {author:40s} - {count:2d} 篇 [{nationality}]")
    
    report.append("\n" + "=" * 80)
    report.append("⚠️  注意：国籍判断基于姓名启发式规则，可能存在误差")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    print("🚀 开始分析...")
    
    # 加载数据
    with open('recent_papers_2019_2026.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # 批量分析
    analysis_results = analyze_authors_batch(papers)
    
    # 生成报告
    report = generate_report(papers, analysis_results)
    
    # 打印报告
    print("\n" + report)
    
    # 保存报告
    with open('author_nationality_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存详细数据
    with open('author_nationality_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已保存:")
    print(f"   - author_nationality_report.txt")
    print(f"   - author_nationality_analysis.json")

if __name__ == '__main__':
    main()
