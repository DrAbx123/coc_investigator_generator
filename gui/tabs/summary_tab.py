#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QTextDocument
from PyQt6.QtPrintSupport import QPrinter

class SummaryTab(QWidget):
    """摘要标签页"""
    
    def __init__(self, parent):
        """初始化摘要标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # 创建滚动内容
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # 创建基本信息组
        basic_info_group = QGroupBox("基本信息")
        basic_info_layout = QGridLayout(basic_info_group)
        
        # 添加基本信息字段
        basic_info_layout.addWidget(QLabel("姓名:"), 0, 0)
        self.name_label = QLabel()
        basic_info_layout.addWidget(self.name_label, 0, 1)
        
        basic_info_layout.addWidget(QLabel("玩家:"), 0, 2)
        self.player_label = QLabel()
        basic_info_layout.addWidget(self.player_label, 0, 3)
        
        basic_info_layout.addWidget(QLabel("性别:"), 1, 0)
        self.gender_label = QLabel()
        basic_info_layout.addWidget(self.gender_label, 1, 1)
        
        basic_info_layout.addWidget(QLabel("年龄:"), 1, 2)
        self.age_label = QLabel()
        basic_info_layout.addWidget(self.age_label, 1, 3)
        
        basic_info_layout.addWidget(QLabel("职业:"), 2, 0)
        self.occupation_label = QLabel()
        basic_info_layout.addWidget(self.occupation_label, 2, 1)
        
        basic_info_layout.addWidget(QLabel("居住地:"), 2, 2)
        self.residence_label = QLabel()
        basic_info_layout.addWidget(self.residence_label, 2, 3)
        
        basic_info_layout.addWidget(QLabel("出生地:"), 3, 0)
        self.birthplace_label = QLabel()
        basic_info_layout.addWidget(self.birthplace_label, 3, 1)
        
        # 添加基本信息组到滚动布局
        scroll_layout.addWidget(basic_info_group)
        
        # 创建属性组
        attributes_group = QGroupBox("属性")
        attributes_layout = QGridLayout(attributes_group)
        
        # 添加属性标题
        attributes_layout.addWidget(QLabel("属性"), 0, 0)
        attributes_layout.addWidget(QLabel("值"), 0, 1)
        attributes_layout.addWidget(QLabel("半值"), 0, 2)
        attributes_layout.addWidget(QLabel("五分之一值"), 0, 3)
        
        # 创建属性标签
        self.attribute_labels = {}
        
        row = 1
        for attr_name in ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]:
            # 属性名
            attributes_layout.addWidget(QLabel(attr_name), row, 0)
            
            # 属性值
            value_label = QLabel()
            attributes_layout.addWidget(value_label, row, 1)
            
            # 半值
            half_label = QLabel()
            attributes_layout.addWidget(half_label, row, 2)
            
            # 五分之一值
            fifth_label = QLabel()
            attributes_layout.addWidget(fifth_label, row, 3)
            
            # 存储标签
            self.attribute_labels[attr_name] = {
                "value": value_label,
                "half": half_label,
                "fifth": fifth_label
            }
            
            row += 1
        
        # 添加属性组到滚动布局
        scroll_layout.addWidget(attributes_group)
        
        # 创建衍生属性组
        derived_group = QGroupBox("衍生属性")
        derived_layout = QGridLayout(derived_group)
        
        # 添加衍生属性
        derived_layout.addWidget(QLabel("生命值:"), 0, 0)
        self.hp_label = QLabel()
        derived_layout.addWidget(self.hp_label, 0, 1)
        
        derived_layout.addWidget(QLabel("魔法值:"), 0, 2)
        self.mp_label = QLabel()
        derived_layout.addWidget(self.mp_label, 0, 3)
        
        derived_layout.addWidget(QLabel("理智值:"), 1, 0)
        self.san_label = QLabel()
        derived_layout.addWidget(self.san_label, 1, 1)
        
        derived_layout.addWidget(QLabel("伤害加值:"), 1, 2)
        self.db_label = QLabel()
        derived_layout.addWidget(self.db_label, 1, 3)
        
        derived_layout.addWidget(QLabel("体格:"), 2, 0)
        self.build_label = QLabel()
        derived_layout.addWidget(self.build_label, 2, 1)
        
        derived_layout.addWidget(QLabel("移动速度:"), 2, 2)
        self.mov_label = QLabel()
        derived_layout.addWidget(self.mov_label, 2, 3)
        
        # 添加衍生属性组到滚动布局
        scroll_layout.addWidget(derived_group)
        
        # 创建技能组
        skills_group = QGroupBox("技能")
        skills_layout = QVBoxLayout(skills_group)
        
        # 添加技能表格
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(2)
        self.skills_table.setHorizontalHeaderLabels(["技能名称", "技能值"])
        self.skills_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.skills_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        skills_layout.addWidget(self.skills_table)
        
        # 添加技能组到滚动布局
        scroll_layout.addWidget(skills_group)
        
        # 创建武器组
        weapons_group = QGroupBox("武器")
        weapons_layout = QVBoxLayout(weapons_group)
        
        # 添加武器表格
        self.weapons_table = QTableWidget()
        self.weapons_table.setColumnCount(4)
        self.weapons_table.setHorizontalHeaderLabels(["名称", "数量", "伤害/效果", "射程/范围"])
        self.weapons_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.weapons_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.weapons_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.weapons_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        weapons_layout.addWidget(self.weapons_table)
        
        # 添加武器组到滚动布局
        scroll_layout.addWidget(weapons_group)
        
        # 创建装备组
        equipment_group = QGroupBox("装备")
        equipment_layout = QVBoxLayout(equipment_group)
        
        # 添加装备表格
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(4)
        self.equipment_table.setHorizontalHeaderLabels(["名称", "数量", "伤害/效果", "射程/范围"])
        self.equipment_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.equipment_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.equipment_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.equipment_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        equipment_layout.addWidget(self.equipment_table)
        
        # 添加装备组到滚动布局
        scroll_layout.addWidget(equipment_group)
        
        # 创建财产组
        assets_group = QGroupBox("财产")
        assets_layout = QGridLayout(assets_group)
        
        # 添加财产信息
        assets_layout.addWidget(QLabel("现金:"), 0, 0)
        self.cash_label = QLabel()
        assets_layout.addWidget(self.cash_label, 0, 1)
        
        assets_layout.addWidget(QLabel("消费水平:"), 0, 2)
        self.spending_level_label = QLabel()
        assets_layout.addWidget(self.spending_level_label, 0, 3)
        
        assets_layout.addWidget(QLabel("资产:"), 1, 0)
        self.assets_label = QLabel()
        self.assets_label.setWordWrap(True)
        assets_layout.addWidget(self.assets_label, 1, 1, 1, 3)
        
        # 添加财产组到滚动布局
        scroll_layout.addWidget(assets_group)
        
        # 创建背景组
        background_group = QGroupBox("背景")
        background_layout = QVBoxLayout(background_group)
        
        # 添加背景信息
        background_layout.addWidget(QLabel("个人描述:"))
        self.personal_description_label = QLabel()
        self.personal_description_label.setWordWrap(True)
        background_layout.addWidget(self.personal_description_label)
        
        background_layout.addWidget(QLabel("思想信念:"))
        self.ideology_label = QLabel()
        self.ideology_label.setWordWrap(True)
        background_layout.addWidget(self.ideology_label)
        
        background_layout.addWidget(QLabel("重要之人:"))
        self.significant_people_label = QLabel()
        self.significant_people_label.setWordWrap(True)
        background_layout.addWidget(self.significant_people_label)
        
        background_layout.addWidget(QLabel("意义非凡之地:"))
        self.meaningful_locations_label = QLabel()
        self.meaningful_locations_label.setWordWrap(True)
        background_layout.addWidget(self.meaningful_locations_label)
        
        background_layout.addWidget(QLabel("宝贵之物:"))
        self.treasured_possessions_label = QLabel()
        self.treasured_possessions_label.setWordWrap(True)
        background_layout.addWidget(self.treasured_possessions_label)
        
        background_layout.addWidget(QLabel("特质:"))
        self.traits_label = QLabel()
        self.traits_label.setWordWrap(True)
        background_layout.addWidget(self.traits_label)
        
        # 添加背景组到滚动布局
        scroll_layout.addWidget(background_group)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(scroll_area)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        # 添加打印按钮
        self.print_button = QPushButton("打印角色卡")
        button_layout.addWidget(self.print_button)
        
        # 添加导出按钮
        self.export_button = QPushButton("导出为文本")
        button_layout.addWidget(self.export_button)
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
        
        # 连接信号和槽
        self.print_button.clicked.connect(self.print_character_sheet)
        self.export_button.clicked.connect(self.export_to_text)
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新基本信息
        self.name_label.setText(investigator.name)
        self.player_label.setText(investigator.player)
        self.gender_label.setText(investigator.gender)
        self.age_label.setText(str(investigator.age))
        self.occupation_label.setText(investigator.occupation)
        self.residence_label.setText(investigator.residence)
        self.birthplace_label.setText(investigator.birthplace)
        
        # 更新属性
        for attr_name, labels in self.attribute_labels.items():
            value = investigator.attributes.get(attr_name, 0)
            half_value = investigator.attribute_half.get(attr_name, 0)
            fifth_value = investigator.attribute_fifth.get(attr_name, 0)
            
            labels["value"].setText(str(value))
            labels["half"].setText(str(half_value))
            labels["fifth"].setText(str(fifth_value))
        
        # 更新衍生属性
        self.hp_label.setText(str(investigator.hp))
        self.mp_label.setText(str(investigator.mp))
        self.san_label.setText(str(investigator.san))
        self.db_label.setText(str(investigator.db))
        self.build_label.setText(str(investigator.build))
        self.mov_label.setText(str(investigator.mov))
        
        # 更新技能表格
        self.skills_table.setRowCount(0)
        
        row = 0
        for skill_name, skill_value in sorted(investigator.skills.items()):
            self.skills_table.insertRow(row)
            self.skills_table.setItem(row, 0, QTableWidgetItem(skill_name))
            self.skills_table.setItem(row, 1, QTableWidgetItem(str(skill_value)))
            row += 1
        
        # 更新武器和装备表格
        self.weapons_table.setRowCount(0)
        self.equipment_table.setRowCount(0)
        
        weapons_row = 0
        equipment_row = 0
        
        for equipment in investigator.equipment:
            if equipment.get("damage"):
                # 武器
                self.weapons_table.insertRow(weapons_row)
                self.weapons_table.setItem(weapons_row, 0, QTableWidgetItem(equipment["name"]))
                self.weapons_table.setItem(weapons_row, 1, QTableWidgetItem(equipment["quantity"]))
                self.weapons_table.setItem(weapons_row, 2, QTableWidgetItem(equipment["damage"]))
                self.weapons_table.setItem(weapons_row, 3, QTableWidgetItem(equipment["range"]))
                weapons_row += 1
            else:
                # 普通装备
                self.equipment_table.insertRow(equipment_row)
                self.equipment_table.setItem(equipment_row, 0, QTableWidgetItem(equipment["name"]))
                self.equipment_table.setItem(equipment_row, 1, QTableWidgetItem(equipment["quantity"]))
                self.equipment_table.setItem(equipment_row, 2, QTableWidgetItem(equipment["damage"]))
                self.equipment_table.setItem(equipment_row, 3, QTableWidgetItem(equipment["range"]))
                equipment_row += 1
        
        # 更新财产信息
        self.cash_label.setText(str(investigator.cash))
        
        # 根据现金确定消费水平
        if investigator.cash < 10:
            level = "贫穷"
        elif investigator.cash < 50:
            level = "标准"
        elif investigator.cash < 100:
            level = "小康"
        elif investigator.cash < 500:
            level = "富裕"
        else:
            level = "富豪"
        
        self.spending_level_label.setText(level)
        self.assets_label.setText(investigator.assets)
        
        # 更新背景信息
        self.personal_description_label.setText(investigator.personal_description)
        self.ideology_label.setText(investigator.ideology)
        self.significant_people_label.setText(investigator.significant_people)
        self.meaningful_locations_label.setText(investigator.meaningful_locations)
        self.treasured_possessions_label.setText(investigator.treasured_possessions)
        self.traits_label.setText(investigator.traits)
    
    def print_character_sheet(self):
        """打印角色卡"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 创建打印机
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageSize(QPrinter.PageSize.A4)
        
        # 创建文档
        document = QTextDocument()
        
        # 构建HTML内容
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ text-align: center; }}
                h2 {{ margin-top: 20px; border-bottom: 1px solid #ccc; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ccc; padding: 5px; }}
                th {{ background-color: #f0f0f0; }}
            </style>
        </head>
        <body>
            <h1>克苏鲁的呼唤 - 调查员角色卡</h1>
            
            <h2>基本信息</h2>
            <table>
                <tr>
                    <th>姓名</th>
                    <td>{investigator.name}</td>
                    <th>玩家</th>
                    <td>{investigator.player}</td>
                </tr>
                <tr>
                    <th>性别</th>
                    <td>{investigator.gender}</td>
                    <th>年龄</th>
                    <td>{investigator.age}</td>
                </tr>
                <tr>
                    <th>职业</th>
                    <td>{investigator.occupation}</td>
                    <th>居住地</th>
                    <td>{investigator.residence}</td>
                </tr>
                <tr>
                    <th>出生地</th>
                    <td colspan="3">{investigator.birthplace}</td>
                </tr>
            </table>
            
            <h2>属性</h2>
            <table>
                <tr>
                    <th>属性</th>
                    <th>值</th>
                    <th>半值</th>
                    <th>五分之一值</th>
                </tr>
        """
        
        # 添加属性
        for attr_name in ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]:
            value = investigator.attributes.get(attr_name, 0)
            half_value = investigator.attribute_half.get(attr_name, 0)
            fifth_value = investigator.attribute_fifth.get(attr_name, 0)
            
            html += f"""
                <tr>
                    <th>{attr_name}</th>
                    <td>{value}</td>
                    <td>{half_value}</td>
                    <td>{fifth_value}</td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <h2>衍生属性</h2>
            <table>
                <tr>
                    <th>生命值</th>
                    <td>{investigator.hp}</td>
                    <th>魔法值</th>
                    <td>{investigator.mp}</td>
                </tr>
                <tr>
                    <th>理智值</th>
                    <td>{investigator.san}</td>
                    <th>伤害加值</th>
                    <td>{investigator.db}</td>
                </tr>
                <tr>
                    <th>体格</th>
                    <td>{investigator.build}</td>
                    <th>移动速度</th>
                    <td>{investigator.mov}</td>
                </tr>
            </table>
            
            <h2>技能</h2>
            <table>
                <tr>
                    <th>技能名称</th>
                    <th>技能值</th>
                </tr>
        """
        
        # 添加技能
        for skill_name, skill_value in sorted(investigator.skills.items()):
            html += f"""
                <tr>
                    <td>{skill_name}</td>
                    <td>{skill_value}</td>
                </tr>
            """
        
        html += f"""
            </table>
            
            <h2>武器</h2>
            <table>
                <tr>
                    <th>名称</th>
                    <th>数量</th>
                    <th>伤害/效果</th>
                    <th>射程/范围</th>
                </tr>
        """
        
        # 添加武器
        for equipment in investigator.equipment:
            if equipment.get("damage"):
                html += f"""
                    <tr>
                        <td>{equipment['name']}</td>
                        <td>{equipment['quantity']}</td>
                        <td>{equipment['damage']}</td>
                        <td>{equipment['range']}</td>
                    </tr>
                """
        
        html += f"""
            </table>
            
            <h2>装备</h2>
            <table>
                <tr>
                    <th>名称</th>
                    <th>数量</th>
                    <th>效果</th>
                    <th>范围</th>
                </tr>
        """
        
        # 添加装备
        for equipment in investigator.equipment:
            if not equipment.get("damage"):
                html += f"""
                    <tr>
                        <td>{equipment['name']}</td>
                        <td>{equipment['quantity']}</td>
                        <td>{equipment['damage']}</td>
                        <td>{equipment['range']}</td>
                    </tr>
                """
        
        html += f"""
            </table>
            
            <h2>财产</h2>
            <p><strong>现金:</strong> {investigator.cash}</p>
            <p><strong>资产:</strong> {investigator.assets}</p>
            
            <h2>背景</h2>
            <p><strong>个人描述:</strong> {investigator.personal_description}</p>
            <p><strong>思想信念:</strong> {investigator.ideology}</p>
            <p><strong>重要之人:</strong> {investigator.significant_people}</p>
            <p><strong>意义非凡之地:</strong> {investigator.meaningful_locations}</p>
            <p><strong>宝贵之物:</strong> {investigator.treasured_possessions}</p>
            <p><strong>特质:</strong> {investigator.traits}</p>
        </body>
        </html>
        """
        
        # 设置文档内容
        document.setHtml(html)
        
        # 打印文档
        document.print_(printer)
    
    def export_to_text(self):
        """导出为文本"""
        if not self.parent.current_investigator:
            return
        
        # 调用文件处理器导出为文本
        self.parent.export_investigator_to_text() 