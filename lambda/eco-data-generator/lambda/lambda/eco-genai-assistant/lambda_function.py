import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'eco-score-raw-eniya-2026'
BUILDINGS = ['Block-A', 'Block-B', 'Block-C', 'Block-D', 'Block-E']

def get_latest_scores():
    scores = []
    for building in BUILDINGS:
        prefix = f"scores/{building}/"
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if 'Contents' not in response:
            continue
        latest = max(response['Contents'], key=lambda x: x['LastModified'])
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest['Key'])
        scores.append(json.loads(obj['Body'].read()))
    return scores

def generate_answer(question, scores):
    sorted_scores = sorted(scores, key=lambda x: x['eco_score'])
    worst = sorted_scores[0]
    best = sorted_scores[-1]

    answer = f"""Based on current campus data:

🏆 Best performing: {best['building']} (score: {best['eco_score']})
⚠️ Needs improvement: {worst['building']} (score: {worst['eco_score']})

Recommendations for {worst['building']}:
- Energy: Reduce consumption by switching to LED lighting
- Water: Fix leaks and install low-flow fixtures
- Waste: Implement recycling and composting programs
- Temperature: Optimize HVAC scheduling"""
    return answer

def lambda_handler(event, context):
    question = event.get('question', 'Which building has the best eco-score?')
    scores = get_latest_scores()
    answer = generate_answer(question, scores)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'question': question,
            'answer': answer
        })
    }
