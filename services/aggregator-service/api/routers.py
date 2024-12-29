from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException, FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from api import schemas
from api.database import get_db_engine, get_redshift_engine


def fetch_data_from_rds(engine, query):
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.fetchall()
        column_names = result.keys()
        return column_names, rows


def load_data_to_redshift(engine, columns, rows, table_name):
    # Extract column names and convert to a SQL-friendly format
    columns = ", ".join(columns)
    
    # Convert DataFrame rows to a list of SQL-friendly tuples
    values = ", ".join(
        [
            f"({', '.join([repr(value) for value in row])})"
            for row in rows
        ]
    )
    
    insert_query = f"""
    INSERT INTO {table_name} ({columns})
    VALUES {values};
    """

    with engine.connect() as connection:
        connection.execute(insert_query)


# Lifespan management for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(aggregate_data, CronTrigger(minute="0", hour="*"))
    scheduler.start()
    
    print("Scheduler started.")
    
    try:
        yield
    finally:
        scheduler.shutdown()
        print("Scheduler stopped.")


app = APIRouter(lifespan=lifespan)


@app.get("/aggregate")
async def aggregate_data():
    try:
        redshift_client = get_redshift_engine()
        rds_client = get_db_engine()

        # Aggregate metrics
        dim_query = """
                        SELECT d.id as doctor_id, d.name as doctor_name, d.specialty as speciality, a.common_symptoms
                        FROM public.doctors as d
                        LEFT join 
                        ( select doctor_id, 
                        string_agg(reason, ', ' ORDER BY reason) as common_symptoms
                        from public.appointments a group by doctor_id) as a 
                        on a.doctor_id = d.id;
                    """
        rds_dim_columns, rods_dim_rows = fetch_data_from_rds(rds_client, dim_query)
        print(rds_dim_columns)
        print(rods_dim_rows)
        load_data_to_redshift(redshift_client, rds_dim_columns, rods_dim_rows, 'public.dim_doctor_symptoms')

        fact_query = """
                        SELECT d.id as doctor_id, a.no_of_appointments_cumulative, a.appointment_frequency
                        FROM public.doctors as d
                        LEFT join 
                        ( select doctor_id, 
                        count(id) as no_of_appointments_cumulative,
                        'daily' as appointment_frequency
                        from public.appointments ad group by doctor_id, extract('day' from appointment_time)
                        union all
                        select doctor_id, 
                        count(id) as no_of_appointments_cumulative,
                        'weekly' as appointment_frequency
                        from public.appointments aw group by doctor_id, extract('week' from appointment_time)
                        ) as a 
                        on a.doctor_id = d.id;
                    """
        rds_fact_columns, rds_fact_rows = fetch_data_from_rds(rds_client, fact_query)
        print(rds_fact_columns)
        print(rds_fact_rows)
        load_data_to_redshift(redshift_client, rds_fact_columns, rds_fact_rows, 'public.fact_appointments')


        print(f"[{datetime.now()}] Data aggregation completed successfully.")
        return {"status": status.HTTP_200_OK, "message": "Data aggregated"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to aggregate: {str(e)}"
        }

    
@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}