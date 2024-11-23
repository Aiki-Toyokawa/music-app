# utl5_title_file_creator.py

import os
import re

# -----------------------------------------------------------------------------------
# サニタイズされたタイトルをファイル名として、拡張子 .title を付けたファイルを作成します。
# ファイル内には動画のタイトルを記載します。
#
# Parameters:
#    video_title (str): 動画のタイトル。
#    video_dir (str): ファイルを作成するディレクトリのパス。
#
# Returns:
#    str: 作成したファイルのパス。失敗した場合はNone。
# -----------------------------------------------------------------------------------

def create_title_file(video_title, video_dir):

    sanitized_title = re.sub(r'[\\/*?:"<>|]', '', video_title) # サニタイズするファイル(video_title), ファイル名に使えない文字をｓ
    title_filename = f"{sanitized_title}.title"
    title_file_path = os.path.join(video_dir, title_filename)

    try:
        print(f"タイトルファイルの作成を開始します...\npath: {title_file_path}")
        # ファイルを作成し、タイトルを書き込む
        with open(title_file_path, 'w', encoding='utf-8') as f:
            f.write("## このファイルは識別しやすくするデバッグ用ファイルです\n" + "title : " + video_title)
        print(f"タイトルファイルを作成完了: {title_file_path}")
        return title_file_path
    except OSError as e:
        print(f"タイトルファイルの作成中にエラーが発生しました: {e}")
        return None
