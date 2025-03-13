#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class SkillsTab(QWidget):
    """技能标签页"""
    
    def __init__(self, parent):
        """初始化技能标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建技能点信息组
        skill_points_group = QGroupBox("技能点信息")
        skill_points_layout = QGridLayout(skill_points_group)
        
        # 添加职业技能点信息
        skill_points_layout.addWidget(QLabel("职业技能点:"), 0, 0)
        self.occupation_skill_points = QLineEdit()
        self.occupation_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.occupation_skill_points, 0, 1)
        
        skill_points_layout.addWidget(QLabel("已分配职业技能点:"), 0, 2)
        self.allocated_occupation_skill_points = QLineEdit()
        self.allocated_occupation_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.allocated_occupation_skill_points, 0, 3)
        
        # 添加兴趣技能点信息
        skill_points_layout.addWidget(QLabel("兴趣技能点:"), 1, 0)
        self.interest_skill_points = QLineEdit()
        self.interest_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.interest_skill_points, 1, 1)
        
        skill_points_layout.addWidget(QLabel("已分配兴趣技能点:"), 1, 2)
        self.allocated_interest_skill_points = QLineEdit()
        self.allocated_interest_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.allocated_interest_skill_points, 1, 3)
        
        # 添加技能点信息组到主布局
        main_layout.addWidget(skill_points_group)
        
        # 创建搜索和过滤组
        search_filter_group = QGroupBox("搜索和过滤")
        search_filter_layout = QHBoxLayout(search_filter_group)
        
        # 添加搜索框
        search_filter_layout.addWidget(QLabel("搜索:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入技能名称搜索...")
        search_filter_layout.addWidget(self.search_edit)
        
        # 添加过滤选项
        search_filter_layout.addWidget(QLabel("显示:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["所有技能", "职业技能", "已分配技能"])
        search_filter_layout.addWidget(self.filter_combo)
        
        # 添加搜索和过滤组到主布局
        main_layout.addWidget(search_filter_group)
        
        # 创建技能表格
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(6)
        self.skills_table.setHorizontalHeaderLabels(["技能名称", "基础值", "职业技能", "加点", "最终值", "操作"])
        self.skills_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.skills_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # 添加技能表格到主布局
        main_layout.addWidget(self.skills_table)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        # 添加重置按钮
        self.reset_button = QPushButton("重置技能点")
        button_layout.addWidget(self.reset_button)
        
        # 添加随机分配按钮
        self.random_button = QPushButton("随机分配技能点")
        button_layout.addWidget(self.random_button)
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
        
        # 连接信号和槽
        self.search_edit.textChanged.connect(self.filter_skills)
        self.filter_combo.currentIndexChanged.connect(self.filter_skills)
        self.reset_button.clicked.connect(self.reset_skill_points)
        self.random_button.clicked.connect(self.random_allocate_skill_points)
    
    def load_skills(self):
        """加载技能列表"""
        if not self.parent.skills or not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 清空表格
        self.skills_table.setRowCount(0)
        
        # 获取职业技能
        occupation_skills = []
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation:
                occupation_skills = occupation.get("skills", [])
        
        # 添加技能到表格
        row = 0
        for skill_name, skill in sorted(self.parent.skills.skills.items()):
            # 检查过滤条件
            if self.filter_combo.currentText() == "职业技能" and skill_name not in occupation_skills:
                continue
            
            if self.filter_combo.currentText() == "已分配技能" and skill_name not in investigator.skills:
                continue
            
            # 检查搜索条件
            search_text = self.search_edit.text().lower()
            if search_text and search_text not in skill_name.lower():
                continue
            
            # 添加新行
            self.skills_table.insertRow(row)
            
            # 技能名称
            name_item = QTableWidgetItem(skill_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.skills_table.setItem(row, 0, name_item)
            
            # 基础值
            base_value = skill.get("base", 0)
            base_item = QTableWidgetItem(str(base_value))
            base_item.setFlags(base_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.skills_table.setItem(row, 1, base_item)
            
            # 职业技能
            is_occupation_skill = skill_name in occupation_skills
            occupation_item = QTableWidgetItem()
            occupation_item.setFlags(occupation_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            occupation_item.setCheckState(Qt.CheckState.Checked if is_occupation_skill else Qt.CheckState.Unchecked)
            self.skills_table.setItem(row, 2, occupation_item)
            
            # 加点
            points = investigator.skills.get(skill_name, 0) - base_value
            points_spin = QSpinBox()
            points_spin.setRange(0, 100)
            points_spin.setValue(points)
            points_spin.valueChanged.connect(lambda value, r=row, s=skill_name: self.on_points_changed(r, s, value))
            self.skills_table.setCellWidget(row, 3, points_spin)
            
            # 最终值
            final_value = investigator.skills.get(skill_name, base_value)
            final_item = QTableWidgetItem(str(final_value))
            final_item.setFlags(final_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.skills_table.setItem(row, 4, final_item)
            
            # 操作按钮
            roll_button = QPushButton("掷骰")
            roll_button.clicked.connect(lambda checked, s=skill_name: self.roll_skill(s))
            self.skills_table.setCellWidget(row, 5, roll_button)
            
            row += 1
    
    def filter_skills(self):
        """根据搜索文本和过滤条件过滤技能列表"""
        self.load_skills()
    
    def on_points_changed(self, row, skill_name, value):
        """技能点变化时的处理"""
        if not self.parent.current_investigator or not self.parent.skills:
            return
        
        investigator = self.parent.current_investigator
        skill = self.parent.skills.get_skill(skill_name)
        
        if not skill:
            return
        
        # 获取原始加点
        old_points = investigator.skills.get(skill_name, skill.get("base", 0)) - skill.get("base", 0)
        
        # 计算差值
        diff = value - old_points
        
        if diff == 0:
            return
        
        # 检查是否是职业技能
        is_occupation_skill = False
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation and skill_name in occupation.get("skills", []):
                is_occupation_skill = True
        
        # 检查技能点是否足够
        if diff > 0:
            if is_occupation_skill:
                if investigator.occupation_skill_points_allocated + diff > investigator.occupation_skill_points:
                    # 职业技能点不足，恢复原值
                    points_spin = self.skills_table.cellWidget(row, 3)
                    points_spin.setValue(old_points)
                    return
            else:
                if investigator.interest_skill_points_allocated + diff > investigator.interest_skill_points:
                    # 兴趣技能点不足，恢复原值
                    points_spin = self.skills_table.cellWidget(row, 3)
                    points_spin.setValue(old_points)
                    return
        
        # 更新技能值
        new_value = skill.get("base", 0) + value
        investigator.skills[skill_name] = new_value
        
        # 更新已分配技能点
        if is_occupation_skill:
            investigator.occupation_skill_points_allocated += diff
        else:
            investigator.interest_skill_points_allocated += diff
        
        # 更新UI
        self.update_ui()
        
        # 更新最终值
        final_item = QTableWidgetItem(str(new_value))
        final_item.setFlags(final_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.skills_table.setItem(row, 4, final_item)
    
    def roll_skill(self, skill_name):
        """掷骰检定技能"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        skill_value = investigator.skills.get(skill_name, 0)
        
        # 掷骰
        result = self.parent.investigator_generator.dice_roller.roll_d100()
        
        # 判定结果
        if result <= skill_value / 5:
            success_level = "大成功"
        elif result <= skill_value / 2:
            success_level = "困难成功"
        elif result <= skill_value:
            success_level = "成功"
        elif result > 95:
            success_level = "大失败"
        else:
            success_level = "失败"
        
        # 显示结果
        message = f"{skill_name}检定：掷骰结果{result}，技能值{skill_value}，{success_level}"
        self.parent.show_message(message)
    
    def reset_skill_points(self):
        """重置技能点"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 重置技能
        for skill_name, skill in self.parent.skills.skills.items():
            if skill_name in investigator.skills:
                investigator.skills[skill_name] = skill.get("base", 0)
        
        # 重置已分配技能点
        investigator.occupation_skill_points_allocated = 0
        investigator.interest_skill_points_allocated = 0
        
        # 更新UI
        self.update_ui()
    
    def random_allocate_skill_points(self):
        """随机分配技能点"""
        if not self.parent.current_investigator or not self.parent.skills:
            return
        
        investigator = self.parent.current_investigator
        
        # 重置技能点
        self.reset_skill_points()
        
        # 获取职业技能
        occupation_skills = []
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation:
                occupation_skills = occupation.get("skills", [])
        
        # 随机分配职业技能点
        remaining_occupation_points = investigator.occupation_skill_points
        while remaining_occupation_points > 0 and occupation_skills:
            # 随机选择一个职业技能
            skill_name = self.parent.investigator_generator.dice_roller.random_choice(occupation_skills)
            skill = self.parent.skills.get_skill(skill_name)
            
            if not skill:
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_occupation_points, 20)
            points = self.parent.investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.occupation_skill_points_allocated += points
            remaining_occupation_points -= points
        
        # 随机分配兴趣技能点
        remaining_interest_points = investigator.interest_skill_points
        all_skills = list(self.parent.skills.skills.keys())
        while remaining_interest_points > 0 and all_skills:
            # 随机选择一个技能
            skill_name = self.parent.investigator_generator.dice_roller.random_choice(all_skills)
            
            # 跳过已经分配过的职业技能
            if skill_name in occupation_skills:
                all_skills.remove(skill_name)
                continue
            
            skill = self.parent.skills.get_skill(skill_name)
            
            if not skill:
                all_skills.remove(skill_name)
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_interest_points, 20)
            points = self.parent.investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.interest_skill_points_allocated += points
            remaining_interest_points -= points
            
            # 从列表中移除已分配的技能
            all_skills.remove(skill_name)
        
        # 更新UI
        self.update_ui()
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新技能点信息
        self.occupation_skill_points.setText(str(investigator.occupation_skill_points))
        self.allocated_occupation_skill_points.setText(str(investigator.occupation_skill_points_allocated))
        self.interest_skill_points.setText(str(investigator.interest_skill_points))
        self.allocated_interest_skill_points.setText(str(investigator.interest_skill_points_allocated))
        
        # 重新加载技能列表
        self.load_skills() 