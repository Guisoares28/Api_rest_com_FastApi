CREATE TABLE IF NOT EXISTS receitas(
    id integer primary key autoincrement,
    descricao varchar(200) not null,
    valor real not null,
    data date not null
);

CREATE TABLE IF NOT EXISTS despesas(
    id integer primary key autoincrement,
    descricao varchar(200) not null,
    valor real not null,
    data date not null
);


