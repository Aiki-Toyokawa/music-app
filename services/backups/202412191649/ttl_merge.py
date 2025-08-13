# ttl_merge.py

import io
import os
import sys

from utl1_info_json_creator import create_info_json
from utl2_video_downloader import download_video
from utl3_thumbnail_downloader import download_thumbnail
from utl4_title_file_creator import create_title_file
from utl5_video_urls_extractor import extract_video_urls

# 文字化け防止のため、標準出力と標準エラー出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# メイン関数: YouTube動画をダウンロードし、メタデータ、サムネイル、タイトルファイルを生成します。
def main():
    # ---------------------------
    # 1. 初期設定
    # ---------------------------
    download_dir = 'dl'  # ダウンロードディレクトリ
    input_url = 'https://www.youtube.com/@officialyoutubechannel163/videos'  # 動画のURL
    easy_setting = True
    format_code = '0' if easy_setting else '00634'  # 簡単設定 or 動画形式, 画質, 音声形式, 音質, コーデック
    
    # https://www.youtube.com/watch?v=9bZyUSQd9LE&list=RD5OKqwd-eDs0&index=2
    # https://www.youtube.com/watch?v=iinnMpZVZ-8&list=PLr6UNN7Eb0H7GS7uswtWp3iaM73LOxulb&index=2
    
    
    # ---------------------------
    # 2. 動画URLリストの取得
    # ---------------------------
    video_urls = extract_video_urls(input_url)
    if not video_urls:
        print("動画URLの取得に失敗しました。")
        sys.exit(1)

    # ---------------------------
    # 3. 各動画を順次処理
    # ---------------------------
    for index, video_url in enumerate(video_urls, start=1):
        print(f"\n===== 動画 {index} / {len(video_urls)} =====")
        print(f"URL: {video_url}")

        # ---------------------------
        # 3.1. 動画のダウンロード
        # ---------------------------
        info_dict = download_video(video_url, download_dir, format_code)
        print("xxxxxxx")

        # ---------------------------
        # 3.2. 動画IDの取得とフォルダパスの作成
        # ---------------------------
        video_id = info_dict.get('id')
        each_video_folder_path = os.path.join(download_dir, video_id)    # download_dir + video_id
        
        
        # ---------------------------
        # 3.3. メタデータの抽出と保存
        # ---------------------------
        info_json_file_path = create_info_json(info_dict, each_video_folder_path)
        

        # ---------------------------
        # 3.4. サムネイルのダウンロード
        # ---------------------------
        thumbnail_url = info_dict.get('thumbnail', '不明')
        thumbnail_file_path = download_thumbnail(thumbnail_url, each_video_folder_path)


        # ---------------------------
        # 3.5. タイトルファイルの作成
        # ---------------------------
        video_title = info_dict.get('title', '無題')
        title_file_path = create_title_file(video_title, each_video_folder_path)


        # ---------------------------
        # 3.6. 処理完了の報告
        # ---------------------------
        print("\nすべての処理が完了しました。")
        print(f"動画ID: {video_id}")
        print(f"タイトル: {video_title}")
        print(f"メタデータ: {info_json_file_path}")
        print(f"動画ファイル: {os.path.join(each_video_folder_path, 'music.mp4')}")
        print(f"サムネイル画像: {thumbnail_file_path}" if thumbnail_file_path else "サムネイル画像: なし")  # サムネイル画像あるなし三項演算子
        print(f"タイトルファイル: {title_file_path}" if title_file_path else "タイトルファイル: なし") # タイトルファイルあるなし三項演算子

    print("\nすべての動画のダウンロードが完了しました。")

if __name__ == "__main__":
    main()