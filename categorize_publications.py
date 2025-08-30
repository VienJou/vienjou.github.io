#!/usr/bin/env python3
import os
import re
import yaml

def is_conference_paper(filepath):
    """判断是否为会议论文"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                if data:
                    venue = data.get('venue', '').lower()
                    # 会议关键词
                    conference_keywords = [
                        'conference', 'symposium', 'workshop', 'meeting', 'assembly',
                        'egu', 'ieee', 'acm', 'isprs', 'igrass', 'igarss'
                    ]
                    
                    # 检查venue是否包含会议关键词
                    for keyword in conference_keywords:
                        if keyword in venue:
                            return True
                    
                    # 检查是否有会议特有的字段
                    if 'abstract_id' in data or 'talk_type' in data or 'date_range' in data:
                        return True
                    
                    # 检查特定会议名称
                    if any(conf in venue for conf in ['EGU', 'IEEE', 'ACM', 'ISPRS']):
                        return True
                        
            except yaml.YAMLError:
                pass
        
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def update_category(filepath, new_category):
    """更新文件的category字段"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换category字段
        content = re.sub(r'category:\s*manuscripts', f'category: {new_category}', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    publications_dir = '_publications'
    files = [f for f in os.listdir(publications_dir) if f.endswith('.md')]
    
    print("=== 自动分类出版物 ===\n")
    
    journal_count = 0
    conference_count = 0
    
    for filename in files:
        filepath = os.path.join(publications_dir, filename)
        
        if is_conference_paper(filepath):
            category = 'conferences'
            conference_count += 1
            print(f"会议论文: {filename}")
        else:
            category = 'journals'
            journal_count += 1
            print(f"期刊论文: {filename}")
        
        # 更新文件
        if update_category(filepath, category):
            print(f"  已更新为: {category}")
        else:
            print(f"  更新失败")
        print()
    
    print(f"总计: {len(files)} 个文件")
    print(f"期刊论文: {journal_count} 个")
    print(f"会议论文: {conference_count} 个")
    print("\n分类完成！")

if __name__ == "__main__":
    main() 