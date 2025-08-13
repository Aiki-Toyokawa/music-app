# utl1_video_urls_extractor.py

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

    # @を含むチャンネルハンドルURLの場合、自動的に/videosを付与
    if '@' in input_url and not input_url.endswith('/videos'):
        input_url = input_url.rstrip('/') + '/videos'

    try:
        info = get_info(input_url)
    except yt_dlp.utils.DownloadError as e:
        print(f"情報の取得中にエラーが発生しました: {e}")
        return []

    if 'entries' in info and info['entries']:
        raw_video_urls = [
            entry['url'] if 'url' in entry else entry.get('webpage_url') 
            for entry in info['entries'] if entry
        ]
        video_urls = [url for url in raw_video_urls if url and 'watch?v=' in url]
        print(f"対象の動画数: {len(video_urls)}")
        return video_urls
    else:
        # 単一動画の場合の確認
        video_url = info.get('webpage_url')
        if video_url and 'watch?v=' in video_url:
            print("単一動画が指定されました。")
            return [video_url]

        print("動画URLの取得に失敗しました。")
        return []
