#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Occupations:
    """职业数据类"""
    
    def __init__(self):
        """初始化职业数据"""
        self.occupations = {}
    
    def load_occupations(self, file_path):
        """从文件加载职业数据
        
        Args:
            file_path: 职业数据文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.occupations = json.load(f)
            return True
        except Exception as e:
            print(f"加载职业数据失败: {e}")
            # 使用默认职业数据
            self.occupations = self.get_all_occupations()
            return False
    
    def get_occupation(self, occupation_name):
        """获取指定职业
        
        Args:
            occupation_name: 职业名称
        
        Returns:
            职业数据字典
        """
        return self.occupations.get(occupation_name, None)
    
    def calculate_skill_points(self, occupation_name, edu):
        """计算职业技能点
        
        Args:
            occupation_name: 职业名称
            edu: 教育值
        
        Returns:
            技能点数
        """
        occupation = self.get_occupation(occupation_name)
        if not occupation:
            return 0
        
        skill_points_formula = occupation.get("skill_points", "")
        
        # 解析技能点公式
        if "教育×4" in skill_points_formula:
            return edu * 4
        elif "教育×2+敏捷×2" in skill_points_formula:
            # 由于我们没有敏捷值，暂时使用教育值的一半作为敏捷值
            dex = edu // 2
            return edu * 2 + dex * 2
        elif "教育×2+力量×2" in skill_points_formula:
            # 由于我们没有力量值，暂时使用教育值的一半作为力量值
            str_val = edu // 2
            return edu * 2 + str_val * 2
        elif "教育×2+外貌×2" in skill_points_formula:
            # 由于我们没有外貌值，暂时使用教育值的一半作为外貌值
            app = edu // 2
            return edu * 2 + app * 2
        else:
            # 默认返回教育值的4倍
            return edu * 4
    
    @staticmethod
    def get_all_occupations():
        """获取所有职业"""
        return {
            "古文物学家/古董收藏家": {
                "description": "【原作向】",
                "skills": ["估价", "艺术与手艺（任一）", "历史", "图书馆使用", "其他语言", "一种社交技能（取悦、话术、恐吓或说服）", "侦查", "自选一技能"],
                "credit_rating": (30, 70),
                "skill_points": "教育×4"
            },
            "艺术家": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "历史或博物学", "一种社交技能（取悦、话术、恐吓或说服）", "其他语言", "心理学", "侦查", "自选二技能"],
                "credit_rating": (9, 50),
                "skill_points": "教育×2+敏捷×2"
            },
            "运动员": {
                "description": "",
                "skills": ["攀爬", "跳跃", "格斗（斗殴）", "骑乘或游泳", "一种社交技能（取悦、话术、恐吓或说服）", "投掷", "自选二技能"],
                "credit_rating": (9, 70),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "作家（原作向）": {
                "description": "【原作向】",
                "skills": ["艺术（文学）", "历史", "图书馆使用", "博物学或神秘学", "其他语言", "心理学", "自选二技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "酒保": {
                "description": "",
                "skills": ["会计", "取悦", "格斗（斗殴）", "聆听", "心理学", "侦查", "自选二技能"],
                "credit_rating": (8, 25),
                "skill_points": "教育×2+外貌×2"
            },
            "猎人": {
                "description": "",
                "skills": ["弓术或手枪", "潜行", "聆听", "博物学", "导航", "生存（任一）", "追踪", "自选一技能"],
                "credit_rating": (20, 50),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "书商": {
                "description": "",
                "skills": ["会计", "估价", "艺术与手艺（任一）", "历史", "图书馆使用", "其他语言", "说服", "自选一技能"],
                "credit_rating": (20, 40),
                "skill_points": "教育×4"
            },
            "赏金猎人": {
                "description": "",
                "skills": ["汽车驾驶", "电气维修", "格斗（斗殴）", "射击（任一）", "恐吓", "法律", "心理学", "追踪"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "神职人员": {
                "description": "",
                "skills": ["会计", "历史", "图书馆使用", "聆听", "其他语言", "说服", "心理学", "自选一技能"],
                "credit_rating": (9, 60),
                "skill_points": "教育×4"
            },
            "计算机程序员/黑客": {
                "description": "",
                "skills": ["计算机使用", "电气维修", "电子学", "图书馆使用", "一种社交技能（取悦、话术、恐吓或说服）", "侦查", "自选二技能"],
                "credit_rating": (10, 70),
                "skill_points": "教育×4"
            },
            "罪犯": {
                "description": "",
                "skills": ["艺术与手艺（表演）", "乔装", "格斗（斗殴）", "射击（手枪）", "恐吓", "锁匠", "妙手", "潜行"],
                "credit_rating": (5, 65),
                "skill_points": "教育×2+敏捷×2"
            },
            "厨师": {
                "description": "",
                "skills": ["会计", "艺术与手艺（烹饪）", "取悦", "格斗（斗殴）", "聆听", "博物学", "侦查", "自选一技能"],
                "credit_rating": (9, 40),
                "skill_points": "教育×2+敏捷×2"
            },
            "设计师": {
                "description": "",
                "skills": ["会计", "艺术与手艺（任一）", "计算机使用", "手艺（任一）", "历史", "图书馆使用", "说服", "侦查"],
                "credit_rating": (20, 60),
                "skill_points": "教育×2+敏捷×2"
            },
            "业余艺术爱好者": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "历史", "图书馆使用", "其他语言", "一种社交技能（取悦、话术、恐吓或说服）", "自选三技能"],
                "credit_rating": (50, 99),
                "skill_points": "教育×2+外貌×2"
            },
            "医生（医学博士）": {
                "description": "",
                "skills": ["急救", "其他语言（拉丁文）", "医学", "心理学", "科学（生物学）", "科学（药学）", "自选二技能"],
                "credit_rating": (30, 80),
                "skill_points": "教育×4"
            },
            "司机": {
                "description": "",
                "skills": ["机械维修", "导航", "一种社交技能（取悦、话术、恐吓或说服）", "汽车驾驶", "电气维修", "聆听", "自选二技能"],
                "credit_rating": (9, 20),
                "skill_points": "教育×2+敏捷×2"
            },
            "编辑": {
                "description": "",
                "skills": ["艺术与手艺（摄影）", "历史", "图书馆使用", "其他语言", "一种社交技能（取悦、话术、恐吓或说服）", "心理学", "自选二技能"],
                "credit_rating": (10, 30),
                "skill_points": "教育×4"
            },
            "工程师": {
                "description": "",
                "skills": ["艺术与手艺（技术制图）", "电气维修", "机械维修", "操作重型机械", "物理", "自选三技能"],
                "credit_rating": (30, 60),
                "skill_points": "教育×4"
            },
            "艺人": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "乔装", "取悦", "聆听", "心理学", "自选三技能"],
                "credit_rating": (9, 70),
                "skill_points": "教育×2+外貌×2"
            },
            "农民": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "驯兽", "机械维修", "博物学", "操作重型机械", "科学（植物学）", "自选二技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "特工/间谍": {
                "description": "",
                "skills": ["艺术与手艺（摄影）", "乔装", "电气维修", "聆听", "其他语言", "心理学", "妙手", "潜行"],
                "credit_rating": (20, 60),
                "skill_points": "教育×2+外貌×2或敏捷×2"
            },
            "消防员": {
                "description": "",
                "skills": ["攀爬", "闪避", "急救", "格斗（斗殴）", "机械维修", "操作重型机械", "投掷", "自选一技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+力量×2"
            },
            "赌徒": {
                "description": "",
                "skills": ["会计", "取悦", "话术", "聆听", "心理学", "侦查", "妙手", "自选一技能"],
                "credit_rating": (9, 50),
                "skill_points": "教育×2+外貌×2或敏捷×2"
            },
            "黑帮成员": {
                "description": "",
                "skills": ["格斗（斗殴）", "射击（手枪）", "恐吓", "一种社交技能（取悦、话术或说服）", "汽车驾驶", "聆听", "妙手", "潜行"],
                "credit_rating": (9, 50),
                "skill_points": "教育×2+力量×2或敏捷×2"
            },
            "绅士/淑女": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "历史", "其他语言", "骑乘", "一种社交技能（取悦、话术、恐吓或说服）", "自选三技能"],
                "credit_rating": (40, 90),
                "skill_points": "教育×2+外貌×2"
            },
            "游民": {
                "description": "",
                "skills": ["攀爬", "跳跃", "聆听", "导航", "一种社交技能（取悦、话术、恐吓或说服）", "潜行", "生存（任一）", "游泳"],
                "credit_rating": (0, 5),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "记者（原作向）": {
                "description": "【原作向】",
                "skills": ["艺术与手艺（摄影）", "历史", "图书馆使用", "其他语言", "一种社交技能（取悦、话术、恐吓或说服）", "心理学", "自选二技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "律师": {
                "description": "",
                "skills": ["会计", "法律", "图书馆使用", "一种社交技能（取悦、话术、恐吓或说服）", "心理学", "自选三技能"],
                "credit_rating": (30, 80),
                "skill_points": "教育×4"
            },
            "图书馆管理员（原作向）": {
                "description": "【原作向】",
                "skills": ["会计", "图书馆使用", "其他语言", "自选五技能"],
                "credit_rating": (9, 35),
                "skill_points": "教育×4"
            },
            "技师": {
                "description": "",
                "skills": ["艺术与手艺（技术制图）", "电气维修", "图书馆使用", "机械维修", "操作重型机械", "物理", "自选二技能"],
                "credit_rating": (9, 40),
                "skill_points": "教育×4"
            },
            "军官": {
                "description": "",
                "skills": ["会计", "射击（步枪/霰弹枪）", "恐吓", "导航", "说服", "心理学", "生存（任一）", "自选一技能"],
                "credit_rating": (20, 70),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "传教士": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "急救", "机械维修", "医学", "博物学", "说服", "心理学", "生存（任一）"],
                "credit_rating": (0, 30),
                "skill_points": "教育×4"
            },
            "音乐家": {
                "description": "",
                "skills": ["艺术与手艺（乐器）", "取悦", "聆听", "心理学", "自选四技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2"
            },
            "护士": {
                "description": "",
                "skills": ["急救", "聆听", "医学", "心理学", "科学（生物学）", "侦查", "自选二技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "神秘学家": {
                "description": "",
                "skills": ["人类学", "历史", "图书馆使用", "神秘学", "其他语言", "一种社交技能（取悦、话术、恐吓或说服）", "心理学", "自选一技能"],
                "credit_rating": (9, 65),
                "skill_points": "教育×4"
            },
            "旅行家/探险家": {
                "description": "",
                "skills": ["攀爬", "射击（步枪/霰弹枪）", "历史", "跳跃", "博物学", "导航", "生存（任一）", "游泳"],
                "credit_rating": (30, 70),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "摄影师": {
                "description": "",
                "skills": ["艺术与手艺（摄影）", "取悦", "心理学", "侦查", "潜行", "自选三技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "飞行员": {
                "description": "",
                "skills": ["电气维修", "机械维修", "导航", "操作重型机械", "驾驶（飞行器）", "科学（天文学）", "生存（任一）", "自选一技能"],
                "credit_rating": (20, 70),
                "skill_points": "教育×2+敏捷×2"
            },
            "警察": {
                "description": "",
                "skills": ["艺术与手艺（表演）", "格斗（斗殴）", "射击（手枪）", "急救", "恐吓", "法律", "心理学", "追踪"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+力量×2或敏捷×2"
            },
            "私家侦探": {
                "description": "",
                "skills": ["艺术与手艺（摄影）", "乔装", "法律", "图书馆使用", "说服", "心理学", "侦查", "潜行"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "教授（原作向）": {
                "description": "【原作向】",
                "skills": ["图书馆使用", "其他语言", "自选六技能"],
                "credit_rating": (20, 70),
                "skill_points": "教育×4"
            },
            "精神病医生（原作向）": {
                "description": "【原作向】",
                "skills": ["聆听", "医学", "其他语言", "心理学", "精神分析", "自选三技能"],
                "credit_rating": (30, 80),
                "skill_points": "教育×4"
            },
            "研究员": {
                "description": "",
                "skills": ["图书馆使用", "其他语言", "自选六技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "水手": {
                "description": "",
                "skills": ["艺术与手艺（任一）", "格斗（斗殴）", "机械维修", "博物学", "导航", "驾驶（船）", "游泳", "投掷"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "推销员": {
                "description": "",
                "skills": ["会计", "取悦", "话术", "汽车驾驶", "聆听", "心理学", "自选二技能"],
                "credit_rating": (9, 40),
                "skill_points": "教育×2+外貌×2"
            },
            "科学家": {
                "description": "",
                "skills": ["图书馆使用", "其他语言", "科学（任一）", "科学（任一）", "科学（任一）", "自选三技能"],
                "credit_rating": (9, 70),
                "skill_points": "教育×4"
            },
            "秘书": {
                "description": "",
                "skills": ["会计", "艺术与手艺（打字）", "取悦", "历史", "图书馆使用", "其他语言", "说服", "自选一技能"],
                "credit_rating": (9, 30),
                "skill_points": "教育×4"
            },
            "店老板": {
                "description": "",
                "skills": ["会计", "取悦", "格斗（斗殴）", "聆听", "说服", "心理学", "侦查", "自选一技能"],
                "credit_rating": (20, 40),
                "skill_points": "教育×2+外貌×2"
            },
            "士兵": {
                "description": "",
                "skills": ["攀爬", "闪避", "格斗（斗殴）", "射击（步枪/霰弹枪）", "潜行", "生存（任一）", "游泳", "投掷"],
                "credit_rating": (9, 30),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "部落成员": {
                "description": "",
                "skills": ["攀爬", "格斗（斗殴）", "聆听", "博物学", "导航", "侦查", "生存（任一）", "游泳或投掷"],
                "credit_rating": (0, 15),
                "skill_points": "教育×2+敏捷×2或力量×2"
            },
            "殡葬师": {
                "description": "",
                "skills": ["会计", "艺术与手艺（任一）", "汽车驾驶", "历史", "说服", "心理学", "科学（生物学）", "自选一技能"],
                "credit_rating": (20, 40),
                "skill_points": "教育×4"
            },
            "工会活动家": {
                "description": "",
                "skills": ["会计", "格斗（斗殴）", "历史", "恐吓", "聆听", "说服", "心理学", "自选一技能"],
                "credit_rating": (9, 50),
                "skill_points": "教育×2+外貌×2或力量×2"
            },
            "服务生": {
                "description": "",
                "skills": ["会计", "艺术与手艺（任一）", "取悦", "聆听", "其他语言", "心理学", "侦查", "自选一技能"],
                "credit_rating": (9, 20),
                "skill_points": "教育×2+外貌×2"
            },
            "白领工人/管理者": {
                "description": "",
                "skills": ["会计", "取悦", "法律", "聆听", "说服", "心理学", "自选二技能"],
                "credit_rating": (9, 50),
                "skill_points": "教育×4"
            },
            "狂热者": {
                "description": "",
                "skills": ["历史", "恐吓", "说服", "心理学", "潜行", "自选三技能"],
                "credit_rating": (0, 30),
                "skill_points": "教育×2+外貌×2"
            },
            "动物园管理员": {
                "description": "",
                "skills": ["会计", "驯兽", "闪避", "格斗（斗殴）", "急救", "博物学", "科学（动物学）", "兽医学"],
                "credit_rating": (9, 40),
                "skill_points": "教育×4"
            }
        } 