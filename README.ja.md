# stealthwatch-cloud-aws-lambda

* Stealthwatch Cloud APIを用いてフロー数を取得し、フロー数が一定値以下になったらLINE Notify で通知します。
* AWS EventBridgeからAWS Lambdaを定期実行し、フロー数が一定値以下になったらAWS S3にファイルを作成し、現在の状態を保存します。
