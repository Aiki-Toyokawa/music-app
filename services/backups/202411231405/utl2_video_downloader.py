# utl2_video_downloader.py

import yt_dlp
import os

# ------------------------------------------------------------------
# 指定されたYouTube動画をダウンロードし、メタデータを生成します。
# 
# Parameters:
#     video_url (str): ダウンロードするYouTube動画のURL。
#     download_dir (str): ダウンロード先のディレクトリパス。
#
# Returns:
#     dict: ダウンロードした動画の情報辞書 (`info_dict`)。
# ------------------------------------------------------------------

# フォーマットコードとフォーマット文字列のマッピング
FORMAT_MAP = {
    '0': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # デフォルト
    '1': 'bestvideo[ext=mp4][height=144]+bestaudio[ext=m4a]/best[ext=mp4]',
    '2': 'bestvideo[ext=mp4][height=240]+bestaudio[ext=m4a]/best[ext=mp4]',
    '3': 'bestvideo[ext=mp4][height=360]+bestaudio[ext=m4a]/best[ext=mp4]',
    '4': 'bestvideo[ext=mp4][height=480]+bestaudio[ext=m4a]/best[ext=mp4]',
    '5': 'bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/best[ext=mp4]',
    '6': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
    '7': 'bestvideo[ext=mp4][height=1440]+bestaudio[ext=m4a]/best[ext=mp4]',
    '8': 'bestvideo[ext=mp4][height=2160]+bestaudio[ext=m4a]/best[ext=mp4]',
    '9': 'bestvideo[ext=mp4][height=4320]+bestaudio[ext=m4a]/best[ext=mp4]',
    'a': 'bestaudio[ext=m4a]/best[ext=m4a]',  # 音声のみ
}

def download_video(video_url, download_dir, format_code):
    
    if not ('youtube.com/' in video_url or 'youtu.be/' in video_url):
        print(f"無効なYoutube URLです: {video_url}")
        return None

    selected_format = FORMAT_MAP[format_code]

    print(f"\n単一動画のダウンロードを開始します: {video_url}")
    ydl_opts = {
        'format': selected_format,
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
