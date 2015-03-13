-- get each flatmate's basket total
select
  flatmate.name,
  round(sum(purchase_share.price), 2)
from (
  -- get price of a share of a purchase (depending on how many
  -- flatmates ordered the same item)
  select
    purchase.id as id,
    purchase.price / count(distinct basket_item.flatmate_id) as price
  from purchase
  inner join basket_item on purchase.id = basket_item.purchase_id
  where purchase.order_id = ?
  group by purchase.id
) purchase_share
inner join basket_item on purchase_share.id = basket_item.purchase_id
inner join flatmate    on flatmate.id = basket_item.flatmate_id
group by flatmate.name;