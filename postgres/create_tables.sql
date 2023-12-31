create table if not exists telegram_users(
    id int primary key,
    first_name text not null,
    username text,
    last_name text,
    language_code text,
    is_premium bool,
    is_admin bool
);
create table if not exists coworking(
    id serial primary key,
    status text not null,
    responsible_id integer not null references telegram_users(id),
    duration integer default null,
    created_at timestamp not null default NOW()
);