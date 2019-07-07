# スクレイピングツールby lambda
## ファイル概要
### models/*
scrap用DynamoDBのモデルファイル
pynamodbを利用して記述。

### lambda.json
lambda_uploadarに必要なファイル。
- role
  - Lambda関数のExecution Roleを設定
  - roleの作成は[こちら](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-intro-execution-role.html)参照
- refs
  - [AWS Lambda Pythonをlambda-uploaderでデプロイ](https://dev.classmethod.jp/cloud/deploy-aws-lambda-python-with-lambda-uploader/)
  - [github](https://github.com/rackerlabs/lambda-uploader)
  - [lambda-uploaderを使ってAWS Lambdaをリモートで開発、実行、デプロイする](https://qiita.com/Esfahan/items/08fa6af8811dada4cb2a)

### funacjp.py
Lambdaで呼び出すメイン処理ファイル。

### migrate.py
DynamoDBへの初期化処理やてテーブル削除など、migrate処理関連ファイル

### index.py
lambdaに接続するテストファイル

### requirements.txt
pipのインストールするパッケージファイル

#### 使い方

詳細は[こちら](https://pynamodb.readthedocs.io/en/latest/)
