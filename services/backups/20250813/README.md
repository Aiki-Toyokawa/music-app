## バックアップ 20250813 内容

jsonファイル出力オンリー
ローカルffmpegとvenvでpython runtime以外のグローバル依存を排除


## pull後の環境構築
```
# python の存在・バージョン確認(入っている python 一覧表示)
py -0p

# 仮想環境 .venvを入れる
# 最新の Python 3 系で作成（3.13 指定なら py -3.13 -m venv .venv）
py -3 -m venv .venv 

# 仮想環境有効化
./.venv/Scripts/Activate.ps1

# 仮想環境無効化
deactivate

# pip更新
python.exe -m pip install --upgrade pip

# pip で requirements.txt からインストール
pip install -r requirements.txt

# ffmpegのローカルインストール
./third_party/ffmpeg/update_ffmpeg.ps1
```


## git comment

- fix：バグ修正
- add：新規（ファイル）機能追加
- update：機能修正（バグではない）
- remove：削除（ファイル）
- move : 移動（ファイル）

## file name

- ttl : total
- utl : utility


## やること□ (なるべく優先度順)
- ttl_merge.pyのmain引数は現在ハードコーディングしているformat_code, download_dir, input_url
- component-2を作成し、そちらでUIフロントエンドを作成していく
- yt-dlpの標準機能のcommand-line dl parcent(とdl速度/sec)から動的に値を取得してUIで表示する
- 中断と再会処理

## やったこと☑ (消化が新しい順, 積層式)
- 公開予定動画があると、それもdlしようとしてエラーで止まるのを防ぐ
- electron + vite + svelteで作る -> electron, vanilla JSでやる
- utlの順番を変更
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
git checkout -b feature/add-login-function

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


Happy New Year!! 2025/01/01 <- in Sendai Morning
