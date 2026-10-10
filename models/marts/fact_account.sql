select
    account_id,
    account_name,
    account_type,
    billing_country,
    industry,
    annual_revenue,
    number_of_employees,
    ownership
from {{ ref('stg_account') }}
