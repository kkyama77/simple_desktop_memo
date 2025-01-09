import tkinter as tk
import ctypes
import os

# ★文字打つごとに更新、ウィンドウ移動不可★
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

# テキストボックス
text = tk.Text(
    root,
    wrap="word",
    font=("游ゴシック", 11),
    bg="#333333",  # 背景色をグレー
    fg="#FFFFFF",  # 文字色を白
    insertbackground="#FFFFFF",  # カーソル色を白に設定
    borderwidth=0,  # 枠線を消去
    padx=10,  # 左右に2pxの余白
    pady=50,  # 上下に2pxの余白
)
text.pack(expand=True, fill="both")

# 保存された内容を読み込む
def load_content():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            text.insert("1.0", content)  # テキストボックスに内容を挿入

# 内容を保存する
def save_content(event=None):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        file.write(text.get("1.0", "end-1c"))  # テキストボックスの内容を取得して保存

# ウィンドウを閉じるボタン
def close_window():
    save_content()  # 閉じる前に内容を保存
    root.destroy()

close_btn = tk.Button(
    root, text="X", command=close_window, bg="#333333", fg="#FFFFFF", borderwidth=0
)
close_btn.place(x=window_width - 30, y=0)

# アプリ起動時に内容を読み込む
load_content()

# テキストボックスの変更時に自動保存
text.bind("<KeyRelease>", save_content)  # キーが離されたタイミングで保存

root.protocol("WM_DELETE_WINDOW", close_window)  # ウィンドウが閉じられるときに保存
root.mainloop()
