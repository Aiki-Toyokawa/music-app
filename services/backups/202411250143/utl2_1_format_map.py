# utl2_1_format_map.py

# 動画形式のマッピング
VIDEO_FORMATS = {
    '0': 'mp4',
    '1': 'webm',
    # 必要に応じて追加
}

# 動画の画質のマッピング
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

# 音声形式のマッピング
AUDIO_FORMATS = {
    '0': 'm4a',
    '1': 'webm',
    '2': 'mp3',
    # 必要に応じて追加
}

# 音声の音質のマッピング
AUDIO_QUALITIES = {
    '0': '128k',
    '1': '192k',
    '2': '256k',
    '3': '320k',
    # 必要に応じて追加
}

# コーデックのマッピング
CODECS = {
    '0': 'h264',
    '1': 'vp9',
    '2': 'av1',
    # 必要に応じて追加
}

# easy_setting が True の場合のフォーマットマッピング
EASY_FORMAT_MAP = {
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

def build_format_string(video_format=None, resolution=None, audio_format=None, audio_quality=None, codec=None):
    if video_format and resolution and audio_format and audio_quality and codec:
        format_str = f"bestvideo[ext={video_format}][vcodec={codec}][height={resolution}]+bestaudio[ext={audio_format}][acodec=aac]/best[ext={video_format}]"
        return format_str
    else:
        # デフォルト
        return EASY_FORMAT_MAP.get('0')
