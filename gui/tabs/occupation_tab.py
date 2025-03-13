#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class OccupationTab(QWidget):
    """职业标签页"""
    
    def __init__(self, parent):
        """初始化职业标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建水平布局
        h_layout = QHBoxLayout()
        
        # 创建职业列表组
        occupation_list_group = QGroupBox("职业列表")
        occupation_list_layout = QVBoxLayout(occupation_list_group)
        
        # 添加搜索框
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入职业名称搜索...")
        search_layout.addWidget(self.search_edit)
        occupation_list_layout.addLayout(search_layout)
        
        # 添加职业列表
        self.occupation_list = QListWidget()
        occupation_list_layout.addWidget(self.occupation_list)
        
        # 添加职业列表组到水平布局
        h_layout.addWidget(occupation_list_group, 1)
        
        # 创建职业详情组
        occupation_detail_group = QGroupBox("职业详情")
        occupation_detail_layout = QVBoxLayout(occupation_detail_group)
        
        # 添加职业名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("职业名称:"))
        self.occupation_name = QLineEdit()
        self.occupation_name.setReadOnly(True)
        name_layout.addWidget(self.occupation_name)
        occupation_detail_layout.addLayout(name_layout)
        
        # 添加信用评级
        credit_layout = QHBoxLayout()
        credit_layout.addWidget(QLabel("信用评级:"))
        self.credit_rating = QLineEdit()
        self.credit_rating.setReadOnly(True)
        credit_layout.addWidget(self.credit_rating)
        occupation_detail_layout.addLayout(credit_layout)
        
        # 添加职业技能点
        skill_points_layout = QHBoxLayout()
        skill_points_layout.addWidget(QLabel("职业技能点:"))
        self.skill_points = QLineEdit()
        self.skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.skill_points)
        occupation_detail_layout.addLayout(skill_points_layout)
        
        # 添加职业描述
        occupation_detail_layout.addWidget(QLabel("职业描述:"))
        self.occupation_description = QTextEdit()
        self.occupation_description.setReadOnly(True)
        occupation_detail_layout.addWidget(self.occupation_description)
        
        # 添加职业技能
        occupation_detail_layout.addWidget(QLabel("职业技能:"))
        self.occupation_skills = QTextEdit()
        self.occupation_skills.setReadOnly(True)
        occupation_detail_layout.addWidget(self.occupation_skills)
        
        # 添加选择按钮
        self.select_button = QPushButton("选择此职业")
        occupation_detail_layout.addWidget(self.select_button)
        
        # 添加职业详情组到水平布局
        h_layout.addWidget(occupation_detail_group, 2)
        
        # 添加水平布局到主布局
        main_layout.addLayout(h_layout)
        
        # 添加当前选择的职业组
        current_occupation_group = QGroupBox("当前选择的职业")
        current_occupation_layout = QGridLayout(current_occupation_group)
        
        # 添加当前职业信息
        current_occupation_layout.addWidget(QLabel("职业:"), 0, 0)
        self.current_occupation_name = QLineEdit()
        self.current_occupation_name.setReadOnly(True)
        current_occupation_layout.addWidget(self.current_occupation_name, 0, 1)
        
        current_occupation_layout.addWidget(QLabel("信用评级:"), 0, 2)
        self.current_credit_rating = QLineEdit()
        self.current_credit_rating.setReadOnly(True)
        current_occupation_layout.addWidget(self.current_credit_rating, 0, 3)
        
        current_occupation_layout.addWidget(QLabel("职业技能点:"), 1, 0)
        self.current_skill_points = QLineEdit()
        self.current_skill_points.setReadOnly(True)
        current_occupation_layout.addWidget(self.current_skill_points, 1, 1)
        
        current_occupation_layout.addWidget(QLabel("已分配技能点:"), 1, 2)
        self.allocated_skill_points = QLineEdit()
        self.allocated_skill_points.setReadOnly(True)
        current_occupation_layout.addWidget(self.allocated_skill_points, 1, 3)
        
        # 添加当前职业组到主布局
        main_layout.addWidget(current_occupation_group)
        
        # 添加弹性空间
        main_layout.addStretch(1)
        
        # 连接信号和槽
        self.search_edit.textChanged.connect(self.filter_occupations)
        self.occupation_list.itemClicked.connect(self.show_occupation_details)
        self.select_button.clicked.connect(self.select_occupation)
    
    def load_occupations(self):
        """加载职业列表"""
        if not self.parent.occupations:
            return
        
        # 清空列表
        self.occupation_list.clear()
        
        # 添加职业到列表
        for occupation_name in sorted(self.parent.occupations.occupations.keys()):
            self.occupation_list.addItem(occupation_name)
    
    def filter_occupations(self, text):
        """根据搜索文本过滤职业列表"""
        if not self.parent.occupations:
            return
        
        # 清空列表
        self.occupation_list.clear()
        
        # 添加匹配的职业到列表
        for occupation_name in sorted(self.parent.occupations.occupations.keys()):
            if text.lower() in occupation_name.lower():
                self.occupation_list.addItem(occupation_name)
    
    def show_occupation_details(self, item):
        """显示职业详情"""
        if not self.parent.occupations:
            return
        
        occupation_name = item.text()
        occupation = self.parent.occupations.get_occupation(occupation_name)
        
        if not occupation:
            return
        
        # 更新职业详情
        self.occupation_name.setText(occupation_name)
        self.credit_rating.setText(f"{occupation.get('credit_rating_min', 0)}-{occupation.get('credit_rating_max', 0)}")
        
        # 计算技能点
        if self.parent.current_investigator:
            edu = self.parent.current_investigator.attributes.get("教育", 0)
            skill_points = self.parent.occupations.calculate_skill_points(occupation_name, edu)
            self.skill_points.setText(str(skill_points))
        else:
            self.skill_points.setText("需要先设置教育属性")
        
        # 更新职业描述
        self.occupation_description.setText(occupation.get("description", ""))
        
        # 更新职业技能
        skills_text = "\n".join(occupation.get("skills", []))
        self.occupation_skills.setText(skills_text)
    
    def select_occupation(self):
        """选择当前显示的职业"""
        if not self.parent.current_investigator or not self.occupation_name.text():
            return
        
        occupation_name = self.occupation_name.text()
        occupation = self.parent.occupations.get_occupation(occupation_name)
        
        if not occupation:
            return
        
        # 更新调查员的职业
        investigator = self.parent.current_investigator
        investigator.occupation = occupation_name
        
        # 计算技能点
        edu = investigator.attributes.get("教育", 0)
        skill_points = self.parent.occupations.calculate_skill_points(occupation_name, edu)
        investigator.occupation_skill_points = skill_points
        investigator.occupation_skill_points_allocated = 0
        
        # 更新UI
        self.update_ui()
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新当前职业信息
        self.current_occupation_name.setText(investigator.occupation)
        
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation:
                self.current_credit_rating.setText(f"{occupation.get('credit_rating_min', 0)}-{occupation.get('credit_rating_max', 0)}")
        else:
            self.current_credit_rating.setText("")
        
        # 更新技能点信息
        self.current_skill_points.setText(str(investigator.occupation_skill_points))
        self.allocated_skill_points.setText(str(investigator.occupation_skill_points_allocated))
        
        # 加载职业列表（如果尚未加载）
        if self.occupation_list.count() == 0:
            self.load_occupations() 