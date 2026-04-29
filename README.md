🌱 Eco-Campus Sustainability System

An AWS-based serverless system to monitor and calculate eco-scores for university campus buildings.

🏗️ Architecture
eco-data-generator (Lambda)
↓
S3 (raw data)
↓
eco-score-calculator (Lambda) → CloudWatch Dashboard
↓                     → SNS Email Alerts
S3 (scores)
↓
Athena (SQL queries)
↓
eco-genai-assistant (Lambda)

🚀 AWS Services Used

- **AWS Lambda** - 3 serverless functions
- **Amazon S3** - Raw sensor data + eco-scores storage
- **Amazon Athena** - SQL queries on S3 data
- **Amazon CloudWatch** - Real-time dashboard
- **Amazon SNS** - Email alerts for low eco-scores
- **IAM** - Zero-trust least-privilege security

  Campus Buildings

| Building | Description |
|---|---|
| Block-A | Academic Block A |
| Block-B | Academic Block B |
| Block-C | Academic Block C |
| Block-D | Academic Block D |
| Block-E | Academic Block E |

📊 Eco-Score Calculation

| Metric | Weight | Good | Bad |
|---|---|---|---|
| Energy (kWh) | 40% | ≤200 | ≥400 |
| Water (liters) | 30% | ≤800 | ≥1600 |
| Waste (kg) | 20% | ≤40 | ≥80 |
| Temperature (°C) | 10% | ≤24 | ≥30 |

🔒 Security

- S3 public access blocked
- Least-privilege IAM policy
- Zero-trust architecture

👩‍💻 Developer
--> Eniya
