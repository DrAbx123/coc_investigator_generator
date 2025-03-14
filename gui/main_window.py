#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui.tabs.attribute_tab import AttributeTab
from gui.tabs.occupation_tab import OccupationTab
from gui.tabs.skills_tab import SkillsTab
from gui.tabs.background_tab import BackgroundTab
from gui.tabs.equipment_tab import EquipmentTab
from gui.tabs.summary_tab import SummaryTab

from core.generator import InvestigatorGenerator
from utils.file_handler import FileHandler

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, config, investigator_generator, occupations, skills, backgrounds, file_handler):
        """初始化主窗口"""
        super().__init__()
        
        self.config = config
        self.investigator_generator = investigator_generator
        self.occupations = occupations
        self.skills = skills
        self.backgrounds = backgrounds
        self.file_handler = file_handler
        
        self.current_investigator = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 设置窗口标题和大小
        self.setWindowTitle(self.config.app_name)
        self.resize(self.config.window_width, self.config.window_height)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标题标签
        title_label = QLabel(self.config.app_name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.new_button = QPushButton("新建调查员")
        self.random_button = QPushButton("随机生成")
        self.save_button = QPushButton("保存")
        self.load_button = QPushButton("加载")
        self.export_button = QPushButton("导出为文本")
        
        # 添加按钮到布局
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.random_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.export_button)
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 创建各个标签页
        self.attribute_tab = AttributeTab(self)
        self.occupation_tab = OccupationTab(self)
        self.skills_tab = SkillsTab(self)
        self.background_tab = BackgroundTab(self)
        self.equipment_tab = EquipmentTab(self)
        self.summary_tab = SummaryTab(self)
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(self.attribute_tab, "属性")
        self.tab_widget.addTab(self.occupation_tab, "职业")
        self.tab_widget.addTab(self.skills_tab, "技能")
        self.tab_widget.addTab(self.background_tab, "背景")
        self.tab_widget.addTab(self.equipment_tab, "装备")
        self.tab_widget.addTab(self.summary_tab, "摘要")
        
        # 添加标签页控件到主布局
        main_layout.addWidget(self.tab_widget)
        
        # 连接信号和槽
        self.new_button.clicked.connect(self.create_new_investigator)
        self.random_button.clicked.connect(self.generate_random_investigator)
        self.save_button.clicked.connect(self.save_investigator)
        self.load_button.clicked.connect(self.load_investigator)
        self.export_button.clicked.connect(self.export_investigator_to_text)
        
        # 标签页切换时更新数据
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # 创建一个新的调查员
        self.create_new_investigator()
    
    def create_new_investigator(self):
        """创建新的调查员"""
        # 创建一个空的调查员
        self.current_investigator = self.investigator_generator.create_empty_investigator()
        
        # 更新所有标签页
        self.update_all_tabs()
        
        # 切换到属性标签页
        self.tab_widget.setCurrentIndex(0)
    
    def generate_random_investigator(self):
        """随机生成调查员"""
        # 生成随机调查员
        self.current_investigator = self.investigator_generator.generate_random_investigator()
        
        # 更新所有标签页
        self.update_all_tabs()
        
        # 切换到摘要标签页
        self.tab_widget.setCurrentIndex(5)
    
    def save_investigator(self):
        """保存调查员"""
        if not self.current_investigator:
            self.show_message("没有调查员可保存")
            return
        
        # 在保存前先更新所有标签页的数据
        self.update_investigator_from_tabs()
        
        # 获取保存路径，如果已有文件路径则使用
        if hasattr(self.current_investigator, 'file_path') and self.current_investigator.file_path:
            file_path = self.current_investigator.file_path
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存调查员", "", "JSON文件 (*.json)"
            )
        
        if not file_path:
            return
        
        # 保存调查员，并记录文件路径
        success = self.file_handler.save_investigator(self.current_investigator, file_path)
        
        if success:
            self.current_investigator.file_path = file_path
            self.show_message(f"调查员已保存到: {file_path}")
        else:
            self.show_message("保存调查员失败")
    
    def load_investigator(self):
        """加载调查员"""
        # 获取加载路径
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载调查员", "", "JSON文件 (*.json)"
        )
        
        if not file_path:
            return
        
        # 加载调查员
        investigator = self.file_handler.load_investigator(file_path)
        
        if investigator:
            self.current_investigator = investigator
            # 保存文件路径到调查员对象
            self.current_investigator.file_path = file_path
            self.update_all_tabs()
            self.tab_widget.setCurrentIndex(5)  # 切换到摘要标签页
            self.show_message(f"调查员已加载: {file_path}")
        else:
            self.show_message("加载调查员失败")
    
    def export_investigator_to_text(self):
        """导出调查员为文本"""
        if not self.current_investigator:
            self.show_message("没有调查员可导出")
            return
        
        # 在导出前先更新所有标签页的数据
        self.update_investigator_from_tabs()
        
        # 获取导出路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出调查员为文本", "", "文本文件 (*.txt)"
        )
        
        if not file_path:
            return
        
        # 导出调查员
        success = self.file_handler.export_investigator_to_text(self.current_investigator, file_path)
        
        if success:
            self.show_message(f"调查员已导出到: {file_path}")
        else:
            self.show_message("导出调查员失败")
    
    def on_tab_changed(self, index):
        """标签页切换时的处理"""
        # 更新当前标签页
        current_tab = self.tab_widget.widget(index)
        if hasattr(current_tab, "update_ui"):
            current_tab.update_ui()
        
        # 保存调查员数据
        self.update_investigator_from_tabs()
    
    def update_investigator_from_tabs(self):
        """从标签页更新调查员数据"""
        if not self.current_investigator:
            return
        
        # 更新属性标签页数据
        if hasattr(self.attribute_tab, "update_investigator"):
            self.attribute_tab.update_investigator()
        
        # 更新职业标签页数据
        if hasattr(self.occupation_tab, "update_investigator"):
            self.occupation_tab.update_investigator()
        
        # 更新技能标签页数据
        if hasattr(self.skills_tab, "update_investigator"):
            self.skills_tab.update_investigator()
        
        # 更新背景标签页数据
        if hasattr(self.background_tab, "save_background"):
            self.background_tab.save_background(show_message=False)
        
        # 更新装备标签页数据
        if hasattr(self.equipment_tab, "update_investigator"):
            self.equipment_tab.update_investigator()
    
    def update_all_tabs(self):
        """更新所有标签页"""
        # 更新属性标签页
        if hasattr(self.attribute_tab, "update_ui"):
            self.attribute_tab.update_ui()
        
        # 更新职业标签页
        if hasattr(self.occupation_tab, "update_ui"):
            self.occupation_tab.update_ui()
        
        # 更新技能标签页
        if hasattr(self.skills_tab, "update_ui"):
            self.skills_tab.update_ui()
        
        # 更新背景标签页
        if hasattr(self.background_tab, "update_ui"):
            self.background_tab.update_ui()
        
        # 更新装备标签页
        if hasattr(self.equipment_tab, "update_ui"):
            self.equipment_tab.update_ui()
        
        # 更新摘要标签页
        if hasattr(self.summary_tab, "update_ui"):
            self.summary_tab.update_ui()
    
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        if self.current_investigator:
            # 更新并保存当前调查员数据
            self.update_investigator_from_tabs()
            
            # 如果文件名已经存在，直接保存
            if hasattr(self.current_investigator, 'file_path') and self.current_investigator.file_path:
                self.file_handler.save_investigator(self.current_investigator, self.current_investigator.file_path)
            else:
                # 询问用户是否保存
                reply = QMessageBox.question(
                    self, '保存调查员', 
                    '是否在退出前保存当前调查员?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # 获取保存路径
                    file_path, _ = QFileDialog.getSaveFileName(
                        self, "保存调查员", "", "JSON文件 (*.json)"
                    )
                    
                    if file_path:
                        self.file_handler.save_investigator(self.current_investigator, file_path)
                    else:
                        # 用户取消保存，但允许关闭窗口
                        pass
                elif reply == QMessageBox.StandardButton.Cancel:
                    # 用户不想关闭窗口
                    event.ignore()
                    return
        
        # 接受关闭事件
        event.accept()
    
    def show_message(self, message):
        """显示消息"""
        QMessageBox.information(self, "提示", message) 