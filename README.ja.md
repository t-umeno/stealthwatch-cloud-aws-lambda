# stealthwatch-cloud-aws-lambda

* Stealthwatch Cloud APIを用いてフロー数を取得し、フロー数が一定値以下になったらLINE Notify で通知します。
* AWS EventBridgeからAWS Lambdaを定期実行し、フロー数が一定値以下になったらAWS S3にファイルを作成し、現在の状態を保存します。

## 実行方法
AWS, Stealthwatch Cloud, LINEのアカウントは取得済の前提で記載します。

1. Ubuntu 18.04 LTS 環境を用意します。  
[Ubuntu 18.04.5 LTS (Bionic Beaver)](https://releases.ubuntu.com/18.04.5/)からISOイメージなどを入手し、パソコンやVirtualBoxなどの環境でUbuntu 18.04 LTSをインストールします。

1. Ubuntu 18.04 LTS 上に AWS CLI バージョン2 をインストールします。  
[Linux での AWS CLI バージョン 2 のインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-linux.html) の記載に従って AWS CLI バージョン2をインストールします。

1. AWS IAM グループ AdministratorGroup 作成  
[AWS IAM グループ](https://console.aws.amazon.com/iam/home#/groups) で「新しいグループの作成」ボタンを押し、グループ名に「AdministratorGroup」を指定し、「ポリシーのアタッチ」で「AdministratorAccess」を選択したグループを作成します。

1. AWS IAM ユーザー administrator 作成  
[AWS IAM ユーザー](https://console.aws.amazon.com/iam/home#/users) で「ユーザーを追加」ボタンを押し、「ユーザー詳細の設定」の「ユーザー名」に「administrator」を入力、「プログラムによるアクセス」にチェックし、「次のステップ: アクセス権限」
を押し、「ユーザーをグループに追加」で「AdministratorGroup」にチェックを押し、「次のステップ: タグ」を押し、「次のステップ: 確認」を押し、「ユーザーの作成」を押して、ユーザーを作成します。

1. AWS CLI バージョン 2 の設定を行います。  
[設定の基本](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html) に沿ってAWS CLI バージョン 2 の設定を行います。

[アクセスキー ID とシークレットアクセスキー](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds)に記載された方法で administrator の アクセスキー ID とシークレットアクセスキー を入手します。

[aws configure を使用したクイック設定](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) に沿って設定を行います。必要に応じて Default region name を設定してください。

```
$ aws configure
AWS Access Key ID [None]: 入手したアクセスキー ID
AWS Secret Access Key [None]: 入手したシークレットアクセスキー
Default region name [None]: us-west-2
Default output format [None]: json
```

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
