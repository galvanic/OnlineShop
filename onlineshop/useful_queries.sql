
-- each flatmate's basket of purchases
select 
  flatmate.name,
  group_concat(purchase.description)
from purchase
inner join basket_item on purchase.id = basket_item.purchase_id
inner join flatmate    on flatmate.id = basket_item.flatmate_id
where purchase.order_id = ?
group by flatmate.name;

-- which flatmates bought the purchases (incl. non-assigned purchases)
select
  purchase.description,
  group_concat(flatmate.name)
from purchase
left outer join basket_item on purchase.id = basket_item.purchase_id
left outer join flatmate    on flatmate.id = basket_item.flatmate_id
where purchase.order_id = ?
group by purchase.id;

-- how many flatmates each purchase is assigned to (incl. non-assigned purchases)
select
  purchase.description,
  count(distinct basket_item.flatmate_id)
from purchase
left outer join basket_item on purchase.id = basket_item.purchase_id
where purchase.order_id = ?
group by purchase.id;

-- get price of a share of a purchase (depending on how many
-- flatmates ordered the same item)
create temporary table purchase_share as
  select
    purchase.id as id,
    purchase.price / count(distinct basket_item.flatmate_id) as price
  from purchase
  inner join basket_item on purchase.id = basket_item.purchase_id
  where purchase.order_id = ?
  group by purchase.id;
-- now I have the id of purchase + price for each share per person
-- get each flatmate's basket total
select
  flatmate.name,
  round(sum(purchase_share.price), 2)
from purchase_share
inner join basket_item on purchase_share.id = basket_item.purchase_id
inner join flatmate    on flatmate.id = basket_item.flatmate_id
group by flatmate.name;

-- clearer version of above ^
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

-- version also considering percentage of purchase for each flatmate
select
  flatmate.name,
  sum(purchase_count.price / purchase_count.flatmate_count * basket_item) as total_price
from (
  select
    purchase.id,
    purchase.price,
    sum(basket_item.share_count) as flatmate_count
  from purchase
  inner join basket_item on purchase.id = basket_item.purchase_id
  where purchase.order_id = ?
  group by purchase.id, purchase.price
) purchase_count
inner join basket_item on purchase_count.id = basket_item.purchase_id
inner join flatmate on flatmate.id  =  basket_item.flatmate_id
group by flatmate.name;