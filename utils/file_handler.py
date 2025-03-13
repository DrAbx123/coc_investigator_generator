#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from core.investigator import Investigator

class FileHandler:
    """文件处理工具类"""
    
    @staticmethod
    def save_investigator(investigator, file_path):
        """
        保存调查员数据到文件
        
        参数:
            investigator (Investigator): 调查员对象
            file_path (str): 文件路径
            
        返回:
            bool: 是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 将调查员对象转换为字典
            data = investigator.to_dict()
            
            # 将字典保存为JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            return True
        except Exception as e:
            print(f"保存调查员数据失败: {e}")
            return False
    
    @staticmethod
    def load_investigator(file_path):
        """
        从文件加载调查员数据
        
        参数:
            file_path (str): 文件路径
            
        返回:
            Investigator: 调查员对象，如果加载失败则返回None
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                return None
            
            # 从JSON文件加载字典
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 将字典转换为调查员对象
            investigator = Investigator.from_dict(data)
            
            return investigator
        except Exception as e:
            print(f"加载调查员数据失败: {e}")
            return None
    
    @staticmethod
    def get_investigator_files(directory):
        """
        获取目录中的所有调查员文件
        
        参数:
            directory (str): 目录路径
            
        返回:
            list: 调查员文件路径列表
        """
        try:
            # 确保目录存在
            os.makedirs(directory, exist_ok=True)
            
            # 获取目录中的所有JSON文件
            files = []
            for file_name in os.listdir(directory):
                if file_name.endswith('.json'):
                    files.append(os.path.join(directory, file_name))
                    
            return files
        except Exception as e:
            print(f"获取调查员文件失败: {e}")
            return []
    
    @staticmethod
    def export_investigator_to_text(investigator, file_path):
        """
        将调查员数据导出为文本文件
        
        参数:
            investigator (Investigator): 调查员对象
            file_path (str): 文件路径
            
        返回:
            bool: 是否导出成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 生成文本内容
            content = []
            
            # 基本信息
            content.append("=== 基本信息 ===")
            content.append(f"姓名: {investigator.name}")
            content.append(f"玩家: {investigator.player}")
            content.append(f"职业: {investigator.occupation}")
            content.append(f"年龄: {investigator.age}")
            content.append(f"性别: {investigator.gender}")
            content.append(f"居住地: {investigator.residence}")
            content.append(f"出生地: {investigator.birthplace}")
            content.append("")
            
            # 属性
            content.append("=== 属性 ===")
            for attr_name, attr_value in investigator.attributes.items():
                half_value = investigator.attribute_half.get(attr_name, 0)
                fifth_value = investigator.attribute_fifth.get(attr_name, 0)
                content.append(f"{attr_name}: {attr_value} (半值: {half_value}, 五分之一值: {fifth_value})")
            content.append("")
            
            # 衍生属性
            content.append("=== 衍生属性 ===")
            content.append(f"生命值: {investigator.hp}")
            content.append(f"魔法值: {investigator.mp}")
            content.append(f"理智值: {investigator.san}")
            content.append(f"伤害加值: {investigator.db}")
            content.append(f"体格: {investigator.build}")
            content.append(f"移动速度: {investigator.mov}")
            content.append("")
            
            # 技能
            content.append("=== 技能 ===")
            content.append("职业技能:")
            for skill in investigator.occupation_skills:
                content.append(f"- {skill}")
            content.append(f"职业技能点: {investigator.occupation_skill_points}")
            content.append(f"兴趣技能点: {investigator.interest_skill_points}")
            content.append("")
            
            if investigator.skills:
                content.append("已分配技能:")
                for skill_name, skill_value in investigator.skills.items():
                    content.append(f"{skill_name}: {skill_value}")
                content.append("")
            
            # 背景
            content.append("=== 背景 ===")
            content.append(f"形象描述: {investigator.personal_description}")
            content.append(f"思想/信念: {investigator.ideology_beliefs}")
            content.append(f"重要之人: {investigator.significant_people}")
            content.append(f"意义非凡之地: {investigator.meaningful_locations}")
            content.append(f"宝贵之物: {investigator.treasured_possessions}")
            content.append(f"特质: {investigator.traits}")
            content.append("")
            
            # 装备和资产
            content.append("=== 装备和资产 ===")
            content.append(f"现金: {investigator.cash}")
            content.append(f"资产: {investigator.assets}")
            content.append(f"消费水平: {investigator.spending_level}")
            
            if investigator.items:
                content.append("物品:")
                for item in investigator.items:
                    content.append(f"- {item}")
            
            if investigator.weapons:
                content.append("武器:")
                for weapon in investigator.weapons:
                    content.append(f"- {weapon}")
            
            # 将内容写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
                
            return True
        except Exception as e:
            print(f"导出调查员数据失败: {e}")
            return False 