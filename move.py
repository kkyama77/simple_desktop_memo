import tkinter as tk
import ctypes
import os

# ★✖で更新、ウィンドウ移動可能★
# DPI対応（Windows用）
ctypes.windll.user32.SetProcessDPIAware()

# 保存ファイルのパス（スクリプトと同じフォルダに保存）
SAVE_FILE = "memo_content.txt"

# 画面の幅と高さを取得
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# ウィンドウの初期位置（右上隅に表示）
window_width = 500
window_height = screen_height - 100
x_pos = screen_width - window_width - 10  # 右端から10px
y_pos = 10  # 上端から10px

# メインウィンドウの設定
root = tk.Tk()
root.title("デスクトップメモ")
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")  # サイズと初期位置
root.attributes("-topmost", False)  # 常に最前面にはしない
root.overrideredirect(True)  # ウィンドウ枠を非表示

# ウィンドウ移動用の変数
offset_x = 0
offset_y = 0

def start_move(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def do_move(event):
    x = root.winfo_x() + event.x - offset_x
    y = root.winfo_y() + event.y - offset_y
    root.geometry(f"+{x}+{y}")

# タイトルバー代わりのフレーム
title_bar = tk.Frame(root, bg="#444444", relief="raised", bd=0, height=30)
title_bar.pack(fill="x")
title_bar.bind("<Button-1>", start_move)  # マウスクリック時に位置を記録
title_bar.bind("<B1-Motion>", do_move)  # ドラッグ時に位置を更新



# テキストボックス
text = tk.Text(
    root,
    wrap="word",
    font=("游ゴシック", 11),
    bg="#333333",  # 背景色をグレー
    fg="#FFFFFF",  # 文字色を白
    insertbackground="#FFFFFF",  # カーソル色を白に設定
    borderwidth=0,  # 枠線を消去
    padx=10,  # 左右に余白
    pady=10,  # 上下に余白
)
text.pack(expand=True, fill="both")

# 保存された内容を読み込む
def load_content():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            text.insert("1.0", content)  # テキストボックスに内容を挿入

# 内容を保存する
def save_content():
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        file.write(text.get("1.0", "end-1c"))  # テキストボックスの内容を取得して保存

# アプリ終了時に内容を保存
def close_window():
    save_content()
    root.destroy()

# 閉じるボタン
close_btn = tk.Button(
    title_bar, text="X", command=close_window, bg="#444444", fg="#FFFFFF", borderwidth=0
)
close_btn.pack(side="right", padx=5, pady=5)

# 閉じる動作を設定
root.protocol("WM_DELETE_WINDOW", close_window)

# アプリ起動時に内容を読み込む
load_content()

root.mainloop()
