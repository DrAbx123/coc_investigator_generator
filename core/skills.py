#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from enum import Enum

"""
技能管理模块

负责处理克苏鲁的呼唤第七版规则中的技能系统，包括：
- 技能加载和管理
- 技能检定规则实现
- 技能专攻系统
- 技能成长系统
- 孤注一掷机制

技能分类:
- 知识类：如历史、科学等学术性技能
- 社交类：取悦、话术、恐吓、说服等互动技能
- 战斗类：格斗、射击等战斗相关技能
- 感知类：侦查、聆听等感知能力
- 身体类：闪避、游泳、攀爬等身体技能
- 技能类：急救、驾驶、机械维修等专业技能

难度等级:
- 常规难度：检定值需小于等于技能值
- 困难难度：检定值需小于等于技能值的一半
- 极难难度：检定值需小于等于技能值的五分之一
"""

class DifficultyLevel(Enum):
    """技能检定难度等级"""
    REGULAR = 1      # 常规难度
    HARD = 2         # 困难难度
    EXTREME = 3      # 极难难度

class SkillCheckResult(Enum):
    """技能检定结果"""
    CRITICAL_SUCCESS = 1  # 大成功
    HARD_SUCCESS = 2      # 困难成功
    SUCCESS = 3           # 成功
    FAILURE = 4           # 失败
    CRITICAL_FAILURE = 5  # 大失败

class Skills:
    """技能数据类"""

    def __init__(self):
        """初始化技能数据"""
        self.skills = {}
        self.skill_categories = ["知识", "社交", "战斗", "感知", "身体", "技能"]

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

    def get_skill_categories(self):
        """获取所有技能分类"""
        return self.skill_categories

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

    def get_skill_info(self, skill_name):
        """获取指定技能信息（get_skill的别名）

        Args:
            skill_name: 技能名称

        Returns:
            技能信息字典
        """
        return self.get_skill(skill_name)

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

    def check_skill(self, skill_value, difficulty=DifficultyLevel.REGULAR, bonus_dice=0, penalty_dice=0):
        """进行技能检定

        Args:
            skill_value: 技能值
            difficulty: 难度等级
            bonus_dice: 奖励骰数量
            penalty_dice: 惩罚骰数量

        Returns:
            (roll_result, check_result): 骰子结果和检定结果枚举
        """
        # 计算有效骰子数量（奖励骰-惩罚骰）
        effective_dice = bonus_dice - penalty_dice

        # 进行掷骰
        if effective_dice == 0:
            # 常规掷骰
            roll_result = random.randint(1, 100)
        else:
            # 有奖励骰或惩罚骰的情况
            rolls = [random.randint(1, 100)]
            for _ in range(abs(effective_dice)):
                rolls.append(random.randint(1, 100))

            # 奖励骰取最低值，惩罚骰取最高值
            if effective_dice > 0:
                roll_result = min(rolls)
            else:
                roll_result = max(rolls)

        # 根据难度等级确定目标值
        if difficulty == DifficultyLevel.REGULAR:
            target = skill_value
        elif difficulty == DifficultyLevel.HARD:
            target = skill_value // 2
        elif difficulty == DifficultyLevel.EXTREME:
            target = skill_value // 5
        else:
            target = skill_value

        # 确定成功等级
        if roll_result == 1 or (roll_result <= 5 and roll_result <= skill_value):
            return roll_result, SkillCheckResult.CRITICAL_SUCCESS
        elif roll_result <= target:
            if roll_result <= skill_value // 5:
                return roll_result, SkillCheckResult.EXTREME_SUCCESS
            elif roll_result <= skill_value // 2:
                return roll_result, SkillCheckResult.HARD_SUCCESS
            else:
                return roll_result, SkillCheckResult.SUCCESS
        else:
            if roll_result >= 96 and skill_value < 50 or roll_result == 100:
                return roll_result, SkillCheckResult.CRITICAL_FAILURE
            else:
                return roll_result, SkillCheckResult.FAILURE

    def opposed_check(self, skill_value1, skill_value2):
        """进行对抗技能检定

        Args:
            skill_value1: 第一个技能值
            skill_value2: 第二个技能值

        Returns:
            (result1, result2, winner): 两个检定结果和胜者(1或2，平局为0)
        """
        # 进行两次技能检定
        roll1, result1 = self.check_skill(skill_value1)
        roll2, result2 = self.check_skill(skill_value2)

        # 判断胜者
        # 首先比较成功等级
        if result1.value < result2.value:
            winner = 1
        elif result2.value < result1.value:
            winner = 2
        else:
            # 成功等级相同，比较技能值
            if skill_value1 > skill_value2:
                winner = 1
            elif skill_value2 > skill_value1:
                winner = 2
            else:
                winner = 0  # 平局

        return (roll1, result1, roll2, result2, winner)

    def combined_check(self, skill_values, require_all=True):
        """进行组合技能检定

        Args:
            skill_values: 技能值列表
            require_all: 是否要求全部成功

        Returns:
            (results, success): 所有检定结果和整体是否成功的布尔值
        """
        results = []
        successes = 0

        # 进行所有技能检定
        for skill in skill_values:
            roll, result = self.check_skill(skill)
            results.append((roll, result))
            if result in [SkillCheckResult.CRITICAL_SUCCESS,
                         SkillCheckResult.HARD_SUCCESS,
                         SkillCheckResult.SUCCESS]:
                successes += 1

        # 判断整体成功与否
        if require_all:
            # 要求全部成功
            return results, successes == len(skill_values)
        else:
            # 要求任一成功
            return results, successes > 0

    def push_roll(self, skill_value):
        """进行孤注一掷检定

        Args:
            skill_value: 技能值

        Returns:
            (normal_roll, normal_result, push_roll, push_result): 正常检定和孤注一掷的结果
        """
        # 正常检定
        normal_roll, normal_result = self.check_skill(skill_value)

        # 只有失败时才能孤注一掷
        if normal_result in [SkillCheckResult.FAILURE, SkillCheckResult.CRITICAL_FAILURE]:
            # 孤注一掷检定
            push_roll, push_result = self.check_skill(skill_value)
            return normal_roll, normal_result, push_roll, push_result
        else:
            return normal_roll, normal_result, None, None

    def transfer_skill_bonus(self, specializations):
        """处理技能专攻间的转移加值

        这是可选规则：当一项专攻技能达到50%或90%时，
        相关专攻技能都可以获得10%的提升（上限为50%）

        Args:
            specializations: 专攻技能字典，格式为{专攻名: 技能值}

        Returns:
            更新后的专攻技能字典
        """
        result = specializations.copy()

        # 检查是否有专攻达到50%或90%
        has_fifty = any(value >= 50 for value in specializations.values())
        has_ninety = any(value >= 90 for value in specializations.values())

        if not has_fifty and not has_ninety:
            return result

        # 应用转移规则
        for spec_name, value in result.items():
            bonus = 0
            if has_fifty:
                bonus += 10
            if has_ninety:
                bonus += 10

            # 应用加值，但不超过50%
            if value < 50:
                result[spec_name] = min(50, value + bonus)

        return result

    @staticmethod
    def get_all_skills():
        """获取所有技能"""
        return {
            "会计": {
                "base_value": 5,
                "category": "知识",
                "description": "处理财务记录，发现账目中的不规则之处。",
                "difficulty": {
                    "regular": "检查简单的账目，发现明显的异常。",
                    "hard": "发现精心隐藏的账目问题，或分析复杂的财务记录。",
                    "extreme": "识别极其隐蔽的财务欺诈，或重构被故意销毁的账目。"
                },
                "opposed": ["会计"],
                "push": "花费更多时间重新检查账目；寻找其他证明文件；询问相关人员。",
                "push_failure": "被淹没在数字和细节中；被误导得出错误结论；惹上法律麻烦。"
            },
            "人类学": {
                "base_value": 1,
                "category": "知识",
                "description": "理解不同文化的习俗、信仰和社会结构。",
                "difficulty": {
                    "regular": "花费一个月或更长时间研究接触一个文化。",
                    "hard": "仅花费一周或更少时间研究一个文化。",
                    "extreme": "通过极少的接触判断一个完全陌生的文化。"
                },
                "opposed": ["人类学"],
                "push": "花更多时间研究目标；去'当地'体验一段时间；参与特定文化的仪式或活动。",
                "push_failure": "得出完全错误的结论；冒犯当地文化习俗；引起敌对反应。"
            },
            # ... 更多技能 ...
        }