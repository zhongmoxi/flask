drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  author string not null,
  time string not null,
  title string not null,
  text string not null
);
