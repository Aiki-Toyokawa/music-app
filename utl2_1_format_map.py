# utl2_1_format_map.py

# 動画形式のマッピング 0
VIDEO_FORMATS = {
    '0': 'mp4',    # MPEG-4 Part 14
    '1': 'webm',   # WebM format
    '2': 'flv',    # Flash Video
    '3': 'mkv',    # Matroska Video
    '4': 'avi',    # Audio Video Interleave
    '5': 'mov',    # QuickTime File Format
    '6': 'wmv',    # Windows Media Video
    '7': 'mpeg4',  # MPEG-4 Part 2
    '8': '3gp',    # 3GPP format
    '9': 'mpeg',   # MPEG-1 or MPEG-2
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
}

# 音声形式のマッピング 2
AUDIO_FORMATS = {
    '0': 'flac',    # Free Lossless Audio Codec - 最も高品質な無損失音声形式
    '1': 'mp3',     # MPEG-1 Audio Layer III - 最も汎用性が高い音声形式
    '2': 'aac',     # Advanced Audio Coding - 高圧縮効率と高音質を両立
    '3': 'wav',     # Waveform Audio File Format - 無圧縮の高品質音声形式
    '4': 'opus',    # Opus Interactive Audio Codec - 高効率で低遅延のオープン音声形式
    '5': 'ogg',     # Ogg Vorbis - オープンソースの音声圧縮形式
    '6': 'm4a',     # MPEG-4 Audio - AACを含むコンテナ形式
    '7': 'alac',    # Apple Lossless Audio Codec - Apple製の無損失音声形式
    '8': 'aiff',    # Audio Interchange File Format - Apple製の非圧縮音声形式
    '9': 'wma',     # Windows Media Audio - Microsoft製の音声圧縮形式
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
    '0': 'h264',    # Advanced Video Coding (AVC) - 最も広く使用されているビデオコーデック
    '1': 'h265',    # High Efficiency Video Coding (HEVC) - h264の後継で高い圧縮効率
    '2': 'vp8',     # VP8 - オープンソースのビデオコーデック、主にWeb向け
    '3': 'vp9',     # VP9 - VP8の後継で、さらに高い圧縮効率を提供
    '4': 'av1',     # AV1 - 次世代のオープンソースコーデック、HEVCに匹敵する圧縮効率
    '5': 'theora',  # Theora - オープンソースのビデオコーデック、主にWeb用途
    '6': 'mpeg4',   # MPEG-4 Part 2 - 広く使用されている古典的なビデオコーデック
    '7': 'mpeg2',   # MPEG-2 - DVDやデジタルテレビ放送で使用されるビデオコーデック
    '8': 'mpeg1',   # MPEG-1 - VCDや初期のデジタルビデオカメラで使用
    '9': 'xvid',    # Xvid - MPEG-4 Part 2のオープンソース実装、広くサポートされている
}

# easy_setting が True の場合のフォーマットマッピング
EASY_FORMAT_MAP = {
    '0': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # デフォルト
    '1': 'bestvideo[ext=mp4][height=480]+bestaudio[ext=m4a]/best[ext=mp4]',
    '2': 'bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/best[ext=mp4]',
    '3': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
    'a': 'bestaudio/best[ext=mp4]',  # 音声のみ
}

def build_format_string(video_format=None, resolution=None, audio_format=None, audio_quality=None, codec=None):
    if video_format and resolution and audio_format and audio_quality and codec:
        format_str = f"bestvideo[ext={video_format}][vcodec={codec}][height={resolution}]+bestaudio[ext={audio_format}][acodec=aac]/best[ext={video_format}]"
        return format_str
    else:
        # デフォルト
        return EASY_FORMAT_MAP.get('0')
