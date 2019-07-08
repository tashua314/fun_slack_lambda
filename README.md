# fun_slack_lambda
## 概要
関連情報を定期的にスクレイピングし、
slackに流す。

## 利用ツール
- AWS CloudWatch
  - 定期的にlambdaのスクリプトをを呼び出す
- AWS Lambda
  - Batchで呼び出される処理部
    - pythonで記述
  - 主な処理部
- AWS DynamoDB
  - 過去のスクレイピング情報の保管

## 処理フロー
1. AWS CloudWatch
    1. Lambdaの処理を呼び出す
1. AWS Lambda
    1. 過去のスクレイピングデータをDynamoDBから取得
    1. 現ページに記載されている情報をスクレイピング
    1. 過去登録されているかどうかを比較
    1. 登録されていないデータをDynamoDBへ登録
    1. 登録されたデータをSlackへ通知

## ディレクトリ構成
- lambda/
  - Lambdaで起動するファイル群
  - 詳細は[/lambda/README.md](./lambda/README.md)
- bin/lambda-exec
  - lambdaの関数の実行ファイル
  - `lambda/event.json` をパラメータとして設定可能（本関数では不要）
- 実行例
  - `bin/lambda-exec scrapAndTweetToSlack lambda/envent.json`

## 利用手順
### 環境準備
1. virtualenvの環境を用意する
1. `virtualenv env`
1. `source env/bin/active`
1. `pip install -r lambda/requirements.txt` で必要パッケージインストール
1. awscliコマンドをインストールしてAWSにアクセスできる状態にする
    - `aws configure`
1. AWS Lambdaで関数を作成する
1. IAMで、LambdaとDynamoDBへのアクセスが可能なroleを作成する
1. `lambda.json` を調整する
    - role: IAMにて作成したroleのarnを設定
    - region: Lambdaにて作成した関数のregionを設定
    - その他変更箇所があれば
1. CloudWatchにスケジュールを設定してLambdaの作成した関数と紐付ける
1. 環境変数にSlackのapikeyなどを設定する

### 初期化
- `cd lambda`
- DynamoDB上に必要なテーブルを作成する
  - `python migrate.py create_tables`
- デプロイする
  - `lambda-uploader`
- 実行してみる(テスト)
  - `../bin/lambda-exec scrapAndTweetToSlack event.json`

## 関連情報一覧
- [公立はこだて未来大学公式HP](https://www.fun.ac.jp/)

## 注意
- virtualenvの設定ディレクトリ `env/` は、プロジェクトルートに置く。
  - `lambda/`ディレクトリ配下に置くと、`lambda_uploader` 実行時に一緒にパッケージングしようとして、アップロードファイルサイズが大きくなってしまう
- lambda_uploaderはlambdaディレクトリにて実行する
