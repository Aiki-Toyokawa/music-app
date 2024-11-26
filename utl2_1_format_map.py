# utl2_1_format_map.py

# 動画形式のマッピング 0
VIDEO_FORMATS = {
    '0': 'mp4',
    '1': 'webm',
    '2': 'flv',
    '3': 'mkv',
    '4': 'avi',
    '5': 'mov',
}

# 動画の画質のマッピング 1
VIDEO_RESOLUTIONS = {
    '0': '144',
    '1': '240',
    '2': '360',
    '3': '480',
    '4': '720',
    '5': '1080',
    '6': '1440',
    '7': '2160',
    '8': '4320',
    # 必要に応じて追加
}

# 音声形式のマッピング 2
AUDIO_FORMATS = {
    '0': 'm4a',
    '1': 'webm',
    '2': 'mp3',
    '3': 'opus',
    '4': 'aac',
    '5': 'flac',
    '6': 'wav',
}

# 音声の音質のマッピング 3
AUDIO_QUALITIES = {
    '1': '64k',
    '2': '96k',
    '3': '128k',
    '4': '160k',
    '5': '192k',
    '6': '256k',
    '7': '320k',
    '8': '384k',
}

# コーデックのマッピング 4
CODECS = {
    '0': 'h264',
    '1': 'vp9',
    '2': 'av1',
    '3': 'h265',
    '4': 'vp8',
    '5': 'theora',
    '6': 'mpeg4',
}

# easy_setting が True の場合のフォーマットマッピング
EASY_FORMAT_MAP = {
    '0': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # デフォルト
    '1': 'bestvideo[ext=mp4][height=144]+bestaudio[ext=m4a]/best[ext=mp4]',
    '3': 'bestvideo[ext=mp4][height=360]+bestaudio[ext=m4a]/best[ext=mp4]',
    '4': 'bestvideo[ext=mp4][height=480]+bestaudio[ext=m4a]/best[ext=mp4]',
    '5': 'bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/best[ext=mp4]',
    '6': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
    'a': 'bestaudio[ext=m4a]/best[ext=m4a]',  # 音声のみ
}

def build_format_string(video_format=None, resolution=None, audio_format=None, audio_quality=None, codec=None):
    if video_format and resolution and audio_format and audio_quality and codec:
        format_str = f"bestvideo[ext={video_format}][vcodec={codec}][height={resolution}]+bestaudio[ext={audio_format}][acodec=aac]/best[ext={video_format}]"
        return format_str
    else:
        # デフォルト
        return EASY_FORMAT_MAP.get('0')
