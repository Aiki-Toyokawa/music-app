# utl1_video_urls_extractor.py

import yt_dlp
import time

# ----------------------------------------------------
# 指定されたURLが単一動画、チャンネル、または再生リストの場合、
# それぞれの動画URLリストを返します。
#
# Parameters:
#     input_url (str): 単一動画、チャンネル、または再生リストのURL。
# 
# Returns:
#     list: 動画URLのリスト。取得に失敗した場合は空リスト。
#           公開前などダウンロード不可な動画も除外する。
# ----------------------------------------------------

def extract_video_urls(input_url):
    def get_info(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
            'ignoreerrors': True,
        }
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

    # ---------------------------------------------
    # 'entries' があれば複数動画 (チャンネルや再生リストなど)
    # なければ単一動画の可能性
    # ---------------------------------------------
    if 'entries' in info and info['entries']:
        valid_urls = []
        for entry in info['entries']:
            if not entry:
                continue

            # 1) availability (scheduled/private/needs_auth など) 判定
            availability = entry.get('availability', 'unknown')
            if availability in ('private', 'needs_auth', 'scheduled'):
                print(f"【SKIP】ID={entry.get('id')} (availability={availability})")
                continue

            # 2) live_status（ライブ配信やプレミア関連の可能性を確認）
            #    'not_started'/'is_upcoming' などがあれば未公開扱いとみなしてスキップ
            live_status = entry.get('live_status', 'none')
            if live_status in ('not_started', 'is_upcoming'):
                print(f"【SKIP】ID={entry.get('id')} (live_status={live_status})")
                continue

            # 3) premiere_timestamp から「公開時刻が現在時刻より先なら未公開」としてスキップ
            premiere_ts = entry.get('premiere_timestamp')
            if premiere_ts and premiere_ts > time.time():
                print(f"【SKIP】ID={entry.get('id')} (premiere in future)")
                continue

            # 4) watch?v= が含まれるURLならダウンロード対象とみなす
            url_candidate = entry.get('url') or entry.get('webpage_url')
            if url_candidate and 'watch?v=' in url_candidate:
                valid_urls.append(url_candidate)

        print(f"対象の動画数: {len(valid_urls)}")
        return valid_urls
    else:
        # 単一動画の場合
        video_url = info.get('webpage_url')
        availability = info.get('availability', 'unknown')

        # 1) availability 判定
        if availability in ('private', 'needs_auth', 'scheduled'):
            print(f"【SKIP】単一動画 (availability={availability}) → URL={video_url}")
            return []

        # 2) live_status 判定
        live_status = info.get('live_status', 'none')
        if live_status in ('not_started', 'is_upcoming'):
            print(f"【SKIP】単一動画 (live_status={live_status}) → URL={video_url}")
            return []

        # 3) premiere_timestamp 判定
        premiere_ts = info.get('premiere_timestamp')
        if premiere_ts and premiere_ts > time.time():
            print(f"【SKIP】単一動画 (premiere in future) → URL={video_url}")
            return []

        if video_url and 'watch?v=' in video_url:
            print("単一動画が指定されました。")
            return [video_url]

        print("動画URLの取得に失敗しました。")
        return []
