#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class BackgroundTab(QWidget):
    """背景标签页"""
    
    def __init__(self, parent):
        """初始化背景标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建背景信息组
        background_group = QGroupBox("背景信息")
        background_layout = QVBoxLayout(background_group)
        
        # 添加个人描述
        background_layout.addWidget(QLabel("个人描述:"))
        self.personal_description = QTextEdit()
        background_layout.addWidget(self.personal_description)
        
        # 添加思想信念
        background_layout.addWidget(QLabel("思想信念:"))
        self.ideology = QTextEdit()
        background_layout.addWidget(self.ideology)
        
        # 添加重要之人
        background_layout.addWidget(QLabel("重要之人:"))
        self.significant_people = QTextEdit()
        background_layout.addWidget(self.significant_people)
        
        # 添加意义非凡之地
        background_layout.addWidget(QLabel("意义非凡之地:"))
        self.meaningful_locations = QTextEdit()
        background_layout.addWidget(self.meaningful_locations)
        
        # 添加宝贵之物
        background_layout.addWidget(QLabel("宝贵之物:"))
        self.treasured_possessions = QTextEdit()
        background_layout.addWidget(self.treasured_possessions)
        
        # 添加特质
        background_layout.addWidget(QLabel("特质:"))
        self.traits = QTextEdit()
        background_layout.addWidget(self.traits)
        
        # 添加创伤和疯狂
        background_layout.addWidget(QLabel("创伤和疯狂:"))
        self.injuries_scars = QTextEdit()
        background_layout.addWidget(self.injuries_scars)
        
        # 添加恐惧和狂热
        background_layout.addWidget(QLabel("恐惧和狂热:"))
        self.phobias_manias = QTextEdit()
        background_layout.addWidget(self.phobias_manias)
        
        # 添加奥秘和邪教
        background_layout.addWidget(QLabel("奥秘和邪教:"))
        self.arcane_tomes_spells = QTextEdit()
        background_layout.addWidget(self.arcane_tomes_spells)
        
        # 添加背景故事
        background_layout.addWidget(QLabel("背景故事:"))
        self.background_story = QTextEdit()
        background_layout.addWidget(self.background_story)
        
        # 添加背景信息组到主布局
        main_layout.addWidget(background_group)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        # 添加随机生成按钮
        self.random_button = QPushButton("随机生成背景")
        button_layout.addWidget(self.random_button)
        
        # 添加保存按钮
        self.save_button = QPushButton("保存背景")
        button_layout.addWidget(self.save_button)
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
        
        # 连接信号和槽
        self.random_button.clicked.connect(self.generate_random_background)
        self.save_button.clicked.connect(lambda: self.save_background(show_message=True))
        
        # 连接文本编辑器的文本变化信号
        self.personal_description.textChanged.connect(self.on_text_changed)
        self.ideology.textChanged.connect(self.on_text_changed)
        self.significant_people.textChanged.connect(self.on_text_changed)
        self.meaningful_locations.textChanged.connect(self.on_text_changed)
        self.treasured_possessions.textChanged.connect(self.on_text_changed)
        self.traits.textChanged.connect(self.on_text_changed)
        self.injuries_scars.textChanged.connect(self.on_text_changed)
        self.phobias_manias.textChanged.connect(self.on_text_changed)
        self.arcane_tomes_spells.textChanged.connect(self.on_text_changed)
        self.background_story.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self):
        """文本变化时的处理"""
        # 这里可以添加一些处理逻辑，比如标记为已修改等
        pass
    
    def generate_random_background(self):
        """随机生成背景"""
        if not self.parent.current_investigator or not self.parent.backgrounds:
            return
        
        investigator = self.parent.current_investigator
        
        # 获取随机背景
        background = self.parent.backgrounds.get_random_background(
            self.parent.investigator_generator.dice_roller
        )
        
        if not background:
            return
        
        # 更新调查员的背景
        investigator.personal_description = background.personal_description
        investigator.ideology = background.ideology
        investigator.significant_people = background.significant_people
        investigator.meaningful_locations = background.meaningful_locations
        investigator.treasured_possessions = background.treasured_possessions
        investigator.traits = background.traits
        investigator.injuries_scars = background.injuries_scars
        investigator.phobias_manias = background.phobias_manias
        investigator.arcane_tomes_spells = background.arcane_tomes_spells
        investigator.background_story = background.background_story
        
        # 更新UI
        self.update_ui()
    
    def save_background(self, show_message=False):
        """保存背景信息
        
        Args:
            show_message (bool): 是否显示保存成功的消息，默认为False
        """
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新调查员的背景
        investigator.personal_description = self.personal_description.toPlainText()
        investigator.ideology = self.ideology.toPlainText()
        investigator.significant_people = self.significant_people.toPlainText()
        investigator.meaningful_locations = self.meaningful_locations.toPlainText()
        investigator.treasured_possessions = self.treasured_possessions.toPlainText()
        investigator.traits = self.traits.toPlainText()
        investigator.injuries_scars = self.injuries_scars.toPlainText()
        investigator.phobias_manias = self.phobias_manias.toPlainText()
        investigator.arcane_tomes_spells = self.arcane_tomes_spells.toPlainText()
        investigator.background_story = self.background_story.toPlainText()
        
        # 只有在指定时才显示保存成功消息
        if show_message:
            self.parent.show_message("背景信息已保存")
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新背景信息
        self.personal_description.setText(investigator.personal_description)
        self.ideology.setText(investigator.ideology)
        self.significant_people.setText(investigator.significant_people)
        self.meaningful_locations.setText(investigator.meaningful_locations)
        self.treasured_possessions.setText(investigator.treasured_possessions)
        self.traits.setText(investigator.traits)
        self.injuries_scars.setText(investigator.injuries_scars)
        self.phobias_manias.setText(investigator.phobias_manias)
        self.arcane_tomes_spells.setText(investigator.arcane_tomes_spells)
        self.background_story.setText(investigator.background_story) 