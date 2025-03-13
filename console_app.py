#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

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

def print_menu():
    """打印菜单"""
    print("\n===== 克苏鲁的呼唤 - 调查员生成器 =====")
    print("1. 随机生成调查员")
    print("2. 自定义调查员")
    print("3. 保存调查员")
    print("4. 加载调查员")
    print("5. 导出调查员为文本")
    print("6. 退出")
    print("=====================================")
    return input("请选择操作 (1-6): ")

def print_investigator(investigator):
    """打印调查员信息"""
    print("\n===== 调查员信息 =====")
    print(f"姓名: {investigator.name}")
    print(f"玩家: {investigator.player}")
    print(f"职业: {investigator.occupation}")
    print(f"年龄: {investigator.age}")
    print(f"性别: {investigator.gender}")
    print(f"居住地: {investigator.residence}")
    print(f"出生地: {investigator.birthplace}")
    
    print("\n----- 属性 -----")
    for attr_name, attr_value in investigator.attributes.items():
        half_value = investigator.attribute_half.get(attr_name, 0)
        fifth_value = investigator.attribute_fifth.get(attr_name, 0)
        print(f"{attr_name}: {attr_value} (半值: {half_value}, 五分之一值: {fifth_value})")
    
    print("\n----- 衍生属性 -----")
    print(f"生命值: {investigator.hp}")
    print(f"魔法值: {investigator.mp}")
    print(f"理智值: {investigator.san}")
    print(f"伤害加值: {investigator.db}")
    print(f"体格: {investigator.build}")
    print(f"移动速度: {investigator.mov}")
    
    print("\n----- 技能 -----")
    for skill_name, skill_value in sorted(investigator.skills.items()):
        print(f"{skill_name}: {skill_value}")
    
    print("\n----- 背景 -----")
    print(f"个人描述: {investigator.personal_description}")
    print(f"思想信念: {investigator.ideology}")
    print(f"重要之人: {investigator.significant_people}")
    print(f"意义非凡之地: {investigator.meaningful_locations}")
    print(f"宝贵之物: {investigator.treasured_possessions}")
    print(f"特质: {investigator.traits}")
    
    print("\n----- 装备和资产 -----")
    print(f"现金: {investigator.cash}")
    print(f"资产: {investigator.assets}")
    if investigator.equipment:
        print("装备:")
        for item in investigator.equipment:
            print(f"- {item}")
    print("=====================")

def custom_investigator(investigator_generator):
    """自定义调查员"""
    investigator = investigator_generator.create_empty_investigator()
    
    print("\n===== 自定义调查员 =====")
    
    # 基本信息
    investigator.name = input("姓名: ")
    investigator.player = input("玩家: ")
    investigator.gender = input("性别: ")
    
    age_str = input("年龄 (默认30): ")
    investigator.age = int(age_str) if age_str else 30
    
    investigator.residence = input("居住地: ")
    investigator.birthplace = input("出生地: ")
    
    # 属性
    print("\n----- 属性 -----")
    print("1. 随机生成所有属性")
    print("2. 手动输入属性")
    attr_choice = input("请选择 (1-2): ")
    
    if attr_choice == "1":
        # 随机生成所有属性
        for attr_name in investigator.attributes.keys():
            attr_config = investigator_generator.config.attributes.get(attr_name)
            if attr_config:
                value = investigator_generator.dice_roller.roll_attribute(
                    attr_config["dice"], attr_config["multiplier"]
                )
                investigator.attributes[attr_name] = value
    else:
        # 手动输入属性
        for attr_name in investigator.attributes.keys():
            attr_str = input(f"{attr_name} (0-100): ")
            if attr_str:
                investigator.attributes[attr_name] = int(attr_str)
    
    # 重新计算属性的半值和五分之一值
    investigator.calculate_half_fifth_values()
    
    # 重新计算衍生属性
    investigator.calculate_derived_attributes()
    
    # 职业
    print("\n----- 职业 -----")
    occupations = list(investigator_generator.occupations.occupations.keys())
    for i, occupation_name in enumerate(occupations, 1):
        print(f"{i}. {occupation_name}")
    
    occupation_choice = input("请选择职业 (输入序号): ")
    if occupation_choice and occupation_choice.isdigit():
        occupation_index = int(occupation_choice) - 1
        if 0 <= occupation_index < len(occupations):
            investigator.occupation = occupations[occupation_index]
            
            # 计算职业技能点
            edu = investigator.attributes.get("教育", 0)
            occupation = investigator_generator.occupations.get_occupation(investigator.occupation)
            if occupation:
                skill_points = investigator_generator.occupations.calculate_skill_points(investigator.occupation, edu)
                investigator.occupation_skill_points = skill_points
                investigator.interest_skill_points = investigator.attributes.get("智力", 0) * 2
    
    # 技能
    print("\n----- 技能 -----")
    print(f"职业技能点: {investigator.occupation_skill_points}")
    print(f"兴趣技能点: {investigator.interest_skill_points}")
    print("1. 随机分配技能点")
    print("2. 手动分配技能点")
    skill_choice = input("请选择 (1-2): ")
    
    if skill_choice == "1":
        # 随机分配技能点
        # 获取职业技能
        occupation_skills = []
        if investigator.occupation:
            occupation = investigator_generator.occupations.get_occupation(investigator.occupation)
            if occupation:
                occupation_skills = occupation.get("skills", [])
        
        # 随机分配职业技能点
        remaining_occupation_points = investigator.occupation_skill_points
        while remaining_occupation_points > 0 and occupation_skills:
            # 随机选择一个职业技能
            skill_name = investigator_generator.dice_roller.random_choice(occupation_skills)
            skill = investigator_generator.skills.get_skill(skill_name)
            
            if not skill:
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_occupation_points, 20)
            points = investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.occupation_skill_points_allocated += points
            remaining_occupation_points -= points
        
        # 随机分配兴趣技能点
        remaining_interest_points = investigator.interest_skill_points
        all_skills = list(investigator_generator.skills.skills.keys())
        while remaining_interest_points > 0 and all_skills:
            # 随机选择一个技能
            skill_name = investigator_generator.dice_roller.random_choice(all_skills)
            
            # 跳过已经分配过的职业技能
            if skill_name in occupation_skills:
                all_skills.remove(skill_name)
                continue
            
            skill = investigator_generator.skills.get_skill(skill_name)
            
            if not skill:
                all_skills.remove(skill_name)
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_interest_points, 20)
            points = investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.interest_skill_points_allocated += points
            remaining_interest_points -= points
            
            # 从列表中移除已分配的技能
            all_skills.remove(skill_name)
    
    # 背景
    print("\n----- 背景 -----")
    print("1. 随机生成背景")
    print("2. 手动输入背景")
    background_choice = input("请选择 (1-2): ")
    
    if background_choice == "1":
        # 随机生成背景
        background = investigator_generator.backgrounds.get_random_background(
            investigator_generator.dice_roller
        )
        
        if background:
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
    else:
        # 手动输入背景
        investigator.personal_description = input("个人描述: ")
        investigator.ideology = input("思想信念: ")
        investigator.significant_people = input("重要之人: ")
        investigator.meaningful_locations = input("意义非凡之地: ")
        investigator.treasured_possessions = input("宝贵之物: ")
        investigator.traits = input("特质: ")
    
    # 装备和资产
    print("\n----- 装备和资产 -----")
    cash_str = input("现金: ")
    if cash_str:
        investigator.cash = int(cash_str)
    
    investigator.assets = input("资产: ")
    
    equipment_str = input("装备 (用逗号分隔): ")
    if equipment_str:
        investigator.equipment = [item.strip() for item in equipment_str.split(",")]
    
    return investigator

def main():
    """主函数"""
    try:
        print("开始初始化应用程序...")
        
        # 确保数据目录存在
        os.makedirs("data", exist_ok=True)
        
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
        
        # 当前调查员
        current_investigator = None
        
        # 主循环
        while True:
            choice = print_menu()
            
            if choice == "1":
                # 随机生成调查员
                current_investigator = investigator_generator.generate_random_investigator()
                print_investigator(current_investigator)
            
            elif choice == "2":
                # 自定义调查员
                current_investigator = custom_investigator(investigator_generator)
                print_investigator(current_investigator)
            
            elif choice == "3":
                # 保存调查员
                if not current_investigator:
                    print("没有调查员可保存")
                    continue
                
                file_path = input("请输入保存路径 (默认为 data/investigator.json): ")
                if not file_path:
                    file_path = "data/investigator.json"
                
                success = file_handler.save_investigator(current_investigator, file_path)
                
                if success:
                    print(f"调查员已保存到: {file_path}")
                else:
                    print("保存调查员失败")
            
            elif choice == "4":
                # 加载调查员
                file_path = input("请输入加载路径 (默认为 data/investigator.json): ")
                if not file_path:
                    file_path = "data/investigator.json"
                
                investigator = file_handler.load_investigator(file_path)
                
                if investigator:
                    current_investigator = investigator
                    print_investigator(current_investigator)
                else:
                    print("加载调查员失败")
            
            elif choice == "5":
                # 导出调查员为文本
                if not current_investigator:
                    print("没有调查员可导出")
                    continue
                
                file_path = input("请输入导出路径 (默认为 data/investigator.txt): ")
                if not file_path:
                    file_path = "data/investigator.txt"
                
                success = file_handler.export_investigator_to_text(current_investigator, file_path)
                
                if success:
                    print(f"调查员已导出到: {file_path}")
                else:
                    print("导出调查员失败")
            
            elif choice == "6":
                # 退出
                print("感谢使用克苏鲁的呼唤 - 调查员生成器！")
                break
            
            else:
                print("无效的选择，请重新输入")
        
        return 0
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 