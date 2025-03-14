#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
语言技能信息显示程序

这个程序提供了一个简单的界面来查看语言技能信息，
包括技能描述、语言族群、技能转移规则等。
"""

import sys
import argparse
from core.skill_viewer import SkillViewer
from core.skills import Skills
from core.investigator import Investigator

def show_language_skill_info():
    """显示语言技能信息"""
    print("\n===== 语言技能系统信息 =====\n")
    
    # 创建技能查看器
    skill_viewer = SkillViewer()
    
    # 获取语言技能信息
    language_info = skill_viewer.get_skill_description("语言")
    
    # 显示基本信息
    print(f"技能：{language_info['name']}")
    print(f"基础值：{language_info['base_value']}%")
    print(f"类别：{language_info['category']}")
    print(f"\n描述：\n{language_info['description']}")
    
    # 显示可用专攻
    if "specializations" in language_info:
        print(f"\n可用语言专攻：")
        for spec in language_info["specializations"]:
            print(f"- 语言（{spec}）")
    
    # 显示语言族群信息
    if "language_families" in language_info:
        print("\n语言族群关系：")
        for family, langs in language_info["language_families"].items():
            print(f"\n- {family}：")
            for lang in langs:
                print(f"  • {lang}")
    
    # 显示技能转移规则
    print("\n===== 语言技能转移规则 =====\n")
    print("1. 当一名角色首次将一门语言（除了母语）提升到50%，")
    print("   同系语言都会提升10%（但不会超过50%）。")
    print("2. 当角色首次将一门语言提升到90%，")
    print("   同系语言会再次提升10%（但不会高于90%）。")
    
    print("\n语言技能等级意义：")
    print("- 5%：能够正确地辨认出这门语言。")
    print("- 10%：可以交流简单的想法。")
    print("- 30%：可以对社交上的需求进行理解。")
    print("- 50%：可以进行流畅的交流。")
    print("- 75%：可以将这门语言说得像是本地人一样。")

def test_language_skill_transfer():
    """测试语言技能转移规则"""
    print("\n===== 语言技能转移规则测试 =====\n")
    
    # 创建技能查看器和调查员
    skills = Skills()
    skills.load_skills("data/skills.json")
    investigator = Investigator()
    
    # 设置初始语言技能
    print("设置初始语言技能...")
    investigator.add_skill("语言（英语）", 40)
    investigator.add_skill("语言（德语）", 20)
    investigator.add_skill("语言（荷兰语）", 15)
    investigator.add_skill("语言（法语）", 30)
    investigator.add_skill("语言（西班牙语）", 10)
    
    # 打印初始语言技能
    print("\n初始语言技能值:")
    print(f"英语: {investigator.skills.get('语言（英语）', 0)}%")
    print(f"德语: {investigator.skills.get('语言（德语）', 0)}%")
    print(f"荷兰语: {investigator.skills.get('语言（荷兰语）', 0)}%")
    print(f"法语: {investigator.skills.get('语言（法语）', 0)}%")
    print(f"西班牙语: {investigator.skills.get('语言（西班牙语）', 0)}%")
    
    # 增加英语技能到55%，应该触发50%阈值的技能转移规则
    print("\n增加英语技能到55%...")
    investigator.add_skill("语言（英语）", 55)
    
    # 打印更新后的语言技能
    print("\n达到50%阈值后的语言技能值:")
    print(f"英语: {investigator.skills.get('语言（英语）', 0)}%")
    print(f"德语: {investigator.skills.get('语言（德语）', 0)}%")
    print(f"荷兰语: {investigator.skills.get('语言（荷兰语）', 0)}%")
    print(f"法语: {investigator.skills.get('语言（法语）', 0)}%")
    print(f"西班牙语: {investigator.skills.get('语言（西班牙语）', 0)}%")
    
    # 检查其他可能受影响的语言
    print("\n检查其他可能受影响的语言:")
    print(f"瑞典语: {investigator.skills.get('语言（瑞典语）', 0)}%")
    print(f"挪威语: {investigator.skills.get('语言（挪威语）', 0)}%")
    print(f"丹麦语: {investigator.skills.get('语言（丹麦语）', 0)}%")
    
    # 增加英语技能到90%，应该触发90%阈值的技能转移规则
    print("\n增加英语技能到90%...")
    investigator.add_skill("语言（英语）", 90)
    
    # 打印更新后的语言技能
    print("\n达到90%阈值后的语言技能值:")
    print(f"英语: {investigator.skills.get('语言（英语）', 0)}%")
    print(f"德语: {investigator.skills.get('语言（德语）', 0)}%")
    print(f"荷兰语: {investigator.skills.get('语言（荷兰语）', 0)}%")
    print(f"法语: {investigator.skills.get('语言（法语）', 0)}%")
    print(f"西班牙语: {investigator.skills.get('语言（西班牙语）', 0)}%")
    
    # 检查其他可能受影响的语言
    print("\n检查其他可能受影响的语言:")
    print(f"瑞典语: {investigator.skills.get('语言（瑞典语）', 0)}%")
    print(f"挪威语: {investigator.skills.get('语言（挪威语）', 0)}%")
    print(f"丹麦语: {investigator.skills.get('语言（丹麦语）', 0)}%")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="语言技能信息显示程序")
    parser.add_argument("action", choices=["info", "test"], 
                        help="要执行的操作: info (显示信息) 或 test (测试技能转移)")
    
    # 解析参数
    args = parser.parse_args()
    
    if args.action == "info":
        show_language_skill_info()
    elif args.action == "test":
        test_language_skill_transfer()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 