-- creating database for project
create database project;

-- toggling safe mode of mysql
set sql_safe_updates = 0;

-- reviewing current table
use project;
select * from residex order by 1, 2;

-- assigning proper names to columns
delete from residex where MyUnknownColumn = 'City';
alter table residex rename column MyUnknownColumn to city;
alter table residex rename column `MyUnknownColumn_[0]` to quarter;
alter table residex rename column `Carpet Area Prices(Rs.Per Sq.Ft.)` to composite;
alter table residex rename column `MyUnknownColumn_[1]` to onebhk;
alter table residex rename column `MyUnknownColumn_[2]` to twobhk;
alter table residex rename column `MyUnknownColumn_[3]` to threebhk;

-- cleaning data & changing data type where needed
update residex
set quarter = str_to_date(concat(substring(quarter, 5, 4), substring(quarter, 1, 3), '01'), "%Y%b%d");
update residex 
set composite = replace(composite, ',', '');
update residex
set onebhk = replace(onebhk, ',', '');
update residex
set twobhk = replace(twobhk, ',', '');
update residex
set threebhk = replace(threebhk, ',', '');

-- handling exceptions where city column contains extra information enclosed in brackets
update residex 
set city = case 
			when locate(' (', city) = 0 then
				city
			else
				substring(city, 1, locate(' (', city))
			end;

-- calculating QoQ change for each city and appartment size
select 
	*,
    lag(onebhk) over(partition by city order by quarter) `change_onebhk`,
    lag(twobhk) over(partition by city order by quarter) `change_twobhk`,
    lag(threebhk) over(partition by city order by quarter) `change_threebhk`
from residex
order by city, quarter;

select 
	*,
    round(((onebhk - lag(onebhk) over(partition by city order by quarter)) / lag(onebhk) over(partition by city order by quarter)) * 100, 3) `%change_onebhk`,
	round(((twobhk - lag(twobhk) over(partition by city order by quarter)) / lag(twobhk) over(partition by city order by quarter)) * 100, 3) `%change_twobhk`,
    round(((threebhk - lag(threebhk) over(partition by city order by quarter)) / lag(threebhk) over(partition by city order by quarter)) * 100, 3) `%change_threebhk`
from residex
order by city, quarter;

-- calculating YoY change for each city and appartment size
select 
	*,
    lag(onebhk, 4) over(partition by city order by quarter) `change_onebhk`,
    lag(twobhk, 4) over(partition by city order by quarter) `change_twobhk`,
    lag(threebhk, 4) over(partition by city order by quarter) `change_threebhk`
from residex
order by city, quarter;

select 
	city, onebhk,
    round(((onebhk - lag(onebhk, 4) over(partition by city order by quarter)) / lag(onebhk) over(partition by city order by quarter)) * 100, 3) `%change_onebhk`,
	round(((twobhk - lag(twobhk, 4) over(partition by city order by quarter)) / lag(twobhk) over(partition by city order by quarter)) * 100, 3) `%change_twobhk`,
    round(((threebhk - lag(threebhk, 4) over(partition by city order by quarter)) / lag(threebhk) over(partition by city order by quarter)) * 100, 3) `%change_threebhk`
from residex
order by city, quarter;