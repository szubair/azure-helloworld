#!/usr/bin/python -u
import boto3
import sys
sys.stdout.flush()

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')
data = []

v1_res = cloudwatch.get_metric_statistics( Namespace='AWS/Lambda', MetricName='Invocations',
    Dimensions=[{'Name': 'FunctionName','Value': 'PIS_Lambda_Demo'},
    {'Name': 'Resource','Value': 'PIS_Lambda_Demo:PIS_Alias'},
    {'Name': 'ExecutedVersion','Value': '1'},
    ],
    StartTime='2019-02-14T01:00:00',
    EndTime='2019-02-14T03:00:00',
    Period=300,
    Statistics=['Sum'],
    Unit='Count')

v2_res = cloudwatch.get_metric_statistics( Namespace='AWS/Lambda', MetricName='Invocations',
    Dimensions=[{'Name': 'FunctionName','Value': 'PIS_Lambda_Demo'},
    {'Name': 'Resource','Value': 'PIS_Lambda_Demo:PIS_Alias'},
    {'Name': 'ExecutedVersion','Value': '2'},
    ],
    StartTime='2019-02-14T01:00:00',
    EndTime='2019-02-14T03:00:00',
    Period=300,
    Statistics=['Sum'],
    Unit='Count')

i = 0
v1_length = len(v1_res['Datapoints'])
v2_length = len(v2_res['Datapoints'])
#print "No. of timestamp on v1 ",v1_length
#print "No. of timestamp on v2 ",v2_length

if v1_length == v2_length:
   while i < v1_length:
      mylist = []
      mylist.append(str(v1_res['Datapoints'][i]['Timestamp']))
      mylist.append(v1_res['Datapoints'][i]['Sum'])
      mylist.append(v2_res['Datapoints'][i]['Sum'])
      data.append(mylist)
      i = i + 1
else:
   print "# of timestamps are not matching, quit!"
   exit(1)

sorted_data = sorted(data)
print ('Timestamp                |sum v1|sum v2')
for item in sorted_data:
    print ('{} {:>5} {:>5}'.format(*item))

