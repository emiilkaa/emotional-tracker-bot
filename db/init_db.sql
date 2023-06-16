create sequence if not exists seq_emotions start with 1;
create table if not exists emotions
(
    ID              numeric                        NOT NULL
        constraint PK_EMOTIONS PRIMARY KEY,
    ASSESSMENT_DATE DATE                           NOT NULL,
    USER_EXT_ID     varchar(255)                   NOT NULL,
    EMOJI1          char(1)                        NOT NULL,
    EMOJI2          char(1),
    EMOJI3          char(1),
    DATE_CREATED    TIMESTAMP DEFAULT CURRENT_DATE NOT NULL,
    DATE_UPDATED    TIMESTAMP
);

create sequence if not exists seq_marks start with 1;
create table if not exists marks
(
    ID              numeric                        NOT NULL
        constraint PK_MARKS PRIMARY KEY,
    ASSESSMENT_DATE DATE                           NOT NULL,
    USER_EXT_ID     varchar(255)                   NOT NULL,
    MARK            numeric                        NOT NULL,
    DATE_CREATED    TIMESTAMP DEFAULT CURRENT_DATE NOT NULL,
    DATE_UPDATED    TIMESTAMP
);

create sequence if not exists seq_notes start with 1;
create table if not exists notes
(
    ID              numeric                        NOT NULL
        constraint PK_NOTES PRIMARY KEY,
    ASSESSMENT_DATE DATE                           NOT NULL,
    USER_EXT_ID     varchar(255)                   NOT NULL,
    NOTE            text                           NOT NULL,
    DATE_CREATED    TIMESTAMP DEFAULT CURRENT_DATE NOT NULL
);

create sequence if not exists seq_media start with 1;
create table if not exists media
(
    ID              numeric                        NOT NULL
        constraint PK_MEDIA PRIMARY KEY,
    ASSESSMENT_DATE DATE                           NOT NULL,
    USER_EXT_ID     varchar(255)                   NOT NULL,
    MEDIA_URL       varchar(255)                   NOT NULL,
    DATE_CREATED    TIMESTAMP DEFAULT CURRENT_DATE NOT NULL
);

create sequence if not exists seq_users start with 1;
create table users
(
    ID              numeric                        NOT NULL
        constraint PK_USERS PRIMARY KEY,
    USER_EXT_ID     varchar(255)                   NOT NULL,
    FIRST_NAME      varchar(255)                   NOT NULL,
    SECOND_NAME     varchar(255),
    USERNAME        varchar(255),
    SUBSCRIBED      boolean   DEFAULT false        NOT NULL,
    DATE_REGISTERED TIMESTAMP DEFAULT CURRENT_DATE NOT NULL
);

create index if not exists indx_emotions_user on emotions(user_ext_id);
create index if not exists indx_emotions_user_date on emotions(user_ext_id, assessment_date);

create index if not exists indx_marks_user on marks(user_ext_id);
create index if not exists indx_marks_user_date on marks(user_ext_id, assessment_date);

create index if not exists indx_notes_user on notes(user_ext_id);
create index if not exists indx_notes_user_date on notes(user_ext_id, assessment_date);

create index if not exists indx_media_user on media(user_ext_id);
create index if not exists indx_media_user_date on media(user_ext_id, assessment_date);

create index if not exists indx_users_user on users(user_ext_id);
create index if not exists indx_users_subscribed on users(subscribed);