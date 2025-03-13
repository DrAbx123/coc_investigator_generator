#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class EquipmentTab(QWidget):
    """装备标签页"""
    
    def __init__(self, parent):
        """初始化装备标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建财产和现金组
        assets_group = QGroupBox("财产和现金")
        assets_layout = QGridLayout(assets_group)
        
        # 添加现金
        assets_layout.addWidget(QLabel("现金:"), 0, 0)
        self.cash_edit = QLineEdit()
        assets_layout.addWidget(self.cash_edit, 0, 1)
        
        # 添加消费水平
        assets_layout.addWidget(QLabel("消费水平:"), 0, 2)
        self.spending_level = QLineEdit()
        self.spending_level.setReadOnly(True)
        assets_layout.addWidget(self.spending_level, 0, 3)
        
        # 添加资产
        assets_layout.addWidget(QLabel("资产:"), 1, 0)
        self.assets_edit = QTextEdit()
        assets_layout.addWidget(self.assets_edit, 1, 1, 1, 3)
        
        # 添加财产和现金组到主布局
        main_layout.addWidget(assets_group)
        
        # 创建装备组
        equipment_group = QGroupBox("装备")
        equipment_layout = QVBoxLayout(equipment_group)
        
        # 添加装备表格
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels(["名称", "数量", "伤害/效果", "射程/范围", "操作"])
        self.equipment_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.equipment_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.equipment_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.equipment_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.equipment_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        equipment_layout.addWidget(self.equipment_table)
        
        # 添加装备输入区域
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("名称:"), 0, 0)
        self.name_edit = QLineEdit()
        input_layout.addWidget(self.name_edit, 0, 1)
        
        input_layout.addWidget(QLabel("数量:"), 0, 2)
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 100)
        input_layout.addWidget(self.quantity_spin, 0, 3)
        
        input_layout.addWidget(QLabel("伤害/效果:"), 1, 0)
        self.damage_edit = QLineEdit()
        input_layout.addWidget(self.damage_edit, 1, 1)
        
        input_layout.addWidget(QLabel("射程/范围:"), 1, 2)
        self.range_edit = QLineEdit()
        input_layout.addWidget(self.range_edit, 1, 3)
        
        # 添加按钮
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("添加装备")
        button_layout.addWidget(self.add_button)
        
        self.clear_button = QPushButton("清空输入")
        button_layout.addWidget(self.clear_button)
        
        # 添加输入区域和按钮到装备布局
        equipment_layout.addLayout(input_layout)
        equipment_layout.addLayout(button_layout)
        
        # 添加装备组到主布局
        main_layout.addWidget(equipment_group)
        
        # 创建武器组
        weapons_group = QGroupBox("常用武器")
        weapons_layout = QVBoxLayout(weapons_group)
        
        # 添加武器列表
        self.weapons_list = QListWidget()
        weapons_layout.addWidget(self.weapons_list)
        
        # 添加武器组到主布局
        main_layout.addWidget(weapons_group)
        
        # 添加弹性空间
        main_layout.addStretch(1)
        
        # 连接信号和槽
        self.add_button.clicked.connect(self.add_equipment)
        self.clear_button.clicked.connect(self.clear_input)
        self.cash_edit.textChanged.connect(self.update_spending_level)
    
    def add_equipment(self):
        """添加装备"""
        name = self.name_edit.text().strip()
        quantity = self.quantity_spin.value()
        damage = self.damage_edit.text().strip()
        range_value = self.range_edit.text().strip()
        
        if not name:
            self.parent.show_message("请输入装备名称")
            return
        
        # 添加到表格
        row = self.equipment_table.rowCount()
        self.equipment_table.insertRow(row)
        
        # 设置表格项
        self.equipment_table.setItem(row, 0, QTableWidgetItem(name))
        self.equipment_table.setItem(row, 1, QTableWidgetItem(str(quantity)))
        self.equipment_table.setItem(row, 2, QTableWidgetItem(damage))
        self.equipment_table.setItem(row, 3, QTableWidgetItem(range_value))
        
        # 添加删除按钮
        delete_button = QPushButton("删除")
        delete_button.clicked.connect(lambda: self.delete_equipment(row))
        self.equipment_table.setCellWidget(row, 4, delete_button)
        
        # 如果是武器，添加到武器列表
        if damage:
            self.weapons_list.addItem(f"{name} - {damage}")
        
        # 清空输入
        self.clear_input()
        
        # 更新调查员数据
        self.update_investigator()
    
    def delete_equipment(self, row):
        """删除装备"""
        # 获取装备名称
        name = self.equipment_table.item(row, 0).text()
        
        # 从表格中删除
        self.equipment_table.removeRow(row)
        
        # 从武器列表中删除
        for i in range(self.weapons_list.count()):
            if self.weapons_list.item(i).text().startswith(name):
                self.weapons_list.takeItem(i)
                break
        
        # 更新调查员数据
        self.update_investigator()
    
    def clear_input(self):
        """清空输入"""
        self.name_edit.clear()
        self.quantity_spin.setValue(1)
        self.damage_edit.clear()
        self.range_edit.clear()
    
    def update_spending_level(self):
        """更新消费水平"""
        try:
            cash = float(self.cash_edit.text())
            
            # 根据现金确定消费水平
            if cash < 10:
                level = "贫穷"
            elif cash < 50:
                level = "标准"
            elif cash < 100:
                level = "小康"
            elif cash < 500:
                level = "富裕"
            else:
                level = "富豪"
            
            self.spending_level.setText(level)
            
            # 更新调查员数据
            self.update_investigator()
            
        except ValueError:
            self.spending_level.setText("")
    
    def update_investigator(self):
        """更新调查员数据"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新现金和资产
        try:
            investigator.cash = float(self.cash_edit.text())
        except ValueError:
            investigator.cash = 0
        
        investigator.assets = self.assets_edit.toPlainText()
        
        # 更新装备
        investigator.equipment = []
        for row in range(self.equipment_table.rowCount()):
            name = self.equipment_table.item(row, 0).text()
            quantity = self.equipment_table.item(row, 1).text()
            damage = self.equipment_table.item(row, 2).text()
            range_value = self.equipment_table.item(row, 3).text()
            
            equipment = {
                "name": name,
                "quantity": quantity,
                "damage": damage,
                "range": range_value
            }
            
            investigator.equipment.append(equipment)
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新现金和资产
        self.cash_edit.setText(str(investigator.cash))
        self.assets_edit.setText(investigator.assets)
        
        # 更新装备表格
        self.equipment_table.setRowCount(0)
        self.weapons_list.clear()
        
        for equipment in investigator.equipment:
            row = self.equipment_table.rowCount()
            self.equipment_table.insertRow(row)
            
            self.equipment_table.setItem(row, 0, QTableWidgetItem(equipment["name"]))
            self.equipment_table.setItem(row, 1, QTableWidgetItem(equipment["quantity"]))
            self.equipment_table.setItem(row, 2, QTableWidgetItem(equipment["damage"]))
            self.equipment_table.setItem(row, 3, QTableWidgetItem(equipment["range"]))
            
            # 添加删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(lambda checked, r=row: self.delete_equipment(r))
            self.equipment_table.setCellWidget(row, 4, delete_button)
            
            # 如果是武器，添加到武器列表
            if equipment["damage"]:
                self.weapons_list.addItem(f"{equipment['name']} - {equipment['damage']}")
        
        # 更新消费水平
        self.update_spending_level() 