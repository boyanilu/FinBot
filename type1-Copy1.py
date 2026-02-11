# debug_data.py
import json

def debug_data_file(filepath):
    """调试数据文件"""
    print(f"检查文件: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"总行数: {len(lines)}")
    
    valid_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            print(f"第{i+1}行: 空行")
            continue
        
        try:
            data = json.loads(line)
            valid_lines.append(data)
            
            # 检查必要字段
            required_fields = ['id', 'question', 'type', 'answer']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"第{i+1}行: 缺少字段 {missing_fields}")
            
            # 检查type字段
            if 'type' in data:
                print(f"第{i+1}行: id={data['id']}, type={data['type']}")
                
        except json.JSONDecodeError as e:
            print(f"第{i+1}行: JSON解析错误 - {e}")
    
    print(f"\n有效数据行数: {len(valid_lines)}")
    
    # 统计各类型数量
    type_counts = {}
    for data in valid_lines:
        if 'type' in data:
            t = data['type']
            type_counts[t] = type_counts.get(t, 0) + 1
    
    print("\n各类型问题数量统计:")
    for t, count in sorted(type_counts.items()):
        print(f"  Type {t}: {count}")
    
    return valid_lines

# 检查标准答案文件
print("=== 标准答案文件检查 ===")
standard_data = debug_data_file("./data/test/C-list-answer.json")

# 检查预测文件
print("\n=== 预测文件检查 ===")
predict_data = debug_data_file("./data/result_20260123.json")