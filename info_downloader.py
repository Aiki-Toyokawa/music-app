# info_downloader.py

import json 
from datetime import datetime, timedelta

class InfoDownloader:
    def __init__(self, output_filename="info.json"):
        """
        初期化メソッド。
        
        Parameters:
            output_filename (str): 出力するJSONファイルの名前。
        """
        self.output_filename = output_filename

    def time_convert(self, seconds):
        """
        秒数をHH:MM:SS形式またはMM:SS形式に変換します。
        
        Parameters:
            seconds (int): 秒数。
        
        Returns:
            str: 変換後の時間文字列。
        """
        try:
            sec = int(seconds)
            return str(timedelta(seconds=sec))
        except (ValueError, TypeError):
            return "00:00"

    def get_video_quality(self, info_dict):
        """
        利用可能な最高品質の動画解像度を取得します。
        
        Parameters:
            info_dict (dict): 動画の情報辞書。
        
        Returns:
            str: 動画品質（例："1080p"）または "N/A"。
        """
        try:
            formats = info_dict.get('formats', [])
            if not formats:
                return "N/A"
            # 高さが最大のフォーマットを選択
            best_format = max(formats, key=lambda x: x.get('height') or 0)
            height = best_format.get('height')
            return f"{height}p" if height else "N/A"
        except Exception as e:
            print(f"動画品質の取得中にエラーが発生しました: {e}")
            return "N/A"

    def get_audio_quality(self, info_dict):
        """
        利用可能な最高品質の音声ビットレートを取得します。
        
        Parameters:
            info_dict (dict): 動画の情報辞書。
        
        Returns:
            str: 音声品質（例："320 kbps"）または "N/A"。
        """
        try:
            formats = info_dict.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('abr')]
            if not audio_formats:
                return "N/A"
            best_audio = max(audio_formats, key=lambda x: x.get('abr') or 0)
            abr = best_audio.get('abr')
            return f"{abr} kbps" if abr else "N/A"
        except Exception as e:
            print(f"音声品質の取得中にエラーが発生しました: {e}")
            return "N/A"

    def extract_info(self, info_dict, output_filename=None):
        """
        動画情報を抽出し、指定されたJSONファイルに保存します。
        
        Parameters:
            info_dict (dict): 動画の情報辞書。
            output_filename (str): 出力するJSONファイルのパス。指定がない場合は初期化時の値を使用。
        
        Returns:
            dict: 抽出された情報データ。
        """
        if output_filename is None:
            output_filename = self.output_filename

        try:
            # 必要な情報を抽出
            title = info_dict.get('title', 'Unknown Title')
            target_url = info_dict.get('webpage_url', info_dict.get('url', 'Unknown URL'))
            thumbnail_url = info_dict.get('thumbnail', 'Unknown')
            uploader = info_dict.get('uploader', 'Unknown')
            uploader_id = info_dict.get('uploader_id', 'Unknown')
            uploader_url = info_dict.get('uploader_url', 'Unknown')
            channel = info_dict.get('channel', 'Unknown')
            channel_id = info_dict.get('channel_id', 'Unknown')
            channel_url = info_dict.get('channel_url', 'Unknown')
            duration_seconds = info_dict.get('duration', 0)
            duration = self.time_convert(duration_seconds)
            serial_duration = duration_seconds
            upload_date = info_dict.get('upload_date', 'Unknown')
            release_date = info_dict.get('release_date', 'Unknown')
            video_id = info_dict.get('id', 'Unknown')
            site_name = info_dict.get('extractor', 'Unknown')
            video_quality = self.get_video_quality(info_dict)
            audio_quality = self.get_audio_quality(info_dict)
            video_width = info_dict.get('width', 'Unknown')
            video_height = info_dict.get('height', 'Unknown')
            age_limit = info_dict.get('age_limit', 0)
            categories = info_dict.get('categories', [])
            video_tags = info_dict.get('tags', [])
            description_text = info_dict.get('description', 'Unknown')
            description_list = description_text.splitlines() if description_text != 'Unknown' else ['Unknown']

            # 現在の動画品質を取得
            current_format_id = info_dict.get('format_id', '')
            current_video_format = next((f for f in info_dict.get('formats', []) if f.get('format_id') == current_format_id), None)
            if current_video_format and current_video_format.get('height'):
                this_video_quality = f"{current_video_format.get('height')}p"
            else:
                this_video_quality = video_quality

            raw_data = {
                "title": title,
                "target_url": target_url,
                "thumbnail_url": thumbnail_url,
                "uploader": uploader,
                "uploader_id": uploader_id,
                "uploader_url": uploader_url,
                "channel": channel,
                "channel_id": channel_id,
                "channel_url": channel_url,
                "duration": duration,
                "serial_duration": serial_duration,
                "upload_date": upload_date,
                "release_date": release_date,
                "video_id": video_id,
                "site_name": site_name,
                "this_video_quality": this_video_quality,
                "video_quality": video_quality,
                "audio_quality": audio_quality,
                "video_width": video_width,
                "video_height": video_height,
                "age_limit": age_limit,
                "categories": categories,
                "video_tags": video_tags,
                "description": description_list,
            }

            user_data = {
                "user_edited_title": raw_data['title'],  # 必要に応じて編集可能
                "user_download_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "user_notes": "",
                "user_tags": [],
            }

            output_data = {
                "user_data": user_data,
                "raw_data": raw_data,
            }

            # JSONファイルに書き込み
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)

            print(f"情報が {output_filename} に保存されました。")
            return output_data

        except Exception as e:
            print(f"情報抽出中にエラーが発生しました: {e}")
            return None
