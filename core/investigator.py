#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Investigator:
    """调查员模型类"""
    
    def __init__(self):
        """初始化调查员"""
        # 基本信息
        self.name = ""
        self.player = ""
        self.occupation = ""
        self.age = 0
        self.gender = ""
        self.residence = ""
        self.birthplace = ""
        
        # 属性
        self.attributes = {
            "力量": 0,
            "体质": 0,
            "体型": 0,
            "敏捷": 0,
            "外貌": 0,
            "智力": 0,
            "意志": 0,
            "教育": 0,
            "幸运": 0
        }
        
        # 属性的半值和五分之一值
        self.attribute_half = {}
        self.attribute_fifth = {}
        
        # 衍生属性
        self.hp = 0
        self.mp = 0
        self.san = 0
        self.armor = 0
        self.db = "0"
        self.build = 0
        self.mov = 0
        
        # 技能
        self.skills = {}
        self.occupation_skills = []
        self.occupation_skill_points = 0
        self.occupation_skill_points_allocated = 0
        self.interest_skill_points = 0
        self.interest_skill_points_allocated = 0
        
        # 背景
        self.personal_description = ""
        self.ideology = ""
        self.significant_people = ""
        self.meaningful_locations = ""
        self.treasured_possessions = ""
        self.traits = ""
        self.injuries_scars = ""
        self.phobias_manias = ""
        self.arcane_tomes_spells = ""
        self.background_story = ""
        
        # 装备和资产
        self.equipment = []
        self.cash = 0
        self.assets = ""
    
    def calculate_derived_attributes(self):
        """计算衍生属性"""
        # 计算生命值
        self.hp = (self.attributes["体质"] + self.attributes["体型"]) // 10
        
        # 计算魔法值
        self.mp = self.attributes["意志"] // 5
        
        # 计算理智值
        self.san = self.attributes["意志"]
        
        # 计算伤害加值和体格
        str_siz = self.attributes["力量"] + self.attributes["体型"]
        if str_siz <= 64:
            self.db = "-2"
            self.build = -2
        elif str_siz <= 84:
            self.db = "-1"
            self.build = -1
        elif str_siz <= 124:
            self.db = "0"
            self.build = 0
        elif str_siz <= 164:
            self.db = "+1D4"
            self.build = 1
        elif str_siz <= 204:
            self.db = "+1D6"
            self.build = 2
        else:
            self.db = "+2D6"
            self.build = 3
        
        # 计算移动速度
        if self.attributes["敏捷"] < self.attributes["体型"] and self.attributes["力量"] < self.attributes["体型"]:
            self.mov = 7
        elif self.attributes["敏捷"] >= self.attributes["体型"] and self.attributes["力量"] >= self.attributes["体型"]:
            self.mov = 9
        else:
            self.mov = 8
        
        # 根据年龄调整移动速度
        if 40 <= self.age <= 49:
            self.mov -= 1
        elif 50 <= self.age <= 59:
            self.mov -= 2
        elif 60 <= self.age <= 69:
            self.mov -= 3
        elif 70 <= self.age <= 79:
            self.mov -= 4
        elif 80 <= self.age <= 89:
            self.mov -= 5
    
    def calculate_half_fifth_values(self):
        """计算属性的半值和五分之一值"""
        for attr_name, attr_value in self.attributes.items():
            self.attribute_half[attr_name] = attr_value // 2
            self.attribute_fifth[attr_name] = attr_value // 5
    
    def to_dict(self):
        """将调查员对象转换为字典
        
        Returns:
            调查员数据字典
        """
        return {
            "name": self.name,
            "player": self.player,
            "occupation": self.occupation,
            "age": self.age,
            "gender": self.gender,
            "residence": self.residence,
            "birthplace": self.birthplace,
            "attributes": self.attributes,
            "attribute_half": self.attribute_half,
            "attribute_fifth": self.attribute_fifth,
            "hp": self.hp,
            "mp": self.mp,
            "san": self.san,
            "armor": self.armor,
            "db": self.db,
            "build": self.build,
            "mov": self.mov,
            "skills": self.skills,
            "occupation_skills": self.occupation_skills,
            "occupation_skill_points": self.occupation_skill_points,
            "occupation_skill_points_allocated": self.occupation_skill_points_allocated,
            "interest_skill_points": self.interest_skill_points,
            "interest_skill_points_allocated": self.interest_skill_points_allocated,
            "personal_description": self.personal_description,
            "ideology": self.ideology,
            "significant_people": self.significant_people,
            "meaningful_locations": self.meaningful_locations,
            "treasured_possessions": self.treasured_possessions,
            "traits": self.traits,
            "injuries_scars": self.injuries_scars,
            "phobias_manias": self.phobias_manias,
            "arcane_tomes_spells": self.arcane_tomes_spells,
            "background_story": self.background_story,
            "equipment": self.equipment,
            "cash": self.cash,
            "assets": self.assets
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建调查员对象
        
        Args:
            data: 调查员数据字典
        
        Returns:
            调查员对象
        """
        investigator = cls()
        
        investigator.name = data.get("name", "")
        investigator.player = data.get("player", "")
        investigator.occupation = data.get("occupation", "")
        investigator.age = data.get("age", 0)
        investigator.gender = data.get("gender", "")
        investigator.residence = data.get("residence", "")
        investigator.birthplace = data.get("birthplace", "")
        
        investigator.attributes = data.get("attributes", {})
        investigator.attribute_half = data.get("attribute_half", {})
        investigator.attribute_fifth = data.get("attribute_fifth", {})
        
        investigator.hp = data.get("hp", 0)
        investigator.mp = data.get("mp", 0)
        investigator.san = data.get("san", 0)
        investigator.armor = data.get("armor", 0)
        investigator.db = data.get("db", "0")
        investigator.build = data.get("build", 0)
        investigator.mov = data.get("mov", 0)
        
        investigator.skills = data.get("skills", {})
        investigator.occupation_skills = data.get("occupation_skills", [])
        investigator.occupation_skill_points = data.get("occupation_skill_points", 0)
        investigator.occupation_skill_points_allocated = data.get("occupation_skill_points_allocated", 0)
        investigator.interest_skill_points = data.get("interest_skill_points", 0)
        investigator.interest_skill_points_allocated = data.get("interest_skill_points_allocated", 0)
        
        investigator.personal_description = data.get("personal_description", "")
        investigator.ideology = data.get("ideology", "")
        investigator.significant_people = data.get("significant_people", "")
        investigator.meaningful_locations = data.get("meaningful_locations", "")
        investigator.treasured_possessions = data.get("treasured_possessions", "")
        investigator.traits = data.get("traits", "")
        investigator.injuries_scars = data.get("injuries_scars", "")
        investigator.phobias_manias = data.get("phobias_manias", "")
        investigator.arcane_tomes_spells = data.get("arcane_tomes_spells", "")
        investigator.background_story = data.get("background_story", "")
        
        investigator.equipment = data.get("equipment", [])
        investigator.cash = data.get("cash", 0)
        investigator.assets = data.get("assets", "")
        
        return investigator 