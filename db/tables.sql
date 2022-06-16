create table subject (
	code 		varchar(16) 	primary key,
	name 		varchar(128) 	not null,
	branch 		varchar(128) 	not null,
	scheme 		varchar(16) 	not null,
	semester 	int 			not null
);

create table file (
	id 			serial 			primary key,
	subject		varchar(16)		not null,
	module		int				not null,
	url			varchar(255)	not null
);
