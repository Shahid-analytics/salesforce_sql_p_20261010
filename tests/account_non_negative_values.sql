select account_id
from {{ ref('stg_account') }}
where annual_revenue < 0
