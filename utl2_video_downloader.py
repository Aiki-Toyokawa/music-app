# utl2_video_downloader.py

import os
import yt_dlp

from utl2_1_format_map import EASY_FORMAT_MAP, build_format_string, VIDEO_FORMATS, VIDEO_RESOLUTIONS, AUDIO_FORMATS, AUDIO_QUALITIES, CODECS

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
    
    if not ('youtube.com/' in video_url or 'youtu.be/' in video_url):
        print(f"無効なYoutube URLです: {video_url}")
        return None

    # ---------------------------
    # 1. フォーマットの設定
    # ---------------------------
    if len(format_code) == 1 and format_code in EASY_FORMAT_MAP:
        # easy_setting: 簡単設定を使用
        selected_format = EASY_FORMAT_MAP[format_code]
        print(f"Easy setting: 使用フォーマットコード '{format_code}' を選択")
        print(f"選択されたフォーマット: {selected_format}")
    elif len(format_code) == 5:
        # 詳細設定: 5桁のフォーマットコード
        video_format_code = format_code[0]
        resolution_code = format_code[1]
        audio_format_code = format_code[2]
        audio_quality_code = format_code[3]
        codec_code = format_code[4]

        video_format = VIDEO_FORMATS.get(video_format_code)
        resolution = VIDEO_RESOLUTIONS.get(resolution_code)
        audio_format = AUDIO_FORMATS.get(audio_format_code)
        audio_quality = AUDIO_QUALITIES.get(audio_quality_code)
        codec = CODECS.get(codec_code)

        if not (video_format and resolution and audio_format and audio_quality and codec):
            print(f"詳細設定のフォーマットコードが無効です: {format_code}")
            return None

        selected_format = build_format_string(video_format, resolution, audio_format, audio_quality, codec)
        print(f"詳細設定: 使用フォーマットコード '{format_code}' を選択")
        print(f"動画形式: {video_format} ({video_format_code})")
        print(f"動画画質: {resolution}p ({resolution_code})")
        print(f"音声形式: {audio_format} ({audio_format_code})")
        print(f"音声の音質: {audio_quality} ({audio_quality_code})")
        print(f"コーデック: {codec} ({codec_code})")
        print(f"選択されたフォーマット: {selected_format}")
    else:
        print(f"無効なフォーマットコードです: {format_code}")
        return None
    

    # ---------------------------
    # 2. 動画ダウンロード
    # ---------------------------
    print("動画のダウンロードを開始します...")
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
                print(f"動画情報の取得に失敗しました: {video_url}")
                return None
            print(f"動画のダウンロードが完了しました: {video_url}")
            return info_dict
    except yt_dlp.utils.DownloadError as e:
        print(f"ダウンロードエラー: {e}")
        return None
