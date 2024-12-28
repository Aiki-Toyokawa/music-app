## git comment

- fix：バグ修正
- add：新規（ファイル）機能追加
- update：機能修正（バグではない）
- remove：削除（ファイル）
- move : 移動（ファイル）

## file name

- ttl : total
- utl : utility


## やること□
- component-2を作成し、そちらでUIフロントエンドを作成していく
- yt-dlpの標準機能のcommand-line dl parcent(とdl速度/sec)から動的に値を取得してUIで表示する


## やったこと☑ (消化が新しい順, 積層式)
- メンバーシップ限定動画のdl処理でエラーがでるのでdlしないようにする
- リトライ機能 -> yt-dlpについてた
- utl1での画質や音質のハードコーディングをやめる
- いいね、だめだねの記録 
- 再生数の記録
- dlの各種設定を画質だけに限定する -> easy_settingだけでよい
- チャンネル名dlのとき、~/@channel_id/videosのURL必要だが、~/@channel_idだけでもdlできるようにする実装をする
- チャンネル全体の動画を一括dl
- 一括dlの実装
- 動画のdl 再生リストは〇, ミックスリストは✖
- 画質が144pなどができない <- 144pがサポートされない拡張子やフォーマッタがある、不安定
- utl3を削除したことによるutlの順序変更
- utl3_music_downloader.pyの削除
- video_download_pathの命名変更と引数変更


## git branch commit push merge

### 1. メインブランチに切り替え
git checkout main

### 2. リモートメインブランチの最新を取得
git pull origin main

### 3. 新しい機能ブランチを作成して切り替え
git checkout -b feature/add-login-functionality

### 4. 変更をステージング
git add .

### 5. 変更をコミット
git commit -m "Add login functionality"

### 6. 新機能ブランチをリモートにプッシュ
git push origin feature/add-login-functionality

#### （GitHub上でPull Requestを作成・マージ）

### 7. メインブランチに戻る
git checkout main

### 8. リモートメインブランチの最新を取得
git pull origin main

### 9. ローカルの機能ブランチを削除（任意）
git branch -d feature/add-login-functionality

### 10. リモートの機能ブランチを削除（任意）
git push origin --delete feature/add-login-functionality
