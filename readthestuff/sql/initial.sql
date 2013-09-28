-- Initail database schema

CREATE SEQUENCE subscription_id_seq;
CREATE TABLE IF NOT EXISTS subcsriptions (
    id integer PRIMARY KEY DEFAULT nextval('subscription_id_seq'),
    href varchar(255) NOT NULL UNIQUE,

    updated_at timestamp with time zone,
    received_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS user_subscriptions (
    user_id integer NOT NULL,
    subscription_id integer NOT NULL,

    title varchar(64) NOT NULL,
    link varchar(255) NOT NULL DEFAULT '',
    summary text NOT NULL DEFAULT '',

    unread_counter integer NOT NULL DEFAULT 0,

    CONSTRAINT unique_ids_pair UNIQUE (user_id, subscription_id),
    CONSTRAINT unsigned_unread_counter CHECK (unread_counter > 0)
);
