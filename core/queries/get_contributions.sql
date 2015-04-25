-- get each flatmate's basket total
select
  flatmate.name as f_name,
  sum(purchase_share.price) as f_total
from (
  -- get price of a share of a purchase (depending on how many
  -- flatmates ordered the same item)
  select
    purchase.id as id,
    purchase.price / count(distinct assignment.flatmate_id) as price
  from purchase
  inner join assignment on purchase.id = assignment.purchase_id
  where purchase.delivery_id = ?
  group by purchase.id
) purchase_share
inner join assignment on purchase_share.id = assignment.purchase_id
inner join flatmate   on flatmate.id = assignment.flatmate_id
group by flatmate.name;