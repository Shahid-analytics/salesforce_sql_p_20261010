select
    id as account_id,
    name as account_name,
    type as account_type,
    billing_country,
    industry,
    annual_revenue,
    number_of_employees,
    ownership
from {{ source('sql_salesforce_source', 'account') }}
