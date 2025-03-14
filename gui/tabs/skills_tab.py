#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QGroupBox, QListWidget, QTextEdit, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox,
    QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class SkillsTab(QWidget):
    """技能标签页"""
    
    def __init__(self, parent):
        """初始化技能标签页"""
        super().__init__()
        
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建技能点信息组
        skill_points_group = QGroupBox("技能点信息")
        skill_points_layout = QGridLayout(skill_points_group)
        
        # 添加职业技能点信息
        skill_points_layout.addWidget(QLabel("职业技能点:"), 0, 0)
        self.occupation_skill_points = QLineEdit()
        self.occupation_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.occupation_skill_points, 0, 1)
        
        skill_points_layout.addWidget(QLabel("已分配职业技能点:"), 0, 2)
        self.allocated_occupation_skill_points = QLineEdit()
        self.allocated_occupation_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.allocated_occupation_skill_points, 0, 3)
        
        # 添加兴趣技能点信息
        skill_points_layout.addWidget(QLabel("兴趣技能点:"), 1, 0)
        self.interest_skill_points = QLineEdit()
        self.interest_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.interest_skill_points, 1, 1)
        
        skill_points_layout.addWidget(QLabel("已分配兴趣技能点:"), 1, 2)
        self.allocated_interest_skill_points = QLineEdit()
        self.allocated_interest_skill_points.setReadOnly(True)
        skill_points_layout.addWidget(self.allocated_interest_skill_points, 1, 3)
        
        # 添加技能点信息组到主布局
        main_layout.addWidget(skill_points_group)
        
        # 创建搜索和过滤组
        search_filter_group = QGroupBox("搜索和过滤")
        search_filter_layout = QHBoxLayout(search_filter_group)
        
        # 添加搜索框
        search_filter_layout.addWidget(QLabel("搜索:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入技能名称搜索...")
        search_filter_layout.addWidget(self.search_edit)
        
        # 添加过滤选项
        search_filter_layout.addWidget(QLabel("显示:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["所有技能", "职业技能", "已分配技能", "语言技能"])
        search_filter_layout.addWidget(self.filter_combo)
        
        # 添加语言技能转移规则按钮
        self.language_transfer_button = QPushButton("语言技能转移规则")
        self.language_transfer_button.clicked.connect(self.show_language_transfer_rules)
        search_filter_layout.addWidget(self.language_transfer_button)
        
        # 添加保存按钮
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_investigator)
        search_filter_layout.addWidget(self.save_button)
        
        # 添加搜索和过滤组到主布局
        main_layout.addWidget(search_filter_group)
        
        # 创建技能表格
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(6)
        self.skills_table.setHorizontalHeaderLabels(["技能名称", "基础值", "职业技能", "加点", "最终值", "操作"])
        self.skills_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.skills_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.skills_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        # 添加技能表格到主布局
        main_layout.addWidget(self.skills_table)
        
        # 添加按钮布局
        button_layout = QHBoxLayout()
        
        # 添加重置按钮
        self.reset_button = QPushButton("重置技能点")
        button_layout.addWidget(self.reset_button)
        
        # 添加随机分配按钮
        self.random_button = QPushButton("随机分配技能点")
        button_layout.addWidget(self.random_button)
        
        # 添加自动保存开关
        self.autosave_checkbox = QCheckBox("自动保存")
        self.autosave_checkbox.setChecked(True)  # 默认开启自动保存
        button_layout.addWidget(self.autosave_checkbox)
        
        # 添加按钮布局到主布局
        main_layout.addLayout(button_layout)
        
        # 连接信号和槽
        self.search_edit.textChanged.connect(self.filter_skills)
        self.filter_combo.currentIndexChanged.connect(self.filter_skills)
        self.reset_button.clicked.connect(self.reset_skill_points)
        self.random_button.clicked.connect(self.random_allocate_skill_points)
    
    def create_skill_tooltip(self, skill_name, skill):
        """创建技能浮窗详情内容"""
        # 基本信息
        tooltip = f"<div style='font-weight:bold; font-size:10pt;'>{skill_name}</div>"
        tooltip += f"<div>基础值: {skill.get('base_value', 0)}%</div>"
        
        # 添加描述
        if "description" in skill:
            tooltip += f"<div style='margin-top:5px; max-width:300px;'>{skill.get('description', '')}</div>"
            
        # 如果是语言技能，添加语言技能特有信息
        if skill_name == "语言" or skill_name.startswith("语言（"):
            tooltip += "<div style='margin-top:5px;'><b>语言技能等级含义：</b></div>"
            tooltip += "<div>5%: 能够正确地辨认出这门语言</div>"
            tooltip += "<div>10%: 可以交流简单的想法</div>"
            tooltip += "<div>30%: 可以对社交上的需求进行理解</div>"
            tooltip += "<div>50%: 可以进行流畅的交流</div>"
            tooltip += "<div>75%: 可以将这门语言说得像是本地人一样</div>"
            
            # 如果是特定语言，显示语系信息
            if skill_name.startswith("语言（") and "）" in skill_name:
                language = skill_name[skill_name.find("（")+1:skill_name.find("）")]
                language_info = self.parent.skills.get_skill_info("语言")
                
                if language_info and "language_families" in language_info:
                    # 查找该语言属于哪个语系
                    for family, languages in language_info["language_families"].items():
                        if language in languages:
                            tooltip += f"<div style='margin-top:5px;'><b>语系：</b>{family}</div>"
                            tooltip += f"<div><b>同族语言：</b>{', '.join([lang for lang in languages if lang != language])}</div>"
                            
                            # 添加技能转移规则提示
                            tooltip += "<div style='margin-top:5px; color:#008800;'><b>技能转移规则：</b></div>"
                            tooltip += "<div style='color:#008800;'>当提升到50%时，同族语言提升至10%</div>"
                            tooltip += "<div style='color:#008800;'>当提升到90%时，同族语言再提升10%</div>"
                            break
        
        return tooltip
        
    def load_skills(self):
        """加载技能列表"""
        if not self.parent.skills or not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 清空表格
        self.skills_table.setRowCount(0)
        
        # 获取职业技能
        occupation_skills = []
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation:
                occupation_skills = occupation.get("skills", [])
        
        # 添加技能到表格
        row = 0
        for skill_name, skill in sorted(self.parent.skills.skills.items()):
            # 检查过滤条件
            filter_text = self.filter_combo.currentText()
            if filter_text == "职业技能" and skill_name not in occupation_skills:
                continue
            
            if filter_text == "已分配技能" and skill_name not in investigator.skills:
                continue
                
            if filter_text == "语言技能" and not (skill_name == "语言" or skill_name.startswith("语言（")):
                continue
            
            # 检查搜索条件
            search_text = self.search_edit.text().lower()
            if search_text and search_text not in skill_name.lower():
                continue
            
            # 添加新行
            self.skills_table.insertRow(row)
            
            # 技能名称
            name_item = QTableWidgetItem(skill_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # 添加详细工具提示
            skill_tooltip = self.create_skill_tooltip(skill_name, skill)
            name_item.setToolTip(skill_tooltip)
            
            self.skills_table.setItem(row, 0, name_item)
            
            # 基础值
            base_value = skill.get("base_value", 0)
            base_item = QTableWidgetItem(str(base_value))
            base_item.setFlags(base_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            base_item.setToolTip(skill_tooltip)  # 同样添加工具提示
            self.skills_table.setItem(row, 1, base_item)
            
            # 职业技能
            is_occupation_skill = skill_name in occupation_skills
            occupation_item = QTableWidgetItem()
            occupation_item.setFlags(occupation_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            occupation_item.setCheckState(Qt.CheckState.Checked if is_occupation_skill else Qt.CheckState.Unchecked)
            self.skills_table.setItem(row, 2, occupation_item)
            
            # 加点
            points = investigator.skills.get(skill_name, 0) - base_value
            points_spin = QSpinBox()
            points_spin.setRange(0, 100)
            points_spin.setValue(points)
            points_spin.setKeyboardTracking(False)  # 禁用键盘追踪，防止在输入过程中触发valueChanged信号
            points_spin.valueChanged.connect(lambda value, r=row, s=skill_name: self.on_points_changed(r, s, value))
            self.skills_table.setCellWidget(row, 3, points_spin)
            
            # 最终值
            final_value = investigator.skills.get(skill_name, base_value)
            final_item = QTableWidgetItem(str(final_value))
            final_item.setFlags(final_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            final_item.setToolTip(skill_tooltip)  # 同样添加工具提示
            self.skills_table.setItem(row, 4, final_item)
            
            # 操作按钮
            roll_button = QPushButton("掷骰")
            roll_button.clicked.connect(lambda checked, s=skill_name: self.roll_skill(s))
            self.skills_table.setCellWidget(row, 5, roll_button)
            
            row += 1
    
    def filter_skills(self):
        """根据搜索文本和过滤条件过滤技能列表"""
        self.load_skills()
    
    def on_points_changed(self, row, skill_name, value):
        """技能点变化时的处理"""
        if not self.parent.current_investigator or not self.parent.skills:
            return
        
        investigator = self.parent.current_investigator
        skill = self.parent.skills.get_skill(skill_name)
        
        if not skill:
            return
        
        # 获取原始加点
        base_value = skill.get("base_value", 0)
        old_points = investigator.skills.get(skill_name, base_value) - base_value
        
        # 计算差值
        diff = value - old_points
        
        if diff == 0:
            return
        
        # 检查是否是职业技能
        is_occupation_skill = False
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation and skill_name in occupation.get("skills", []):
                is_occupation_skill = True
        
        # 检查技能点是否足够
        if diff > 0:
            if is_occupation_skill:
                remaining_points = investigator.occupation_skill_points - investigator.occupation_skill_points_allocated
                if investigator.occupation_skill_points_allocated + diff > investigator.occupation_skill_points:
                    # 职业技能点不足，恢复原值
                    points_spin = self.skills_table.cellWidget(row, 3)
                    points_spin.setValue(old_points)
                    return
            else:
                remaining_points = investigator.interest_skill_points - investigator.interest_skill_points_allocated
                if investigator.interest_skill_points_allocated + diff > investigator.interest_skill_points:
                    # 兴趣技能点不足，恢复原值
                    points_spin = self.skills_table.cellWidget(row, 3)
                    points_spin.setValue(old_points)
                    return
        
        # 更新技能值
        new_value = base_value + value
        
        # 记录更新前所有语言技能的值
        pre_update_language_skills = {}
        if skill_name.startswith("语言（") or skill_name == "语言":
            # 获取所有语言技能当前值
            for s_name, s_value in investigator.skills.items():
                if s_name.startswith("语言（") or s_name == "语言":
                    pre_update_language_skills[s_name] = s_value
        
        # 使用add_skill方法而不是直接设置，以触发技能转移规则
        investigator.add_skill(skill_name, new_value)
        
        # 更新已分配技能点
        if is_occupation_skill:
            investigator.occupation_skill_points_allocated += diff
        else:
            investigator.interest_skill_points_allocated += diff
        
        # 检查语言技能是否发生了转移
        affected_languages = []
        if pre_update_language_skills and (skill_name.startswith("语言（") or skill_name == "语言"):
            for s_name, old_val in pre_update_language_skills.items():
                # 跳过当前正在修改的技能
                if s_name == skill_name:
                    continue
                
                # 检查值是否有变化
                new_val = investigator.skills.get(s_name, old_val)
                if new_val > old_val:
                    affected_languages.append((s_name, old_val, new_val))
        
        # 更新UI
        self.update_ui()
        
        # 更新最终值 - 注意这里需要从investigator.skills获取最新值，因为可能已被技能转移规则修改
        final_value = investigator.skills.get(skill_name, new_value)
        final_item = QTableWidgetItem(str(final_value))
        final_item.setFlags(final_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.skills_table.setItem(row, 4, final_item)
        
        # 显示语言技能转移通知
        if affected_languages:
            notification = f"由于{skill_name}达到了{new_value}%，以下相关语言也得到了提升：\n"
            for lang, old_val, new_val in affected_languages:
                notification += f"• {lang}: {old_val}% → {new_val}%\n"
                
                # 高亮显示受影响的技能行
                self.highlight_affected_skill(lang, old_val, new_val)
                
            self.parent.show_message(notification)
            
        # 如果开启了自动保存，调用主窗口的update_investigator_from_tabs方法更新调查员
        if self.autosave_checkbox.isChecked():
            self.parent.update_investigator_from_tabs()
    
    def highlight_affected_skill(self, skill_name, old_value, new_value):
        """高亮显示受影响的技能"""
        # 查找表格中的技能行
        for row in range(self.skills_table.rowCount()):
            name_item = self.skills_table.item(row, 0)
            if name_item and name_item.text() == skill_name:
                # 高亮显示最终值单元格
                final_item = self.skills_table.item(row, 4)
                if final_item:
                    final_item.setText(f"{new_value} (+{new_value - old_value})")
                    final_item.setBackground(QColor(200, 255, 200))  # 浅绿色背景
                break
    
    def roll_skill(self, skill_name):
        """掷骰检定技能"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        skill_value = investigator.skills.get(skill_name, 0)
        
        # 掷骰
        result = self.parent.investigator_generator.dice_roller.roll_d100()
        
        # 判定结果
        if result <= skill_value / 5:
            success_level = "大成功"
        elif result <= skill_value / 2:
            success_level = "困难成功"
        elif result <= skill_value:
            success_level = "成功"
        elif result > 95:
            success_level = "大失败"
        else:
            success_level = "失败"
        
        # 显示结果
        message = f"{skill_name}检定：掷骰结果{result}，技能值{skill_value}，{success_level}"
        self.parent.show_message(message)
    
    def reset_skill_points(self):
        """重置技能点"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 重置技能
        for skill_name, skill in self.parent.skills.skills.items():
            if skill_name in investigator.skills:
                investigator.skills[skill_name] = skill.get("base_value", 0)
        
        # 重置已分配技能点
        investigator.occupation_skill_points_allocated = 0
        investigator.interest_skill_points_allocated = 0
        
        # 更新UI
        self.update_ui()
        
        # 如果开启了自动保存，更新调查员数据
        if self.autosave_checkbox.isChecked():
            self.parent.update_investigator_from_tabs()
            self.parent.show_message("技能点已重置并保存")
        else:
            self.parent.show_message("技能点已重置")
    
    def random_allocate_skill_points(self):
        """随机分配技能点"""
        if not self.parent.current_investigator or not self.parent.skills:
            return
        
        investigator = self.parent.current_investigator
        
        # 重置技能点
        self.reset_skill_points()
        
        # 获取职业技能
        occupation_skills = []
        if investigator.occupation:
            occupation = self.parent.occupations.get_occupation(investigator.occupation)
            if occupation:
                occupation_skills = occupation.get("skills", [])
        
        # 随机分配职业技能点
        remaining_occupation_points = investigator.occupation_skill_points
        while remaining_occupation_points > 0 and occupation_skills:
            # 随机选择一个职业技能
            skill_name = self.parent.investigator_generator.dice_roller.random_choice(occupation_skills)
            skill = self.parent.skills.get_skill(skill_name)
            
            if not skill:
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_occupation_points, 20)
            points = self.parent.investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base_value", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.occupation_skill_points_allocated += points
            remaining_occupation_points -= points
        
        # 随机分配兴趣技能点
        remaining_interest_points = investigator.interest_skill_points
        all_skills = list(self.parent.skills.skills.keys())
        while remaining_interest_points > 0 and all_skills:
            # 随机选择一个技能
            skill_name = self.parent.investigator_generator.dice_roller.random_choice(all_skills)
            
            # 跳过已经分配过的职业技能
            if skill_name in occupation_skills:
                all_skills.remove(skill_name)
                continue
            
            skill = self.parent.skills.get_skill(skill_name)
            
            if not skill:
                all_skills.remove(skill_name)
                continue
            
            # 随机分配点数（最多20点）
            max_points = min(remaining_interest_points, 20)
            points = self.parent.investigator_generator.dice_roller.roll_between(1, max_points)
            
            # 更新技能值
            current_value = investigator.skills.get(skill_name, skill.get("base_value", 0))
            investigator.skills[skill_name] = current_value + points
            
            # 更新已分配技能点
            investigator.interest_skill_points_allocated += points
            remaining_interest_points -= points
            
            # 从列表中移除已分配的技能
            all_skills.remove(skill_name)
        
        # 更新UI
        self.update_ui()
        
        # 如果开启了自动保存，更新调查员数据
        if self.autosave_checkbox.isChecked():
            self.parent.update_investigator_from_tabs()
            self.parent.show_message("技能点已随机分配并保存")
        else:
            self.parent.show_message("技能点已随机分配")
    
    def update_ui(self):
        """更新UI"""
        if not self.parent.current_investigator:
            return
        
        investigator = self.parent.current_investigator
        
        # 更新技能点信息
        self.occupation_skill_points.setText(str(investigator.occupation_skill_points))
        self.allocated_occupation_skill_points.setText(str(investigator.occupation_skill_points_allocated))
        self.interest_skill_points.setText(str(investigator.interest_skill_points))
        self.allocated_interest_skill_points.setText(str(investigator.interest_skill_points_allocated))
        
        # 重新加载技能列表
        self.load_skills()
    
    def show_language_transfer_rules(self):
        """显示语言技能转移规则"""
        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("语言技能转移规则")
        dialog.resize(600, 400)
        
        # 创建布局
        layout = QVBoxLayout(dialog)
        
        # 添加标题
        title_label = QLabel("语言技能转移规则")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 添加规则文本
        rules_text = QTextEdit()
        rules_text.setReadOnly(True)
        
        # 获取语言技能信息
        language_info = self.parent.skills.get_skill_info("语言")
        
        # 设置规则文本内容
        rules_content = """
<h3>语言技能转移规则</h3>
<p>当角色提升语言技能时，同一语系的其他语言也会受益：</p>
<ul>
    <li>当一名角色首次将一门语言（除了母语）提升到50%，同系语言都会提升10%（但不会超过50%）。</li>
    <li>当角色首次将一门语言提升到90%，同系语言会再次提升10%（但不会高于90%）。</li>
</ul>

<h3>语言技能等级含义</h3>
<ul>
    <li>5%：能够正确地辨认出这门语言。</li>
    <li>10%：可以交流简单的想法。</li>
    <li>30%：可以对社交上的需求进行理解。</li>
    <li>50%：可以进行流畅的交流。</li>
    <li>75%：可以将这门语言说得像是本地人一样。</li>
</ul>

<h3>语言族群关系</h3>
"""
        
        # 添加语言族群信息
        if language_info and "language_families" in language_info:
            for family, languages in language_info["language_families"].items():
                rules_content += f"<p><b>{family}</b>: {', '.join(languages)}</p>"
        
        rules_text.setHtml(rules_content)
        layout.addWidget(rules_text)
        
        # 添加确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        
        # 显示对话框
        dialog.exec()
    
    def save_investigator(self):
        """保存调查员数据"""
        # 调用主窗口的保存方法
        self.parent.save_investigator()
        
    def update_investigator(self):
        """更新调查员对象的技能数据"""
        # 这个方法将被主窗口在保存前调用，用于确保调查员对象包含最新的技能数据
        if not self.parent.current_investigator:
            return
            
        # 技能数据已经在on_points_changed方法中更新了，这里不需要额外操作
        # 如果有其他需要更新的数据，可以在这里添加
        pass 