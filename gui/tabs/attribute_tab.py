#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AttributeTab(QWidget):
    """属性标签页"""
    
    def __init__(self, parent):
        """初始化属性标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建基本信息组
        basic_info_group = QGroupBox("基本信息")
        basic_info_layout = QGridLayout(basic_info_group)
        
        # 添加基本信息字段
        basic_info_layout.addWidget(QLabel("姓名:"), 0, 0)
        self.name_edit = QLineEdit()
        basic_info_layout.addWidget(self.name_edit, 0, 1)
        
        basic_info_layout.addWidget(QLabel("玩家:"), 0, 2)
        self.player_edit = QLineEdit()
        basic_info_layout.addWidget(self.player_edit, 0, 3)
        
        basic_info_layout.addWidget(QLabel("性别:"), 1, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "男", "女"])
        basic_info_layout.addWidget(self.gender_combo, 1, 1)
        
        basic_info_layout.addWidget(QLabel("年龄:"), 1, 2)
        self.age_spin = QSpinBox()
        self.age_spin.setRange(15, 90)
        self.age_spin.setValue(30)
        basic_info_layout.addWidget(self.age_spin, 1, 3)
        
        basic_info_layout.addWidget(QLabel("居住地:"), 2, 0)
        self.residence_edit = QLineEdit()
        basic_info_layout.addWidget(self.residence_edit, 2, 1)
        
        basic_info_layout.addWidget(QLabel("出生地:"), 2, 2)
        self.birthplace_edit = QLineEdit()
        basic_info_layout.addWidget(self.birthplace_edit, 2, 3)
        
        # 添加基本信息组到主布局
        main_layout.addWidget(basic_info_group)
        
        # 创建属性组
        attributes_group = QGroupBox("属性")
        attributes_layout = QGridLayout(attributes_group)
        
        # 添加属性标题
        attributes_layout.addWidget(QLabel("属性"), 0, 0)
        attributes_layout.addWidget(QLabel("值"), 0, 1)
        attributes_layout.addWidget(QLabel("半值"), 0, 2)
        attributes_layout.addWidget(QLabel("五分之一值"), 0, 3)
        attributes_layout.addWidget(QLabel("操作"), 0, 4)
        
        # 创建属性控件
        self.attribute_widgets = {}
        
        row = 1
        for attr_name in ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]:
            # 属性名
            attributes_layout.addWidget(QLabel(attr_name), row, 0)
            
            # 属性值
            value_edit = QLineEdit()
            value_edit.setReadOnly(True)
            attributes_layout.addWidget(value_edit, row, 1)
            
            # 半值
            half_edit = QLineEdit()
            half_edit.setReadOnly(True)
            attributes_layout.addWidget(half_edit, row, 2)
            
            # 五分之一值
            fifth_edit = QLineEdit()
            fifth_edit.setReadOnly(True)
            attributes_layout.addWidget(fifth_edit, row, 3)
            
            # 掷骰按钮
            roll_button = QPushButton("掷骰")
            attributes_layout.addWidget(roll_button, row, 4)
            
            # 存储控件
            self.attribute_widgets[attr_name] = {
                "value": value_edit,
                "half": half_edit,
                "fifth": fifth_edit,
                "roll": roll_button
            }
            
            # 连接信号和槽
            roll_button.clicked.connect(lambda checked, name=attr_name: self.roll_attribute(name))
            
            row += 1
        
        # 添加属性组到主布局
        main_layout.addWidget(attributes_group)
        
        # 创建衍生属性组
        derived_group = QGroupBox("衍生属性")
        derived_layout = QGridLayout(derived_group)
        
        # 添加衍生属性
        derived_layout.addWidget(QLabel("生命值:"), 0, 0)
        self.hp_edit = QLineEdit()
        self.hp_edit.setReadOnly(True)
        derived_layout.addWidget(self.hp_edit, 0, 1)
        
        derived_layout.addWidget(QLabel("魔法值:"), 0, 2)
        self.mp_edit = QLineEdit()
        self.mp_edit.setReadOnly(True)
        derived_layout.addWidget(self.mp_edit, 0, 3)
        
        derived_layout.addWidget(QLabel("理智值:"), 1, 0)
        self.san_edit = QLineEdit()
        self.san_edit.setReadOnly(True)
        derived_layout.addWidget(self.san_edit, 1, 1)
        
        derived_layout.addWidget(QLabel("伤害加值:"), 1, 2)
        self.db_edit = QLineEdit()
        self.db_edit.setReadOnly(True)
        derived_layout.addWidget(self.db_edit, 1, 3)
        
        derived_layout.addWidget(QLabel("体格:"), 2, 0)
        self.build_edit = QLineEdit()
        self.build_edit.setReadOnly(True)
        derived_layout.addWidget(self.build_edit, 2, 1)
        
        derived_layout.addWidget(QLabel("移动速度:"), 2, 2)
        self.mov_edit = QLineEdit()
        self.mov_edit.setReadOnly(True)
        derived_layout.addWidget(self.mov_edit, 2, 3)
        
        # 添加衍生属性组到主布局
        main_layout.addWidget(derived_group)
        
        # 添加弹性空间
        main_layout.addStretch(1)
        
        # 连接信号和槽
        self.age_spin.valueChanged.connect(self.on_age_changed)
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新基本信息
        self.name_edit.setText(investigator.name)
        self.player_edit.setText(investigator.player)
        
        index = self.gender_combo.findText(investigator.gender)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)
        
        self.age_spin.setValue(investigator.age)
        self.residence_edit.setText(investigator.residence)
        self.birthplace_edit.setText(investigator.birthplace)
        
        # 更新属性
        for attr_name, widgets in self.attribute_widgets.items():
            value = investigator.attributes.get(attr_name, 0)
            half_value = investigator.attribute_half.get(attr_name, 0)
            fifth_value = investigator.attribute_fifth.get(attr_name, 0)
            
            widgets["value"].setText(str(value))
            widgets["half"].setText(str(half_value))
            widgets["fifth"].setText(str(fifth_value))
        
        # 更新衍生属性
        self.hp_edit.setText(str(investigator.hp))
        self.mp_edit.setText(str(investigator.mp))
        self.san_edit.setText(str(investigator.san))
        self.db_edit.setText(str(investigator.db))
        self.build_edit.setText(str(investigator.build))
        self.mov_edit.setText(str(investigator.mov))
    
    def update_investigator(self):
        """更新调查员数据"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新基本信息
        investigator.name = self.name_edit.text()
        investigator.player = self.player_edit.text()
        investigator.gender = self.gender_combo.currentText()
        investigator.age = self.age_spin.value()
        investigator.residence = self.residence_edit.text()
        investigator.birthplace = self.birthplace_edit.text()
    
    def roll_attribute(self, attr_name):
        """掷骰生成属性"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        config = self.parent.config
        
        # 获取属性配置
        attr_config = config.attributes.get(attr_name)
        if not attr_config:
            return
        
        # 掷骰生成属性值
        value = self.parent.investigator_generator.dice_roller.roll_attribute(
            attr_config["dice"], attr_config["multiplier"]
        )
        
        # 更新属性值
        investigator.attributes[attr_name] = value
        
        # 重新计算属性的半值和五分之一值
        investigator.calculate_half_fifth_values()
        
        # 重新计算衍生属性
        investigator.calculate_derived_attributes()
        
        # 更新UI
        self.update_ui()
    
    def on_age_changed(self, age):
        """年龄变化时的处理"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        investigator.age = age
        
        # 重新计算衍生属性
        investigator.calculate_derived_attributes()
        
        # 更新UI
        self.update_ui() 