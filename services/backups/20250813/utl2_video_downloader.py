# utl2_video_downloader.py

import os
import sys
from pathlib import Path
import yt_dlp

from utl2_1_format_map import FORMAT_MAP

# ---- ffmpeg のローカル検出（extractor と同じ実装） ----------------------
REQUIRE_LOCAL_FFMPEG = False  # ← True にすると「ローカルが無ければ即エラー」

def get_local_ffmpeg_dir():
    env_dir = os.getenv("FFMPEG_DIR")
    if env_dir and Path(env_dir).is_dir():
        return env_dir
    guess = (Path(__file__).resolve().parent
             / "third_party" / "ffmpeg" / "win-x64" / "current" / "bin")
    if guess.is_dir():
        return str(guess)
    return None

def apply_ffmpeg_location_to_env(ffmpeg_dir: str | None):
    if not ffmpeg_dir:
        if REQUIRE_LOCAL_FFMPEG:
            print("エラー: プロジェクト内に ffmpeg/ffprobe が見つかりません。")
            sys.exit(1)
        return
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# ------------------------------------------------------------------
# 指定されたYouTube動画をダウンロードし、メタデータを生成します。
# ------------------------------------------------------------------
def download_video(video_url, download_dir, format_code):
    if not video_url:
        print("動画URLの取得に失敗しました。")
        sys.exit(1)
    if not ('youtube.com/' in video_url or 'youtu.be/' in video_url):
        print(f"無効なYoutube URLです: {video_url}")
        sys.exit(1)

    # --- ffmpeg の場所を決定（ローカル優先／必要なら必須化） ---
    ffmpeg_dir = get_local_ffmpeg_dir()
    apply_ffmpeg_location_to_env(ffmpeg_dir)

    # 1. フォーマット
    if format_code in FORMAT_MAP:
        selected_format = FORMAT_MAP[format_code]
        print(f"Easy setting: 使用フォーマットコード '{format_code}' を選択")
        print(f"選択されたフォーマット: {selected_format}")
    else:
        print(f"無効なフォーマットコードです: {format_code}")
        sys.exit(1)

    # 2. ダウンロード
    print("動画のダウンロードを開始します...")
    print(f"\n単一動画のダウンロードを開始します: {video_url}")

    ydl_opts = {
        'format': selected_format,
        'outtmpl': os.path.join(download_dir, '%(id)s', 'media.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,
        'ignoreerrors': True,
        'extractor_args': {
            'youtube': {
                # tvを優先 web/ios/androidは任意
                'player_client': ['tv'],
                # 'player_client': ['tv', 'web', 'ios', 'android'],
            },
        }
        # 出力拡張子を固定したい場合は有効化（必要なら）
        # 'merge_output_format': 'mp4',
    }
    if ffmpeg_dir:
        ydl_opts['ffmpeg_location'] = ffmpeg_dir

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            if info_dict is None:
                print(f"動画情報の取得に失敗しました: {video_url}")
                sys.exit(1)
            print(f"動画のダウンロードが完了しました: {video_url}")
            return info_dict
    except yt_dlp.utils.DownloadError as e:
        # リクエストしたフォーマットが無い場合のヒントを追加
        print(f"ダウンロードエラー: {e}")
        print("ヒント: 指定のフォーマット枝が存在しない可能性があります。"
              " 一度 FORMAT_MAP['0'] を "
              "'best[ext=mp4]' など簡易にして試すか、"
              " --list-formats 相当で実際の提供フォーマットを確認してみてください。")
        sys.exit(1)
