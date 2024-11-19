# title_file_creator.py

import os
import re

def sanitize_filename(filename):
    """
    ファイル名として使用できない文字を取り除きます。

    Parameters:
        filename (str): サニタイズするファイル名。

    Returns:
        str: サニタイズされたファイル名。
    """
    # Windowsで禁止されている文字: \ / : * ? " < > | 
    # 他のOSでも一部の文字が問題となるため、共通のパターンを使用
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def create_title_file(video_title, video_dir):
    """
    サニタイズされたタイトルをファイル名として、拡張子 .title を付けたファイルを作成します。
    ファイル内には動画のタイトルを記載します。

    Parameters:
        video_title (str): 動画のタイトル。
        video_dir (str): ファイルを作成するディレクトリのパス。

    Returns:
        str: 作成したファイルのパス。失敗した場合はNone。
    """
    sanitized_title = sanitize_filename(video_title)
    title_filename = f"{sanitized_title}.title"
    title_file_path = os.path.join(video_dir, title_filename)

    try:
        # ファイルを作成し、タイトルを書き込む
        with open(title_file_path, 'w', encoding='utf-8') as f:
            f.write("## このファイルは識別しやすくするファイルです\n" + "title : " + video_title)
        print(f"タイトルファイルを作成しました: {title_file_path}")
        return title_file_path
    except OSError as e:
        print(f"タイトルファイルの作成中にエラーが発生しました: {e}")
        return None
