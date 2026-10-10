select
    user_id,
    first_name,
    last_name,
    country,
    country_code,
    is_active
from {{ ref('stg_user') }}
