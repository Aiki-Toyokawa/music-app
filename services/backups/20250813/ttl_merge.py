# ttl_merge.py

import io
import os
import sys

from utl1_video_urls_extractor import extract_video_urls
from utl2_video_downloader import download_video
from utl3_info_json_creator import create_info_json
from utl4_thumbnail_downloader import download_thumbnail
from utl5_title_file_creator import create_title_file

# 文字化け防止のため、標準出力と標準エラー出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# メイン関数: YouTube動画をダウンロードし、メタデータ、サムネイル、タイトルファイルを生成します。
def main():
    try:
        # ---------------------------
        # 1. 初期設定
        # ---------------------------
        format_code = 'a'
        download_dir = 'dl'  # ダウンロードディレクトリ
        input_url = 'https://www.youtube.com/watch?v=dROnSxQnrVU'  # 640pが480pでサムネdlされる不具合テストURL 
        # input_url = 'https://www.youtube.com/watch?v=F9Ay74LfKd4'


        # ---------------------------
        # 2. 動画URLリストの取得
        # ---------------------------
        video_urls = extract_video_urls(input_url)
                

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
            # 一番高解像度のサムネイルを自動選択して保存
            thumbnail_file_path = download_thumbnail(info_dict, each_video_folder_path)


            # ---------------------------
            # 3.5. タイトルファイルの作成
            # ---------------------------
            video_title = info_dict.get('title', '無題')
            title_file_path = create_title_file(video_title, each_video_folder_path)


            # ---------------------------
            # 3.6. 処理完了の報告
            # ---------------------------
            print("\nすべての処理が完了しました。")
            print(f"動画のＩＤ　　　　: {video_id}")
            print(f"タイトル名　　　　: {video_title}")
            print(f"メタデータ　　　　: {info_json_file_path}")
            print(f"動画データ　　　　: {os.path.join(each_video_folder_path, 'media.mp4')}")
            print(f"サムネ画像　　　　: {thumbnail_file_path}" if thumbnail_file_path else "サムネイル画像: なし")  # サムネイル画像あるなし三項演算子
            print(f"タイトルファイル名: {title_file_path}" if title_file_path else "タイトルファイル: なし") # タイトルファイルあるなし三項演算子

        print("\nすべての動画のダウンロードが完了しました。")
        
        
    except KeyboardInterrupt:
        print("\n ctrl+cで処理が中断されました")
        sys.exit(1)

if __name__ == "__main__":
    main()