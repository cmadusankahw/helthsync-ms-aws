from fastapi import APIRouter, Depends, status, HTTPException
from aioredis import Redis
from sqlalchemy.orm import Session
import boto3
from api import schemas
from api.database import get_db
from api.utils import generate_aggregate_report

app = APIRouter()
redis = Redis(host='redis-endpoint', port=6379)

redshift_client = boto3.client('redshift', region_name='your-region')

@app.get("/aggregate")
async def aggregate_data():
    try:
        # Fetch data from Redis (cached patient and appointment data)
        patients = await redis.get('patients')
        appointments = await redis.get('appointments')

        # Aggregate metrics (simplified example)
        total_appointments = len(appointments)

        # Send aggregated metrics to Redshift
        redshift_client.execute_statement(
            ClusterIdentifier='your-cluster-id',
            Database='your-db',
            Sql="INSERT INTO metrics (metric_name, value) VALUES ('total_appointments', %s)",
            Parameters=[{'name': 'value', 'value': total_appointments}]
        )
        return {"status": status.HTTP_200_OK, "message": "Data aggregated"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to aggregate: {str(e)}"
        }


@app.get("/aggregator/report", response_model=schemas.AggregateReport)
async def get_aggregate_report(db: Session = Depends(get_db)):
    try:
        report = generate_aggregate_report(db)
        return {"status": status.HTTP_200_OK, "message": report}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to generate aggregation report: {str(e)}"
        }
    
@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}