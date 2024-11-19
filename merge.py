# merge.py

import os
import sys
from video_downloader import download_video
from info_downloader import info_extract
from thumbnail_downloader import download_thumbnail

def main():
    # ベタ打ちで入力するYouTube動画のURL
    video_url = 'https://www.youtube.com/watch?v=7QxG722bXjM'

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

    # YouTube動画のURLを再度渡す必要があるため、info_extract関数を使用
    target_url = info_dict.get('webpage_url', video_url)
    info_data = info_extract(target_url, output_filename=info_json_path)
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

    print("\nすべての処理が完了しました。")
    print(f"動画ファイル: {os.path.join(video_dir, 'music.mp4')}")
    print(f"メタデータ: {info_json_path}")
    if thumbnail_path:
        print(f"サムネイル画像: {thumbnail_path}")
    else:
        print("サムネイル画像: なし")

if __name__ == "__main__":
    main()
