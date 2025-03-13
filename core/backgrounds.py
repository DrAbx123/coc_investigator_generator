#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Background:
    """背景类"""
    
    def __init__(self):
        """初始化背景"""
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

class Backgrounds:
    """背景数据类"""
    
    def __init__(self):
        """初始化背景数据"""
        self.backgrounds = {}
    
    def load_backgrounds(self, file_path):
        """从文件加载背景数据
        
        Args:
            file_path: 背景数据文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.backgrounds = json.load(f)
            return True
        except Exception as e:
            print(f"加载背景数据失败: {e}")
            return False
    
    def get_random_background(self, dice_roller):
        """随机生成背景
        
        Args:
            dice_roller: 骰子工具
        
        Returns:
            随机生成的背景
        """
        background = Background()
        
        # 随机选择个人描述
        personal_descriptions = self.get_personal_descriptions()
        if personal_descriptions:
            index = dice_roller.roll_dice(1, len(personal_descriptions)) - 1
            background.personal_description = personal_descriptions[index]
        
        # 随机选择思想信念
        ideology_beliefs = self.get_ideology_beliefs()
        if ideology_beliefs:
            index = dice_roller.roll_dice(1, len(ideology_beliefs)) - 1
            background.ideology = ideology_beliefs[index]
        
        # 随机选择重要之人
        significant_people_who = self.get_significant_people_who()
        significant_people_why = self.get_significant_people_why()
        if significant_people_who and significant_people_why:
            who_index = dice_roller.roll_dice(1, len(significant_people_who)) - 1
            why_index = dice_roller.roll_dice(1, len(significant_people_why)) - 1
            background.significant_people = f"{significant_people_who[who_index]}\n{significant_people_why[why_index]}"
        
        # 随机选择意义非凡之地
        meaningful_locations = self.get_meaningful_locations()
        if meaningful_locations:
            index = dice_roller.roll_dice(1, len(meaningful_locations)) - 1
            background.meaningful_locations = meaningful_locations[index]
        
        # 随机选择宝贵之物
        treasured_possessions = self.get_treasured_possessions()
        if treasured_possessions:
            index = dice_roller.roll_dice(1, len(treasured_possessions)) - 1
            background.treasured_possessions = treasured_possessions[index]
        
        # 随机选择特质
        traits = self.get_traits()
        if traits:
            index = dice_roller.roll_dice(1, len(traits)) - 1
            background.traits = traits[index]
        
        # 随机生成创伤和疯狂
        if dice_roller.roll_dice(1, 10) <= 3:  # 30%的概率有创伤
            background.injuries_scars = "有一处旧伤或疤痕，提醒着你过去的危险经历。"
        else:
            background.injuries_scars = "没有明显的创伤或疤痕。"
        
        # 随机生成恐惧和狂热
        if dice_roller.roll_dice(1, 10) <= 2:  # 20%的概率有恐惧症
            phobias = ["高处恐惧症", "幽闭恐惧症", "血液恐惧症", "黑暗恐惧症", "水恐惧症", "昆虫恐惧症", "蛇恐惧症", "雷电恐惧症"]
            index = dice_roller.roll_dice(1, len(phobias)) - 1
            background.phobias_manias = f"你患有{phobias[index]}。"
        else:
            background.phobias_manias = "没有特别的恐惧症或狂热。"
        
        # 随机生成奥秘和邪教
        if dice_roller.roll_dice(1, 10) <= 1:  # 10%的概率接触过奥秘
            background.arcane_tomes_spells = "你曾经接触过一些神秘学知识，但并不深入。"
        else:
            background.arcane_tomes_spells = "你对超自然和神秘学一无所知。"
        
        # 生成背景故事
        background.background_story = "这是一个普通人的故事，直到他/她遇到了不可名状的恐怖..."
        
        return background
    
    @staticmethod
    def get_personal_descriptions():
        """获取形象描述列表"""
        return [
            "结实的", "英俊的", "笨拙的", "机灵的", "迷人的", "聪明的", "邋遢的", 
            "肮脏的", "耀眼的", "年轻的", "疲倦脸", "啤酒肚", "长头发", "优雅的", 
            "稀烂的", "苍白的", "阴沉的", "乐观的", "棕褐色", "古板的", "狐臭的", 
            "健壮的", "娇俏的", "魁梧的", "迟钝的", "娃娃脸", "死人脸", "书呆子", 
            "肥胖的", "苗条的", "矮壮的", "平庸的", "皱纹人", "狡猾的", "筋肉人", 
            "虚弱的"
        ]
    
    @staticmethod
    def get_ideology_beliefs():
        """获取思想/信念"""
        return [
            "你信仰并遵从一个良善的组织或教派。",
            "你信仰社会和政治的稳定和保守。",
            "你信仰人文主义和民主制度。",
            "传统和责任比其他东西都重要。",
            "人类无法抵挡自然的伟力。（例如进化论，弱肉强食）",
            "艺术与表达方式绝不能遭到约束。",
            "现代化和工业化是解决现代难题的钥匙。",
            "科学万能！科学万岁！你将选择其中之一。（例如进化论，低温学，太空探索）",
            "命中注定。（例如因果报应，种姓系统，超自然存在）",
            "社团或秘密结社的一员。（例如共济会，女协，匿名者）",
            "社会坏掉了，而你将成为正义的伙伴。应斩除之物是？（例如毒品，暴力，种族歧视）",
            "神秘依然在。（例如占星术，招魂术，塔罗）",
            "诸君，我喜欢政治。（例如保守党，共产党，自由党）",
            "\"金钱就是力量，我的朋友，我将竭尽全力获取我能看到的一切。\"（例如贪婪心，进取心，冷酷心）",
            "竞选者/激进主义者。（例如女权运动人，平等主义家，工会权柄）"
        ]
    
    @staticmethod
    def get_significant_people_who():
        """获取重要之人（是谁）列表"""
        return [
            "父辈。（例如母亲，父亲，继母）",
            "祖父辈。（例如外祖母，祖父）",
            "兄弟。（例如妹妹，半血亲妹妹，无血缘妹妹）",
            "孩子。（儿子或女儿）",
            "另一半。（例如配偶，未婚夫，爱人）",
            "那位指引你人生技能的人。指明该技能和该人。（例如学校教师，师傅，父亲）",
            "青梅竹马。（例如同学，邻居，幼驯染）",
            "名人。偶像或者英雄。当然也许你从未见过他。（例如电影明星，政治家，音乐家。）",
            "游戏中的另一位调查员伙伴。随机或自选。",
            "游戏中另一外ＮＰＣ。详情咨询你的守秘人。"
        ]
    
    @staticmethod
    def get_significant_people_why():
        """获取重要之人（为什么）列表"""
        return [
            "你欠了他们人情。他们帮助了你什么？（例如，经济上，困难时期的庇护，给你第一份工作）",
            "他们教会了你一些东西。（例如，技能，如何去爱，如何成为男子汉）",
            "他们给了你生命的意义。（例如，你渴望成为他们那样的人，你苦苦追寻着他们，你想让他们高兴）",
            "你曾害了他们，而现在寻求救赎。例如，偷窃了他们的钱财，向警方报告了他们的行踪，在他们绝望时拒绝救助）",
            "同甘共苦。（例如，你们共同经历过困难时期，你们携手成长，共同度过战争）",
            "你想向他们证明自己。（例如，自己找到工作，自己搞到老婆，自己考到学历）",
            "你崇拜他们。（例如，崇拜他们的名头，他们的魅力，他们的工作）",
            "后悔的感觉。（例如，你本应死在他们面前，你背弃了你的誓言，你在可以助人之时驻足不前）",
            "你试图证明你比他们更出色。他们的缺点是？（例如，懒惰，酗酒，冷漠）",
            "他们扰乱了你的人生，而你寻求复仇。发生了什么？（例如，射杀爱人之日，国破家亡之时，明镜两分之际）"
        ]
    
    @staticmethod
    def get_meaningful_locations():
        """获取意义非凡之地列表"""
        return [
            "你最爱的学府。（例如，中学，大学）",
            "你的故乡。（例如，乡下老家，小村镇，大都市）",
            "相识初恋之处。（例如，音乐会，度假村，核弹避难所）",
            "静思之地。（例如，图书馆，你的乡土别墅，钓场）",
            "社交之地。（例如，绅士俱乐部，地方酒吧，叔叔的家）",
            "联系你思想/信念的场所。（例如，小教堂，麦加，巨石阵）",
            "重要之人的坟墓。（例如，另一半，孩子，爱人）",
            "家族所在。（例如，乡下小屋，租屋，幼年的孤儿院）",
            "生命中最高兴时的所在。（例如，初吻时坐着的公园长椅，你的大学）",
            "工作地点。（例如，办公室，图书馆，银行）"
        ]
    
    @staticmethod
    def get_treasured_possessions():
        """获取宝贵之物列表"""
        return [
            "与你得意技相关之物。（例如华服，假ＩＤ卡，青铜指虎）",
            "职业必需品。（例如医疗包，汽车，撬锁器）",
            "童年的遗留物。（例如漫画书，随身小刀，幸运币）",
            "逝者遗物。（例如烛堡，钱包里的遗照，信）",
            "重要之人给予之物。（例如戒指，日志，地图）",
            "收藏品。（例如撤票，标本，记录）",
            "你发掘而不知真相的东西。答案追寻中。（例如，橱柜里找到的未知语言信件，一根奇怪的从父亲出继承来的来源不明的风琴，花园里挖出来的奇妙的银球）",
            "体育用品。（例如，球棒，签名棒球，鱼竿）",
            "武器。（例如，半自动左轮，老旧的猎用来福，靴刃）",
            "宠物。（例如狗，猫，乌龟）"
        ]
    
    @staticmethod
    def get_traits():
        """获取特质列表"""
        return [
            "慷慨大方。（例如，小费大手，及时雨，慈善家）",
            "善待动物。（例如，爱猫人士，农场出生，与马同舞）",
            "梦想家。（例如，惯常异想天开，预言家，创造者）",
            "享乐主义者。（例如，派对大师，酒吧醉汉，\"放纵到死\"）",
            "赌徒，冒险家。（例如，扑克脸，任何事都来一遍，活在生死边缘）",
            "好厨子，好吃货。（例如，烤得一手好蛋糕，无米之炊都能做好，优雅的食神）",
            "女人缘/万人迷。（例如，长袖善舞，甜言蜜语，电眼乱放）",
            "忠心在我。（例如，背负自己的朋友，从未破誓，为信念而死）",
            "好名头。（例如，村里最好的饭后聊天人士，虔信圣徒，不惧任何危险）",
            "雄心壮志。（例如，梦想远大，目标是成为ＢＯＳＳ，渴求一切）"
        ] 