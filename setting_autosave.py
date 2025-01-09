import tkinter as tk
from tkinter import colorchooser, font
import ctypes
import os
import json

# 設定機能あり、ウインドウ移動不可、自動上書
# DPI対応（Windows用）
ctypes.windll.user32.SetProcessDPIAware()

# 保存ファイルのパス（スクリプトと同じフォルダに保存）
SAVE_FILE = "memo_content.txt"
SETTINGS_FILE = "settings.json"

# 画面の幅と高さを取得
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# ウィンドウの初期位置（右上隅に表示）
window_width = 500
window_height = screen_height - 100
x_pos = screen_width - window_width - 10  # 右端から10px
y_pos = 10  # 上端から10px

# デフォルト設定
default_settings = {
    "bg_color": "#333333",
    "font_family": "游ゴシック",
    "font_size": 11,
    "text_color": "#FFFFFF",
}

# 設定を読み込む
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_settings

# 設定を保存する
def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file)

# 現在の設定
settings = load_settings()

# メインウィンドウの設定
root = tk.Tk()
root.title("デスクトップメモ")
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")  # サイズと初期位置
root.attributes("-topmost", False)  # 常に最前面にはしない
root.overrideredirect(True)  # ウィンドウ枠を非表示

# テキストボックス
text = tk.Text(
    root,
    wrap="word",
    font=(settings["font_family"], settings["font_size"]),
    bg=settings["bg_color"],
    fg=settings["text_color"],
    insertbackground=settings["text_color"],
    borderwidth=0,
    padx=10,
    pady=50,
)
text.pack(expand=True, fill="both")

# 保存された内容を読み込む
def load_content():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            text.insert("1.0", content)

# 内容を保存する
def save_content(event=None):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        file.write(text.get("1.0", "end-1c"))

# ウィンドウを閉じるボタン
def close_window():
    save_content()
    root.destroy()

close_btn = tk.Button(
    root, text="X", command=close_window, bg="#333333", fg="#FFFFFF", borderwidth=0
)
close_btn.place(x=window_width - 30, y=0)

# 設定ウィンドウ
def open_settings():
    def apply_settings():
        settings["bg_color"] = bg_color_var.get()
        settings["font_family"] = font_family_var.get()
        settings["font_size"] = int(font_size_var.get())
        settings["text_color"] = text_color_var.get()
        save_settings(settings)
        update_textbox()
        settings_window.destroy()

    def choose_bg_color():
        color_code = colorchooser.askcolor(title="背景色を選択")[1]
        if color_code:
            bg_color_var.set(color_code)

    def choose_text_color():
        color_code = colorchooser.askcolor(title="文字色を選択")[1]
        if color_code:
            text_color_var.set(color_code)

    def update_textbox():
        text.config(
            bg=settings["bg_color"],
            fg=settings["text_color"],
            font=(settings["font_family"], settings["font_size"]),
            insertbackground=settings["text_color"],
        )

    settings_window = tk.Toplevel(root)
    settings_window.title("設定")
    settings_window.geometry("400x500")
    settings_window.resizable(False, False)

    # 背景色設定
    tk.Label(settings_window, text="背景色:").pack(anchor="w", padx=10, pady=5)
    bg_color_var = tk.StringVar(value=settings["bg_color"])
    tk.Entry(settings_window, textvariable=bg_color_var).pack(fill="x", padx=10)
    tk.Button(settings_window, text="選択", command=choose_bg_color).pack(pady=5)

    # 文字色設定
    tk.Label(settings_window, text="文字色:").pack(anchor="w", padx=10, pady=5)
    text_color_var = tk.StringVar(value=settings["text_color"])
    tk.Entry(settings_window, textvariable=text_color_var).pack(fill="x", padx=10)
    tk.Button(settings_window, text="選択", command=choose_text_color).pack(pady=5)

    # フォント設定
    tk.Label(settings_window, text="フォント名:").pack(anchor="w", padx=10, pady=5)
    font_family_var = tk.StringVar(value=settings["font_family"])
    tk.Entry(settings_window, textvariable=font_family_var).pack(fill="x", padx=10)

    tk.Label(settings_window, text="フォントサイズ:").pack(anchor="w", padx=10, pady=5)
    font_size_var = tk.StringVar(value=settings["font_size"])
    tk.Entry(settings_window, textvariable=font_size_var).pack(fill="x", padx=10)

    # 適用ボタン
    tk.Button(settings_window, text="適用", command=apply_settings).pack(pady=20)

# 設定ボタン
settings_btn = tk.Button(
    root, text="設定", command=open_settings, bg="#333333", fg="#FFFFFF", borderwidth=0
)
settings_btn.place(x=window_width - 80, y=0)

# アプリ起動時に内容を読み込む
load_content()

# テキストボックスの変更時に自動保存
text.bind("<KeyRelease>", save_content)

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
