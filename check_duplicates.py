#!/usr/bin/env python3
import os
import re
import yaml
from collections import defaultdict

def extract_title_from_md(filepath):
    """从markdown文件中提取标题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找YAML front matter中的title
        yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                if data and 'title' in data:
                    return data['title'].strip()
            except yaml.YAMLError:
                pass
        
        # 如果没有找到title，使用文件名
        return os.path.basename(filepath).replace('.md', '')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return os.path.basename(filepath).replace('.md', '')

def main():
    publications_dir = '_publications'
    files = [f for f in os.listdir(publications_dir) if f.endswith('.md')]
    
    # 按标题分组
    title_groups = defaultdict(list)
    
    for filename in files:
        filepath = os.path.join(publications_dir, filename)
        title = extract_title_from_md(filepath)
        title_groups[title].append(filename)
    
    print("=== 重复文件分析 ===\n")
    
    duplicates_found = False
    for title, filenames in title_groups.items():
        if len(filenames) > 1:
            duplicates_found = True
            print(f"标题: {title}")
            print(f"重复文件 ({len(filenames)}个):")
            for filename in filenames:
                print(f"  - {filename}")
            print()
    
    if not duplicates_found:
        print("没有发现重复文件！")
    
    print(f"\n总计: {len(files)} 个文件")
    print(f"唯一标题: {len(title_groups)} 个")

if __name__ == "__main__":
    main() 