select
    opportunity_id,
    account_id,
    opportunity_name,
    stage_name,
    amount,
    probability,
    expected_revenue,
    close_date,
    type,
    forecast_category
from {{ ref('stg_opportunity') }}
