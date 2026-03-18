#!/usr/bin/env python3
"""
手动增强高产作者的国籍识别
基于深度分析的专家规则
"""
import json
from collections import Counter, defaultdict

# 手动识别的高产作者（基于深入分析）
MANUAL_NATIONALITY_MAP = {
    # 中文拼音特征的作者
    'Ge, Xuming': 'China',
    'Di, Kaichang': 'China',
    'Tong, Xiaohua': 'China',
    'Sheng, Qinghong': 'China',
    'Niu, Chaoyang': 'China',
    'Zhong, Jiageng': 'China',
    'Su, Dong': 'China',
    
    # 南亚作者
    'Javed, Akib': 'Pakistan',
    'Thenkabail, Prasad S.': 'India',
    'Ullah, Inam': 'Pakistan',
    'Ara, Iffat': 'Pakistan',
    
    # 美国作者
    'Parrish, Christopher E.': 'USA',
    'McCormick, Richard': 'USA',
    'Foley, Daniel': 'USA',
    'Oliphant, Adam J.': 'USA',
    'Goward, Samuel N.': 'USA',
    'Spring, Adam P.': 'USA',
    'Deshpande, Sagar S.': 'USA',
    
    # 阿拉伯/中东作者
    'Habib, Ayman': 'Egypt',
    'Aneece, Itiya': 'Ethiopia',
    'Osama, Nahed': 'Egypt',
    
    # 非洲作者
    'Akumu, Clement E.': 'Kenya',
    'Lyimo, Neema Nicodemus': 'Tanzania',
    
    # 土耳其作者
    'Altan, Orhan': 'Turkey',
    
    # 巴西作者
    'Tommaselli, Antonio Maria Garcia': 'Brazil',
    
    # 德国作者
    'Bulatov, Dimitri': 'Germany',
    'Heipke, C.': 'Germany',
    
    # 斯里兰卡作者
    'Witharana, Chandi': 'Sri Lanka',
    
    # 印度作者
    'Teluguntla, Pardhasaradhi': 'India',
    
    # 土耳其作者
    'Hamal, Seda Nur Gamze': 'Turkey',
}

# 额外的姓氏规则（补充）
ENHANCED_SURNAME_PATTERNS = {
    'Pakistan': ['Javed', 'Ullah', 'Ara', 'Nadeem'],
    'Egypt': ['Osama', 'Nahed'],
    'Ethiopia': ['Aneece'],
    'Kenya': ['Akumu'],
    'Tanzania': ['Lyimo', 'Neema'],
    'Sri Lanka': ['Witharana'],
    'Brazil': ['Tommaselli', 'Garcia'],
}

# 名字前缀/后缀特征
NAME_FEATURES = {
    # 拼音双音节特征
    'china_patterns': [
        r'\b(Ge|Di|Su|Gu|Qu|Mu|Nu|Fu|Pu|Ku|Lu|Tu|Ru|Bu)\b[, ][A-Z]',  # 单音节姓 + 名
        r'[, ](Xuming|Xiaohua|Kaichang|Qinghong|Chaoyang|Jiageng)',  # 常见拼音名
    ],
    # 印度/巴基斯坦特征
    'south_asia_patterns': [
        r'\b(Prasad|Javed|Akib|Ullah|Inam|Iffat|Pardhasaradhi)\b',
    ],
    # 非洲特征
    'africa_patterns': [
        r'\b(Akumu|Clement|Lyimo|Neema|Aneece)\b',
    ],
}

def apply_manual_rules(nationality_map):
    """应用手动规则增强识别"""
    
    updated_count = 0
    
    # 1. 应用手动识别的高产作者
    for author, nationality in MANUAL_NATIONALITY_MAP.items():
        if author in nationality_map:
            if nationality_map[author] == 'Unknown':
                nationality_map[author] = nationality
                updated_count += 1
    
    # 2. 应用增强的姓氏规则
    import re
    for author, current_nat in list(nationality_map.items()):
        if current_nat != 'Unknown':
            continue
        
        # 检查姓氏
        lastname = author.split(',')[0].strip() if ',' in author else author.split()[-1]
        
        for country, surnames in ENHANCED_SURNAME_PATTERNS.items():
            if lastname in surnames:
                nationality_map[author] = country
                updated_count += 1
                break
        
        # 检查名字特征
        if nationality_map[author] == 'Unknown':
            # 中文拼音特征
            for pattern in NAME_FEATURES['china_patterns']:
                if re.search(pattern, author):
                    nationality_map[author] = 'China'
                    updated_count += 1
                    break
            
            # 南亚特征
            if nationality_map[author] == 'Unknown':
                for pattern in NAME_FEATURES['south_asia_patterns']:
                    if re.search(pattern, author):
                        # 进一步区分印度/巴基斯坦
                        if 'Prasad' in author or 'Pardhasaradhi' in author:
                            nationality_map[author] = 'India'
                        else:
                            nationality_map[author] = 'Pakistan'
                        updated_count += 1
                        break
            
            # 非洲特征
            if nationality_map[author] == 'Unknown':
                for pattern in NAME_FEATURES['africa_patterns']:
                    if re.search(pattern, author):
                        # 默认为Kenya（东非最常见）
                        nationality_map[author] = 'Kenya'
                        updated_count += 1
                        break
    
    return updated_count

def enhance_analysis():
    """增强分析"""
    
    print("🚀 开始增强国籍识别...")
    
    # 加载现有分析
    with open('author_nationality_analysis_enhanced.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    original_unknown = sum(1 for nat in analysis['nationality_map'].values() if nat == 'Unknown')
    
    # 应用手动规则
    updated_count = apply_manual_rules(analysis['nationality_map'])
    
    # 重新统计
    nationality_counts = Counter(analysis['nationality_map'].values())
    analysis['nationality_counts'] = dict(nationality_counts)
    
    # 重新计算论文贡献
    nationality_paper_counts = defaultdict(int)
    for author, count in analysis['author_counts'].items():
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        nationality_paper_counts[nationality] += count
    analysis['nationality_paper_counts'] = dict(nationality_paper_counts)
    
    new_unknown = sum(1 for nat in analysis['nationality_map'].values() if nat == 'Unknown')
    
    print(f"\n📊 识别率提升:")
    print(f"   原识别数: {len(analysis['nationality_map']) - original_unknown}")
    print(f"   新识别数: {updated_count}")
    print(f"   当前识别数: {len(analysis['nationality_map']) - new_unknown}")
    print(f"   识别率: {(len(analysis['nationality_map']) - new_unknown) / len(analysis['nationality_map']) * 100:.1f}%")
    print(f"   提升: {updated_count / len(analysis['nationality_map']) * 100:.1f}个百分点")
    
    # 保存最终版本
    with open('author_nationality_analysis_final.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 最终分析已保存: author_nationality_analysis_final.json")
    
    return analysis

if __name__ == '__main__':
    analysis = enhance_analysis()
    
    # 显示新增识别的国家
    print(f"\n🌍 新增识别的国家:")
    new_countries = set()
    for nat in analysis['nationality_counts'].keys():
        if nat not in ['China', 'Unknown', 'Arab', 'Turkey', 'Germany', 'USA', 'Korea', 'India', 'Japan', 'Saudi Arabia', 'Netherlands', 'France', 'Spain', 'Canada']:
            new_countries.add(nat)
    
    for country in sorted(new_countries):
        count = analysis['nationality_counts'][country]
        print(f"   {country}: {count}")
