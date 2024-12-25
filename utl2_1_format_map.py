# utl2_1_format_map.py

FORMAT_MAP = {
    '0': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # デフォルト
    '1': 'bestvideo[ext=mp4][height=144]+bestaudio[ext=m4a]/best[ext=mp4]',
    '2': 'bestvideo[ext=mp4][height=240]+bestaudio[ext=m4a]/best[ext=mp4]',
    '3': 'bestvideo[ext=mp4][height=360]+bestaudio[ext=m4a]/best[ext=mp4]',
    '4': 'bestvideo[ext=mp4][height=480]+bestaudio[ext=m4a]/best[ext=mp4]',
    '5': 'bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/best[ext=mp4]',
    '6': 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
    '7': 'bestvideo[ext=mp4][height=2160]+bestaudio[ext=m4a]/best[ext=mp4]',
    'a': 'bestaudio[ext=m4a]/bestaudio/best',  # 音声のみ
}
