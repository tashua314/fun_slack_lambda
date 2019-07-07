# fun_slack_lambda
## 概要
関連情報を定期的にスクレイピングし、
slackに流す。

## 利用ツール
- AWS Batch
  - 定期的にlambdaのスクリプトをを呼び出す
- AWS Lambda
  - Batchで呼び出される処理部
    - pythonで記述
  - 主な処理部
- AWS DynamoDB
  - 過去のスクレイピング情報の保管

## 処理フロー
1. AWS Batch
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
  - funacjp.py
    - 公立はこだて未来大学の公式サイトを処理
  - migrate.py
    - 全テーブルへの処理ツール
  - models/
    - DynamoDBのモデル一覧
    - 詳細は[/lambda/README.md](./lambda/README.md)
- batch/
  - Batch関連

## 関連情報一覧
- [公立はこだて未来大学公式HP](https://www.fun.ac.jp/)
