# utl1_video_urls_extractor.py

import os
import time
from pathlib import Path
import yt_dlp

# ---- ffmpeg のローカル検出（共通ユーティリティ） -------------------------
REQUIRE_LOCAL_FFMPEG = False  # ← True にすると「ローカルが無い場合は即エラー」

def get_local_ffmpeg_dir():
    """
    優先順位:
      1) 環境変数 FFMPEG_DIR
      2) このファイルからの相対: third_party/ffmpeg/win-x64/current/bin
    見つかればディレクトリの str を返す。無ければ None。
    """
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
            raise SystemExit(1)
        return
    # Windows なら PATH 前置（他OSでも悪さはしない）
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# ----------------------------------------------------
# 指定されたURLが単一動画、チャンネル、または再生リストの場合、
# それぞれの動画URLリストを返します。
# ----------------------------------------------------
def extract_video_urls(input_url):
    # 先に ffmpeg の場所を適用（警告の抑制 & 後続統一）
    ffmpeg_dir = get_local_ffmpeg_dir()
    apply_ffmpeg_location_to_env(ffmpeg_dir)

    def get_info(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
            'ignoreerrors': True,
            'extractor_args': {
                'youtube': {
                    # webクライアントを外す。tv/ios/androidを優先
                    'player_client': ['tv', 'web', 'ios', 'android'],
                }
            },
        }
        # 見つかった場合のみ ffmpeg_location を渡す
        if ffmpeg_dir:
            ydl_opts['ffmpeg_location'] = ffmpeg_dir

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    # @を含むチャンネルハンドルURLの場合、自動的に/videosを付与
    if '@' in input_url and not input_url.endswith('/videos'):
        input_url = input_url.rstrip('/') + '/videos'

    try:
        info = get_info(input_url)
    except yt_dlp.utils.DownloadError as e:
        print(f"情報の取得中にエラーが発生しました: {e}")
        return []

    # 'entries' があれば複数動画 (チャンネル/再生リスト)
    if 'entries' in info and info['entries']:
        valid_urls = []
        for entry in info['entries'] or []:
            if not entry:
                continue
            availability = entry.get('availability', 'unknown')
            if availability in ('private', 'needs_auth', 'scheduled'):
                print(f"【SKIP】ID={entry.get('id')} (availability={availability})")
                continue
            live_status = entry.get('live_status', 'none')
            if live_status in ('not_started', 'is_upcoming'):
                print(f"【SKIP】ID={entry.get('id')} (live_status={live_status})")
                continue
            premiere_ts = entry.get('premiere_timestamp')
            if premiere_ts and premiere_ts > time.time():
                print(f"【SKIP】ID={entry.get('id')} (premiere in future)")
                continue

            url_candidate = entry.get('url') or entry.get('webpage_url')
            if url_candidate and 'watch?v=' in url_candidate:
                valid_urls.append(url_candidate)

        print(f"対象の動画数: {len(valid_urls)}")
        return valid_urls

    # 単一動画
    video_url = info.get('webpage_url')
    availability = info.get('availability', 'unknown')
    if availability in ('private', 'needs_auth', 'scheduled'):
        print(f"【SKIP】単一動画 (availability={availability}) → URL={video_url}")
        return []
    live_status = info.get('live_status', 'none')
    if live_status in ('not_started', 'is_upcoming'):
        print(f"【SKIP】単一動画 (live_status={live_status}) → URL={video_url}")
        return []
    premiere_ts = info.get('premiere_timestamp')
    if premiere_ts and premiere_ts > time.time():
        print(f"【SKIP】単一動画 (premiere in future) → URL={video_url}")
        return []

    if video_url and 'watch?v=' in video_url:
        print("単一動画が指定されました。")
        return [video_url]

    print("動画URLの取得に失敗しました。")
    return []
