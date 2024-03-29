# 東京理科大学管弦楽団Discordボット
# 概要
- 東京理科大学管弦楽団内でのコミュニケーションを円滑にする機能を実装しています。

# コマンド一覧
## ユーザーコマンド
- このコマンドは、ユーザーのプロフィール画面の`アプリ`から呼び出せます。
### ユーザー情報を取得する
- 選択したユーザーのボット側の設定情報が送られます。（`出席率`、`出席コード閲覧権限`、`練習連絡DM受信権限`）
## メッセージコマンド
- このコマンドは、メッセージを右クリックまたは長押しし、表示されたメニューからアプリを選択した後、コマンド名を選択すると呼び出すことができます。
### 埋め込みテキストを転送する
- サーバー内の埋め込みテキストを、ボットとのDMチャンネルやサーバー内の任意のチャンネルに転送することができるコマンドです。
## アプリケーションコマンド
- このコマンドは、サーバー内の任意のチャンネル、またはスレッドで`/コマンド名`と入力することで、呼び出すことができます。
- コマンドによっては、コマンド名の他に引数を入力する必要があります。
- 緑色のボタンを押さない限り、他のユーザーにメッセージが閲覧されることはないです。
### `/dm` グループ
- 団員に、埋め込みテキストでDMを送る為のコマンド群です。
- 送信先リストは、`全員` `ロール` `チャンネル` `個人`から複数選ぶことができます。
- メニューの選択肢は15個ほどしか表示されませんが、直接入力することで最大25項目まで選択できます。

#### `/dm activity`
- 活動連絡DMを送る為のコマンドです。
- 引数に、`year` `month` `day` を必ず記入する必要があります。

##### 引数一覧
- `year` ... 開催する西暦を表します。`int型`を指定
- `month` ... 開催する月を表します。`int型`を指定
- `day` ... 開催する日を表します。`int型`を指定
- `start_hour` ... 始まる時間を表します。`int型`を指定、デフォルトでは`10`
- `start_minute` ... 始まる分を表します。`int型`を指定、デフォルトでは`0`
- `finish_hour` ... 終わる時間を表します。`int型`を指定、デフォルトでは`16`
- `finish_minute` ... 終わる分を表します。`int型`を指定、デフォルトでは`30`
- `prepare_minutes` ... 開始時刻の何分前に集合時間を設定するのかを指定します。`int型`を指定、デフォルトでは`15`
- `send_type` ... 受信者に送信先を表示するか選択できます。`Cc`, `Bcc`から選択、デフォルトでは`Cc`

#### `/dm normal`
- 通常連絡DMを送信する為のコマンドです。
##### 引数一覧
- `send_type` ... 受信者に送信先を表示するか選択できます。`Cc`, `Bcc`から選択、デフォルトでは`Cc`

#### `/dm alert`
- 緊急連絡DMを送信する為のコマンドです。
##### 引数一覧
- `send_type` ... 受信者に送信先を表示するか選択できます。`Cc`, `Bcc`から選択、デフォルトでは`Cc`

### `/ch` グループ
- 現在閲覧中のチャンネルに埋め込みテキストを送信する為のコマンド群です。
#### `/ch normal`
- 通常連絡を送信する為のコマンドです。

#### `/ch alert`
- 緊急連絡を送信する為のコマンドです。

#### `\ch upload_file`
- `Dropbox`を通してファイル共有を行うコマンドです。


### `/help` グループ
- 使い方ガイドを閲覧する為のコマンド群です。
#### `/help how_to_use`
- この説明書のURLが送られます。

#### `/help markdown_reference`
- Discordでテキストを装飾する為のMarkdown記法等の解説を閲覧できます。

### `/set` グループ
- ボット側の設定を閲覧するた為のコマンド群です。
#### `/set actibity_dm`
- 乗り番連絡DMを受信するかどうか設定することができます。
- `types`に、`受信する`か`受信しない`と設定する必要があります。

#### `/set profile`
- サーバー内のニックネームやロールの初期設定を行います。
- 基本的に使用する必要はありません。

### `/dev` グループ
- 開発者用コマンド群です。
- 一般的には使う必要はありません。

#### `/dev repo`
- `tus-orchestra-discord-bot`リポジトリを閲覧する為のコマンドです。

#### `/dev server`
- ホスティングサーバーの実行ログを閲覧する為のコマンドです。

### その他
#### `/status`
- 自身の設定情報が送られます。（`出席率`、`出席コード閲覧権限`、`練習連絡DM受信権限`）
#### `/preview`
- 送りたいテキストが実際にどのように表示されるのか確かめることができます。
- 閲覧後、閲覧しているチャンネルに送信することもできます。

# プログラムについて
- [ここ](https://github.com/dOtOb9/tus-orchestra-discord-bot/issues)に現在把握しているバグや導入予定の新機能について記載しています。
- サーバーには、[Railway](https://railway.app)というホスティングサービスを使っています。
- 

# 参考
- [【Discord】テキストを装飾する方法 | Markdown記法 チートシート](https://qiita.com/xero/items/6026ed007d5d34623a50)
<br> Discordでテキストに装飾できるMarkdown記法等の機能についてとても分かりやすくまとまっています。
