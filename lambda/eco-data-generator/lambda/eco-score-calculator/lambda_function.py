import json
import boto3
import datetime

s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

BUCKET_NAME = 'eco-score-raw-eniya-2026'
BUILDINGS = ['Block-A', 'Block-B', 'Block-C', 'Block-D', 'Block-E']
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:103493890058:eco-score-alerts'
ALERT_THRESHOLD = 30

def calculate_score(value, good, bad):
    if value <= good:
        return 100.0
    elif value >= bad:
        return 0.0
    else:
        return round(100 * (bad - value) / (bad - good), 2)

def get_latest_data(building):
    prefix = f"raw/{building}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    if 'Contents' not in response:
        return None
    latest = max(response['Contents'], key=lambda x: x['LastModified'])
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest['Key'])
    return json.loads(obj['Body'].read())

def lambda_handler(event, context):
    results = []
    alerts = []
    timestamp = datetime.datetime.utcnow().isoformat()

    for building in BUILDINGS:
        data = get_latest_data(building)
        if not data:
            continue

        energy_score = calculate_score(data['energy_kwh'], 200, 400)
        water_score  = calculate_score(data['water_liters'], 800, 1600)
        waste_score  = calculate_score(data['waste_kg'], 40, 80)
        temp_score   = calculate_score(data['temperature'], 24, 30)

        eco_score = round(
            0.4 * energy_score +
            0.3 * water_score +
            0.2 * waste_score +
            0.1 * temp_score, 2
        )

        result = {
            "building": building,
            "timestamp": timestamp,
            "eco_score": eco_score,
            "breakdown": {
                "energy_score": energy_score,
                "water_score": water_score,
                "waste_score": waste_score,
                "temp_score": temp_score
            }
        }
        results.append(result)

        key = f"scores/{building}/{datetime.datetime.utcnow().strftime('%Y/%m/%d/%H%M%S')}.json"
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(result))

        cloudwatch.put_metric_data(
            Namespace='EcoScoring',
            MetricData=[{
                'MetricName': 'EcoScore',
                'Dimensions': [{'Name': 'Building', 'Value': building}],
                'Value': eco_score,
                'Unit': 'None'
            }]
        )

        if eco_score < ALERT_THRESHOLD:
            alerts.append(building)
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'⚠️ Low Eco-Score Alert: {building}',
                Message=f"""Campus Sustainability Alert!
Building: {building}
Eco-Score: {eco_score}/100
Timestamp: {timestamp}"""
            )

    return {
        'statusCode': 200,
        'body': json.dumps({'results': results, 'alerts_sent': alerts})
    }
