drop table if exists todo;
create table todo (
	id integer primary key autoincrement,
	description text not null,
	done boolean,
	created_ts text,
	finished_ts text,
	due_date text
);