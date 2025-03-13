#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AppConfig:
    """应用程序配置类"""
    
    def __init__(self):
        """初始化配置"""
        # 应用程序名称
        self.app_name = "克苏鲁的呼唤 - 调查员生成器"
        
        # 应用程序版本
        self.app_version = "1.0.0"
        
        # 默认窗口大小
        self.window_width = 1024
        self.window_height = 768
        
        # 属性相关配置
        self.attributes = {
            "力量": {"dice": "3D6", "multiplier": 5},
            "体质": {"dice": "3D6", "multiplier": 5},
            "体型": {"dice": "2D6+6", "multiplier": 5},
            "敏捷": {"dice": "3D6", "multiplier": 5},
            "外貌": {"dice": "3D6", "multiplier": 5},
            "智力": {"dice": "2D6+6", "multiplier": 5},
            "意志": {"dice": "3D6", "multiplier": 5},
            "教育": {"dice": "2D6+6", "multiplier": 5},
            "幸运": {"dice": "3D6", "multiplier": 5}
        }
        
        # 年龄段配置
        self.age_groups = {
            "15-19": {
                "str_siz_reduction": 5,
                "edu_reduction": 5,
                "luck_rolls": 2,
                "edu_improvement_checks": 0,
                "app_reduction": 0,
                "str_con_dex_reduction": 0
            },
            "20-39": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 1,
                "app_reduction": 0,
                "str_con_dex_reduction": 0
            },
            "40-49": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 2,
                "app_reduction": 5,
                "str_con_dex_reduction": 5
            },
            "50-59": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 3,
                "app_reduction": 10,
                "str_con_dex_reduction": 10
            },
            "60-69": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 4,
                "app_reduction": 15,
                "str_con_dex_reduction": 20
            },
            "70-79": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 4,
                "app_reduction": 20,
                "str_con_dex_reduction": 40
            },
            "80-89": {
                "str_siz_reduction": 0,
                "edu_reduction": 0,
                "luck_rolls": 1,
                "edu_improvement_checks": 4,
                "app_reduction": 25,
                "str_con_dex_reduction": 80
            }
        } 