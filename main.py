#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易桌面文本工具
功能：文本输入 / 保存到文件 / 清空内容
依赖：Python 标准库（无需额外安装）
运行：python main.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os


# ──────────────────────────────────────────
#  配置常量（可按需修改）
# ──────────────────────────────────────────
APP_TITLE       = "简易文本工具"
WIN_SIZE        = "700x500"
FONT_TEXT       = ("微软雅黑", 12)    # 编辑区字体
FONT_BTN        = ("微软雅黑", 10)    # 按钮字体
COLOR_BG        = "#F7F7F7"           # 窗口背景色
COLOR_BTN_SAVE  = "#4A90D9"           # 保存按钮颜色
COLOR_BTN_CLEAR = "#E06060"           # 清空按钮颜色
COLOR_BTN_FG    = "#FFFFFF"           # 按钮文字颜色


# ──────────────────────────────────────────
#  主程序类
# ──────────────────────────────────────────
class TextTool:
    """简易文本工具主窗口。"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WIN_SIZE)
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(True, True)   # 允许缩放

        # 尝试加载图标（icon.ico 与脚本同目录）
        self._load_icon()

        # 构建界面
        self._build_ui()

        # 绑定快捷键
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-l>", lambda e: self.clear_text())

    # ── 图标加载 ──────────────────────────
    def _load_icon(self):
        """加载窗口图标，文件不存在时静默跳过。"""
        try:
            ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            if os.path.exists(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

    # ── 界面构建 ──────────────────────────
    def _build_ui(self):
        """构建标题栏、文本编辑区、按钮栏三层布局。"""

        # ── ① 顶部标题 ──
        title_bar = tk.Frame(self.root, bg="#4A90D9", height=42)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text=f"  📝  {APP_TITLE}",
            bg="#4A90D9", fg="white",
            font=("微软雅黑", 13, "bold"),
            anchor="w",
        ).pack(side=tk.LEFT, padx=10, pady=6)

        # ── ② 文本编辑区（带滚动条）──
        editor_frame = tk.Frame(self.root, bg=COLOR_BG, padx=12, pady=10)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = tk.Scrollbar(editor_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 多行文本框
        self.text_area = tk.Text(
            editor_frame,
            font=FONT_TEXT,
            wrap=tk.WORD,               # 按单词折行
            undo=True,                  # 支持撤销
            relief=tk.FLAT,
            bd=0,
            bg="white",
            fg="#2C2C2C",
            insertbackground="#4A90D9", # 光标颜色
            selectbackground="#4A90D9",
            selectforeground="white",
            padx=10,
            pady=8,
            yscrollcommand=scrollbar.set,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)

        # 占位提示文字（点击后消失）
        self._hint_text = "在此输入文本内容…"
        self.text_area.insert("1.0", self._hint_text)
        self.text_area.config(fg="#AAAAAA")
        self.text_area.bind("<FocusIn>",  self._clear_hint)
        self.text_area.bind("<FocusOut>", self._restore_hint)

        # ── ③ 底部按钮栏 ──
        btn_bar = tk.Frame(self.root, bg=COLOR_BG, pady=10)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # 字符统计标签（左侧）
        self.char_count_var = tk.StringVar(value="共 0 字")
        tk.Label(
            btn_bar,
            textvariable=self.char_count_var,
            bg=COLOR_BG, fg="#999999",
            font=("微软雅黑", 9),
        ).pack(side=tk.LEFT, padx=16)

        # 实时更新字符统计
        self.text_area.bind("<KeyRelease>", self._update_char_count)

        # 清空按钮（右侧）
        tk.Button(
            btn_bar,
            text="🗑  清  空   Ctrl+L",
            command=self.clear_text,
            font=FONT_BTN,
            bg=COLOR_BTN_CLEAR, fg=COLOR_BTN_FG,
            activebackground="#C04040",
            activeforeground="white",
            relief=tk.FLAT,
            padx=16, pady=7,
            cursor="hand2",
            bd=0,
        ).pack(side=tk.RIGHT, padx=8)

        # 保存按钮（右侧）
        tk.Button(
            btn_bar,
            text="💾  保  存   Ctrl+S",
            command=self.save_file,
            font=FONT_BTN,
            bg=COLOR_BTN_SAVE, fg=COLOR_BTN_FG,
            activebackground="#2A70B9",
            activeforeground="white",
            relief=tk.FLAT,
            padx=16, pady=7,
            cursor="hand2",
            bd=0,
        ).pack(side=tk.RIGHT, padx=4)

    # ── 占位提示逻辑 ──────────────────────
    def _clear_hint(self, event=None):
        """获得焦点时，若内容是占位提示则清除。"""
        if self.text_area.get("1.0", tk.END).strip() == self._hint_text:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg="#2C2C2C")

    def _restore_hint(self, event=None):
        """失去焦点时，若内容为空则恢复占位提示。"""
        if not self.text_area.get("1.0", tk.END).strip():
            self.text_area.insert("1.0", self._hint_text)
            self.text_area.config(fg="#AAAAAA")

    def _get_real_content(self) -> str:
        """返回文本框中的实际内容（排除占位提示）。"""
        content = self.text_area.get("1.0", tk.END).rstrip("\n")
        if content == self._hint_text:
            return ""
        return content

    # ── 字符统计 ──────────────────────────
    def _update_char_count(self, event=None):
        """按键后实时更新左下角字符统计。"""
        count = len(self._get_real_content())
        self.char_count_var.set(f"共 {count} 字")

    # ── 核心功能：保存 ─────────────────────
    def save_file(self):
        """
        将文本框内容保存为文件。
        弹出"另存为"对话框，支持 .txt / .md / 所有文件。
        """
        content = self._get_real_content()

        # 内容为空时提示
        if not content:
            messagebox.showwarning("提示", "内容为空，请先输入文字再保存！")
            return

        # 弹出文件保存对话框
        path = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".txt",
            filetypes=[
                ("文本文件",   "*.txt"),
                ("Markdown",  "*.md"),
                ("所有文件",  "*.*"),
            ],
        )

        # 用户取消时直接返回
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("保存成功", f"文件已保存至：\n{path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"无法写入文件：\n{e}")

    # ── 核心功能：清空 ─────────────────────
    def clear_text(self):
        """
        清空文本框内容。
        若有实际内容，先弹出确认对话框防止误操作。
        """
        if not self._get_real_content():
            return  # 本来就是空的，无需操作

        confirmed = messagebox.askyesno(
            "确认清空",
            "确定要清空所有内容吗？\n此操作不可撤销。",
        )
        if confirmed:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg="#AAAAAA")
            self.text_area.insert("1.0", self._hint_text)
            self.char_count_var.set("共 0 字")


# ──────────────────────────────────────────
#  程序入口
# ──────────────────────────────────────────
def main():
    root = tk.Tk()
    TextTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
