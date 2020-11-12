# SNSToLambdaToSlack

## 目的
- 建立制式的 sns -> lambda -> slack 的回報機制
- 情境 : 可使用 alarm 來觸發 sns 來達到通知的目的

## 環境設定
- 設定憑證環境變數 : 
  - `export AWS_PROFILE=...`
  - `export AWS_REGION=...`
- template.yaml 設定參數
  - NotifyLambdaName
  - SlackHookUrl, ex : "https://hooks.slack.com/services/..."
  - InfoChannel, ex : "#general"
  - IssueChannel, ex : "#general"

## Deploy the sample application

```bash
sam build
sam deploy --guided
```

- 設定 stack name : `SNSToLambdaToSlack`
- 線上測試 : `aws sns publish --topic-arn $Get_SNS_Arn --subject "ServiceIssue" --message "hello world"`

## Use the SAM CLI to build and test locally

```bash
sam build
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


# 測試從 alarm 中觸發此服務

1. 建立 alarm, 觸發 sns topic
  - 設定名稱為 myAlarmToSNSToLambdaToSlack
2. `aws cloudwatch set-alarm-state --alarm-name myAlarmToSNSToLambdaToSlack --state-value ALARM --state-reason for_test`

``` alarm test issue
{
  "AlarmName": "myAlarmToSNSToLambdaToSlack",
  "AlarmDescription": "hello",
  "AWSAccountId": "424613967558",
  "NewStateValue": "ALARM",
  "NewStateReason": "for_test",
  "StateChangeTime": "2020-09-25T09:19:02.730+0000",
  "Region": "Asia Pacific (Singapore)",
  "AlarmArn": "arn:aws:cloudwatch:ap-southeast-1:424613967558:alarm:alarm",
  "OldStateValue": "INSUFFICIENT_DATA",
  "Trigger": {
    "MetricName": "test",
    "Namespace": "test",
    "StatisticType": "Statistic",
    "Statistic": "SUM",
    "Unit": null,
    "Dimensions": [],
    "Period": 300,
    "EvaluationPeriods": 1,
    "ComparisonOperator": "GreaterThanThreshold",
    "Threshold": 100000,
    "TreatMissingData": "- TreatMissingData:                    missing",
    "EvaluateLowSampleCountPercentile": ""
  }
}
```