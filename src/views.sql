CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    AVG(temperature) AS media_temperatura
FROM temperature_readings
GROUP BY device_id;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    DATE_TRUNC('hour', timestamp) AS hora,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(timestamp) AS dia,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY DATE(timestamp)
ORDER BY dia;
