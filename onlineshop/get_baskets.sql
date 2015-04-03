-- get each flatmate's basket total
select
  flatmate.name as f_name,
  round(sum(purchase_share.price), 2) as f_total
from (
  -- get price of a share of a purchase (depending on how many
  -- flatmates ordered the same item)
  select
    purchase.id as id,
    purchase.price / count(distinct flatmate_purchase.flatmate_id) as price
  from purchase
  inner join flatmate_purchase on purchase.id = flatmate_purchase.purchase_id
  where purchase.delivery_id = ?
  group by purchase.id
) purchase_share
inner join flatmate_purchase on purchase_share.id = flatmate_purchase.purchase_id
inner join flatmate    on flatmate.id = flatmate_purchase.flatmate_id
group by flatmate.name;