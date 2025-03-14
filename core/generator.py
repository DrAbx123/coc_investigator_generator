#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调查员生成器模块

MIT License
Copyright (c) 2025 COC Investigator Generator
"""

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
        
        # 设置初始理智值和理智值上限
        # 克苏鲁神话初始为0，所以理智值上限等于意志值
        investigator.san = investigator.attributes["意志"]
        investigator.initial_san = investigator.san
        investigator.max_san = investigator.san
        
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
        
        # 生成并分配技能点
        self.generate_skills(investigator)
        
        # 如果没有克苏鲁神话技能，初始化为0
        if "克苏鲁神话" not in investigator.skills:
            investigator.add_skill("克苏鲁神话", 0)
        
        # 确保理智值上限正确
        investigator.update_max_sanity()
        
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
    
    def generate_skills(self, investigator):
        """生成并分配技能点
        
        Args:
            investigator: 调查员对象
        """
        # 计算职业技能点
        occupation = self.occupations.get_occupation(investigator.occupation)
        if not occupation:
            print(f"警告: 未找到职业 '{investigator.occupation}'")
            return
        
        # 初始化所有技能为基础值
        for skill_name, skill_data in self.skills.skills.items():
            base_value = skill_data.get("base_value", 0)
            investigator.skills[skill_name] = base_value
            
            # 处理技能专攻
            if "specializations" in skill_data:
                investigator.skill_specializations[skill_name] = {}
                for spec in skill_data["specializations"]:
                    full_name = f"{skill_name}（{spec}）"
                    # 特殊处理某些常用技能专攻的基础值
                    if skill_name == "格斗" and spec == "斗殴":
                        base_spec_value = 25  # 斗殴基础值25%
                    elif skill_name == "射击" and spec == "手枪":
                        base_spec_value = 20  # 手枪基础值20%
                    elif skill_name == "驾驶" and spec == "汽车":
                        base_spec_value = 20  # 汽车基础值20%
                    elif skill_name == "语言" and spec == "母语":
                        # 母语基础值EDU
                        base_spec_value = investigator.attributes.get("教育", 0)
                    else:
                        base_spec_value = base_value
                    
                    investigator.skill_specializations[skill_name][full_name] = base_spec_value
        
        # 特殊处理闪避技能
        investigator.skills["闪避"] = investigator.attributes.get("敏捷", 0) // 2
        
        # 添加母语和其他默认语言
        if "语言" in self.skills.skills:
            # 使用新的语言技能生成方法
            self.generate_language_skills(investigator)
        
        # 分配职业技能点
        edu = investigator.attributes.get("教育", 0)
        investigator.occupation_skill_points = self.occupations.calculate_skill_points(investigator.occupation, edu)
        
        # 分配兴趣技能点
        investigator.interest_skill_points = investigator.attributes.get("智力", 0) * 2
        
        # 如果有职业技能列表，随机分配职业技能点
        if "skills" in occupation:
            investigator.occupation_skills = occupation["skills"]
            self._distribute_occupation_skill_points(investigator)
        
        # 随机分配兴趣技能点
        self._distribute_interest_skill_points(investigator)
        
        # 应用技能转移规则
        self._apply_skill_transfer_rules(investigator)

    def _distribute_occupation_skill_points(self, investigator):
        """分配职业技能点
        
        Args:
            investigator: 调查员对象
        """
        occupation_skills = []
        
        # 处理职业技能列表，展开"任一"和"自选"选项
        for skill in investigator.occupation_skills:
            if "任一" in skill:
                # 例如"艺术与手艺（任一）"，随机选择一个专攻
                main_skill = skill.split("（")[0].strip()
                if main_skill in self.skills.skills and "specializations" in self.skills.skills[main_skill]:
                    specs = self.skills.skills[main_skill]["specializations"]
                    selected_spec = random.choice(specs)
                    occupation_skills.append(f"{main_skill}（{selected_spec}）")
                else:
                    occupation_skills.append(skill)
            elif "自选" in skill:
                # 例如"自选一技能"，随机选择一个非职业技能
                non_occupation_skills = [s for s in self.skills.skills.keys() 
                                       if s not in investigator.occupation_skills and "自选" not in s]
                if non_occupation_skills:
                    selected_skill = random.choice(non_occupation_skills)
                    occupation_skills.append(selected_skill)
            else:
                occupation_skills.append(skill)
        
        # 更新调查员的职业技能列表
        investigator.occupation_skills = occupation_skills
        
        # 剩余可分配点数
        remaining_points = investigator.occupation_skill_points
        
        # 随机分配点数给职业技能
        while remaining_points > 0 and occupation_skills:
            # 随机选择一个技能
            skill = random.choice(occupation_skills)
            
            # 确定可分配的最大点数（不超过提升上限和剩余点数）
            if "（" in skill or "(" in skill:
                # 专攻技能
                main_skill = skill.split("（")[0].split("(")[0].strip()
                current_value = investigator.get_skill(skill)
                max_allocation = min(remaining_points, 75 - current_value)
            else:
                # 普通技能
                current_value = investigator.get_skill(skill)
                max_allocation = min(remaining_points, 75 - current_value)
            
            # 如果无法再分配，从列表中移除该技能
            if max_allocation <= 0:
                occupation_skills.remove(skill)
                continue
            
            # 随机分配1-5点
            points_to_add = random.randint(1, min(5, max_allocation))
            
            # 添加技能点
            if "（" in skill or "(" in skill:
                # 专攻技能
                investigator.add_skill(skill, current_value + points_to_add)
            else:
                investigator.skills[skill] = current_value + points_to_add
            
            # 更新剩余点数
            remaining_points -= points_to_add
            investigator.occupation_skill_points_allocated += points_to_add
    
    def _distribute_interest_skill_points(self, investigator):
        """分配兴趣技能点
        
        Args:
            investigator: 调查员对象
        """
        # 剩余可分配点数
        remaining_points = investigator.interest_skill_points
        
        # 随机选择2-4个兴趣技能
        num_interest_skills = random.randint(2, 4)
        
        # 排除已经是职业技能的技能
        available_skills = []
        for skill_name in self.skills.skills.keys():
            if skill_name not in investigator.occupation_skills:
                if "specializations" in self.skills.skills[skill_name]:
                    # 对于有专攻的技能，添加专攻版本
                    for spec in self.skills.skills[skill_name]["specializations"]:
                        spec_skill = f"{skill_name}（{spec}）"
                        if spec_skill not in investigator.occupation_skills:
                            available_skills.append(spec_skill)
                else:
                    available_skills.append(skill_name)
        
        if not available_skills:
            return
        
        # 随机选择兴趣技能
        interest_skills = random.sample(available_skills, min(num_interest_skills, len(available_skills)))
        
        # 随机分配点数给兴趣技能
        while remaining_points > 0 and interest_skills:
            # 随机选择一个技能
            skill = random.choice(interest_skills)
            
            # 确定可分配的最大点数（不超过提升上限和剩余点数）
            if "（" in skill or "(" in skill:
                # 专攻技能
                current_value = investigator.get_skill(skill)
                max_allocation = min(remaining_points, 75 - current_value)
            else:
                # 普通技能
                current_value = investigator.get_skill(skill)
                max_allocation = min(remaining_points, 75 - current_value)
            
            # 如果无法再分配，从列表中移除该技能
            if max_allocation <= 0:
                interest_skills.remove(skill)
                continue
            
            # 随机分配1-5点
            points_to_add = random.randint(1, min(5, max_allocation))
            
            # 添加技能点
            if "（" in skill or "(" in skill:
                # 专攻技能
                investigator.add_skill(skill, current_value + points_to_add)
            else:
                investigator.skills[skill] = current_value + points_to_add
            
            # 更新剩余点数
            remaining_points -= points_to_add
            investigator.interest_skill_points_allocated += points_to_add
    
    def _apply_skill_transfer_rules(self, investigator):
        """应用技能转移规则
        
        Args:
            investigator: 调查员对象
        """
        # 对每个有专攻的技能，检查并应用技能转移规则
        for main_skill in investigator.skill_specializations.keys():
            investigator._apply_skill_transfer(main_skill)
        
        # 特殊处理语言技能的转移规则
        language_skills = [skill for skill in investigator.skills.keys() if skill.startswith("语言（") and skill.endswith("）")]
        for lang_skill in language_skills:
            # 增强的日志，帮助理解语言技能转移过程
            investigator._apply_skill_transfer(lang_skill)
            
        # 不再需要输出语言技能值的循环

    def _show_language_skills(self, investigator):
        """显示调查员的语言技能
        
        Args:
            investigator: 调查员对象
            
        Returns:
            str: 格式化的语言技能文本
        """
        result = "语言技能:\n"
        
        # 获取语言族群信息
        language_families = self.skills.get_skill_info("语言").get("language_families", {})
        
        # 按语言族群组织语言技能
        languages_by_family = {}
        
        for skill_name, skill_value in investigator.skills.items():
            if skill_name.startswith("语言（") and skill_name.endswith("）"):
                # 提取语言名称
                language = skill_name[3:-1]  # 去掉"语言（"和"）"
                
                # 查找语言所属的族群
                family = "其他"
                for f_name, langs in language_families.items():
                    if language in langs:
                        family = f_name
                        break
                
                # 添加到对应族群
                if family not in languages_by_family:
                    languages_by_family[family] = []
                languages_by_family[family].append((language, skill_value))
        
        # 输出结果
        for family, languages in languages_by_family.items():
            result += f"\n{family}:\n"
            for language, value in sorted(languages, key=lambda x: x[1], reverse=True):
                # 添加技能等级描述
                level_desc = ""
                if value >= 75:
                    level_desc = "（精通，可以像本地人一样流利）"
                elif value >= 50:
                    level_desc = "（流利，可以进行流畅交流）"
                elif value >= 30:
                    level_desc = "（中级，可以满足社交需求）"
                elif value >= 10:
                    level_desc = "（初级，可以交流简单想法）"
                elif value >= 5:
                    level_desc = "（入门，可以辨认这门语言）"
                
                result += f"  - {language}: {value}% {level_desc}\n"
        
        return result

    def generate_language_skills(self, investigator, mother_tongue=None):
        """生成调查员的语言技能
        
        Args:
            investigator: 调查员对象
            mother_tongue: 指定的母语（可选，如果不指定则根据出生地确定）
        """
        if "语言" not in self.skills.skills:
            return
        
        # 如果未指定母语，则根据出生地设置默认母语
        if not mother_tongue:
            birthplace = investigator.birthplace or "阿卡姆"  # 默认为阿卡姆
            
            # 根据出生地推断可能的母语
            birthplace_language_map = {
                "阿卡姆": "英语",
                "波士顿": "英语",
                "纽约": "英语",
                "芝加哥": "英语",
                "伦敦": "英语",
                "巴黎": "法语",
                "柏林": "德语",
                "罗马": "意大利语",
                "开罗": "阿拉伯语",
                "上海": "中文",
                "东京": "日语",
                "莫斯科": "俄语",
                "马德里": "西班牙语",
                "布拉格": "捷克语",
                "华沙": "波兰语",
                "斯德哥尔摩": "瑞典语",
                "奥斯陆": "挪威语",
                "哥本哈根": "丹麦语",
                "首尔": "韩语",
                "里斯本": "葡萄牙语",
                "布加勒斯特": "罗马尼亚语",
                "基辅": "乌克兰语",
                "贝尔格莱德": "塞尔维亚语",
                "拉萨": "藏语",
                "耶路撒冷": "希伯来语"
            }
            
            mother_tongue_lang = birthplace_language_map.get(birthplace, "英语")
        else:
            mother_tongue_lang = mother_tongue
        
        # 设置母语
        mother_tongue_skill = f"语言（{mother_tongue_lang}）"
        investigator.add_skill(mother_tongue_skill, investigator.attributes.get("教育", 0))
        
        # 获取所有语言及其语系
        language_families = self.skills.get_skill_info("语言").get("language_families", {})
        
        # 找出母语所属的语系
        same_family_languages = []
        mother_family = None
        for family, langs in language_families.items():
            if mother_tongue_lang in langs:
                same_family_languages = [lang for lang in langs if lang != mother_tongue_lang]
                mother_family = family
                break
        
        # 为同系语言设置初始值
        if same_family_languages:
            for lang in same_family_languages:
                lang_skill = f"语言（{lang}）"
                # 同系语言初始值为5-15%（根据教育值）
                base_value = max(5, min(15, investigator.attributes.get("教育", 0) // 10))
                investigator.add_skill(lang_skill, base_value)
        
        # 为其他常见语言设置基础值为1-5%
        # 优先添加国际通用语言
        common_languages = ["英语", "法语", "德语", "西班牙语", "拉丁语", "中文", "俄语", "阿拉伯语"]
        for lang in common_languages:
            if lang != mother_tongue_lang and lang not in same_family_languages:
                lang_skill = f"语言（{lang}）"
                if lang_skill not in investigator.skills:
                    # 非同系常见语言初始值为1-5%
                    base_value = max(1, min(5, investigator.attributes.get("智力", 0) // 20))
                    investigator.add_skill(lang_skill, base_value) 