# utl5_video_url_extractor.py

import yt_dlp

def extract_video_url(input_url):
    """
    指定されたURLが単一動画、チャンネル、または再生リストの場合、
    それぞれの動画URLリストを返します。

    Parameters:
        input_url (str): 単一動画、チャンネル、または再生リストのURL。

    Returns:
        list: 動画URLのリスト。取得に失敗した場合は空リスト。
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # メタ情報のみを取得
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(input_url, download=False)
            if 'entries' in info:
                # プレイリストまたはチャンネルの場合
                video_urls = [entry['url'] if 'url' in entry else entry.get('webpage_url') 
                              for entry in info['entries'] if entry]
                print(f"対象の動画数: {len(video_urls)}")
                return video_urls
            else:
                # 単一動画の場合
                print("単一動画が指定されました。")
                return [info.get('webpage_url')]
        except yt_dlp.utils.DownloadError as e:
            print(f"情報の取得中にエラーが発生しました: {e}")
            return []
