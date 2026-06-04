TOP5_MOST_DANGEROUS_WEATHER_CRASH_TYPE_COMBINATIONS = """
SELECT
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE,
    COUNT(*) AS total_crashes
FROM traffic_data_us.Chicago_Traffic_Crashes
GROUP BY
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE
ORDER BY
    total_crashes DESC
LIMIT 5;
"""

TOP10_STREETS_BY_INJURY_CRASH_COUNT = """
SELECT
    STREET_NAME,
    COUNT(*) AS injury_crash_count
FROM traffic_data_us.Chicago_Traffic_Crashes
WHERE INJURIES_TOTAL > 0
GROUP BY STREET_NAME
ORDER BY injury_crash_count DESC
LIMIT 10;
"""

INJURY_PERCENTAGE_BY_CRASH_TYPE = """
SELECT
    FIRST_CRASH_TYPE,
    COUNT(*) AS total_crashes,
    SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS injury_crashes,
    ROUND(
        100.0 * SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS injury_percentage
FROM traffic_data_us.Chicago_Traffic_Crashes
GROUP BY FIRST_CRASH_TYPE
ORDER BY injury_percentage DESC;
"""

PEAK_CRASH_HOUR_BY_MONTH = """
WITH hourly_counts AS (
    SELECT
        CRASH_MONTH,
        CRASH_HOUR,
        COUNT(*) AS crash_count
    FROM traffic_data_us.Chicago_Traffic_Crashes
    GROUP BY
        CRASH_MONTH,
        CRASH_HOUR
),
ranked AS (
    SELECT
        CRASH_MONTH,
        CRASH_HOUR,
        crash_count,
        RANK() OVER (
            PARTITION BY CRASH_MONTH
            ORDER BY crash_count DESC
        ) AS rnk
    FROM hourly_counts
)
SELECT
    CRASH_MONTH,
    CRASH_HOUR AS peak_crash_hour,
    crash_count
FROM ranked
WHERE rnk = 1
ORDER BY CRASH_MONTH;
"""

TOP5_NIGHTTIME_PRIMARY_CONTRIBUTORY_CAUSES = """
SELECT
    PRIM_CONTRIBUTORY_CAUSE,
    COUNT(*) AS crash_count
FROM traffic_data_us.Chicago_Traffic_Crashes
WHERE CRASH_HOUR >= 18
GROUP BY PRIM_CONTRIBUTORY_CAUSE
ORDER BY crash_count DESC
LIMIT 5;
"""





AVERAGE_INJURIES_DAYLIGHT_VS_DARKNESS = """
SELECT
    CASE 
        WHEN LIGHTING_CONDITION = 'DAYLIGHT' THEN 'DAYLIGHT'
        ELSE 'DARKNESS'
    END AS light_group,
    AVG(INJURIES_TOTAL) AS avg_injuries,
    COUNT(*) AS total_crashes
FROM traffic_data_us.Chicago_Traffic_Crashes
WHERE LIGHTING_CONDITION IN ('DAYLIGHT', 'DARKNESS', 'DARKNESS, LIGHTED ROAD')
GROUP BY 1;
"""
MAX_AVERAGE_INJURIES_BY_TRAFFIC_CONTROL_DEVICE = """
SELECT
    TRAFFIC_CONTROL_DEVICE,
    AVG(INJURIES_TOTAL) AS avg_injuries_per_crash
FROM traffic_data_us.Chicago_Traffic_Crashes
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY avg_injuries_per_crash DESC
LIMIT 1;
"""
TOP5_CRASH_FREQUENCY_LOCATIONS_LAT_LONG = """
SELECT
    LATITUDE,
    LONGITUDE,
    COUNT(*) AS crash_count
FROM traffic_data_us.Chicago_Traffic_Crashes
GROUP BY LATITUDE, LONGITUDE
ORDER BY crash_count DESC
LIMIT 5;
"""
TOP5_STREETS_BY_INJURY_RATE_MIN_100_CRASHES = """
SELECT
    STREET_NAME,
    COUNT(*) AS total_crashes,
    SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS injury_crashes,
    ROUND(
        1.0 * SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) / COUNT(*),
        4
    ) AS injury_rate
FROM traffic_data_us.Chicago_Traffic_Crashes
GROUP BY STREET_NAME
HAVING COUNT(*) > 100
ORDER BY injury_rate DESC
LIMIT 5;
"""
MOST_COMMON_CRASH_TYPE_BY_YEAR = """
WITH crash_counts AS (
    SELECT
        YEAR,
        FIRST_CRASH_TYPE,
        COUNT(*) AS crash_count
    FROM traffic_data_us.Chicago_Traffic_Crashes
    GROUP BY YEAR, FIRST_CRASH_TYPE
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY YEAR
            ORDER BY crash_count DESC
        ) AS rn
    FROM crash_counts
)
SELECT
    YEAR,
    FIRST_CRASH_TYPE AS most_common_crash_type,
    crash_count
FROM ranked
WHERE rn = 1
ORDER BY YEAR;
"""







DAY_OF_WEEK_HIGHEST_AVG_CRASHES_PER_HOUR = """
SELECT CRASH_DAY_OF_WEEK, AVG(hourly_crashes) AS avg_crashes_per_hour
FROM (
    SELECT
        CRASH_DAY_OF_WEEK,
        CRASH_HOUR,
        COUNT(*) AS hourly_crashes
    FROM traffic_data_us.Chicago_Traffic_Crashes
    GROUP BY CRASH_DAY_OF_WEEK, CRASH_HOUR
) t
GROUP BY CRASH_DAY_OF_WEEK
ORDER BY avg_crashes_per_hour DESC
LIMIT 1;
"""
HIGH_RISK_TIME_SLOT_BY_INJURY_CRASHES = """
SELECT
    time_bucket,
    COUNT(*) AS injury_crashes
FROM (
    SELECT
        CASE
            WHEN CRASH_HOUR BETWEEN 6 AND 11 THEN 'Morning'
            WHEN CRASH_HOUR BETWEEN 12 AND 17 THEN 'Afternoon'
            WHEN CRASH_HOUR BETWEEN 18 AND 21 THEN 'Evening'
            ELSE 'Night'
        END AS time_bucket
    FROM traffic_data_us.Chicago_Traffic_Crashes
    WHERE INJURIES_TOTAL > 0
) t
GROUP BY time_bucket
ORDER BY injury_crashes DESC;
"""
TOP3_CONTRIBUTORY_CAUSES_BY_CRASH_TYPE = """
WITH cause_counts AS (
    SELECT
        FIRST_CRASH_TYPE,
        PRIM_CONTRIBUTORY_CAUSE,
        COUNT(*) AS crash_count
    FROM traffic_data_us.Chicago_Traffic_Crashes
    GROUP BY FIRST_CRASH_TYPE, PRIM_CONTRIBUTORY_CAUSE
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY FIRST_CRASH_TYPE
            ORDER BY crash_count DESC
        ) AS rn
    FROM cause_counts
)
SELECT
    FIRST_CRASH_TYPE,
    PRIM_CONTRIBUTORY_CAUSE,
    crash_count
FROM ranked
WHERE rn <= 3
ORDER BY FIRST_CRASH_TYPE, crash_count DESC;
"""
YEAR_OVER_YEAR_CRASH_GROWTH_RATE = """
WITH yearly_crashes AS (
    SELECT
        YEAR,
        COUNT(*) AS total_crashes
    FROM traffic_data_us.Chicago_Traffic_Crashes
    GROUP BY YEAR
),
growth AS (
    SELECT
        YEAR,
        total_crashes,
        LAG(total_crashes) OVER (ORDER BY YEAR) AS prev_year_crashes
    FROM yearly_crashes
)
SELECT
    YEAR,
    total_crashes,
    prev_year_crashes,
    ROUND(
        100.0 * (total_crashes - prev_year_crashes) / prev_year_crashes,
        2
    ) AS yoy_growth_pct
FROM growth
WHERE prev_year_crashes IS NOT NULL
ORDER BY YEAR;
"""
CRASH_HOTSPOT_ZONES_BY_LAT_LONG_CLUSTERING = """
SELECT
    ROUND(LATITUDE, 2) AS lat_zone,
    ROUND(LONGITUDE, 2) AS long_zone,
    COUNT(*) AS crash_count
FROM traffic_data_us.Chicago_Traffic_Crashes
WHERE LATITUDE IS NOT NULL
  AND LONGITUDE IS NOT NULL
GROUP BY ROUND(LATITUDE, 2), ROUND(LONGITUDE, 2)
ORDER BY crash_count DESC
LIMIT 10;
"""

QUERY_MAP = {

    "Top 5 Dangerous Weather + Crash Type": TOP5_MOST_DANGEROUS_WEATHER_CRASH_TYPE_COMBINATIONS,

    "Top 10 Injury Streets": TOP10_STREETS_BY_INJURY_CRASH_COUNT,

    "Injury Percentage by Crash Type": INJURY_PERCENTAGE_BY_CRASH_TYPE,

    "Peak Crash Hour by Month": PEAK_CRASH_HOUR_BY_MONTH,

    "Top 5 Nighttime Contributing Causes": TOP5_NIGHTTIME_PRIMARY_CONTRIBUTORY_CAUSES,

    "Avg Injuries: Daylight vs Darkness": AVERAGE_INJURIES_DAYLIGHT_VS_DARKNESS,

    "Max Avg Injuries by Traffic Control Device": MAX_AVERAGE_INJURIES_BY_TRAFFIC_CONTROL_DEVICE,

    "Top 5 Crash Frequency Locations": TOP5_CRASH_FREQUENCY_LOCATIONS_LAT_LONG,

    "Top 5 High Injury Rate Streets (>100 crashes)": TOP5_STREETS_BY_INJURY_RATE_MIN_100_CRASHES,

    "Most Common Crash Type by Year": MOST_COMMON_CRASH_TYPE_BY_YEAR,

    "Day of Week Highest Avg Crashes per Hour": DAY_OF_WEEK_HIGHEST_AVG_CRASHES_PER_HOUR,

    "High Risk Time Slots by Injury Crashes": HIGH_RISK_TIME_SLOT_BY_INJURY_CRASHES,

    "Top 3 Contributing Causes by Crash Type": TOP3_CONTRIBUTORY_CAUSES_BY_CRASH_TYPE,

    "Year over Year Crash Growth Rate": YEAR_OVER_YEAR_CRASH_GROWTH_RATE,

    "Crash Hotspot Zones (Lat/Long Clusters)": CRASH_HOTSPOT_ZONES_BY_LAT_LONG_CLUSTERING
}