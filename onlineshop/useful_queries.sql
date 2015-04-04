
-- each flatmate's basket of purchases
select 
  flatmate.name,
  group_concat(purchase.description)
from purchase
inner join assignment on purchase.id = assignment.purchase_id
inner join flatmate   on flatmate.id = assignment.flatmate_id
where purchase.delivery_id = ?
group by flatmate.name;

-- which flatmates bought the purchases (incl. non-assigned purchases)
select
  purchase.description,
  group_concat(flatmate.name)
from purchase
left outer join assignment on purchase.id = assignment.purchase_id
left outer join flatmate   on flatmate.id = assignment.flatmate_id
where purchase.delivery_id = ?
group by purchase.id;

-- how many flatmates each purchase is assigned to (incl. non-assigned purchases)
select
  purchase.description,
  count(distinct assignment.flatmate_id)
from purchase
left outer join assignment on purchase.id = assignment.purchase_id
where purchase.delivery_id = ?
group by purchase.id;

-- get price of a share of a purchase (depending on how many
-- flatmates ordered the same item)
create temporary table purchase_share as
  select
    purchase.id as id,
    purchase.price / count(distinct assignment.flatmate_id) as price
  from purchase
  inner join assignment on purchase.id = assignment.purchase_id
  where purchase.delivery_id = ?
  group by purchase.id;
-- now I have the id of purchase + price for each share per person
-- get each flatmate's basket total
select
  flatmate.name,
  round(sum(purchase_share.price), 2)
from purchase_share
inner join assignment on purchase_share.id = assignment.purchase_id
inner join flatmate   on flatmate.id = assignment.flatmate_id
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
    purchase.price / count(distinct assignment.flatmate_id) as price
  from purchase
  inner join assignment on purchase.id = assignment.purchase_id
  where purchase.delivery_id = ?
  group by purchase.id
) purchase_share
inner join assignment on purchase_share.id = assignment.purchase_id
inner join flatmate   on flatmate.id = assignment.flatmate_id
group by flatmate.name;

-- version also considering percentage of purchase for each flatmate
select
  flatmate.name,
  sum(purchase_count.price / purchase_count.flatmate_count * assignment) as total_price
from (
  select
    purchase.id,
    purchase.price,
    sum(assignment.share_count) as flatmate_count
  from purchase
  inner join assignment on purchase.id = assignment.purchase_id
  where purchase.delivery_id = ?
  group by purchase.id, purchase.price
) purchase_count
inner join assignment on purchase_count.id = assignment.purchase_id
inner join flatmate   on flatmate.id = assignment.flatmate_id
group by flatmate.name;