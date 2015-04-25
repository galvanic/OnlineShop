
pragma foreign_keys = on

create table flatmate (
    id          integer primary key,
    name        char(30) not null unique
)

create table delivery (
    id          integer primary key,
    date        text not null unique,
    total       real not null
)

create table purchase (
    id          integer primary key,
    description char(100),
    price       real not null,
    quantity    integer default 1,
    order_id    integer not null,
    foreign key(delivery_id) references delivery(id)
)

create table assignment (
    id          integer primary key,
    purchase_id integer not null,
    flatmate_id integer not null,
    foreign key(purchase_id) references purchase(id),
    foreign key(flatmate_id) references flatmate(id)
)