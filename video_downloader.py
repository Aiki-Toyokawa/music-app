# video_downloader.py

import yt_dlp
import os

class VideoDownloader:
    def __init__(self, download_dir='src/dl'):
        """
        初期化メソッド。
        
        Parameters:
            download_dir (str): ダウンロード先のディレクトリパス。
        """
        self.download_dir = download_dir

    def is_valid_youtube_url(self, url):
        """
        YouTubeのURLかどうかを簡易的にチェックします。
        
        Parameters:
            url (str): チェックするURL。
        
        Returns:
            bool: 有効なYouTube URLの場合はTrue、そうでない場合はFalse。
        """
        return 'youtube.com/watch?v=' in url or 'youtu.be/' in url

    def download_video(self, url):
        """
        指定されたYouTube動画をダウンロードします。
        
        Parameters:
            url (str): ダウンロードするYouTube動画のURL。
        
        Returns:
            dict: ダウンロードした動画の情報辞書 (`info_dict`)。
        """
        if not self.is_valid_youtube_url(url):
            print(f"無効なYouTube URLです: {url}")
            return None

        print(f"動画のダウンロードを開始します: {url}")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(self.download_dir, '%(id)s', 'music.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'noplaylist': True,  # 再生リストの動画を個別に扱う
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                if info_dict is None:
                    print(f"情報取得に失敗しました: {url}")
                    return None
                print(f"動画のダウンロードが完了しました: {url}")
                return info_dict
        except yt_dlp.utils.DownloadError as e:
            print(f"ダウンロードエラー: {e}")
            return None
