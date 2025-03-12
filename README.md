# ソラグチ（空にグチをこぼすアプリ）
https://soraguchi-g9anc2e6hud4cqcw.japaneast-01.azurewebsites.net/soraguchi/

### 目的
- 天気のせいで憂鬱になることはありませんか？
- そのような方の生活の味方です。
- 気温の変化に左右される日々に対しての愚痴を共有して励まし合いましょう。
- 辛いのはあなただけではありません。
- （追加機能：AIにも相談できる...?）

### 使用技術
- Python3
- Django
- PostgreSQL
- Azure
- AWS Bedrock

### 機能
- ユーザー登録（id, name, email, password, prefecture, created_at, updated_at）
  - ログイン
- 投稿（id, title, content, user_id, created_at, updated_at）
  - 新規投稿
  - 投稿詳細、編集、削除
  - 投稿一覧(都道府県ごとの絞り込み)
- 天気データ（id, date, prefecture, temperature_max, temperature_min,　precipitation(降水確率), weather_type, description, created_at, updated_at）
  - 地域ごとの天気、降水確率、最高気温、最低気温の表示。
  - 一週間の天気の表示。
- AIコンテンツ（id, user_id, post_id, content, created_at, updated_at）
  - AIへの相談チャット。
  - ユーザーが希望するカテゴリーへの相談。
- カテゴリー（id, AiContent_id, cheering(励まし), clothes(洋服), washing(洗濯), farming(農業)）
  - ユーザーが指定したカテゴリーについて相談できる。（送るメッセージの効率化。）

#### 詳細
- ログインユーザー
  - 愚痴を発信し共有できる。
  - LINEと連携し、通知をもらうことができる。
- 未ログインユーザー
  - 天気を確認できる。
  - チャットに相談ができる。

### 今後実装したい機能
- 天気APIの導入。
- AIの導入。(AWS Bedrock)
  - 例：
  - 天気に合わせた洋服の提案。（洋服）
  - ドレスや水着を着る際に、何を羽織ったらいいか教えてくれる。（洋服）
  - 優しく元気づけてくれる。（励まし）
  - もっと天気が悪い地域を教えてくれる。（励まし）
  - 洗濯が有効かの判断をしてくれる。（洗濯）
  - そばの適切な水分量を教えてくれる。（料理）
  - 農業の進め方のアドバイスをくれる。（農業）
  - 車のワイパーを立てておいた方がいいか教えてくれる。（車）
  - 交通情報。（車）
  - スノボ。（スポーツ）
- Googleログイン機能
- LINE連携
  - 決まった時間に通知してくれる。

### AzureとAWS Bedrockを選んだ理由
- Azureに触れたことがなく、「面白そう」「触ってみたい」と思ったから。
- Bedrockはサーバーレスで管理しやすいことに加えて、複数のモデルを利用できることによるカスタマイズ性が高いから。


