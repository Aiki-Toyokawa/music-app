# utl2_video_downloader.py

import yt_dlp
import os

"""
指定されたYouTube動画をダウンロードし、メタデータを生成します。

Parameters:
    video_url (str): ダウンロードするYouTube動画のURL。
    download_dir (str): ダウンロード先のディレクトリパス。

Returns:
    dict: ダウンロードした動画の情報辞書 (`info_dict`)。
"""

def download_video(video_url, download_dir='dl'):
    
    if not ('youtube.com/watch?v=' in video_url or 'youtu.be/' in video_url):
        print(f"無効なYoutube URLです: {video_url}")
        return None

    print(f"\n単一動画のダウンロードを開始します: {video_url}")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(download_dir, '%(id)s', 'music.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,  # 再生リストの動画を個別に扱う
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            if info_dict is None:
                print(f"情報取得に失敗しました: {video_url}")
                return None
            print(f"動画のダウンロードが完了しました: {video_url}")
            return info_dict
    except yt_dlp.utils.DownloadError as e:
        print(f"ダウンロードエラー: {e}")
        return None
