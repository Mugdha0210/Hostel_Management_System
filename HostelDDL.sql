CREATE TABLE IF NOT EXISTS Student_Info 
	(MIS		varchar(9),
	 first_name		varchar(20) not null,
     middle_name		varchar(20),
     last_name		varchar(20),
	 student_address		varchar(100) not null,
     gender     varchar(10) not null
        check (gender in ('female', 'male')), 
      isNRI      BOOLEAN not null,
     contact_no     varchar(10) not null,
	 primary key (MIS),
     foreign key (MIS) references Login(MIS) on delete cascade
	);

CREATE TABLE IF NOT EXISTS Student_academic_record
	(MIS		varchar(9),
     year		varchar(50)
        check (year in ('First Year B.Tech', 'Second Year B.Tech', 'Third Year B.Tech', 'Final Year B.Tech')),
	 branch		varchar(50)
        check (branch in ('Computer', 'Electronics and Telecommunication', 'Electrical', 'Instrumentation', 'Mechanical', 'Production', 'Civil', 'Metallutgy', 'Planning')), 
	 CGPA       numeric(5,2) check (CGPA >= 0.00 and CGPA <= 10.00),
	 primary key (MIS),
     foreign key (MIS) references Student_Info(MIS) on delete cascade
	);

CREATE TABLE IF NOT EXISTS Student_CET
	(MIS		varchar(9), 
	 CET_rank   numeric(10,0) check (CET_rank > 0),
	 primary key (MIS),
	 foreign key (MIS) references Student_Info(MIS) on delete cascade
	);

CREATE TABLE IF NOT EXISTS Student_board_percentage
	(MIS		varchar(9), 
	 board_percentage   numeric(6,2) check (board_percentage > 0),
	 primary key (MIS),
	 foreign key (MIS) references Student_Info(MIS) on delete cascade
	);

CREATE TABLE IF NOT EXISTS Mess_name
    (mess_name      varchar(10)
        check (mess_name in ('Saee', 'Aswaad', 'Cosmo', 'Fusion', 'FX Cosmo')),
     primary key (mess_name)
    );

CREATE TABLE IF NOT EXISTS Hostel_blocks
	(block_code		varchar(3)
        check (block_code in ('A', 'B', 'GHB', 'C', 'D', 'E', 'F', 'G', 'H', 'I')),
     block_name     varchar(10),   
     mess_name      varchar(10),
     num_floors     numeric(2, 0)
        check (num_floors > 0 and num_floors < 12),
     num_rooms      numeric(3, 0),
	 primary key (block_code), 
     foreign key (mess_name) references Mess_name(mess_name) on delete set null    
	);


CREATE TABLE IF NOT EXISTS stays_in
	(MIS		varchar(9),
	 block_code		varchar(3),
	 room_number	numeric(3), 
	 primary key (MIS),
	 foreign key (MIS) references Student_Info(MIS) on delete cascade,
	 foreign key (block_code) references Hostel_blocks(block_code) on delete cascade
	);

CREATE TABLE IF NOT EXISTS Staff_payments
    (job        varchar(20)
      check (job in ('Rector', 'Warden', 'Assistant', 'Mess', 'Watchwoman', 'Watchman')), 
     salary			numeric(8,2) check (salary >= 0),
     isOutsourced   BOOLEAN not null,
     primary key(job)
    );

CREATE TABLE IF NOT EXISTS Staff
	(ID			varchar(9), 
	 first_name		varchar(20) not null,
     middle_name		varchar(20),
     last_name		varchar(20), 
	 job		varchar(20), 
	 primary key (ID),
    foreign key (job) references Staff_payments(job) on delete set null
	);

CREATE TABLE IF NOT EXISTS works_for
    (ID			varchar(9),
     block_code		varchar(3),
     primary key (ID),
     foreign key (block_code) references Hostel_blocks(block_code) on delete set null
    );

CREATE TABLE IF NOT EXISTS Mess
	(MIS			varchar(9),
     number_of_meals    numeric(2,0)
        check (number_of_meals >= 16 and number_of_meals <= 31),
     total_bill         numeric(10, 2)
        check (total_bill >= 0),
     hasPaid BOOLEAN,
	 primary key (MIS),
	 foreign key (MIS) references stays_in(MIS) on delete set null
	);

CREATE TABLE IF NOT EXISTS pays
    (MIS    varchar(9),
     Transaction_id     varchar(50) not null UNIQUE,
     primary key (MIS, Transaction_id)
     foreign key (MIS) references stays_in(MIS) on delete cascade
    );

CREATE TABLE IF NOT EXISTS Fees
    (Transaction_id     varchar(50) not null UNIQUE,
     payment_date       DATE,
     primary key (Transaction_id),
     foreign key  (Transaction_id) references pays(Transaction_id) on delete cascade
    );

CREATE TABLE IF NOT EXISTS Login 
    (MIS    varchar(9), 
    password    varchar(255)
    );