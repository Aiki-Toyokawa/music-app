# ttl_merge.py

import io
import os
import sys

from utl1_info_downloader import download_info
from utl2_video_downloader import download_video
from utl4_thumbnail_downloader import download_thumbnail
from utl5_title_file_creator import create_title_file

# 文字化け防止のため、標準出力と標準エラー出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# メイン関数: YouTube動画をダウンロードし、メタデータ、サムネイル、タイトルファイルを生成します。
def main():
    # ---------------------------
    # 1. 初期設定
    # ---------------------------
    download_dir = 'dl'  # ダウンロードディレクトリ
    video_url = 'https://www.youtube.com/watch?v=KT_uYG-sNOk'  # 動画のURL
    format_code = 'a'

    # ---------------------------
    # 2. 動画のダウンロード
    # ---------------------------
    print("動画のダウンロードを開始します...")
    info_dict = download_video(video_url, download_dir, format_code)
    if not info_dict:
        print("動画のダウンロードに失敗しました。")
        sys.exit(1)


    # ---------------------------
    # 3. 動画IDの取得
    # ---------------------------
    video_id = info_dict.get('id')
    if not video_id:
        print("動画IDが取得できませんでした。")
        sys.exit(1)
    print(f"動画ID: {video_id}")


    # ---------------------------
    # 4. メタデータの抽出と保存
    # ---------------------------
    video_dir_path = os.path.join(download_dir, video_id)
    info_json_path = os.path.join(video_dir_path, 'info.json')
    
    info_data = download_info(video_url, output_filename=info_json_path)


    # ---------------------------
    # 5. サムネイルのダウンロード
    # ---------------------------
    thumbnail_url = info_data['raw_data'].get('thumbnail_url', '不明')
    thumbnail_path = download_thumbnail(thumbnail_url, video_id, download_dir)


    # ---------------------------
    # 6. タイトルファイルの作成
    # ---------------------------
    video_title = info_data['raw_data'].get('title', '無題')
    title_file_path = create_title_file(video_title, video_dir_path)


    # ---------------------------
    # 7. 処理完了の報告
    # ---------------------------
    print("\nすべての処理が完了しました。")
    print(f"動画ID: {video_id}")
    print(f"タイトル: {video_title}")
    print(f"メタデータ: {info_json_path}")
    print(f"動画ファイル: {os.path.join(video_dir_path, 'music.mp4')}")
    print(f"サムネイル画像: {thumbnail_path}" if thumbnail_path else print("サムネイル画像: なし"))  # サムネイル画像あるなし三項演算子
    print(f"タイトルファイル: {title_file_path}" if title_file_path else print("タイトルファイル: なし")) # タイトルファイルあるなし三項演算子


if __name__ == "__main__":
    main()
