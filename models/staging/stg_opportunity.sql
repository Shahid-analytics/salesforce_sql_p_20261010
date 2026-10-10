select
    id as opportunity_id,
    account_id,
    name as opportunity_name,
    stage_name,
    amount,
    probability,
    expected_revenue,
    close_date,
    type
from {{ source('sql_salesforce_source', 'opportunity') }}
