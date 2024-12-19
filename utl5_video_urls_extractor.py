# utl5_video_urls_extractor.py

import yt_dlp

# ----------------------------------------------------
# 指定されたURLが単一動画、チャンネル、または再生リストの場合、
# それぞれの動画URLリストを返します。
#
# Parameters:
#     input_url (str): 単一動画、チャンネル、または再生リストのURL。
# 
# Returns:
#     list: 動画URLのリスト。取得に失敗した場合は空リスト。
# ----------------------------------------------------

def extract_video_urls(input_url):
    def get_info(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    try:
        # まずはそのまま取得
        info = get_info(input_url)
    except yt_dlp.utils.DownloadError as e:
        print(f"情報の取得中にエラーが発生しました: {e}")
        return []

    if 'entries' in info and info['entries']:
        # 一覧が取得できた場合
        raw_video_urls = [
            entry['url'] if 'url' in entry else entry.get('webpage_url') 
            for entry in info['entries'] if entry
        ]
        video_urls = [url for url in raw_video_urls if url and 'watch?v=' in url]
        print(f"対象の動画数: {len(video_urls)}")
        return video_urls
    else:
        # 一覧が取得できていない場合、チャンネルハンドルの場合は/videosを付けて再試行
        if '@' in input_url and not input_url.endswith('/videos'):
            try:
                info_videos = get_info(input_url.rstrip('/') + '/videos')
                if 'entries' in info_videos and info_videos['entries']:
                    raw_video_urls = [
                        entry['url'] if 'url' in entry else entry.get('webpage_url')
                        for entry in info_videos['entries'] if entry
                    ]
                    video_urls = [url for url in raw_video_urls if url and 'watch?v=' in url]
                    print(f"対象の動画数: {len(video_urls)} (/videos を付与して再取得)")
                    return video_urls
            except yt_dlp.utils.DownloadError as e:
                print(f"/videos 経由でも取得に失敗しました: {e}")

    # 単一動画の場合の確認
    video_url = info.get('webpage_url')
    if video_url and 'watch?v=' in video_url:
        print("単一動画が指定されました。")
        return [video_url]

    print("動画URLの取得に失敗しました。")
    return []
