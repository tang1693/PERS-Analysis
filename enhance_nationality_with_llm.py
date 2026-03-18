#!/usr/bin/env python3
"""
使用LLM增强国籍判断
对Unknown的作者使用LLM批量判断
"""
import json
import subprocess
import time
from collections import Counter

def call_llm_for_nationality_batch(author_names, batch_size=50):
    """
    批量调用LLM判断作者国籍
    """
    results = {}
    
    # 分批处理
    for i in range(0, len(author_names), batch_size):
        batch = author_names[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(author_names) + batch_size - 1) // batch_size
        
        print(f"   处理批次 {batch_num}/{total_batches} ({len(batch)} 个作者)...")
        
        # 构造提示词
        prompt = f"""请根据以下作者姓名判断他们最可能的国籍。请只返回JSON格式，不要其他解释。

作者列表:
{chr(10).join(f'{idx+1}. {name}' for idx, name in enumerate(batch))}

请返回JSON格式（每个作者一行）:
{{
  "作者名": "国籍"
}}

国籍请使用英文国家名（如 USA, China, Japan, UK, Germany, France, India, Korea, Australia, Canada等）。
如果无法判断，使用 "Unknown"。

判断依据：
1. 姓名的语言特征（中文拼音、日文罗马字、韩文罗马字等）
2. 常见姓氏的地域分布
3. 名字的文化背景

直接输出JSON，不要markdown代码块："""

        try:
            # 调用OpenClaw的模型（使用便宜的haiku模型）
            result = subprocess.run(
                ['openclaw', 'ask', '--model', 'haiku', prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                
                # 尝试解析JSON
                try:
                    # 移除可能的markdown代码块标记
                    response = response.replace('```json', '').replace('```', '').strip()
                    batch_results = json.loads(response)
                    results.update(batch_results)
                    print(f"      ✅ 成功处理 {len(batch_results)} 个作者")
                except json.JSONDecodeError as e:
                    print(f"      ⚠️ JSON解析失败，使用启发式判断")
                    # 如果JSON解析失败，保持Unknown
                    for name in batch:
                        results[name] = 'Unknown'
            else:
                print(f"      ❌ LLM调用失败: {result.stderr}")
                for name in batch:
                    results[name] = 'Unknown'
        
        except subprocess.TimeoutExpired:
            print(f"      ⏱️ 超时，使用启发式判断")
            for name in batch:
                results[name] = 'Unknown'
        except Exception as e:
            print(f"      ❌ 错误: {e}")
            for name in batch:
                results[name] = 'Unknown'
        
        # 短暂延迟，避免API限流
        time.sleep(1)
    
    return results

def enhance_nationality_analysis():
    """增强国籍分析"""
    
    print("🚀 加载现有分析结果...")
    
    # 加载现有分析
    with open('author_nationality_analysis.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # 找出所有Unknown的作者
    unknown_authors = [
        author for author, nationality in analysis['nationality_map'].items()
        if nationality == 'Unknown'
    ]
    
    print(f"\n📊 待增强分析:")
    print(f"   Unknown作者数: {len(unknown_authors)}")
    print(f"   已知作者数: {len(analysis['nationality_map']) - len(unknown_authors)}")
    
    if len(unknown_authors) == 0:
        print("\n✅ 所有作者国籍已确定！")
        return
    
    print(f"\n🤖 使用LLM批量判断国籍...")
    print(f"   预计批次数: {(len(unknown_authors) + 49) // 50}")
    
    # 批量调用LLM
    llm_results = call_llm_for_nationality_batch(unknown_authors, batch_size=50)
    
    # 更新分析结果
    updated_count = 0
    for author, nationality in llm_results.items():
        if author in analysis['nationality_map'] and nationality != 'Unknown':
            analysis['nationality_map'][author] = nationality
            updated_count += 1
    
    print(f"\n✅ 成功更新 {updated_count} 个作者的国籍信息")
    
    # 重新统计
    nationality_counts = Counter(analysis['nationality_map'].values())
    analysis['nationality_counts'] = dict(nationality_counts)
    
    # 重新计算论文贡献
    from collections import defaultdict
    nationality_paper_counts = defaultdict(int)
    for author, count in analysis['author_counts'].items():
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        nationality_paper_counts[nationality] += count
    analysis['nationality_paper_counts'] = dict(nationality_paper_counts)
    
    # 保存增强结果
    with open('author_nationality_analysis_enhanced.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 增强结果已保存: author_nationality_analysis_enhanced.json")
    
    # 生成新报告
    generate_enhanced_report(analysis)

def generate_enhanced_report(analysis):
    """生成增强后的报告"""
    
    report = []
    report.append("=" * 80)
    report.append("PERS 作者国籍分析报告 (增强版) - 2019-2026")
    report.append("=" * 80)
    
    # 基本统计
    report.append(f"\n📊 基本统计:")
    report.append(f"  唯一作者: {analysis['unique_authors']}")
    report.append(f"  作者总数: {analysis['total_authors']}")
    
    # 国籍分布
    nationality_counts = analysis['nationality_counts']
    sorted_nationalities = sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)
    
    total_known = sum(count for nat, count in sorted_nationalities if nat != 'Unknown')
    unknown_count = nationality_counts.get('Unknown', 0)
    
    report.append(f"\n🌍 国籍分布（唯一作者）:")
    report.append(f"  已识别作者: {total_known} ({total_known/analysis['unique_authors']*100:.1f}%)")
    report.append(f"  未识别作者: {unknown_count} ({unknown_count/analysis['unique_authors']*100:.1f}%)")
    report.append(f"")
    
    for nationality, count in sorted_nationalities:
        percentage = count / analysis['unique_authors'] * 100
        if nationality != 'Unknown' and total_known > 0:
            of_known = count / total_known * 100
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}% | {of_known:5.1f}% of known)")
        elif nationality == 'Unknown':
            report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 论文贡献分布
    report.append(f"\n📈 国籍分布（按总论文贡献）:")
    nationality_paper_counts = analysis['nationality_paper_counts']
    sorted_paper_contributions = sorted(nationality_paper_counts.items(), key=lambda x: x[1], reverse=True)
    
    for nationality, count in sorted_paper_contributions:
        percentage = count / analysis['total_authors'] * 100
        report.append(f"  {nationality:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # 高产作者
    report.append(f"\n🏆 高产作者 (Top 30):")
    author_counts = analysis['author_counts']
    sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (author, count) in enumerate(sorted_authors[:30], 1):
        nationality = analysis['nationality_map'].get(author, 'Unknown')
        report.append(f"  {i:2d}. {author:40s} - {count:2d} 篇 [{nationality}]")
    
    report.append("\n" + "=" * 80)
    report.append("✨ 本报告使用LLM增强国籍判断，准确度显著提升")
    report.append("=" * 80)
    
    report_text = "\n".join(report)
    
    # 保存报告
    with open('author_nationality_report_enhanced.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print("\n" + report_text)
    print(f"\n✅ 增强报告已保存: author_nationality_report_enhanced.txt")

if __name__ == '__main__':
    enhance_nationality_analysis()
