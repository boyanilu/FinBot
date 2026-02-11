# 基于微调大模型的金融对话交互智能系统

## 项目背景简介

本项目是以大模型为中心的金融对话交互系统，旨在回答用户的金融相关问题，数据集来源于真实的11588份2019年至2021年期间的上市公司年度报告。

项目目标是构建一个深度解析上市公司年报的对话交互智能系统，面对金融文本中的专业术语与暗含信息，致力于用AI实现专家级别的金融分析。系统可用于股票交易问答助手、智能金融行业分析助手等落地应用。

按照涉及模型的能力和复杂程度，系统分为三种类型：
- **初级：数据基本查询**（能直接在年报中找到的），如：某公司2021年的研发费用是多少？
- **中级：数据统计分析查询**（需要做统计计算的），如：某公司2021年研发费用增长率为多少？
- **高级：开放性问题**（需要做分析总结的），如：某公司2021年主要研发项目是否涉及国家创新领域？

## 项目配置

### 环境安装
1. 确保安装了CUDA、cuDNN和PyTorch-GPU等基本库
2. 安装项目依赖：
   ```bash
   pip install -r requirements2.txt
   ```
3. 在运行过程中，根据缺失的个别包信息，再进行安装

### 模型下载
1. 下载chatglm2-6b和Qwen1.5-7B模型，放到目录 `./data/pretrained_models/` 下
2. 数据准备：将allpdf解压后，目录放到 `./data/` 下

### 配置文件
修改 `config/cfg.py` 下的 `BASE_DIR` 为自己的项目绝对路径

## 运行指南

### 环境安装
1. 确保安装了CUDA、cuDNN和PyTorch-GPU等基本库
2. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 在运行过程中，根据缺失的个别包信息，再进行安装

### 模型下载
1. 下载Qwen3-8B模型，放到目录 `./data/pretrained_models/` 下
2. 数据准备：将allpdf解压后，目录放到 `./data/` 下

### 模型微调
如果需要进行模型微调，可以选择以下两种方式：

#### P-Tuning微调（推荐）
1. **问题分类微调**：
   ```bash
   cd ptuning/CLASSIFY_PUTUNING
   bash train.sh
   # 测试
   bash evaluate.sh
   ```
   观察指标预测情况，在output目录查看 `generated_predictions.txt` 的输出，是否符合预期。

2. **关键词抽取微调**：
   ```bash
   cd ptuning/KEYWORDS_PUTUNING
   bash train.sh
   # 测试
   bash evaluate.sh
   ```
   观察指标预测情况，在output目录查看 `generated_predictions.txt` 的输出，是否符合预期。

3. **SQL生成微调**：
   ```bash
   cd ptuning/NL2SQL_PUTUNING
   bash train.sh
   # 测试
   bash evaluate.sh
   ```
   观察指标预测情况，在output目录查看 `generated_predictions.txt` 的输出，是否符合预期。

#### LoRA微调
进入lora目录分别运行对应模型的训练、预测代码。

### 主代码运行
回到项目根目录，修改 `config/cfg.py` 下的 `BASE_DIR` 为自己的项目绝对路径，然后运行主代码：
```bash
python main.py
```

运行时间会较长，可根据服务器的CPU核数，调整 `config/cfg.py` 下的 `NUM_PROCESSES` 设置，利用并行计算加速模型处理过程。

### 指标计算
运行指标计算脚本，查看模型性能：
```bash
python test_score.py
```

预测指标在：`data/test/output.json`，包括type1, type2, type3以及加权后的总得分。

## 主要代码说明

### main.py
- 包含全流程：数据下载/PDF表格提取/表格生成/问题分类/问题关键词提取/SQL生成/问答结果生成/提交生成

### generate_answer_with_classify.py
- **generate_answer函数**：对每类问题生成问答结果

#### Type1（基本信息类）处理流程：
1. 从问题对应的报表中根据关键词召回可能对应的行
2. 对于行为字符串类型的，对比不同年份的字段内容是否相同
3. 对于问题问是否相同的，直接返回召回的报表
4. 对于其他的，通过prompt组合召回的报表传给模型进行回答

#### Type2（统计计算类）处理流程：
1. 如果是计算增长率，需要召回前一年的数据
2. 将需要计算的内容转换为多个提问，得到计算公式中的每个元素
3. 提取回答中的数值作为公式的单元，最后通过Python计算该公式

#### Type3（总结推理类）处理流程：
1. 提取问题中的关键词
2. 进行文本的召回，采用BM25算法，分别对问题关键词和原问题进行召回
3. 合并召回的文本块，按照和原问题的字符匹配长度取匹配度最高的文本块
4. 组合召回的文本形成prompt传给模型进行回答

## 项目结构

- **config/**: 配置文件目录
- **data/**: 数据和模型目录
- **ptuning/**: P-Tuning微调相关代码
- **lora/**: LoRA微调相关代码
- **main.py**: 主运行文件
- **generate_answer_with_classify.py**: 答案生成相关代码
- **test_score.py**: 指标计算脚本

## 注意事项

1. 项目运行需要较大的GPU内存，建议使用至少16GB显存的GPU
2. 首次运行时，数据处理和模型加载可能需要较长时间
3. 微调过程中，可通过观察 `output` 目录下的 `generated_predictions.txt` 文件，评估模型性能
4. 对于大规模数据处理，可适当调整并行计算参数以提高效率