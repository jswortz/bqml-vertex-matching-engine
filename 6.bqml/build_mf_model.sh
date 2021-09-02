#!/bin/bash

source ../0.setup/env_vars.sh

# Buy Flex slots
bq mk --project_id="${RECAI_PROJECT}" \
  --location=US --capacity_commitment \
  --plan=FLEX --slots=100
# Create reservation
bq mk --project_id="${RECAI_PROJECT}" \
  --location=US --reservation --slots=100 prod
# Assign project to reservation
bq mk --project_id="${RECAI_PROJECT}" \
  --location=US --reservation_assignment \
  --reservation_id="${RECAI_PROJECT}":US.prod \
  --job_type=QUERY --assignee_id="${RECAI_PROJECT}" \
  --assignee_type=PROJECT


# Prepare data and build model
model_data_view="create or replace view \`${RECAI_PROJECT}.css_retail.mf_dataset\` as
with purchases as (
select
  eventType
  , eventTime
  , userInfo.visitorId
  , 1 as trxId
  , productEventDetail.purchaseTransaction.revenue
  , products.id as productId
  , products.quantity
from \`${RECAI_PROJECT}.css_retail.purchase_complete\` as purchase
cross join unnest(purchase.productEventDetail.productDetails) as products
), page_views as (
select
  eventType
  , eventTime
  , userInfo.visitorId
  , 1 as viewCount
  , products.id as productId
from \`${RECAI_PROJECT}.css_retail.detail_page_view\` as views
cross join unnest(views.productEventDetail.productDetails) as products
) select visitorId, productId, (sum(trxId) * 2) as ratings from purchases group by visitorId, productId
union all
select visitorId, productId, sum(viewCount) as ratings from page_views group by visitorId, productId;"
bq query --use_legacy_sql=false "${model_data_view}"

model_query="create or replace model \`${RECAI_PROJECT}.css_retail.${BQML_NAME}\`
options(
    model_type='matrix_factorization'
    , num_factors=15
    , user_col='visitorId'
    , item_col='productId'
    , rating_col='ratings'
    , feedback_type='implicit'
)
as
select
  *
from \`${RECAI_PROJECT}.css_retail.mf_dataset\`
;"
bq query --use_legacy_sql=false "${model_query}"

# Cleanup Reservation, commit and Flex slots
ASSIGNMENT_ID=$(bq show --project_id="${RECAI_PROJECT}" --location=US --reservation_assignment --job_type=QUERY --assignee_id="${RECAI_PROJECT}" --assignee_type=PROJECT | grep ${RECAI_PROJECT} | sed 's/^  \+//g' | cut -d" " -f1)
bq rm --project_id="${RECAI_PROJECT}" \
  --location=US --reservation_assignment "${ASSIGNMENT_ID}"
bq rm --project_id="${RECAI_PROJECT}" \
  --location=US --reservation prod
COMMIT_ID=$(bq ls --capacity_commitment --location=US --project_id="${RECAI_PROJECT}" | grep "${RECAI_PROJECT}" | sed 's/^  \+//g' | cut -d" " -f1)
bq rm --project_id="${RECAI_PROJECT}" \
  --location=US --capacity_commitment "${COMMIT_ID}"