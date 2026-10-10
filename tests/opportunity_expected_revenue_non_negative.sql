select opportunity_id
from {{ ref('stg_opportunity') }}
where expected_revenue < 0
