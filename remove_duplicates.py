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
        
        return os.path.basename(filepath).replace('.md', '')
    except Exception as e:
        return os.path.basename(filepath).replace('.md', '')

def get_file_completeness(filepath):
    """评估文件的完整性"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        score = 0
        yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                if data:
                    # 检查重要字段
                    if 'title' in data: score += 10
                    if 'authors' in data: score += 10
                    if 'date' in data: score += 5
                    if 'venue' in data: score += 5
                    if 'citation' in data: score += 10
                    if 'doi' in data: score += 5
                    if 'volume' in data: score += 3
                    if 'pages' in data: score += 3
                    if 'impact_factor' in data: score += 5
                    if 'permalink' in data: score += 2
                    
                    # 文件名长度（更长的文件名通常更完整）
                    score += len(os.path.basename(filepath)) * 0.1
            except yaml.YAMLError:
                pass
        
        return score
    except Exception as e:
        return 0

def main():
    publications_dir = '_publications'
    files = [f for f in os.listdir(publications_dir) if f.endswith('.md')]
    
    # 按标题分组
    title_groups = defaultdict(list)
    
    for filename in files:
        filepath = os.path.join(publications_dir, filename)
        title = extract_title_from_md(filepath)
        title_groups[title].append(filename)
    
    print("=== 删除重复文件 ===\n")
    
    files_to_delete = []
    files_to_keep = []
    
    for title, filenames in title_groups.items():
        if len(filenames) > 1:
            print(f"标题: {title}")
            
            # 计算每个文件的完整性分数
            file_scores = []
            for filename in filenames:
                filepath = os.path.join(publications_dir, filename)
                score = get_file_completeness(filepath)
                file_scores.append((filename, score))
                print(f"  - {filename} (分数: {score})")
            
            # 选择分数最高的文件保留
            file_scores.sort(key=lambda x: x[1], reverse=True)
            best_file = file_scores[0][0]
            files_to_keep.append(best_file)
            
            # 其他文件标记为删除
            for filename, score in file_scores[1:]:
                files_to_delete.append(filename)
                print(f"    删除: {filename}")
            
            print(f"    保留: {best_file}")
            print()
        else:
            # 单个文件直接保留
            files_to_keep.append(filenames[0])
    
    print(f"总计: {len(files)} 个文件")
    print(f"保留: {len(files_to_keep)} 个文件")
    print(f"删除: {len(files_to_delete)} 个文件")
    
    # 确认删除
    if files_to_delete:
        response = input("\n确认删除这些重复文件? (y/N): ")
        if response.lower() == 'y':
            for filename in files_to_delete:
                filepath = os.path.join(publications_dir, filename)
                try:
                    os.remove(filepath)
                    print(f"已删除: {filename}")
                except Exception as e:
                    print(f"删除失败 {filename}: {e}")
            print("\n重复文件删除完成！")
        else:
            print("取消删除操作。")
    else:
        print("没有重复文件需要删除。")

if __name__ == "__main__":
    main() 