# AWS Daily Cost Usage Reports

AWS Cost And Usage report to Slack on daily 09:01.

* Report type

  * Services

    * This is Cost by AWS Services.
  * Accounts

    * This is Cost by Linked Account (when organization master account)

## Resources

This construct creating resource list.

* Lambda function execution role
* Lambda function
* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-daily-cost-usage-repoter
# or
yarn add @gammarer/aws-daily-cost-usage-repoter
```

### Python

```shell
pip install gammarer.aws-daily-cost-usage-repoter
```

## Example

```shell
npm install @gammarer/aws-daily-cost-usage-repoter
```

```python
import { CostGroupType, DailyCostUsageReporter } from '@gammarer/aws-daily-cost-usage-repoter';

new DailyCostUsageReporter(stack, 'DailyCostUsageReporter', {
  slackWebhookUrl: 'https://hooks.slack.com/services/xxxxxxxxxx', // already created slack webhook url
  slackPostChannel: 'example-channel', // already created slack channel
  costGroupType: CostGroupType.SERVICES,
});
```

## License

This project is licensed under the Apache-2.0 License.
