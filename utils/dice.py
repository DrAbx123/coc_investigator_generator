#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random

class DiceRoller:
    """骰子工具类，用于模拟掷骰子"""
    
    @staticmethod
    def roll(dice_str):
        """
        根据骰子表达式掷骰子
        
        参数:
            dice_str (str): 骰子表达式，如 "3D6", "2D6+6", "D100"
            
        返回:
            int: 骰子结果
        """
        # 将表达式转换为小写
        dice_str = dice_str.upper()
        
        # 匹配骰子表达式
        pattern = r"(\d+)?D(\d+)([+-]\d+)?"
        match = re.match(pattern, dice_str)
        
        if not match:
            raise ValueError(f"无效的骰子表达式: {dice_str}")
        
        # 解析骰子数量、面数和修正值
        num_dice = int(match.group(1) or 1)
        num_faces = int(match.group(2))
        modifier = int(match.group(3) or 0) if match.group(3) else 0
        
        # 掷骰子
        result = sum(random.randint(1, num_faces) for _ in range(num_dice)) + modifier
        
        return result
    
    @staticmethod
    def roll_multiple(dice_str, times=1):
        """
        多次掷骰子
        
        参数:
            dice_str (str): 骰子表达式
            times (int): 掷骰子次数
            
        返回:
            list: 骰子结果列表
        """
        return [DiceRoller.roll(dice_str) for _ in range(times)]
    
    @staticmethod
    def roll_attribute(dice_str, multiplier=5):
        """
        掷属性骰子
        
        参数:
            dice_str (str): 骰子表达式
            multiplier (int): 乘数
            
        返回:
            int: 属性值
        """
        result = DiceRoller.roll(dice_str)
        return result * multiplier
    
    @staticmethod
    def roll_d100():
        """
        掷百分骰（D100）
        
        返回:
            int: 1-100之间的随机数
        """
        return random.randint(1, 100)
    
    @staticmethod
    def roll_between(min_value, max_value):
        """
        在指定范围内掷骰子
        
        参数:
            min_value (int): 最小值
            max_value (int): 最大值
            
        返回:
            int: 范围内的随机数
        """
        return random.randint(min_value, max_value)
    
    @staticmethod
    def random_choice(items):
        """
        从列表中随机选择一项
        
        参数:
            items (list): 选项列表
            
        返回:
            任意类型: 随机选择的项
        """
        return random.choice(items) 