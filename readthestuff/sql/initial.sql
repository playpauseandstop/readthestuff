-- Initail database schema

CREATE SEQUENCE subscription_id_seq;
CREATE TABLE IF NOT EXISTS subscriptions (
    id integer PRIMARY KEY DEFAULT nextval('subscription_id_seq'),
    href varchar(255) NOT NULL UNIQUE,

    updated_at timestamp with time zone,
    received_at timestamp with time zone
);

CREATE SEQUENCE tag_id_seq;
CREATE TABLE IF NOT EXISTS tags (
    id integer PRIMARY KEY DEFAULT nextval('tag_id_seq'),
    name varchar(255) NOT NULL UNIQUE
);

CREATE SEQUENCE user_subscription_id_seq;
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id integer PRIMARY KEY DEFAULT nextval('user_subscription_id_seq'),

    user_id integer NOT NULL,
    subscription_id integer NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,

    title varchar(64) NOT NULL,
    link varchar(255) NOT NULL DEFAULT '',
    summary text NOT NULL DEFAULT '',

    unread_counter integer NOT NULL DEFAULT 0,

    CONSTRAINT unique_ids_us UNIQUE (user_id, subscription_id),
    CONSTRAINT unsigned_unread_counter_us CHECK (unread_counter >= 0)
);

CREATE TABLE IF NOT EXISTS user_tag_subscriptions (
    user_id integer NOT NULL,
    tag_id integer NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    user_subscription_id integer NOT NULL REFERENCES user_subscriptions(id) ON DELETE CASCADE,

    unread_counter integer NOT NULL DEFAULT 0,

    CONSTRAINT unique_ids_uts UNIQUE (user_id, tag_id, user_subscription_id),
    CONSTRAINT unsigned_unread_counter_uts CHECK (unread_counter >= 0)
);
