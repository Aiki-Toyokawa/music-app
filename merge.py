# merge.py

import os
import sys
from video_downloader import VideoDownloader
from info_downloader import InfoDownloader
from thumbnail_downloader import ThumbnailDownloader

def main():
    # ベタ打ちで入力するYouTube動画のURL
    video_url = 'https://www.youtube.com/watch?v=ePTSW8ImP-M'

    # ダウンロードディレクトリの設定
    download_dir = 'dl'

    # 各コンポーネントの初期化
    video_downloader = VideoDownloader(download_dir=download_dir)
    info_downloader = InfoDownloader()
    thumbnail_downloader = ThumbnailDownloader(download_dir=download_dir)

    # 動画のダウンロード
    info_dict = video_downloader.download_video(video_url)
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

    info_data = info_downloader.extract_info(info_dict, output_filename=info_json_path)
    if not info_data:
        print("メタデータの抽出に失敗しました。")
        sys.exit(1)

    # サムネイルのダウンロード
    thumbnail_url = info_data['raw_data'].get('thumbnail_url', 'Unknown')
    thumbnail_path = thumbnail_downloader.download_thumbnail(thumbnail_url, video_id)
    if thumbnail_path:
        print("サムネイルのダウンロードが完了しました。")
    else:
        print("サムネイルのダウンロードに失敗しました。")

    print("\nすべての処理が完了しました。")

if __name__ == "__main__":
    main()
