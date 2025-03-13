# 克苏鲁调查员生成器 (Call of Cthulhu Investigator Generator)

一个基于PyQt6的克苏鲁神话调查员生成工具，可以随机或自定义生成符合克苏鲁神话7版规则的调查员角色。

## 功能特点

- 随机生成调查员角色
- 自定义创建调查员角色
- 调整调查员属性、技能和背景
- 保存和加载调查员数据
- 导出调查员角色为文本格式

## 项目结构

```
cthulhu_investigator_generator/
│
├── main.py                 # 主程序入口
├── requirements.txt        # 项目依赖
│
├── core/                   # 核心逻辑
│   ├── __init__.py         # 包初始化
│   ├── config.py           # 配置管理
│   ├── investigator.py     # 调查员类
│   ├── attributes.py       # 属性管理
│   ├── skills.py           # 技能管理
│   ├── occupations.py      # 职业管理
│   ├── backgrounds.py      # 背景管理
│   └── generator.py        # 调查员生成器
│
├── gui/                    # 图形界面
│   ├── __init__.py         # 包初始化
│   ├── main_window.py      # 主窗口
│   └── tabs/               # 选项卡组件
│       ├── __init__.py     # 包初始化
│       ├── attribute_tab.py # 属性选项卡
│       ├── occupation_tab.py # 职业选项卡
│       ├── skills_tab.py   # 技能选项卡
│       ├── background_tab.py # 背景选项卡
│       ├── equipment_tab.py # 装备选项卡
│       └── summary_tab.py  # 摘要选项卡
│
├── utils/                  # 实用工具
│   ├── __init__.py         # 包初始化
│   ├── dice.py             # 骰子模拟器
│   └── file_handler.py     # 文件处理工具
│
└── data/                   # 数据文件
    ├── skills.json         # 技能数据
    ├── occupations.json    # 职业数据
    └── backgrounds.json    # 背景数据
```

## 使用方法

1. 安装依赖：
```
pip install -r requirements.txt
```

2. 运行程序：
```
python main.py
```

## 环境要求

- Python 3.8 或更高版本
- PyQt6
- 其他依赖见 requirements.txt 文件

## 开发目标

- [x] 基本生成器功能
- [x] 图形界面实现
- [x] 调查员属性生成
- [x] 职业与技能管理
- [x] 角色背景生成
- [x] 文件保存和加载
- [ ] 调查员角色表格导出
- [ ] 多语言支持
- [ ] 自定义规则设置 
