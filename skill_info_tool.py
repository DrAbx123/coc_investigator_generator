#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
技能信息工具

一个命令行工具，用于显示技能信息和语言族群关系。
"""

import sys
import argparse
from core.skill_viewer import SkillViewer

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="技能信息查看工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 查看技能命令
    skill_parser = subparsers.add_parser("skill", help="查看技能信息")
    skill_parser.add_argument("name", help="技能名称")
    
    # 查看语言族群命令
    family_parser = subparsers.add_parser("family", help="查看语言族群信息")
    family_parser.add_argument("name", nargs="?", help="语言族群名称（可选）")
    
    # 列出技能命令
    list_parser = subparsers.add_parser("list", help="列出技能")
    list_parser.add_argument("category", nargs="?", help="技能类别（可选）")
    
    # 查看语言技能转移规则命令
    transfer_parser = subparsers.add_parser("transfer", help="查看语言技能转移规则")
    
    # 解析参数
    args = parser.parse_args()
    
    # 创建技能查看器
    skill_viewer = SkillViewer()
    
    # 处理命令
    if args.command == "skill":
        # 查看技能信息
        skill_info = skill_viewer.get_skill_description(args.name)
        print(f"\n技能：{skill_info['name']}")
        print(f"基础值：{skill_info['base_value']}%")
        print(f"类别：{skill_info['category']}")
        print(f"\n描述：\n{skill_info['description']}")
        
        # 如果有专攻，显示专攻信息
        if "specializations" in skill_info:
            print(f"\n可用专攻：")
            for spec in skill_info["specializations"]:
                print(f"- {spec}")
        
        # 如果是语言技能，显示语言族群信息
        if args.name == "语言" and "language_families" in skill_info:
            print("\n语言族群：")
            for family, langs in skill_info["language_families"].items():
                print(f"- {family}：{', '.join(langs)}")
        
        # 如果是语言专攻技能，显示所属族群和同族语言
        if "language_family" in skill_info:
            print(f"\n所属语系：{skill_info['language_family']}")
            print(f"同族语言：{', '.join(skill_info['same_family_languages'])}")
    
    elif args.command == "family":
        # 查看语言族群信息
        if args.name:
            # 查看特定族群
            languages = skill_viewer.get_language_family_info(args.name)
            if languages:
                print(f"\n语言族群：{args.name}")
                print(f"包含语言：{', '.join(languages)}")
            else:
                print(f"未找到语言族群：{args.name}")
        else:
            # 列出所有族群
            language_families = skill_viewer.get_language_families()
            print("\n所有语言族群：")
            for family, langs in language_families.items():
                print(f"\n- {family}：")
                for lang in langs:
                    print(f"  • {lang}")
    
    elif args.command == "list":
        # 列出技能
        skills_by_category = skill_viewer.list_skills_by_category(args.category)
        
        if not skills_by_category:
            print(f"未找到类别：{args.category}")
            return
        
        for category, skills in skills_by_category.items():
            print(f"\n{category}类技能：")
            for skill in skills:
                print(f"- {skill['name']} (基础值：{skill['base_value']}%)")
                print(f"  {skill['description']}")
    
    elif args.command == "transfer":
        # 显示语言技能转移规则
        print(skill_viewer.display_language_skill_transfer_rules())
    
    else:
        # 如果没有指定命令，显示帮助信息
        parser.print_help()

if __name__ == "__main__":
    main() 