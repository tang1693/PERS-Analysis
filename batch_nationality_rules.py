#!/usr/bin/env python3
"""
增强的国籍判断规则
基于更全面的启发式规则和模式匹配
"""
import re
import json
from collections import Counter, defaultdict

# 扩展的姓氏数据库
SURNAME_DATABASE = {
    'China': [
        # 常见拼音姓氏
        'Wang', 'Zhang', 'Li', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou',
        'Xu', 'Sun', 'Ma', 'Zhu', 'Hu', 'Guo', 'He', 'Lin', 'Gao', 'Luo',
        'Zheng', 'Liang', 'Song', 'Tang', 'Han', 'Deng', 'Feng', 'Cao', 'Peng', 'Zeng',
        'Xiao', 'Tian', 'Dong', 'Pan', 'Yuan', 'Cai', 'Jiang', 'Yu', 'Du', 'Ye',
        'Cheng', 'Wei', 'Ren', 'Lu', 'Yao', 'Shao', 'Wan', 'Qian', 'Dai', 'Qin',
        'Gu', 'Shi', 'Yin', 'Yan', 'Fan', 'Xie', 'Zou', 'Xia', 'Fu', 'Wen',
        'Duan', 'Bai', 'Long', 'Kang', 'Meng', 'Qiu', 'Fang', 'Mo', 'Xiong', 'Shao'
    ],
    'Japan': [
        'Yamamoto', 'Tanaka', 'Suzuki', 'Watanabe', 'Takahashi', 'Sato', 'Ito', 'Nakamura',
        'Kobayashi', 'Kato', 'Yoshida', 'Yamada', 'Sasaki', 'Yamaguchi', 'Matsumoto', 'Inoue',
        'Kimura', 'Hayashi', 'Shimizu', 'Yamazaki', 'Mori', 'Abe', 'Ikeda', 'Hashimoto',
        'Yamashita', 'Ishikawa', 'Nakajima', 'Maeda', 'Fujita', 'Ogawa', 'Goto', 'Okada',
        'Hasegawa', 'Murakami', 'Kondo', 'Ishii', 'Saito', 'Sakamoto', 'Endo', 'Aoki'
    ],
    'Korea': [
        'Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang',
        'Lim', 'Han', 'Oh', 'Seo', 'Shin', 'Kwon', 'Hwang', 'Ahn', 'Song', 'Hong'
    ],
    'India': [
        'Kumar', 'Singh', 'Sharma', 'Patel', 'Gupta', 'Reddy', 'Verma', 'Jain',
        'Agarwal', 'Rao', 'Iyer', 'Nair', 'Pillai', 'Desai', 'Kapoor', 'Chopra',
        'Mehta', 'Shah', 'Thakur', 'Mishra', 'Pandey', 'Sinha', 'Joshi', 'Bhat'
    ],
    'USA': [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Wilson',
        'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin',
        'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Walker'
    ],
    'UK': [
        'Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies',
        'Robinson', 'Wright', 'Thompson', 'Evans', 'Walker', 'White', 'Roberts', 'Green'
    ],
    'Germany': [
        'Mueller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker',
        'Schulz', 'Hoffmann', 'Koch', 'Richter', 'Klein', 'Wolf', 'Schroeder', 'Neumann',
        'Schwarz', 'Zimmermann', 'Braun', 'Krueger', 'Hartmann', 'Lange', 'Schmitt', 'Werner'
    ],
    'France': [
        'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand',
        'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David',
        'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel', 'Girard', 'Andre', 'Lefevre'
    ],
    'Italy': [
        'Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci',
        'Marino', 'Greco', 'Bruno', 'Gallo', 'Conti', 'De Luca', 'Mancini', 'Costa'
    ],
    'Spain': [
        'Garcia', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Sanchez',
        'Ramirez', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz', 'Cruz', 'Morales'
    ],
    'Brazil': [
        'Silva', 'Santos', 'Oliveira', 'Souza', 'Pereira', 'Lima', 'Costa', 'Rodrigues',
        'Almeida', 'Nascimento', 'Araujo', 'Ribeiro', 'Carvalho', 'Martins', 'Ferreira'
    ],
    'Turkey': [
        'Yilmaz', 'Kaya', 'Demir', 'Celik', 'Sahin', 'Yildiz', 'Yildirim', 'Ozturk',
        'Aydin', 'Ozdemir', 'Arslan', 'Dogan', 'Kilic', 'Aslan', 'Cetin', 'Kara'
    ],
    'Netherlands': [
        'De Jong', 'Jansen', 'De Vries', 'Van den Berg', 'Van Dijk', 'Bakker', 'Janssen',
        'Visser', 'Smit', 'Meijer', 'De Boer', 'Mulder', 'De Groot', 'Bos', 'Vos'
    ],
    'Canada': [
        'Tremblay', 'Gagnon', 'Roy', 'Cote', 'Bouchard', 'Gauthier', 'Morin', 'Lavoie',
        'Fortin', 'Gagne', 'Ouellet', 'Pelletier', 'Belanger', 'Levesque', 'Bergeron'
    ],
    'Australia': [
        'Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White',
        'Martin', 'Anderson', 'Thompson', 'Nguyen', 'Thomas', 'Walker', 'Harris'
    ],
    'Poland': [
        'Nowak', 'Kowalski', 'Wisniewski', 'Wojcik', 'Kowalczyk', 'Kaminski', 'Lewandowski',
        'Zielinski', 'Szymanski', 'Wozniak', 'Dabrowski', 'Kozlowski', 'Jankowski'
    ],
    'Russia': [
        'Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Sokolov', 'Lebedev', 'Kozlov', 'Novikov',
        'Morozov', 'Petrov', 'Volkov', 'Solovyov', 'Vasiliev', 'Zaitsev', 'Pavlov'
    ]
}

# 名字模式（中间名或名字特征）
NAME_PATTERNS = {
    'China': [
        # 常见的拼音名字模式
        r'\b(Xiao|Jing|Ming|Wei|Yong|Ying|Hong|Qiang|Yan|Jun|Peng|Tao)\b',
        r'\b(Xiaoming|Xiaoyu|Xiaojun|Jianhua|Guoqiang|Hongwei)\b'
    ],
    'Japan': [
        r'\b(Hiroshi|Takeshi|Masahiro|Yuki|Kenji|Shinji|Akira)\b',
        r'\b(ko|mi|ka)\b$'  # 常见日文名字结尾
    ],
    'India': [
        r'\b(Raj|Vijay|Anil|Suresh|Ramesh|Prakash|Sanjay)\b',
        r'\b(deep|jeet|pal|kumar)\b$'
    ],
    'Arab': [
        r'\b(Mohammed|Muhammad|Ahmad|Ali|Hassan|Hussein|Omar)\b',
        r'\b(Abdul|Abd|bin|ibn)\b'
    ]
}

# 特殊规则
SPECIAL_RULES = {
    # 逗号前后顺序颠倒的中文名
    'reversed_chinese': r'^[A-Z][a-z]+, [A-Z][a-z]+$',
    # 中文名字特征（多音节拼音）
    'chinese_pinyin': r'\b(zhao|qian|sun|li|zhou|wu|zheng|wang|feng|chen|chu|wei|jiang|shen|han|yang|zhu|qin|you|xu|he|lv|shi|zhang|kong|cao|yan|hua|jin|wei|tao|jiang|qi|xie|zou|yu|bai|shao|meng|qiu|fang)\b',
}

def advanced_nationality_guess(full_name):
    """
    高级国籍判断算法
    """
    if not full_name:
        return 'Unknown'
    
    # 移除多余空格
    name = full_name.strip()
    
    # 1. 检查中文字符
    if re.search(r'[\u4e00-\u9fff]', name):
        return 'China'
    
    # 2. 分离姓和名
    parts = name.split(',')
    if len(parts) == 2:
        lastname = parts[0].strip()
        firstname = parts[1].strip()
    else:
        # 如果没有逗号，假设最后一个词是姓
        words = name.split()
        if len(words) >= 2:
            lastname = words[-1]
            firstname = ' '.join(words[:-1])
        else:
            lastname = name
            firstname = ''
    
    # 3. 匹配姓氏数据库
    scores = defaultdict(float)
    
    for country, surnames in SURNAME_DATABASE.items():
        for surname in surnames:
            if lastname.lower() == surname.lower():
                scores[country] += 2.0  # 完全匹配权重高
            elif lastname.lower().startswith(surname.lower()[:3]):
                scores[country] += 0.5  # 部分匹配权重低
    
    # 4. 匹配名字模式
    for country, patterns in NAME_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, firstname, re.IGNORECASE):
                scores[country] += 1.0
            if re.search(pattern, name, re.IGNORECASE):
                scores[country] += 0.5
    
    # 5. 中文拼音特征检测
    if re.search(SPECIAL_RULES['chinese_pinyin'], name.lower()):
        scores['China'] += 1.5
    
    # 6. 检测特殊字符和重音符号
    if re.search(r'[àáâãäåèéêëìíîïòóôõöùúûüýÿ]', name.lower()):
        scores['France'] += 0.5
        scores['Spain'] += 0.5
        scores['Portugal'] += 0.5
    
    if re.search(r'[äöüß]', name.lower()):
        scores['Germany'] += 1.0
    
    if re.search(r'[çğıöşü]', name.lower()):
        scores['Turkey'] += 1.0
    
    # 7. 阿拉伯名字特征
    if 'Abdul' in name or 'Mohammed' in name or 'Ahmad' in name:
        # 可能是中东国家
        scores['Saudi Arabia'] += 1.0
        scores['Egypt'] += 0.5
        scores['UAE'] += 0.5
        scores['Iraq'] += 0.5
    
    # 8. 特殊姓名结构
    if ' bin ' in name or ' ibn ' in name:
        scores['Malaysia'] += 1.0
        scores['Saudi Arabia'] += 1.0
    
    # 9. 返回得分最高的国家
    if scores:
        best_match = max(scores.items(), key=lambda x: x[1])
        if best_match[1] >= 1.0:  # 至少要有1分
            return best_match[0]
    
    return 'Unknown'

def batch_enhance_nationality():
    """批量增强国籍判断"""
    
    print("🚀 开始高级国籍分析...")
    
    # 加载原始分析
    with open('author_nationality_analysis.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # 重新判断所有作者
    print("\n📝 重新分析所有作者...")
    updated_count = 0
    
    for author in analysis['nationality_map'].keys():
        new_nationality = advanced_nationality_guess(author)
        if new_nationality != analysis['nationality_map'][author]:
            if analysis['nationality_map'][author] == 'Unknown' and new_nationality != 'Unknown':
                updated_count += 1
            analysis['nationality_map'][author] = new_nationality
    
    print(f"   更新了 {updated_count} 个作者的国籍信息")
    
    # 重新统计
    nationality_counts = Counter(analysis['nationality_map'].values())
    analysis['nationality_counts'] = dict(nationality_counts)
    
    # 重新计算论文贡献
    nationality_paper_counts = defaultdict(int)
    for author, count in analysis['author_counts'].items():
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        nationality_paper_counts[nationality] += count
    analysis['nationality_paper_counts'] = dict(nationality_paper_counts)
    
    # 保存增强结果
    with open('author_nationality_analysis_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 增强分析已完成")
    
    # 生成报告
    generate_report(analysis)
    
    return analysis

def generate_report(analysis):
    """生成详细报告"""
    
    report = []
    report.append("=" * 80)
    report.append("PERS 作者国籍分析报告 (高级增强版) - 2019-2026")
    report.append("=" * 80)
    
    # 加载论文数据
    with open('recent_papers_2019_2026.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # 基本统计
    report.append(f"\n📊 基本统计:")
    report.append(f"  论文总数: {len(papers)}")
    report.append(f"  作者总数: {analysis['total_authors']}")
    report.append(f"  唯一作者: {analysis['unique_authors']}")
    report.append(f"  平均每篇: {analysis['total_authors']/len(papers):.1f} 人")
    
    # 按年份统计
    year_stats = defaultdict(int)
    for paper in papers:
        year_stats[paper['year']] += 1
    
    report.append(f"\n📅 年份分布:")
    for year in sorted(year_stats.keys(), reverse=True):
        report.append(f"  {year}: {year_stats[year]:3d} 篇")
    
    # 国籍分布（唯一作者）
    nationality_counts = analysis['nationality_counts']
    sorted_nationalities = sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)
    
    total_known = sum(count for nat, count in sorted_nationalities if nat != 'Unknown')
    unknown_count = nationality_counts.get('Unknown', 0)
    
    report.append(f"\n🌍 国籍分布（唯一作者）:")
    report.append(f"  已识别: {total_known} ({total_known/analysis['unique_authors']*100:.1f}%)")
    report.append(f"  未识别: {unknown_count} ({unknown_count/analysis['unique_authors']*100:.1f}%)")
    report.append("")
    
    for nationality, count in sorted_nationalities[:30]:  # Top 30
        percentage = count / analysis['unique_authors'] * 100
        if nationality != 'Unknown' and total_known > 0:
            of_known = count / total_known * 100
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}% | {of_known:5.1f}% of known)")
        else:
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 论文贡献分布
    report.append(f"\n📈 国籍分布（按论文贡献次数）:")
    nationality_paper_counts = analysis['nationality_paper_counts']
    sorted_contributions = sorted(nationality_paper_counts.items(), key=lambda x: x[1], reverse=True)
    
    for nationality, count in sorted_contributions[:30]:
        percentage = count / analysis['total_authors'] * 100
        report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 高产作者
    report.append(f"\n🏆 高产作者 (Top 50):")
    author_counts = analysis['author_counts']
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (author, count) in enumerate(sorted_authors[:50], 1):
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        report.append(f"  {i:2d}. {author:40s} - {count:2d} 篇 [{nationality}]")
    
    # 按国籍的高产作者
    report.append(f"\n🌏 各国高产作者:")
    
    # 按国籍分组作者
    country_authors = defaultdict(list)
    for author, count in sorted_authors:
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        if nationality != 'Unknown':
            country_authors[nationality].append((author, count))
    
    # 显示每个主要国家的Top 5作者
    for country in ['China', 'USA', 'Japan', 'Germany', 'UK', 'India', 'Canada', 'France']:
        if country in country_authors and country_authors[country]:
            report.append(f"\n  {country}:")
            for i, (author, count) in enumerate(country_authors[country][:5], 1):
                report.append(f"    {i}. {author:40s} - {count} 篇")
    
    report.append("\n" + "=" * 80)
    report.append("✨ 使用高级启发式算法，基于姓名特征、文化背景和语言模式")
    report.append("=" * 80)
    
    report_text = "\n".join(report)
    
    # 打印报告
    print("\n" + report_text)
    
    # 保存报告
    with open('author_nationality_report_enhanced.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\n✅ 报告已保存: author_nationality_report_enhanced.txt")

if __name__ == '__main__':
    batch_enhance_nationality()
