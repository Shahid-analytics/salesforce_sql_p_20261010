select opportunity_id
from {{ ref('stg_opportunity') }}
where probability < 1
   or probability > 100
