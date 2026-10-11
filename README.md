# HP Visual Editor

Streamlitで動く、ホームページ用の視覚編集アプリです。画像、動画、文字、ボタンを中央キャンバスで直接動かし、完成した `index.html` / `style.css` / `script.js` / `project.json` を書き出せます。

## 起動

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```

## 最初に押すボタン

左の「画像を追加」「動画を追加」「文字を追加」から始めます。中央の画面で直接ドラッグ移動、四隅リサイズ、文字の直接編集ができます。

## 既存ホームページの読み込み

上部の「既存ページ / project.json」から `project.json` を読み込むと編集状態を復元できます。HTMLファイルを読み込むと、内容を編集用セクションとして配置します。

## 動画リンクの登録

左下の「動画ライブラリ」から、動画タイトル、YouTube URL、MP4 URL、サムネイル、カテゴリを登録します。「ページに追加」で中央キャンバスへ配置できます。

## 保存と書き出し

「保存」で `export/` フォルダへ出力します。「project.jsonをダウンロード」で編集状態を保存し、「ZIP書き出し」でGitHub Pagesへ置ける形式をまとめて取得できます。

## GitHub連携

Streamlit Secrets に以下のどちらかを設定してください。トークンはソースコードに書かないでください。

```toml
GITHUB_TOKEN = "github_pat_xxx"
```

または:

```toml
[github]
token = "github_pat_xxx"
```

アプリ内の「GitHubへ反映」でユーザー名、リポジトリ名、ブランチを指定すると、書き出しファイルをGitHubへ反映します。
