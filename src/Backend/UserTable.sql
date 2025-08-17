-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    chat_id bigint NOT NULL,
    images_amount bigint,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT chat_id_unique UNIQUE (chat_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres_user;