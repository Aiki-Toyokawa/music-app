# thumbnail_downloader.py

import requests
import os

class ThumbnailDownloader:
    def __init__(self, download_dir='dl'):
        """
        初期化メソッド。
        
        Parameters:
            download_dir (str): ダウンロード先のディレクトリパス。
        """
        self.download_dir = download_dir

    def download_thumbnail(self, thumbnail_url, video_id):
        """
        サムネイル画像をダウンロードします。
        
        Parameters:
            thumbnail_url (str): サムネイル画像のURL。
            video_id (str): 動画ID（保存先ディレクトリの名前として使用）。
        
        Returns:
            str: サムネイル画像の保存パス。失敗した場合はNone。
        """
        if not thumbnail_url or thumbnail_url == 'Unknown':
            print("サムネイルURLが提供されていません。")
            return None

        try:
            print(f"サムネイル画像のダウンロードを開始します: {thumbnail_url}")
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            video_dir = os.path.join(self.download_dir, video_id)
            os.makedirs(video_dir, exist_ok=True)
            thumbnail_path = os.path.join(video_dir, 'thumbnail.png')
            with open(thumbnail_path, 'wb') as f:
                f.write(response.content)
            print(f"サムネイル画像を保存しました: {thumbnail_path}")
            return thumbnail_path
        except requests.RequestException as e:
            print(f"サムネイルのダウンロード中にエラーが発生しました: {e}")
            return None
