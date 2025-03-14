#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

"""
疯狂系统模块

负责处理克苏鲁的呼唤第七版规则中的疯狂系统，包括：
- 临时性疯狂
- 不定性疯狂
- 永久性疯狂
- 恐惧症
- 狂躁症
"""

class InsanitySystem:
    """疯狂系统类"""
    
    def __init__(self, dice_roller=None):
        """初始化疯狂系统
        
        Args:
            dice_roller: 骰子工具对象，可选
        """
        self.dice_roller = dice_roller
    
    def set_dice_roller(self, dice_roller):
        """设置骰子工具
        
        Args:
            dice_roller: 骰子工具对象
        """
        self.dice_roller = dice_roller
    
    def roll_insanity_duration(self, insanity_type="temporary"):
        """掷骰确定疯狂持续时间
        
        Args:
            insanity_type: 疯狂类型，可选值为 "temporary" 或 "indefinite"
        
        Returns:
            str: 疯狂持续时间描述
        """
        if not self.dice_roller:
            # 如果没有骰子工具，返回默认值
            if insanity_type == "temporary":
                return "1D10轮"
            else:
                return "1D10 × 10小时"
        
        if insanity_type == "temporary":
            # 临时性疯狂持续1D10轮
            duration = self.dice_roller.roll("1D10")
            return f"{duration}轮"
        else:
            # 不定性疯狂持续1D10 × 10小时
            duration = self.dice_roller.roll("1D10") * 10
            return f"{duration}小时"
    
    def get_temporary_insanity(self):
        """获取随机临时性疯狂症状
        
        Returns:
            dict: 临时性疯狂症状
        """
        # 临时性疯狂表（1D10）
        temp_insanity_table = [
            {
                "name": "失忆",
                "description": "调查员陷入短暂的失忆状态。在这段时间内，他们不记得过去发生的一切，包括自己的名字、职业和与其他人之间的关系。甚至可能走开，随机游荡。",
                "recovery": "当疯狂结束时，调查员会慢慢恢复记忆，但可能会发现自己处于一个陌生的地方，不知道自己是如何到达那里的。"
            },
            {
                "name": "狂躁症",
                "description": "调查员体验到一种狂热的冲动，需要完成一些危险或不合理的行为，如纵火、自残、攻击他人等。这种冲动很难控制，调查员可能会采取极端行动来满足它。",
                "recovery": "当疯狂结束时，调查员会对自己的行为感到震惊和懊悔，可能需要处理由此造成的后果。"
            },
            {
                "name": "妄想",
                "description": "调查员相信一些虚假的事实，通常是与刚刚经历的超自然事件相关的。这些妄想可能包括认为自己已被选中或被诅咒，或者相信有人或某物正在追捕他们。",
                "recovery": "当疯狂结束时，调查员会意识到这些想法是不合理的，但可能仍会对它们有一种不安的感觉。"
            },
            {
                "name": "幻觉",
                "description": "调查员开始看到、听到或感觉到实际上并不存在的事物。这些幻觉通常是恐怖的，反映了调查员内心的恐惧和他们所面临的恐怖。",
                "recovery": "当疯狂结束时，幻觉会消失，但调查员可能会怀疑自己看到的其他事物的真实性。"
            },
            {
                "name": "歇斯底里",
                "description": "调查员陷入极度的情绪状态，可能表现为不受控制的笑声、哭泣或尖叫。他们可能无法控制自己的行为，并且通常会使自己暴露在危险之中。",
                "recovery": "当疯狂结束时，调查员会感到精疲力尽，可能需要一段时间才能完全恢复正常的情绪状态。"
            },
            {
                "name": "恐惧症",
                "description": "调查员突然变得非常恐惧某物或某种情况，这种恐惧是压倒性的，能迫使他们远离恐惧之源。典型的恐惧症包括幽闭恐惧症、恐高症和社交恐惧症。",
                "recovery": "当疯狂结束时，恐惧症会消退，但可能会在类似情况下重新出现。"
            },
            {
                "name": "恐慌",
                "description": "调查员被一种强烈的恐惧感所淹没，导致他们试图以任何必要的手段逃离当前情况。这可能包括丢弃武器、推开同伴或做出其他危险的行为。",
                "recovery": "当疯狂结束时，调查员会逐渐冷静下来，但可能会因自己的行为而感到羞愧，并需要处理任何潜在的后果。"
            },
            {
                "name": "偏执狂",
                "description": "调查员变得高度怀疑和不信任，认为周围的人和事物都有潜在的威胁。他们可能会将普通的行为解读为阴谋或袭击的前兆，并相应地做出反应。",
                "recovery": "当疯狂结束时，调查员的怀疑会减弱，但他们可能仍然对某些人或情况保持警惕。"
            },
            {
                "name": "昏厥",
                "description": "压力和恐惧使调查员失去意识，昏倒在地。在这段时间里，他们完全无助，容易受到任何附近威胁的伤害。",
                "recovery": "当疯狂结束时，调查员会逐渐恢复意识，但通常会感到头晕、困惑和虚弱。"
            },
            {
                "name": "暴力倾向",
                "description": "调查员被一种强烈的暴力冲动所控制，可能会攻击最近的个体，无论是朋友还是敌人。这种攻击通常是毫无顾忌和极其危险的。",
                "recovery": "当疯狂结束时，调查员会对自己的行为感到恐惧和懊悔，并可能需要处理由此造成的伤害或关系破裂。"
            }
        ]
        
        # 随机选择一个临时性疯狂
        if self.dice_roller:
            # 使用骰子工具
            roll = self.dice_roller.roll("1D10") - 1  # 转换为0-9的索引
        else:
            # 使用random模块
            roll = random.randint(0, 9)
        
        selected = temp_insanity_table[roll]
        
        # 添加持续时间
        duration = self.roll_insanity_duration("temporary")
        
        return {
            "type": "temporary",
            "name": selected["name"],
            "description": selected["description"],
            "recovery": selected["recovery"],
            "duration": duration,
            "roll": roll + 1  # 返回实际的掷骰结果（1-10）
        }
    
    def get_indefinite_insanity(self):
        """获取随机不定性疯狂症状
        
        Returns:
            dict: 不定性疯狂症状
        """
        # 不定性疯狂表（1D10）
        indef_insanity_table = [
            {
                "name": "健忘症",
                "description": "调查员遗忘了重要的记忆或个人信息。这可能包括自己的身份、重要事件或与恐怖相关的记忆。这种健忘可能是部分的或全面的。",
                "recovery": "记忆可能会慢慢恢复，但某些事件可能永远无法完全回忆起来。治疗可能需要心理治疗和时间。"
            },
            {
                "name": "躁郁症",
                "description": "调查员经历情绪的极端波动，从亢奋和自大到抑郁和绝望。这些情绪变化可能是突然的，并且难以预测，使社交互动和日常任务变得困难。",
                "recovery": "药物治疗和心理咨询可以帮助管理症状，但完全康复可能需要很长时间。"
            },
            {
                "name": "妄想症",
                "description": "调查员深深地相信一些虚假的事实，即使在面对矛盾证据的情况下也不会改变。这些妄想通常与神话实体或阴谋有关，可能导致危险或奇怪的行为。",
                "recovery": "妄想可能会随着时间的推移而减弱，尤其是在接受治疗的情况下，但它们可能永远不会完全消失。"
            },
            {
                "name": "幻觉",
                "description": "调查员持续体验到不存在的声音、图像或其他感觉。这些幻觉通常是恐怖的，并且与神话实体或事件有关，使日常生活变得困难。",
                "recovery": "药物治疗可以帮助减轻幻觉，但根本原因可能需要通过心理治疗来解决。"
            },
            {
                "name": "抑郁症",
                "description": "调查员经历持续的低落情绪、绝望和失去兴趣。这可能导致他们退缩社交活动，忽视个人卫生，并可能有自杀想法。",
                "recovery": "抑郁症可以通过药物治疗和心理咨询来管理，但可能需要持续的支持和监督。"
            },
            {
                "name": "恐惧症",
                "description": "调查员发展出对特定物体、生物或情况的强烈、不合理的恐惧。这种恐惧是如此强烈，以至于调查员会尽一切可能避开恐惧之源。",
                "recovery": "通过系统减敏和认知行为疗法，恐惧症可以被克服，但可能需要时间和专业帮助。"
            },
            {
                "name": "创伤后应激障碍",
                "description": "调查员经常重温创伤事件，通过噩梦、闪回或入侵性记忆。他们可能对类似的刺激反应过度，并会避免与创伤相关的情况。",
                "recovery": "PTSD可以通过专门的心理治疗和支持小组来管理，但症状可能会持续多年。"
            },
            {
                "name": "被害妄想症",
                "description": "调查员相信他们正在被神秘力量、政府或其他实体监视、跟踪或迫害。这种信念会导致极度的不信任和社交孤立。",
                "recovery": "被害妄想可能很难治疗，通常需要药物治疗和长期心理咨询的结合。"
            },
            {
                "name": "精神分裂症",
                "description": "调查员经历现实感扭曲，可能伴有幻觉、妄想和思维障碍。这种状况严重影响社交功能和日常生活能力。",
                "recovery": "精神分裂症通常需要终身管理，包括药物治疗、心理治疗和社会支持。"
            },
            {
                "name": "解离性身份障碍",
                "description": "调查员发展出多个不同的人格状态，每个都有自己独特的特征、记忆和行为。这些人格可能会在压力或触发条件下交替出现。",
                "recovery": "治疗通常集中在整合不同的人格状态，这是一个复杂且长期的过程，需要专业的心理健康支持。"
            }
        ]
        
        # 随机选择一个不定性疯狂
        if self.dice_roller:
            # 使用骰子工具
            roll = self.dice_roller.roll("1D10") - 1  # 转换为0-9的索引
        else:
            # 使用random模块
            roll = random.randint(0, 9)
        
        selected = indef_insanity_table[roll]
        
        # 添加持续时间
        duration = self.roll_insanity_duration("indefinite")
        
        return {
            "type": "indefinite",
            "name": selected["name"],
            "description": selected["description"],
            "recovery": selected["recovery"],
            "duration": duration,
            "roll": roll + 1  # 返回实际的掷骰结果（1-10）
        }
    
    def get_phobia(self):
        """获取随机恐惧症
        
        Returns:
            dict: 恐惧症信息
        """
        # 恐惧症表
        phobias = [
            {"name": "飞行恐惧症", "description": "对飞行的恐惧", "trigger": "乘坐飞机或其他飞行器"},
            {"name": "高空恐惧症", "description": "对高处的恐惧", "trigger": "处于高处或看到高空景象"},
            {"name": "尖锐物恐惧症", "description": "对尖锐物体的恐惧", "trigger": "看到或接触刀、针等尖锐物体"},
            {"name": "气味恐惧症", "description": "对气味的恐惧", "trigger": "闻到特定的气味"},
            {"name": "幽闭恐惧症", "description": "对封闭空间的恐惧", "trigger": "处于封闭或狭小的空间"},
            {"name": "广场恐惧症", "description": "对开放空间的恐惧", "trigger": "处于开放、空旷的场所"},
            {"name": "湖水恐惧症", "description": "对湖泊的恐惧", "trigger": "看到或接近湖泊"},
            {"name": "海洋恐惧症", "description": "对大海的恐惧", "trigger": "看到或接近海洋"},
            {"name": "血液恐惧症", "description": "对血液的恐惧", "trigger": "看到或接触血液"},
            {"name": "人群恐惧症", "description": "对人群的恐惧", "trigger": "处于人群中或看到大量人群"},
            {"name": "狗恐惧症", "description": "对狗的恐惧", "trigger": "看到或听到狗"},
            {"name": "雷电恐惧症", "description": "对雷电的恐惧", "trigger": "遇到雷雨或听到雷声"},
            {"name": "死亡恐惧症", "description": "对死亡的恐惧", "trigger": "看到死亡相关的事物或思考死亡"},
            {"name": "疾病恐惧症", "description": "对疾病的恐惧", "trigger": "接触可能携带疾病的人或物"},
            {"name": "蛇恐惧症", "description": "对蛇的恐惧", "trigger": "看到或想象蛇"},
            {"name": "陌生人恐惧症", "description": "对陌生人的恐惧", "trigger": "遇到或需要与陌生人交流"},
            {"name": "黑暗恐惧症", "description": "对黑暗的恐惧", "trigger": "处于黑暗环境或夜晚"},
            {"name": "深水恐惧症", "description": "对深水的恐惧", "trigger": "处于或看到深水区"},
            {"name": "桥梁恐惧症", "description": "对桥梁的恐惧", "trigger": "需要通过桥梁"},
            {"name": "昆虫恐惧症", "description": "对昆虫的恐惧", "trigger": "看到或接触昆虫"}
        ]
        
        # 随机选择一个恐惧症
        selected = random.choice(phobias)
        
        return {
            "type": "phobia",
            "name": selected["name"],
            "description": selected["description"],
            "trigger": selected["trigger"],
            "effect": "当调查员遇到恐惧症的触发条件时，需要进行理智检定。如果失败，调查员会尝试逃离或避开恐惧源，可能会做出不理性的行为。"
        }
    
    def get_mania(self):
        """获取随机狂躁症
        
        Returns:
            dict: 狂躁症信息
        """
        # 狂躁症表
        manias = [
            {"name": "纵火狂", "description": "控制不住放火的冲动", "trigger": "有机会纵火时"},
            {"name": "偷窃狂", "description": "控制不住偷窃的冲动", "trigger": "看到没有被监视的贵重物品"},
            {"name": "关系妄想狂", "description": "相信普通事件与自己有特殊关联", "trigger": "遇到巧合或普通事件"},
            {"name": "嫉妒狂", "description": "对他人产生不合理的嫉妒", "trigger": "看到他人获得关注或成功"},
            {"name": "臆想狂", "description": "有不切实际的伟大想法或能力", "trigger": "面对挑战或需要证明自己时"},
            {"name": "恋物狂", "description": "对特定物品有性吸引力", "trigger": "看到或接触特定物品"},
            {"name": "宗教狂", "description": "对宗教有极端热情", "trigger": "讨论宗教或神话相关话题"},
            {"name": "自虐狂", "description": "从伤害自己中获得满足", "trigger": "处于压力或孤独状态"},
            {"name": "窥阴癖", "description": "偷窥他人私密行为的冲动", "trigger": "有机会偷窥时"},
            {"name": "抢劫狂", "description": "对抢劫有不可抗拒的冲动", "trigger": "看到可能的抢劫目标"},
            {"name": "旋转狂", "description": "无法控制地旋转或看着物体旋转", "trigger": "压力情况或看到旋转物体"},
            {"name": "妄想狂", "description": "持有不合理的妄想", "trigger": "面对质疑或怀疑时"},
            {"name": "杀人狂", "description": "有杀人的冲动", "trigger": "感到被威胁或看到潜在受害者"},
            {"name": "被赶走恐惧症", "description": "害怕被驱逐出社交圈", "trigger": "社交场合或群体讨论"},
            {"name": "过度洁癖", "description": "对清洁有不健康的执着", "trigger": "接触被认为不干净的物体或环境"},
            {"name": "向往病痛狂", "description": "渴望生病或受伤", "trigger": "受到医疗关注或看到他人获得同情"},
            {"name": "夸大狂", "description": "过度夸大事实或自我能力", "trigger": "讲述经历或能力时"},
            {"name": "自恋狂", "description": "对自己过度痴迷", "trigger": "照镜子或成为关注焦点"},
            {"name": "收集癖", "description": "无法控制地收集特定物品", "trigger": "看到收集目标或有机会获取"},
            {"name": "暴食症", "description": "无法控制地暴饮暴食", "trigger": "面对食物或压力情况"}
        ]
        
        # 随机选择一个狂躁症
        selected = random.choice(manias)
        
        return {
            "type": "mania",
            "name": selected["name"],
            "description": selected["description"],
            "trigger": selected["trigger"],
            "effect": "当调查员遇到狂躁症的触发条件时，需要进行意志检定。如果失败，调查员会被强迫执行与狂躁症相关的行为，可能导致危险或尴尬的情况。"
        }
    
    def apply_insanity(self, investigator):
        """为调查员应用适当的疯狂效果
        
        Args:
            investigator: 调查员对象
            
        Returns:
            dict: 应用的疯狂效果
        """
        # 检查调查员的疯狂状态
        if investigator.permanent_insanity:
            # 永久性疯狂 - 生成随机恐惧症和狂躁症
            phobia = self.get_phobia()
            mania = self.get_mania()
            
            # 添加到调查员的状态中
            if phobia["name"] not in investigator.phobias:
                investigator.phobias.append(phobia["name"])
            
            if mania["name"] not in investigator.manias:
                investigator.manias.append(mania["name"])
            
            return {
                "type": "permanent",
                "phobia": phobia,
                "mania": mania,
                "message": "调查员的理智已完全崩溃，患上了永久性疯狂。"
            }
        
        elif investigator.indefinite_insanity:
            # 不定性疯狂
            insanity = self.get_indefinite_insanity()
            investigator.status = f"不定性疯狂：{insanity['name']}"
            
            return {
                "type": "indefinite",
                "insanity": insanity,
                "message": f"调查员陷入不定性疯狂状态：{insanity['name']}，预计持续{insanity['duration']}。"
            }
        
        elif investigator.temporary_insanity:
            # 临时性疯狂
            insanity = self.get_temporary_insanity()
            investigator.status = f"临时性疯狂：{insanity['name']}"
            
            return {
                "type": "temporary",
                "insanity": insanity,
                "message": f"调查员陷入临时性疯狂状态：{insanity['name']}，预计持续{insanity['duration']}。"
            }
        
        else:
            # 没有疯狂状态
            return {
                "type": "none",
                "message": "调查员目前精神状态正常。"
            }
    
    def recover_from_insanity(self, investigator):
        """尝试从疯狂状态恢复
        
        Args:
            investigator: 调查员对象
            
        Returns:
            dict: 恢复结果
        """
        # 检查调查员的疯狂状态
        if investigator.permanent_insanity:
            # 永久性疯狂无法恢复
            return {
                "success": False,
                "message": "永久性疯狂无法自行恢复，需要长期专业治疗。"
            }
        
        elif investigator.indefinite_insanity:
            # 不定性疯狂 - 进行POW检定
            pow_check = False
            if self.dice_roller:
                roll = self.dice_roller.roll("1D100")
                pow_check = roll <= investigator.attributes.get("意志", 0)
            else:
                # 没有骰子工具，假设有20%的恢复几率
                pow_check = random.random() < 0.2
            
            if pow_check:
                # 恢复成功
                investigator.indefinite_insanity = False
                investigator.status = "正常" if not investigator.temporary_insanity else "临时性疯狂"
                
                return {
                    "success": True,
                    "message": "调查员成功从不定性疯狂中恢复。"
                }
            else:
                # 恢复失败
                return {
                    "success": False,
                    "message": "调查员仍处于不定性疯狂状态。"
                }
        
        elif investigator.temporary_insanity:
            # 临时性疯狂 - 持续时间结束后自动恢复
            # 在实际游戏中，这通常由裁判根据时间流逝决定
            investigator.temporary_insanity = False
            investigator.status = "正常"
            
            return {
                "success": True,
                "message": "调查员从临时性疯狂中恢复。"
            }
        
        else:
            # 没有疯狂状态
            return {
                "success": True,
                "message": "调查员精神状态正常，无需恢复。"
            } 