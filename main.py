#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox

# 导入配置
from core.config import AppConfig

# 导入核心组件
from utils.dice import DiceRoller
from core.investigator import Investigator
from core.occupations import Occupations
from core.skills import Skills
from core.backgrounds import Backgrounds
from core.generator import InvestigatorGenerator

# 导入工具
from utils.file_handler import FileHandler

# 导入GUI组件
from gui.main_window import MainWindow

def show_error_message(title, message):
    """显示错误消息对话框"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()

def main():
    """主函数"""
    try:
        print("开始初始化应用程序...")
        
        # 确保数据目录存在
        os.makedirs("data", exist_ok=True)
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 显示一个消息框，确认程序已启动
        QMessageBox.information(None, "程序启动", "克苏鲁调查员生成器正在启动...")
        
        # 加载配置
        print("加载配置...")
        config = AppConfig()
        
        # 创建骰子工具
        print("创建骰子工具...")
        dice_roller = DiceRoller()
        
        # 加载职业数据
        print("加载职业数据...")
        occupations = Occupations()
        try:
            occupations.load_occupations("data/occupations.json")
        except Exception as e:
            print(f"加载职业数据失败: {e}")
            print("使用默认职业数据")
            occupations.occupations = occupations.get_all_occupations()
        
        # 加载技能数据
        print("加载技能数据...")
        skills = Skills()
        try:
            skills.load_skills("data/skills.json")
        except Exception as e:
            print(f"加载技能数据失败: {e}")
            print("使用默认技能数据")
            skills.skills = skills.get_all_skills()
        
        # 加载背景数据
        print("加载背景数据...")
        backgrounds = Backgrounds()
        try:
            backgrounds.load_backgrounds("data/backgrounds.json")
        except Exception as e:
            print(f"加载背景数据失败: {e}")
            print("使用默认背景数据")
            backgrounds.backgrounds = {}
        
        # 创建调查员生成器
        print("创建调查员生成器...")
        investigator_generator = InvestigatorGenerator(config, dice_roller, occupations, skills, backgrounds)
        
        # 创建文件处理器
        print("创建文件处理器...")
        file_handler = FileHandler()
        
        # 创建主窗口
        print("创建主窗口...")
        try:
            window = MainWindow(config, investigator_generator, occupations, skills, backgrounds, file_handler)
            print("主窗口创建成功，准备显示...")
            window.show()
            
            print("启动应用程序...")
            print("GUI应该现在显示。如果没有显示，请检查PyQt6安装是否正确。")
            
            # 显示一个消息框，确认程序正在运行
            QMessageBox.information(None, "程序启动", "克苏鲁调查员生成器已启动！")
            
            # 运行应用程序
            return app.exec()
        except Exception as e:
            error_msg = f"创建主窗口失败: {e}"
            print(error_msg)
            traceback.print_exc()
            show_error_message("错误", error_msg)
    except Exception as e:
        error_msg = f"发生错误: {e}"
        print(error_msg)
        traceback.print_exc()
        show_error_message("错误", error_msg)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 