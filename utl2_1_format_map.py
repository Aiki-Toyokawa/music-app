# utl2_1_format_map.py

FORMAT_MAP = {
    # デフォルト (映像1080p,音声最良を取得, フロントで「デフォルト」として表示)
    'd': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
    # 音声のみ (フロントで「音声のみ」として表示)
    'a': 'bestaudio[ext=m4a]/bestaudio/best',
    # 明示的な上限指定プリセット
    '144' : 'bestvideo[ext=mp4][height<=144]+bestaudio[ext=m4a]/best[ext=mp4]',
    '240' : 'bestvideo[ext=mp4][height<=240]+bestaudio[ext=m4a]/best[ext=mp4]',
    '360' : 'bestvideo[ext=mp4][height<=360]+bestaudio[ext=m4a]/best[ext=mp4]',
    '480' : 'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4]',
    '720' : 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]',
    '1080': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',  # 明示的に1080p
    '1440': 'bestvideo[ext=mp4][height<=1440]+bestaudio[ext=m4a]/best[ext=mp4]',  # 追加: 1440p上限
    '2160': 'bestvideo[ext=mp4][height<=2160]+bestaudio[ext=m4a]/best[ext=mp4]',
    '4320': 'bestvideo[ext=mp4][height<=4320]+bestaudio[ext=m4a]/best[ext=mp4]',
}
