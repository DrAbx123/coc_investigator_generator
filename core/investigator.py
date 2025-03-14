#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调查员角色模型模块

实现克苏鲁的呼唤第七版规则中的调查员角色系统，包括：
- 属性系统（力量、体质、体型、敏捷、外貌、智力、意志、教育、幸运）
- 衍生属性计算（生命值、魔法值、理智值、伤害加值、体格、移动速度）
- 技能管理
- 背景信息处理
- 装备系统
- 角色状态跟踪

属性计算规则：
- 半值：属性值的一半（向下取整）
- 五分之一值：属性值的五分之一（向下取整）

衍生属性计算规则：
- 生命值(HP) = (体质 + 体型) / 10（向下取整）
- 魔法值(MP) = 意志 / 5（向下取整）
- 理智值(SAN) = 意志（无克苏鲁神话知识时）
- 伤害加值(DB)：根据力量和体型总和确定
- 体格(Build)：根据力量和体型总和确定
- 移动速度(MOV)：根据敏捷、力量和体型比较确定，并受年龄影响
"""

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
        self.file_path = ""  # 添加文件路径属性

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
        self.skill_specializations = {}  # 添加技能专攻字典
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
        self.spending_level = ""  # 添加消费水平属性
        self.items = []  # 添加物品列表
        self.weapons = []  # 添加武器列表

    # 添加ideology_beliefs作为ideology的别名
    @property
    def ideology_beliefs(self):
        """返回ideology的值，这是为了兼容性添加的别名属性"""
        return self.ideology

    @ideology_beliefs.setter
    def ideology_beliefs(self, value):
        """设置ideology的值，这是为了兼容性添加的别名属性"""
        self.ideology = value

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
            "file_path": self.file_path,  # 添加文件路径
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
            "skill_specializations": self.skill_specializations,
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
            "assets": self.assets,
            "spending_level": self.spending_level,
            "items": self.items,
            "weapons": self.weapons
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
        investigator.file_path = data.get("file_path", "")  # 获取文件路径

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
        investigator.skill_specializations = data.get("skill_specializations", {})
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
        investigator.spending_level = data.get("spending_level", "")
        investigator.items = data.get("items", [])
        investigator.weapons = data.get("weapons", [])

        return investigator

    def add_skill(self, skill_name, value):
        """添加或更新技能值
        
        Args:
            skill_name: 技能名称
            value: 技能值
        """
        # 检查是否是专攻技能
        is_specialization = "（" in skill_name and "）" in skill_name
        
        # 获取当前技能值
        current_value = self.skills.get(skill_name, 0)
        
        # 如果是语言技能，记录是否跨越了50%和90%的阈值
        crossed_fifty = False
        crossed_ninety = False
        
        if skill_name.startswith("语言（") and skill_name.endswith("）"):
            if current_value < 50 and value >= 50:
                crossed_fifty = True
            if current_value < 90 and value >= 90:
                crossed_ninety = True
        
        # 更新技能值
        self.skills[skill_name] = value
        
        # 如果是专攻技能，也更新专攻字典
        if is_specialization:
            main_skill = skill_name.split("（")[0]
            if main_skill not in self.skill_specializations:
                self.skill_specializations[main_skill] = {}
            self.skill_specializations[main_skill][skill_name] = value
        
        # 如果是语言技能并且跨越了阈值，应用技能转移规则
        if (crossed_fifty or crossed_ninety) and skill_name.startswith("语言（"):
            self._apply_skill_transfer(skill_name)
    
    def get_skill(self, skill_name):
        """获取技能值
        
        Args:
            skill_name: 技能名称
            
        Returns:
            int: 技能值
        """
        return self.skills.get(skill_name, 0)
    
    def _apply_skill_transfer(self, skill_name):
        """应用技能转移规则
        
        当一门语言技能达到50%或90%时，同系语言都会获得提升
        
        Args:
            skill_name: 技能名称
        """
        # 只处理语言技能
        if not skill_name.startswith("语言（") or not skill_name.endswith("）"):
            return
        
        # 获取当前技能值
        current_value = self.skills.get(skill_name, 0)
        
        # 如果未达到阈值，不处理
        if current_value < 50:
            return
        
        # 从技能名称中提取语言名称
        language = skill_name[skill_name.find("（")+1:skill_name.find("）")]
        
        # 获取语言族群信息
        # 注意：这里需要从外部加载语言族群信息，这里简化处理
        language_families = {
            "日耳曼语族": ["英语", "德语", "荷兰语", "瑞典语", "挪威语", "丹麦语"],
            "斯拉夫语族": ["俄语", "波兰语", "捷克语", "乌克兰语", "塞尔维亚语"],
            "罗曼语族": ["法语", "西班牙语", "意大利语", "葡萄牙语", "罗马尼亚语"],
            "汉藏语系": ["中文", "藏语"],
            "阿尔泰语系": ["日语", "韩语", "蒙古语", "维吾尔语"],
            "闪含语系": ["阿拉伯语", "希伯来语", "埃塞俄比亚语"],
            "古典语言": ["拉丁语", "希腊语", "梵语", "古埃及语"]
        }
        
        # 查找该语言属于哪个语系
        target_family = None
        related_languages = []
        
        for family, languages in language_families.items():
            if language in languages:
                target_family = family
                related_languages = [lang for lang in languages if lang != language]
                break
        
        if not target_family:
            return
        
        # 确定提升值
        boost_value = 0
        if current_value >= 90:
            boost_value = 20  # 90%阈值提升20%（包括50%阈值的10%）
        elif current_value >= 50:
            boost_value = 10  # 50%阈值提升10%
        
        if boost_value == 0:
            return
        
        # 应用提升到相关语言
        for related_lang in related_languages:
            related_skill = f"语言（{related_lang}）"
            related_value = self.skills.get(related_skill, 0)
            
            # 如果相关语言技能值低于提升后的值，则提升
            if related_value < boost_value:
                self.skills[related_skill] = boost_value
                
                # 如果是专攻技能，也更新专攻字典
                if "语言" in self.skill_specializations:
                    self.skill_specializations["语言"][related_skill] = boost_value
                    
    def update_max_sanity(self):
        """更新理智值上限
        
        根据克苏鲁神话技能值计算理智值上限
        """
        # 获取克苏鲁神话技能值
        cthulhu_mythos = self.skills.get("克苏鲁神话", 0)
        
        # 计算理智值上限
        self.max_san = 99 - cthulhu_mythos
        
        # 确保理智值不超过上限
        if hasattr(self, 'san') and self.san > self.max_san:
            self.san = self.max_san