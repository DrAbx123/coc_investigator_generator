#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
技能查看器模块

提供查看技能详细信息和语言族群关系的功能，方便在主程序中调用。
"""

from core.skills import Skills

class SkillViewer:
    """技能查看器类，用于显示技能详情和语言族群信息"""
    
    def __init__(self):
        """初始化技能查看器"""
        self.skills = Skills()
        self.skills.load_skills("data/skills.json")

    def get_skill_description(self, skill_name):
        """获取技能描述
        
        Args:
            skill_name: 技能名称
            
        Returns:
            dict: 包含技能描述信息的字典
        """
        # 处理专攻技能
        if "（" in skill_name and "）" in skill_name:
            main_skill, specialization = skill_name.split("（")
            specialization = specialization.rstrip("）")
            skill_info = self.skills.get_skill_info(main_skill)
            
            # 构建包含专攻信息的描述
            result = {
                "name": skill_name,
                "base_value": skill_info.get("base_value", 0),
                "category": skill_info.get("category", "未分类"),
                "description": skill_info.get("description", "无描述"),
                "specialization": specialization
            }
            
            # 如果是语言技能，添加语言族群信息
            if main_skill == "语言":
                language_families = skill_info.get("language_families", {})
                result["language_family"] = self._get_language_family(specialization, language_families)
                result["same_family_languages"] = self._get_same_family_languages(specialization, language_families)
            
            return result
        
        # 处理普通技能
        skill_info = self.skills.get_skill_info(skill_name)
        if not skill_info:
            return {"name": skill_name, "description": "未知技能"}
        
        result = {
            "name": skill_name,
            "base_value": skill_info.get("base_value", 0),
            "category": skill_info.get("category", "未分类"),
            "description": skill_info.get("description", "无描述")
        }
        
        # 对于有专攻的技能，列出可用专攻
        if "specializations" in skill_info:
            result["specializations"] = skill_info["specializations"]
        
        # 对于语言技能，添加语言族群信息
        if skill_name == "语言" and "language_families" in skill_info:
            result["language_families"] = skill_info["language_families"]
        
        return result
    
    def get_language_families(self):
        """获取所有语言族群信息
        
        Returns:
            dict: 语言族群字典
        """
        language_info = self.skills.get_skill_info("语言")
        return language_info.get("language_families", {})
    
    def get_language_family_info(self, family_name):
        """获取特定语言族群的信息
        
        Args:
            family_name: 语言族群名称
            
        Returns:
            list: 该族群包含的语言列表
        """
        language_families = self.get_language_families()
        return language_families.get(family_name, [])
    
    def _get_language_family(self, language, language_families):
        """获取语言所属的语言族群
        
        Args:
            language: 语言名称
            language_families: 语言族群字典
            
        Returns:
            str: 语言族群名称，如果不存在则返回"其他"
        """
        for family, langs in language_families.items():
            if language in langs:
                return family
        return "其他"
    
    def _get_same_family_languages(self, language, language_families):
        """获取与指定语言同族的其他语言
        
        Args:
            language: 语言名称
            language_families: 语言族群字典
            
        Returns:
            list: 同族语言列表
        """
        for family, langs in language_families.items():
            if language in langs:
                return [lang for lang in langs if lang != language]
        return []
    
    def list_skills_by_category(self, category=None):
        """按类别列出技能
        
        Args:
            category: 技能类别，如果为None则列出所有类别
            
        Returns:
            dict: 按类别分组的技能字典
        """
        result = {}
        
        for skill_name, skill_info in self.skills.skills.items():
            skill_category = skill_info.get("category", "未分类")
            
            if category and skill_category != category:
                continue
                
            if skill_category not in result:
                result[skill_category] = []
            
            # 添加基本技能信息
            skill_entry = {
                "name": skill_name,
                "base_value": skill_info.get("base_value", 0),
                "description": skill_info.get("description", "").split("\n")[0]  # 只取描述的第一行作为简介
            }
            
            result[skill_category].append(skill_entry)
        
        return result

    def display_language_skill_transfer_rules(self):
        """显示语言技能转移规则
        
        Returns:
            str: 语言技能转移规则的说明文本
        """
        language_info = self.skills.get_skill_info("语言")
        description = language_info.get("description", "")
        
        # 提取关于技能转移的部分
        transfer_info = "语言技能转移规则：\n"
        transfer_info += "当一名角色初次将一门语言（除了母语）提升到50%，所有其他相关的同系语言都会提升10%（但不会超过50%）。\n"
        transfer_info += "当角色初次将一门语言提升到90%，所有相关同系语言会再次提升10%（但不会高于90%）。\n\n"
        
        transfer_info += "语言技能等级含义：\n"
        transfer_info += "- 5%：能够正确地辨认出这门语言而不需要检定。\n"
        transfer_info += "- 10%：可以交流简单的想法。\n"
        transfer_info += "- 30%：可以对社交上的需求进行理解。\n"
        transfer_info += "- 50%：可以进行流畅的交流。\n"
        transfer_info += "- 75%：可以将这门语言说得像是本地人一样。\n\n"
        
        transfer_info += "语言族群：\n"
        for family, languages in self.get_language_families().items():
            transfer_info += f"- {family}：{', '.join(languages)}\n"
        
        return transfer_info 