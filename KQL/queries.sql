CREATE TABLE table_name ( col1 int , col2 varchar , col3 int )

INSERT INTO table_name ( col1 , col2 , col3 ) VALUES ( 1 , 2 , 3 , 1 , 2 , 3 )

SELECT * FROM table_name
SELECT col1 , col2 FROM table_name

select col1 avg(col2) from table_name
select sum(col1) avg(col2) count(col3) from table_name
SELECT * FROM table_name WHERE col1 = 1



INSERT INTO table_name ( col2 , col3 ) VALUES ( 3 , 1 , 2 , 3 )
UPDATE table_name SET col1 = 1 col2 = 2 WHERE col3 = 3
DELETE FROM table_name WHERE col3 = 1 

ALTER TABLE table_name ADD col4 varchar
ALTER TABLE table_name MODIFY col2 int
ALTER TABLE table_name RENAME COLUMN col1 TO colone
ALTER TABLE table_name RENAME TO new_table_name
DROP TABLE table_name
TRUNCATE TABLE table_name