import os
import sys
import yt_dlp
from pathlib import Path
import platform

from utl2_1_format_map import FORMAT_MAP

# ------------------------------------------------------------------
# 指定されたYouTube動画をダウンロードし、メタデータを生成します。
# 
# Parameters:
#     video_url (str): ダウンロードするYouTube動画のURL。
#     download_dir (str): ダウンロード先のディレクトリパス。
#     format_code (str):
#
# Returns:
#     dict: ダウンロードした動画の情報辞書 (`info_dict`)。
# ------------------------------------------------------------------

def download_video(video_url, download_dir, format_code):
    # 1) video_url が空または None の場合 → エラー終了
    if not video_url:
        print("動画URLの取得に失敗しました。")
        sys.exit(1)

    # 2) YouTube のURLでなければ終了
    if not ('youtube.com/' in video_url or 'youtu.be/' in video_url):
        print(f"無効なYoutube URLです: {video_url}")
        sys.exit(1)

    # ---------------------------
    # 1. フォーマットの設定
    # ---------------------------
    if format_code in FORMAT_MAP: 
        selected_format = FORMAT_MAP[format_code]
        print(f"Easy setting: 使用フォーマットコード '{format_code}' を選択")
        print(f"選択されたフォーマット: {selected_format}")
    else:
        print(f"無効なフォーマットコードです: {format_code}")
        sys.exit(1)

    # ---------------------------
    # 2. ffmpeg の場所を決定（ローカル優先）
    # ---------------------------
    ffmpeg_dir_env = os.getenv("FFMPEG_DIR")
    ffmpeg_dir_guess = (
        Path(__file__).resolve().parent
        / "third_party" / "ffmpeg" / "win-x64" / "current" / "bin"
    )
    ffmpeg_location = None
    if ffmpeg_dir_env and Path(ffmpeg_dir_env).is_dir():
        ffmpeg_location = ffmpeg_dir_env
    elif ffmpeg_dir_guess.is_dir():
        ffmpeg_location = str(ffmpeg_dir_guess)

    # Windows の場合は PATH に前置
    if ffmpeg_location and platform.system().lower().startswith("win"):
        os.environ["PATH"] = ffmpeg_location + os.pathsep + os.environ.get("PATH", "")

    # ---------------------------
    # 3. 動画ダウンロード
    # ---------------------------
    print("動画のダウンロードを開始します...")
    print(f"\n単一動画のダウンロードを開始します: {video_url}")
    ydl_opts = {
        'format': selected_format,
        'outtmpl': os.path.join(download_dir, '%(id)s', 'media.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,
        'ignoreerrors': True,
    }

    # ffmpeg_location が見つかった場合のみ追加
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            if info_dict is None:
                print(f"動画情報の取得に失敗しました: {video_url}")
                sys.exit(1)
            print(f"動画のダウンロードが完了しました: {video_url}")
            return info_dict
    except yt_dlp.utils.DownloadError as e:
        print(f"ダウンロードエラー: {e}")
        sys.exit(1)
