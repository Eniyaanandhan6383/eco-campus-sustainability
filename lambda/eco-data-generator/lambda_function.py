import json
import boto3
import random
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'eco-score-raw-eniya-2026'
BUILDINGS = ['Block-A', 'Block-B', 'Block-C', 'Block-D', 'Block-E']

def generate_sensor_data(building):
    return {
        "building": building,
        "timestamp": datetime.utcnow().isoformat(),
        "energy_kwh": round(random.uniform(100, 500), 2),
        "water_liters": round(random.uniform(500, 2000), 2),
        "waste_kg": round(random.uniform(20, 100), 2),
        "temperature": round(random.uniform(20, 35), 1)
    }

def lambda_handler(event, context):
    for building in BUILDINGS:
        data = generate_sensor_data(building)
        key = f"raw/{building}/{datetime.utcnow().strftime('%Y/%m/%d/%H%M%S')}.json"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(data)
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Data generated successfully!')
    }
