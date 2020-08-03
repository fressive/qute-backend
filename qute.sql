create table artist
(
    artist_id    int auto_increment
        primary key,
    avatar_url   mediumtext    null,
    name         mediumtext    null,
    social_links longtext      null,
    description  text          null,
    favorites    int default 0 null,
    constraint artist_pk
        unique (name) using hash,
    constraint social_links
        check (json_valid(`social_links`))
)
    charset = utf8mb4;

create table image
(
    image_id    int auto_increment
        primary key,
    image_url   mediumtext null,
    artist_id   int        null,
    favorites   int        null,
    source_url  mediumtext null,
    tags        text       null,
    title       text       null,
    description text       null,
    width       int        null,
    height      int        null,
    r18         tinyint(1) null,
    source_id   tinyint(2) null,
    constraint image_artist_artist_id_fk
        foreign key (artist_id) references artist (artist_id)
)
    charset = utf8mb4;

create index image_source_id_index
    on image (source_id);

