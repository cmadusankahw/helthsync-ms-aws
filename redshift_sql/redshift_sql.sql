CREATE DATABASE healthsync_data;

CREATE TABLE healthsync_data.public.dim_doctor_symptoms (
    doctor_id INT NOT NULL,           -- Doctor identifier
    doctor_name VARCHAR(255) NOT NULL, -- Doctor's name
    speciality VARCHAR(255) NOT NULL, -- Doctor's speciality
    common_symptoms VARCHAR(500)      -- Most common symptoms treated by the doctor
);

CREATE TABLE healthsync_data.public.fact_appointments (
    doctor_id INT NOT NULL,                   -- Doctor identifier
    no_of_appointments_cumulative INT,       -- Cumulative number of appointments for the doctor
    appointment_frequency VARCHAR(50)        -- Frequency of appointments (e.g., "daily", "weekly")
);