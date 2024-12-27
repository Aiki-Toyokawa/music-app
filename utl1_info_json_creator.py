# utl1_info_json_creator.py

import os
import json
from datetime import datetime, timedelta

# ----------------------------------------------------
# YouTube動画の情報を抽出し、JSONファイルに保存します。
# Parameters:
#     info_dict (str): 情報を抽出するYouTube動画のURL。
#     json_filename (str): 出力するJSONファイルのパス。
# Returns:
#     dict: 抽出された情報データ。
# ----------------------------------------------------

def create_info_json(info_dict, each_video_folder_path):
    if not info_dict:
        print("有効な情報辞書が提供されていません。")
        return None

    # 必要な情報を抽出
    description_text = info_dict.get('description', '不明')
    description_list = description_text.splitlines() if description_text != '不明' else ['不明']

    # ------------------------------------------------
    # (A) 実際にダウンロードされた映像・音声ストリームを取得
    # ------------------------------------------------
    requested_formats = info_dict.get('requested_formats', [])
    downloaded_video = next((f for f in requested_formats if f.get('vcodec') != 'none'), None)
    downloaded_audio = next((f for f in requested_formats if f.get('acodec') != 'none'), None)

    actual_video_quality = '不明'
    actual_audio_quality = '不明'

    if downloaded_video and downloaded_video.get('height'):
        actual_video_quality = f"{downloaded_video['height']}p"

    if downloaded_audio and downloaded_audio.get('abr'):
        actual_audio_quality = f"{downloaded_audio['abr']}kbps"

    # ------------------------------------------------
    # (B) 全フォーマット情報から最高画質・最高音質を確認
    # ------------------------------------------------
    formats = info_dict.get('formats', [])
    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height')]
    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('abr')]

    highest_video_quality = '不明'
    if video_formats:
        best_video = max(video_formats, key=lambda f: f.get('height', 0))
        highest_video_quality = f"{best_video.get('height')}p"

    highest_audio_quality = '不明'
    if audio_formats:
        best_audio = max(audio_formats, key=lambda f: f.get('abr', 0))
        highest_audio_quality = f"{best_audio.get('abr')}kbps"

    # ------------------------------------------------
    # (C) JSONに書き込むデータを構築
    # ------------------------------------------------
    raw_data = {
        "title": info_dict.get('title', '不明'),
        "target_url": info_dict.get('webpage_url', '不明'),
        "thumbnail_url": info_dict.get('thumbnail', '不明'),
        "uploader": info_dict.get('uploader', '不明'),
        "uploader_id": info_dict.get('uploader_id', '不明'),
        "uploader_url": info_dict.get('uploader_url', '不明'),
        "channel": info_dict.get('channel', '不明'),
        "channel_id": info_dict.get('channel_id', '不明'),
        "channel_url": info_dict.get('channel_url', '不明'),
        "duration": str(timedelta(seconds=info_dict.get('duration', 0))),
        "serial_duration": info_dict.get('duration', 0),
        "upload_date": info_dict.get('upload_date', '不明'),
        "release_date": info_dict.get('release_date', '不明'),
        "video_id": info_dict.get('id', '不明'),
        "site_name": info_dict.get('extractor', '不明'),

        # 最高画質・音質
        "highest_video_quality": highest_video_quality,
        "highest_audio_quality": highest_audio_quality,

        # 実際にダウンロードされた画質・音質
        "actual_video_quality": actual_video_quality,
        "actual_audio_quality": actual_audio_quality,

        # 幅・高さ
        "video_width": downloaded_video.get('width', '不明') if downloaded_video else '不明',
        "video_height": downloaded_video.get('height', '不明') if downloaded_video else '不明',

        "age_limit": info_dict.get('age_limit', 0),

        # ★追加: 再生数・高評価数・低評価数
        "view_count": info_dict.get('view_count', 0),
        "like_count": info_dict.get('like_count', 0),
        "dislike_count": info_dict.get('dislike_count', 0),

        "categories": info_dict.get('categories', []),
        "video_tags": info_dict.get('tags', []),
        "description": description_list,
    }

    # ユーザーデータ
    user_data = {
        "user_edited_title": raw_data['title'],
        "user_download_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "user_notes": "",
        "user_tags": [],
    }

    # JSONとしてまとめる
    output_data = {
        "user_data": user_data,
        "raw_data": raw_data,
    }

    info_json_file_path = os.path.join(each_video_folder_path, 'info.json')
    try:
        print(f"動画情報をjsonファイルに書き込みます...\npath: {info_json_file_path}")
        with open(info_json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)
        print(f"動画情報の書き込み完了: {info_json_file_path}")
    except IOError as e:
        print(f"ファイルの書き込み中にエラーが発生しました: {e}")
        return None

    return info_json_file_path