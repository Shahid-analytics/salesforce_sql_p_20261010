select opportunity_id
from {{ ref('stg_opportunity') }}
where amount < 0
