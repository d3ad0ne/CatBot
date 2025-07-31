create table Users(
    Id serial primary key,
    username character varying(32),
    ChatId bigint not null,
    constraint chat_id_unique unique(ChatId)
);