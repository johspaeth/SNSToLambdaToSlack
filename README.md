# SNSToLambdaToSlack

## 目的
- 建立制式的 sns -> lambda -> slack 的回報機制
  - 使用 sns subject 來區分不同的任務回報類型
- 情境
  - 可使用 alarm 來觸發 sns 來達到通知的目的

## 環境設定
- 設定憑證環境變數 : `export AWS_PROFILE=...`
- template.yaml 設定 slack 參數
  - hookUrl, ex : "https://hooks.slack.com/services/..."
  - slackChannel, ex : "#general"

## Deploy the sample application

```bash
sam build --use-container
sam deploy --guided
```

- 設定 stack name : `SNSToLambdaToSlack`
- 線上測試 : `aws sns publish --topic-arn $Get_SNS_Arn --subject "ServiceIssue" --message "hello world"`

## Use the SAM CLI to build and test locally

```bash
sam build --use-container
sam local invoke SNSToLambdaToSlack --event events/event.json
```

## Fetch, tail, and filter Lambda function logs

```bash
sam logs -n myLambdaToSlack --stack-name SNSToLambdaToSlack --tail
```

## Cleanup

```bash
aws cloudformation delete-stack --stack-name SNSToLambdaToSlack
```
