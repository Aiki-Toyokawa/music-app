# merge.py

import io
import os
import sys
from video_downloader import download_video
from info_downloader import download_info
from thumbnail_downloader import download_thumbnail
from title_file_creator import create_title_file  # インポート追加

# 文字化け防止のため、標準出力と標準エラー出力をUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    # ベタ打ちで入力する動画のURL
    video_url = 'https://www.youtube.com/watch?v=EG_BVGUPxsI'

    # ダウンロードディレクトリの設定
    download_dir = 'dl'

    # 動画のダウンロード
    info_dict = download_video(video_url, download_dir=download_dir)
    if not info_dict:
        print("動画のダウンロードに失敗しました。")
        sys.exit(1)

    # 動画IDの取得
    video_id = info_dict.get('id')
    if not video_id:
        print("動画IDが取得できませんでした。")
        sys.exit(1)

    # メタデータの抽出と保存
    video_dir = os.path.join(download_dir, video_id)
    info_json_path = os.path.join(video_dir, 'info.json')

    # 動画のURLを再度渡す必要があるため、download_info関数を使用
    target_url = info_dict.get('webpage_url', video_url)
    info_data = download_info(target_url, output_filename=info_json_path)
    if not info_data:
        print("メタデータの抽出に失敗しました。")
        sys.exit(1)

    # サムネイルのダウンロード
    thumbnail_url = info_data['raw_data'].get('thumbnail_url', '不明')
    thumbnail_path = download_thumbnail(thumbnail_url, video_id, download_dir=download_dir)
    if thumbnail_path:
        print("サムネイルのダウンロードが完了しました。")
    else:
        print("サムネイルのダウンロードに失敗しました。")

    # タイトルファイルの作成
    video_title = info_data['raw_data'].get('title', '無題')
    title_file_path = create_title_file(video_title, video_dir)
    if title_file_path:
        print(f"タイトルファイルが作成されました: {title_file_path}")
    else:
        print("タイトルファイルの作成に失敗しました。")

    print("\nすべての処理が完了しました。")
    print(f"動画ファイル: {os.path.join(video_dir, 'music.mp4')}")
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
