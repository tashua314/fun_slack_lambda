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


## 参考

[公式ドキュメント](https://pynamodb.readthedocs.io/en/latest/)
[PynamoDB参考記事](https://qiita.com/ykarakita/items/2bb4c951cbcb8771c3af#%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E4%BD%9C%E6%88%90)
[ここにハマったDynamoDB](https://blog.brains-tech.co.jp/entry/2015/09/30/222148)
[pylint](http://pylint.pycqa.org/en/latest/)
