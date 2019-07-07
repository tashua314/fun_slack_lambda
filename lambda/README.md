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


#### 使い方

詳細は[こちら](https://pynamodb.readthedocs.io/en/latest/)

## 注意
- `env/` は、プロジェクトルートに置く。
  - `lambda/`ディレクトリ配下に置くと、`lambda_uploader` 実行時に一緒にパッケージングしようとして、アップロードファイルサイズが大きくなってしまう
- lambda_uploaderはlambdaディレクトリにて実行する
