[![wercker status](https://app.wercker.com/status/f2ccef815185d474937c61042034b83f/m "wercker status")](https://app.wercker.com/project/bykey/f2ccef815185d474937c61042034b83f)


## Exhaust-pipe

Script to make dummy CloudFront log files according the following [format](http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html).

*Caution: could flood your hard disk :P*

### Config

Add a **config.yml** under **exhaust-pipe/resources**

```
---
forever: true
interval:
  minSeconds: 1
  maxSeconds: 5

files:
  storage: local
  location: ./logs/
  
  # To Store the logs on AWS S3
  ...

content:
  startDate: "2016-01-01"
  endDate: "2016-03-31"
  minLines: 5000
  maxLines: 50000
```
