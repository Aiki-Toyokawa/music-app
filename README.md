## git comment

- fix：バグ修正
- add：新規（ファイル）機能追加
- update：機能修正（バグではない）
- remove：削除（ファイル）
- move : 移動（ファイル） 

## file name

- ttl : total
- utl : utility


やること□
- チャンネル名dlのとき、~/@channel_id/videosのURL必要だが、~/@channel_idだけでもdlできるようにする実装をする
- 再生数の記録
- いいね、だめだねの記録 

- 優先度低い
  - リトライ機能



やったこと☑
- video_download_pathの命名変更と引数変更
- utl3_music_downloader.pyの削除
- utl3を削除したことによるutlの順序変更
- 画質が144pなどができない <- 144pがサポートされない拡張子やフォーマッタがある、不安定
- 動画のdl 再生リストは〇, ミックスリストは✖
- 一括dlの実装
- チャンネル全体の動画を一括dl