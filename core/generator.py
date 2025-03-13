#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from utils.dice import DiceRoller
from core.investigator import Investigator
from core.occupations import Occupations
from core.skills import Skills
from core.backgrounds import Backgrounds

class InvestigatorGenerator:
    """调查员生成器类"""
    
    def __init__(self, config, dice_roller, occupations, skills, backgrounds):
        """初始化调查员生成器
        
        Args:
            config: 配置对象
            dice_roller: 骰子工具对象
            occupations: 职业数据对象
            skills: 技能数据对象
            backgrounds: 背景数据对象
        """
        self.config = config
        self.dice_roller = dice_roller
        self.occupations = occupations
        self.skills = skills
        self.backgrounds = backgrounds
    
    def generate_attributes(self):
        """生成属性"""
        attributes = {}
        
        for attr_name, attr_config in self.config.attributes.items():
            attributes[attr_name] = self.dice_roller.roll_attribute(attr_config["dice"], attr_config["multiplier"])
        
        return attributes
    
    def adjust_attributes_by_age(self, investigator, age_group):
        """根据年龄调整属性"""
        age_config = self.config.age_groups.get(age_group)
        
        if not age_config:
            return
        
        # 力量和体型减少
        if age_config["str_siz_reduction"] > 0:
            reduction = age_config["str_siz_reduction"]
            # 在力量和体型之间分配减少值
            str_reduction = random.randint(0, reduction)
            siz_reduction = reduction - str_reduction
            
            investigator.attributes["力量"] = max(0, investigator.attributes["力量"] - str_reduction)
            investigator.attributes["体型"] = max(0, investigator.attributes["体型"] - siz_reduction)
        
        # 教育减少
        if age_config["edu_reduction"] > 0:
            investigator.attributes["教育"] = max(0, investigator.attributes["教育"] - age_config["edu_reduction"])
        
        # 力量、体质、敏捷合计减少
        if age_config["str_con_dex_reduction"] > 0:
            reduction = age_config["str_con_dex_reduction"]
            # 在力量、体质、敏捷之间分配减少值
            attrs = ["力量", "体质", "敏捷"]
            while reduction > 0 and any(investigator.attributes[attr] > 0 for attr in attrs):
                attr = random.choice(attrs)
                if investigator.attributes[attr] > 0:
                    investigator.attributes[attr] -= 1
                    reduction -= 1
        
        # 外貌减少
        if age_config["app_reduction"] > 0:
            investigator.attributes["外貌"] = max(0, investigator.attributes["外貌"] - age_config["app_reduction"])
        
        # 教育增强检定
        if age_config["edu_improvement_checks"] > 0:
            for _ in range(age_config["edu_improvement_checks"]):
                roll = random.randint(1, 100)
                if roll > investigator.attributes["教育"]:
                    # 增加1D10点教育
                    edu_increase = self.dice_roller.roll("1D10")
                    investigator.attributes["教育"] = min(99, investigator.attributes["教育"] + edu_increase)
        
        # 幸运值多次掷骰取较好的一次
        if age_config["luck_rolls"] > 1:
            luck_rolls = []
            for _ in range(age_config["luck_rolls"]):
                luck_rolls.append(self.dice_roller.roll_attribute("3D6"))
            investigator.attributes["幸运"] = max(luck_rolls)
    
    def generate_random_investigator(self, age_group="20-39"):
        """生成随机调查员
        
        Args:
            age_group: 年龄段
        
        Returns:
            调查员对象
        """
        # 创建调查员对象
        investigator = Investigator()
        
        # 生成基本信息
        investigator.name = "随机调查员"
        investigator.player = "玩家"
        investigator.gender = random.choice(["男", "女"])
        
        # 根据年龄段设置年龄
        age_ranges = {
            "15-19": (15, 19),
            "20-39": (20, 39),
            "40-49": (40, 49),
            "50-59": (50, 59),
            "60-69": (60, 69),
            "70-79": (70, 79),
            "80-89": (80, 89)
        }
        
        age_range = age_ranges.get(age_group, (20, 39))
        investigator.age = random.randint(age_range[0], age_range[1])
        
        # 生成属性
        attributes = self.generate_attributes()
        investigator.attributes = attributes
        
        # 根据年龄调整属性
        self.adjust_attributes_by_age(investigator, age_group)
        
        # 计算属性的半值和五分之一值
        for attr_name, attr_value in investigator.attributes.items():
            investigator.attribute_half[attr_name] = attr_value // 2
            investigator.attribute_fifth[attr_name] = attr_value // 5
        
        # 计算衍生属性
        investigator.hp = (investigator.attributes["体质"] + investigator.attributes["体型"]) // 10
        investigator.mp = investigator.attributes["意志"] // 5
        investigator.san = investigator.attributes["意志"]
        
        # 计算伤害加值和体格
        str_siz = investigator.attributes["力量"] + investigator.attributes["体型"]
        if str_siz <= 64:
            investigator.db = "-2"
            investigator.build = -2
        elif str_siz <= 84:
            investigator.db = "-1"
            investigator.build = -1
        elif str_siz <= 124:
            investigator.db = "0"
            investigator.build = 0
        elif str_siz <= 164:
            investigator.db = "+1D4"
            investigator.build = 1
        elif str_siz <= 204:
            investigator.db = "+1D6"
            investigator.build = 2
        else:
            investigator.db = "+2D6"
            investigator.build = 3
        
        # 计算移动速度
        if investigator.attributes["敏捷"] < investigator.attributes["体型"] and investigator.attributes["力量"] < investigator.attributes["体型"]:
            investigator.mov = 7
        elif investigator.attributes["敏捷"] >= investigator.attributes["体型"] and investigator.attributes["力量"] >= investigator.attributes["体型"]:
            investigator.mov = 9
        else:
            investigator.mov = 8
        
        # 根据年龄调整移动速度
        if age_group == "40-49":
            investigator.mov -= 1
        elif age_group == "50-59":
            investigator.mov -= 2
        elif age_group == "60-69":
            investigator.mov -= 3
        elif age_group == "70-79":
            investigator.mov -= 4
        elif age_group == "80-89":
            investigator.mov -= 5
        
        # 随机选择职业
        occupation_name = random.choice(list(self.occupations.occupations.keys()))
        occupation_data = self.occupations.get_occupation(occupation_name)
        
        investigator.occupation = occupation_name
        
        # 随机选择居住地和出生地
        cities = ["阿卡姆", "波士顿", "纽约", "芝加哥", "伦敦", "巴黎", "柏林", "罗马", "开罗", "上海"]
        investigator.residence = random.choice(cities)
        investigator.birthplace = random.choice(cities)
        
        # 随机生成背景
        investigator.personal_description = random.choice(self.backgrounds.get_personal_descriptions())
        investigator.ideology = random.choice(self.backgrounds.get_ideology_beliefs())
        investigator.significant_people = random.choice(self.backgrounds.get_significant_people_who()) + " " + random.choice(self.backgrounds.get_significant_people_why())
        investigator.meaningful_locations = random.choice(self.backgrounds.get_meaningful_locations())
        investigator.treasured_possessions = random.choice(self.backgrounds.get_treasured_possessions())
        investigator.traits = random.choice(self.backgrounds.get_traits())
        
        # 设置初始现金和资产
        credit_rating_range = occupation_data.get("credit_rating", (0, 0))
        investigator.cash = random.randint(credit_rating_range[0], credit_rating_range[1])
        investigator.assets = "无特殊资产"
        
        return investigator
    
    def generate_custom_investigator(self, data):
        """生成自定义调查员"""
        investigator = Investigator()
        
        # 设置基本信息
        investigator.name = data.get("name", "")
        investigator.player = data.get("player", "")
        investigator.occupation = data.get("occupation", "")
        investigator.age = data.get("age", 0)
        investigator.gender = data.get("gender", "")
        investigator.residence = data.get("residence", "")
        investigator.birthplace = data.get("birthplace", "")
        
        # 设置属性
        if "attributes" in data:
            investigator.attributes = data["attributes"]
        else:
            investigator.attributes = self.generate_attributes()
            
            # 根据年龄调整属性
            age_group = "20-39"  # 默认年龄段
            for group in self.config.age_groups:
                min_age, max_age = map(int, group.split("-"))
                if min_age <= investigator.age <= max_age:
                    age_group = group
                    break
            
            self.adjust_attributes_by_age(investigator, age_group)
        
        # 计算属性的半值和五分之一值
        investigator.calculate_half_fifth_values()
        
        # 计算衍生属性
        investigator.calculate_derived_attributes()
        
        # 设置职业技能
        if investigator.occupation:
            occupation = Occupations.get_occupation(investigator.occupation)
            if occupation:
                investigator.occupation_skills = occupation["skills"]
                investigator.occupation_skill_points = Occupations.calculate_skill_points(occupation, investigator)
        
        # 计算兴趣技能点
        investigator.interest_skill_points = investigator.attributes["智力"] * 2
        
        # 设置背景
        investigator.personal_description = data.get("personal_description", "")
        investigator.ideology_beliefs = data.get("ideology_beliefs", "")
        investigator.significant_people = data.get("significant_people", "")
        investigator.meaningful_locations = data.get("meaningful_locations", "")
        investigator.treasured_possessions = data.get("treasured_possessions", "")
        investigator.traits = data.get("traits", "")
        
        # 设置技能
        if "skills" in data:
            investigator.skills = data["skills"]
        
        # 设置装备和资产
        investigator.cash = data.get("cash", 0)
        investigator.assets = data.get("assets", 0)
        investigator.spending_level = data.get("spending_level", 0)
        investigator.items = data.get("items", [])
        investigator.weapons = data.get("weapons", [])
        
        return investigator
    
    def create_empty_investigator(self):
        """创建空白调查员
        
        Returns:
            空白调查员对象
        """
        investigator = Investigator()
        
        # 设置默认值
        investigator.name = "新调查员"
        investigator.player = "玩家"
        investigator.gender = "男"
        investigator.age = 30
        investigator.occupation = "无业"
        investigator.residence = "阿卡姆"
        investigator.birthplace = "阿卡姆"
        
        # 初始化属性
        for attr_name in ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]:
            investigator.attributes[attr_name] = 50
            investigator.attribute_half[attr_name] = 25
            investigator.attribute_fifth[attr_name] = 10
        
        # 初始化衍生属性
        investigator.hp = 10
        investigator.mp = 10
        investigator.san = 50
        investigator.db = "0"
        investigator.build = 0
        investigator.mov = 8
        
        # 初始化背景
        investigator.personal_description = "普通人"
        investigator.ideology = "无特殊信念"
        investigator.significant_people = "无"
        investigator.meaningful_locations = "无"
        investigator.treasured_possessions = "无"
        investigator.traits = "无"
        
        # 初始化财产
        investigator.cash = 50
        investigator.assets = "无特殊资产"
        
        return investigator 