# fun_slack_lambda
## 概要
関連情報を定期的にスクレイピングし、
funのslackに流す。

## 構成
- AWS Batch
  - 定期実行の設定
- AWS Lambda
  - Batchで呼び出される処理部
    - python
- AWS DynamoDB
  - 過去のスクレイピング情報の保管
