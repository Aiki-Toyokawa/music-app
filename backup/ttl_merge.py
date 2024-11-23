# ttl_merge.py

import io
import os
import sys

from utl1_info_downloader import download_info
from utl2_video_downloader import download_video
from utl5_title_file_creator import create_title_file
from utl4_thumbnail_downloader import download_thumbnail

# 文字化け防止のため、標準出力と標準エラー出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    """
    メイン関数:
    YouTube動画をダウンロードし、メタデータ、サムネイル、タイトルファイルを生成します。
    """
    
    # ---------------------------
    # 1. 設定
    # ---------------------------
    download_dir = 'dl'  # ダウンロードディレクトリ
    video_url = 'https://www.youtube.com/watch?v=EG_BVGUPxsI'  # 動画のURL
    

    # ---------------------------
    # 2. 動画のダウンロード
    # ---------------------------
    print("動画のダウンロードを開始します...")
    info_dict = download_video(video_url, download_dir=download_dir)
    if not info_dict:
        print("動画のダウンロードに失敗しました。")
        sys.exit(1)
    print("動画のダウンロードが完了しました。")

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
    target_url = info_dict.get('webpage_url', video_url)

    print("メタデータの抽出と保存を開始します...")
    info_data = download_info(target_url, output_filename=info_json_path)
    if not info_data:
        print("メタデータの抽出に失敗しました。")
        sys.exit(1)
    print(f"メタデータが保存されました: {info_json_path}")

    # ---------------------------
    # 5. サムネイルのダウンロード
    # ---------------------------
    thumbnail_url = info_data['raw_data'].get('thumbnail_url', '不明')
    print("サムネイルのダウンロードを開始します...")
    thumbnail_path = download_thumbnail(thumbnail_url, video_id, download_dir=download_dir)
    if thumbnail_path:
        print(f"サムネイルのダウンロードが完了しました: {thumbnail_path}")
    else:
        print("サムネイルのダウンロードに失敗しました。")

    # ---------------------------
    # 6. タイトルファイルの作成
    # ---------------------------
    video_title = info_data['raw_data'].get('title', '無題')
    print("タイトルファイルの作成を開始します...")
    title_file_path = create_title_file(video_title, video_dir_path)
    if title_file_path:
        print(f"タイトルファイルが作成されました: {title_file_path}")
    else:
        print("タイトルファイルの作成に失敗しました。")

    # ---------------------------
    # 7. 処理完了の報告
    # ---------------------------
    print("\nすべての処理が完了しました。")
    print(f"動画ファイル: {os.path.join(video_dir_path, 'music.mp4')}")
    print(f"メタデータ: {info_json_path}")
    
    if thumbnail_path:
        print(f"サムネイル画像: {thumbnail_path}")
    else:
        print("サムネイル画像: なし")
    
    if title_file_path:
        print(f"タイトルファイル: {title_file_path}")
    else:
        print("タイトルファイル: なし")


if __name__ == "__main__":
    main()
