#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Skills:
    """技能数据类"""
    
    def __init__(self):
        """初始化技能数据"""
        self.skills = {}
    
    def load_skills(self, file_path):
        """从文件加载技能数据
        
        Args:
            file_path: 技能数据文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.skills = json.load(f)
            return True
        except Exception as e:
            print(f"加载技能数据失败: {e}")
            # 使用默认技能数据
            self.skills = self.get_all_skills()
            return False
    
    @staticmethod
    def get_all_skills():
        """获取所有技能"""
        return {
            "会计学": {
                "base": 5,
                "category": "学问",
                "description": "允许记录和审计账簿，发现账目中的欺诈行为。"
            },
            "人类学": {
                "base": 1,
                "category": "学问",
                "description": "研究人类文化的学问，包括其起源、发展、信仰和习俗。"
            },
            "估价": {
                "base": 5,
                "category": "学问",
                "description": "对物品的价值做出准确评估的能力。"
            },
            "考古学": {
                "base": 1,
                "category": "学问",
                "description": "通过研究遗迹、化石和文物来了解古代文明的学问。"
            },
            "艺术与手艺": {
                "base": 5,
                "category": "技能",
                "description": "创作艺术品或制作手工艺品的能力。",
                "specializations": ["绘画", "摄影", "雕塑", "文学", "书法", "音乐作曲", "木工", "烹饪", "裁缝", "制陶", "农事", "歌唱", "表演", "舞蹈", "乐器演奏", "伪造", "设计图纸"]
            },
            "魅惑": {
                "base": 15,
                "category": "交际",
                "description": "通过魅力和个人魔力影响他人的能力。"
            },
            "攀爬": {
                "base": 20,
                "category": "身体",
                "description": "攀登树木、墙壁、悬崖等障碍物的能力。"
            },
            "计算机使用": {
                "base": 5,
                "category": "现代",
                "description": "使用计算机和相关技术的能力。"
            },
            "信用评级": {
                "base": 0,
                "category": "特殊",
                "description": "代表调查员的经济状况和社会地位。"
            },
            "克苏鲁神话": {
                "base": 0,
                "category": "特殊",
                "description": "对宇宙恐怖真相的了解程度。"
            },
            "乔装": {
                "base": 5,
                "category": "技能",
                "description": "通过改变外表和行为来伪装成他人的能力。"
            },
            "闪避": {
                "base": 0,
                "category": "身体",
                "description": "躲避攻击的能力。初始值等于敏捷的一半。"
            },
            "汽车驾驶": {
                "base": 20,
                "category": "技能",
                "description": "驾驶各种类型汽车的能力。"
            },
            "电气维修": {
                "base": 10,
                "category": "技能",
                "description": "修理和维护电气设备的能力。"
            },
            "电子学": {
                "base": 1,
                "category": "现代",
                "description": "理解、设计和修理电子设备的能力。"
            },
            "话术": {
                "base": 5,
                "category": "交际",
                "description": "通过欺骗和误导来影响他人的能力。"
            },
            "格斗": {
                "base": 25,
                "category": "战斗",
                "description": "进行近身格斗的能力。",
                "specializations": ["斗殴", "剑", "斧", "矛", "鞭", "链锯"]
            },
            "射击": {
                "base": 25,
                "category": "战斗",
                "description": "使用各种射击武器的能力。",
                "specializations": ["手枪", "步枪/霰弹枪", "冲锋枪", "弓", "重武器", "火焰喷射器"]
            },
            "急救": {
                "base": 30,
                "category": "技能",
                "description": "提供紧急医疗救助的能力。"
            },
            "历史": {
                "base": 5,
                "category": "学问",
                "description": "了解历史事件和历史发展的学问。"
            },
            "恐吓": {
                "base": 15,
                "category": "交际",
                "description": "通过威胁或暴力来影响他人的能力。"
            },
            "跳跃": {
                "base": 20,
                "category": "身体",
                "description": "跳跃障碍物或跨越间隙的能力。"
            },
            "其他语言": {
                "base": 1,
                "category": "学问",
                "description": "使用和理解外语的能力。",
                "specializations": ["英语", "法语", "德语", "西班牙语", "意大利语", "俄语", "中文", "日语", "阿拉伯语", "拉丁语", "希腊语"]
            },
            "母语": {
                "base": 0,
                "category": "学问",
                "description": "使用和理解母语的能力。初始值等于教育。"
            },
            "法律": {
                "base": 5,
                "category": "学问",
                "description": "了解法律体系和法律程序的学问。"
            },
            "图书馆使用": {
                "base": 20,
                "category": "学问",
                "description": "在图书馆或档案馆中查找信息的能力。"
            },
            "聆听": {
                "base": 20,
                "category": "感知",
                "description": "通过听觉获取信息的能力。"
            },
            "锁匠": {
                "base": 1,
                "category": "技能",
                "description": "开锁和制作钥匙的能力。"
            },
            "机械维修": {
                "base": 10,
                "category": "技能",
                "description": "修理和维护机械设备的能力。"
            },
            "医学": {
                "base": 1,
                "category": "学问",
                "description": "诊断和治疗疾病和伤害的学问。"
            },
            "博物学": {
                "base": 10,
                "category": "学问",
                "description": "了解自然世界、动植物和地质的学问。"
            },
            "导航": {
                "base": 10,
                "category": "技能",
                "description": "使用地图、指南针或天文观测来确定位置和方向的能力。"
            },
            "神秘学": {
                "base": 5,
                "category": "学问",
                "description": "了解超自然现象、魔法和神秘学的学问。"
            },
            "操作重型机械": {
                "base": 1,
                "category": "技能",
                "description": "操作大型机械设备的能力。"
            },
            "说服": {
                "base": 10,
                "category": "交际",
                "description": "通过逻辑和理性说服他人的能力。"
            },
            "驾驶": {
                "base": 1,
                "category": "技能",
                "description": "驾驶特定类型交通工具的能力。",
                "specializations": ["飞行器", "船", "火车"]
            },
            "精神分析": {
                "base": 1,
                "category": "学问",
                "description": "理解和治疗心理疾病的学问。"
            },
            "心理学": {
                "base": 10,
                "category": "学问",
                "description": "理解人类行为和动机的学问。"
            },
            "骑术": {
                "base": 5,
                "category": "技能",
                "description": "骑乘和控制马匹的能力。"
            },
            "科学": {
                "base": 1,
                "category": "学问",
                "description": "了解科学原理和方法的学问。",
                "specializations": ["天文学", "生物学", "植物学", "化学", "密码学", "工程学", "法医学", "地质学", "数学", "气象学", "药学", "物理学", "动物学"]
            },
            "妙手": {
                "base": 10,
                "category": "技能",
                "description": "进行精细手部操作的能力，如偷窃或魔术。"
            },
            "侦查": {
                "base": 25,
                "category": "感知",
                "description": "通过视觉观察发现线索和细节的能力。"
            },
            "潜行": {
                "base": 20,
                "category": "身体",
                "description": "隐藏和无声移动的能力。"
            },
            "生存": {
                "base": 10,
                "category": "技能",
                "description": "在野外环境中生存的能力。",
                "specializations": ["沙漠", "海洋", "极地", "森林", "山地", "沼泽"]
            },
            "游泳": {
                "base": 20,
                "category": "身体",
                "description": "在水中移动和保持漂浮的能力。"
            },
            "投掷": {
                "base": 20,
                "category": "身体",
                "description": "准确投掷物体的能力。"
            },
            "追踪": {
                "base": 10,
                "category": "技能",
                "description": "通过痕迹和线索追踪人或动物的能力。"
            }
        }
    
    @staticmethod
    def get_skill_categories():
        """获取所有技能分类"""
        return ["战斗", "交际", "移动", "学问", "感知", "操作", "隐秘", "生存", "其他"]
        
    def get_skill(self, skill_name):
        """获取指定技能信息
        
        Args:
            skill_name: 技能名称
        
        Returns:
            技能信息字典
        """
        if skill_name in self.skills:
            return self.skills[skill_name]
        
        # 如果在加载的数据中找不到，尝试从默认数据中获取
        default_skills = self.get_all_skills()
        if skill_name in default_skills:
            return default_skills[skill_name]
        
        return None
    
    def get_skills_by_category(self, category):
        """获取指定分类的所有技能
        
        Args:
            category: 技能分类
        
        Returns:
            技能字典列表
        """
        result = {}
        for name, skill in self.skills.items():
            if skill.get("category") == category:
                result[name] = skill
        return result 