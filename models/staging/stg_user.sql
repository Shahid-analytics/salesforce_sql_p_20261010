select
    id as user_id,
    first_name,
    name as last_name,
    country,
    country_code,
    is_active
from {{ source('sql_salesforce_source', 'sf_user') }}
