# stealthwatch-cloud-aws-lambda

* Stealthwatch Cloud APIを用いてフロー数を取得し、フロー数が一定値以下になったらLINE Notify で通知します。
* AWS EventBridgeからAWS Lambdaを定期実行し、フロー数が一定値以下になったらAWS S3にファイルを作成し、現在の状態を保存します。

## 実行方法
AWS, Stealthwatch Cloud, LINEのアカウントは取得済の前提で記載します。
1. Stealthwatch Cloud の API Credentials を取得します。
Stealthwatch Cloud の Your Setting のページで API Credentials を取得します。

1. LINE Notify アクセストークンの発行
[LINE Notify マイページ](https://notify-bot.line.me/ja/)でアクセストークンを発行します。

1. AWS IAM role 作成
[AWS IAM role](https://console.aws.amazon.com/iam/home?#/roles) で
「ロールの作成」ボタンを押し、ポリシーに
* AmazonS3FullAccess
* AWSLambdaExecute
をアタッチした lambda-s3fullaceess-role というロールを作成します。
