alter table product add column category int;
alter table product add foreign key (category) references category(id) on delete cascade;