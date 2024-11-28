# utl4_thumbnail_downloader.py

import requests
import os

# -----------------------------------------------------------------
# サムネイル画像をダウンロードし、指定されたディレクトリに保存します。
#
# Parameters:
#     thumbnail_url (str): サムネイル画像のURL。
#     video_id (str): 動画ID（保存先ディレクトリの名前として使用）。
#     download_dir (str): ダウンロード先のディレクトリパス。
#
# Returns:
#     str: サムネイル画像の保存パス。失敗した場合はNone。
# -----------------------------------------------------------------

def download_thumbnail(thumbnail_url, each_video_id_path):
    if not thumbnail_url or thumbnail_url == '不明':
        print("サムネイルURLが提供されていません。")
        return None

    try:
        print(f"サムネイルのダウンロードを開始します...\npath: {thumbnail_url}")
        response = requests.get(thumbnail_url, timeout=10)
        response.raise_for_status()
        os.makedirs(each_video_id_path, exist_ok=True)
        thumbnail_path = os.path.join(each_video_id_path, 'thumbnail.png')
        with open(thumbnail_path, 'wb') as f:
            f.write(response.content)
        print(f"サムネイル画像のダウンロード完了: {thumbnail_path}")
        return thumbnail_path
    except requests.RequestException as e:
        print(f"サムネイルのダウンロード中にエラーが発生しました: {e}")
        return None
