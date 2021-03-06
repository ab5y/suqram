BEGIN TRANSACTION;
CREATE TABLE questiontype (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	name TEXT, 
	CONSTRAINT pk_questiontype PRIMARY KEY (id), 
	CONSTRAINT uq_questiontype_name UNIQUE (name)
);
INSERT INTO "questiontype" VALUES(1,'2016-07-23 17:37:35.644000','multiplechoice');
CREATE TABLE usertype (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	name TEXT, 
	CONSTRAINT pk_usertype PRIMARY KEY (id), 
	CONSTRAINT uq_usertype_name UNIQUE (name)
);
INSERT INTO "usertype" VALUES(1,'2016-07-23 17:37:35.649000','Teacher');
INSERT INTO "usertype" VALUES(2,'2016-07-23 17:37:35.653000','Student');
CREATE TABLE categorytype (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	name TEXT, 
	CONSTRAINT pk_categorytype PRIMARY KEY (id), 
	CONSTRAINT uq_categorytype_name UNIQUE (name)
);
INSERT INTO "categorytype" VALUES(1,'2016-07-23 17:37:35.637000','chapter');
CREATE TABLE question (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	question TEXT, 
	type_id INTEGER, 
	CONSTRAINT pk_question PRIMARY KEY (id), 
	CONSTRAINT fk_question_type_id_questiontype FOREIGN KEY(type_id) REFERENCES questiontype (id)
);
INSERT INTO "question" VALUES(1,'2016-07-23 17:37:36.714000','You are in charge of developing a new product for an organization. Your quality metrics are based on the 80th percentile of each of the last three products developed. This is an example of:',1);
INSERT INTO "question" VALUES(2,'2016-07-23 17:37:36.722000','The project manager decided to improve the predicted completion date for the project by doing in parallel several of the activities that were scheduled to be done in sequence. This is called :',1);
INSERT INTO "question" VALUES(3,'2016-07-23 17:37:36.760000','In communication, the receiver decodes the messages based on all but the following:',1);
INSERT INTO "question" VALUES(4,'2016-07-23 17:37:36.793000','The critical element in a project''s communication system is the:',1);
INSERT INTO "question" VALUES(5,'2016-07-23 17:37:36.816000','A project manager makes a narrative description of the work that must be done for her project. This is calle',1);
INSERT INTO "question" VALUES(6,'2016-07-23 17:37:36.832000','Crashing the schedule means:',1);
INSERT INTO "question" VALUES(7,'2016-07-23 17:37:36.850000','In a very large project having a budget of $5 million and a project team of over one hundred persons, the project manager constructs a work breakdown structure. The project manager will do the WBS to the detail level of which of the following?',1);
INSERT INTO "question" VALUES(8,'2016-07-23 17:37:36.874000','The original schedule (for a project, a work package, or an activity). Plus or minus approved changes, is called:',1);
INSERT INTO "question" VALUES(9,'2016-07-28 19:21:19.130000','Has the Turing Test been passed by a computer?',1);
INSERT INTO "question" VALUES(10,'2016-07-28 19:25:34.258000','Has the Turing Test been passed by a computer?',1);
INSERT INTO "question" VALUES(11,'2016-07-29 04:13:54.871000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(12,'2016-07-29 04:17:16.510000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(13,'2016-07-29 04:18:06.161000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(14,'2016-07-29 04:20:29.708000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(15,'2016-07-29 04:22:29.785000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(16,'2016-07-29 04:23:45.333000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(17,'2016-07-29 05:34:28.845000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(18,'2016-07-29 05:36:10.998000','Has a computer passed the Turing Test yet?',1);
INSERT INTO "question" VALUES(19,'2016-07-29 06:31:47.125000','Has a computer passed the Turing Test yet?',1);

CREATE TABLE 'user' (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	name TEXT NOT NULL, 
	full_name TEXT, 
	password_hash TEXT NOT NULL, 
	last_logged TIMESTAMP, 
	type_id INTEGER, 
	CONSTRAINT pk_user PRIMARY KEY (id), 
	CONSTRAINT uq_user_name UNIQUE (name), 
	CONSTRAINT fk_user_type_id_usertype FOREIGN KEY(type_id) REFERENCES usertype (id)
);
INSERT INTO "user" VALUES(1,'2016-07-23 17:37:36.417000','sudha','Sudha Sankaran','$2b$12$szS/X3bZm8B7RVDgJ3lDjutTCD8ejmKzrV6OwZpcnbpsgNo1DAdly',NULL,1);
INSERT INTO "user" VALUES(2,'2016-07-24 03:46:01.837000','abhay','abhay','$2b$12$yMBY6GS110.ShfMt5LyfGeSCq.QlnJIDGenY4FaRt0N2Tn8b8Gh0O',NULL,2);
CREATE TABLE category (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	name TEXT, 
	type_id INTEGER, 
	creator_id INTEGER, 
	CONSTRAINT pk_category PRIMARY KEY (id), 
	CONSTRAINT uq_category_name UNIQUE (name), 
	CONSTRAINT fk_category_type_id_categorytype FOREIGN KEY(type_id) REFERENCES categorytype (id), 
	CONSTRAINT fk_category_creator_id_user FOREIGN KEY(creator_id) REFERENCES user (id)
);
INSERT INTO "category" VALUES(1,'2016-07-23 17:37:36.481000','TM',1,1);
INSERT INTO "category" VALUES(2,'2016-07-27 05:53:18.214000','Artificial intelligence',1,1);
CREATE TABLE option (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	option TEXT, 
	"isCorrectAnswer" BOOLEAN NOT NULL, 
	question_id INTEGER, 
	CONSTRAINT pk_option PRIMARY KEY (id), 
	CONSTRAINT fk_option_question_id_question FOREIGN KEY(question_id) REFERENCES question (id)
);
INSERT INTO "option" VALUES(1,'2016-07-23 17:37:36.742000','Statistical sampling',0,1);
INSERT INTO "option" VALUES(2,'2016-07-23 17:37:36.748000','Metrics',0,1);
INSERT INTO "option" VALUES(3,'2016-07-23 17:37:36.750000','Benchmarking',1,1);
INSERT INTO "option" VALUES(4,'2016-07-23 17:37:36.752000','Operational definitions',0,1);
INSERT INTO "option" VALUES(5,'2016-07-23 17:37:36.767000','Crashing',0,2);
INSERT INTO "option" VALUES(6,'2016-07-23 17:37:36.774000','Increasing priorities',0,2);
INSERT INTO "option" VALUES(7,'2016-07-23 17:37:36.778000','Hurry Up defense',0,2);
INSERT INTO "option" VALUES(8,'2016-07-23 17:37:36.780000','Fast Tracking',1,2);
INSERT INTO "option" VALUES(9,'2016-07-23 17:37:36.797000','Culture',0,3);
INSERT INTO "option" VALUES(10,'2016-07-23 17:37:36.801000','Sematics',0,3);
INSERT INTO "option" VALUES(11,'2016-07-23 17:37:36.805000','Language',0,3);
INSERT INTO "option" VALUES(12,'2016-07-23 17:37:36.808000','Distance',1,3);
INSERT INTO "option" VALUES(13,'2016-07-23 17:37:36.820000','Progress report',0,4);
INSERT INTO "option" VALUES(14,'2016-07-23 17:37:36.823000','Project Directive',0,4);
INSERT INTO "option" VALUES(15,'2016-07-23 17:37:36.824000','Project Manager',1,4);
INSERT INTO "option" VALUES(16,'2016-07-23 17:37:36.826000','Customer',0,4);
INSERT INTO "option" VALUES(17,'2016-07-23 17:37:36.836000','Project Plan',0,5);
INSERT INTO "option" VALUES(18,'2016-07-23 17:37:36.838000','Control Chart',0,5);
INSERT INTO "option" VALUES(19,'2016-07-23 17:37:36.840000','Statement Of Work',1,5);
INSERT INTO "option" VALUES(20,'2016-07-23 17:37:36.843000','Project Objective',0,5);
INSERT INTO "option" VALUES(21,'2016-07-23 17:37:36.854000','Making the project shorter by any economic means',1,6);
INSERT INTO "option" VALUES(22,'2016-07-23 17:37:36.857000','Running the project team on overtime',0,6);
INSERT INTO "option" VALUES(23,'2016-07-23 17:37:36.860000','Doing activities that were in sequence in parallel',0,6);
INSERT INTO "option" VALUES(24,'2016-07-23 17:37:36.864000','Getting out of town before the project is in trouble',0,6);
INSERT INTO "option" VALUES(25,'2016-07-23 17:37:36.878000',' Task',0,7);
INSERT INTO "option" VALUES(26,'2016-07-23 17:37:36.881000','Activity',0,7);
INSERT INTO "option" VALUES(27,'2016-07-23 17:37:36.883000','WBS element',0,7);
INSERT INTO "option" VALUES(28,'2016-07-23 17:37:36.885000','Work package',1,7);
INSERT INTO "option" VALUES(29,'2016-07-23 17:37:36.989000','The working schedule',0,8);
INSERT INTO "option" VALUES(30,'2016-07-23 17:37:36.993000',' The target schedule',0,8);
INSERT INTO "option" VALUES(31,'2016-07-23 17:37:36.994000','The performance schedule',0,8);
INSERT INTO "option" VALUES(32,'2016-07-23 17:37:36.996000','The baseline schedule',1,8);
INSERT INTO "option" VALUES(33,'2016-07-29 04:23:46.357000','Artificial intelligence',0,16);
INSERT INTO "option" VALUES(34,'2016-07-29 04:23:46.448000','multiplechoice',0,16);
INSERT INTO "option" VALUES(35,'2016-07-29 04:23:46.532000','Has a computer passed the Turing Test yet?',0,16);
INSERT INTO "option" VALUES(36,'2016-07-29 05:34:32.183000','Artificial intelligence',0,17);
INSERT INTO "option" VALUES(37,'2016-07-29 05:34:32.332000','multiplechoice',0,17);
INSERT INTO "option" VALUES(38,'2016-07-29 05:34:32.409000','Has a computer passed the Turing Test yet?',0,17);
INSERT INTO "option" VALUES(39,'2016-07-29 05:36:13.048000','Artificial intelligence',0,18);
INSERT INTO "option" VALUES(40,'2016-07-29 05:36:13.145000','multiplechoice',0,18);
INSERT INTO "option" VALUES(41,'2016-07-29 05:36:13.223000','Has a computer passed the Turing Test yet?',0,18);
INSERT INTO "option" VALUES(42,'2016-07-29 06:31:49.441000','Yes',0,19);
INSERT INTO "option" VALUES(43,'2016-07-29 06:31:49.533000','No',0,19);
INSERT INTO "option" VALUES(44,'2016-07-29 06:31:49.622000','Maybe',0,19);
INSERT INTO "option" VALUES(45,'2016-07-29 06:31:49.715000','None of the above',0,19);
CREATE TABLE follow (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	follower_id INTEGER, 
	followee_id INTEGER, 
	CONSTRAINT pk_follow PRIMARY KEY (id), 
	CONSTRAINT fk_follow_follower_id_user FOREIGN KEY(follower_id) REFERENCES user (id), 
	CONSTRAINT fk_follow_followee_id_user FOREIGN KEY(followee_id) REFERENCES user (id)
);
INSERT INTO "follow" VALUES(1,'2016-07-24 17:30:33.729000',2,1);
CREATE TABLE usercategory (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	user_id INTEGER, 
	category_id INTEGER, 
	started_at TIMESTAMP NOT NULL, 
	CONSTRAINT pk_usercategory PRIMARY KEY (id), 
	CONSTRAINT fk_usercategory_user_id_user FOREIGN KEY(user_id) REFERENCES user (id), 
	CONSTRAINT fk_usercategory_category_id_category FOREIGN KEY(category_id) REFERENCES category (id)
);
INSERT INTO "usercategory" VALUES(1,'2016-07-24 17:31:03.923000',2,1,'2016-07-24 23:00:48.000000');
INSERT INTO "usercategory" VALUES(2,'2016-07-27 17:28:29.705000',2,1,'2016-07-27 22:57:29.000000');
INSERT INTO "usercategory" VALUES(3,'2016-07-29 06:47:06.960000',2,2,'2016-07-29 12:02:09.000000');
INSERT INTO "usercategory" VALUES(4,'2016-07-29 10:15:41.109000',2,1,'2016-07-29 15:45:22.000000');
CREATE TABLE categoryquestion (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	category_id INTEGER, 
	question_id INTEGER, 
	CONSTRAINT pk_categoryquestion PRIMARY KEY (id), 
	CONSTRAINT fk_categoryquestion_category_id_category FOREIGN KEY(category_id) REFERENCES category (id), 
	CONSTRAINT fk_categoryquestion_question_id_question FOREIGN KEY(question_id) REFERENCES question (id)
);
INSERT INTO "categoryquestion" VALUES(1,'2016-07-23 17:37:36.784000',1,2);
INSERT INTO "categoryquestion" VALUES(2,'2016-07-23 17:37:36.868000',1,6);
INSERT INTO "categoryquestion" VALUES(3,'2016-07-23 17:37:36.998000',1,8);
INSERT INTO "categoryquestion" VALUES(4,'2016-07-29 05:36:11.952000',2,18);
INSERT INTO "categoryquestion" VALUES(5,'2016-07-29 06:31:47.976000',2,19);
CREATE TABLE userquestion (
	id INTEGER NOT NULL, 
	created TIMESTAMP, 
	user_id INTEGER, 
	question_id INTEGER, 
	user_category_id INTEGER, 
	selected_option_id INTEGER, 
	CONSTRAINT pk_userquestion PRIMARY KEY (id), 
	CONSTRAINT fk_userquestion_user_id_user FOREIGN KEY(user_id) REFERENCES user (id), 
	CONSTRAINT fk_userquestion_question_id_question FOREIGN KEY(question_id) REFERENCES question (id), 
	CONSTRAINT fk_userquestion_user_category_id_usercategory FOREIGN KEY(user_category_id) REFERENCES usercategory (id), 
	CONSTRAINT fk_userquestion_selected_option_id_option FOREIGN KEY(selected_option_id) REFERENCES option (id)
);
INSERT INTO "userquestion" VALUES(1,'2016-07-24 17:31:03.932000',2,8,1,30);
INSERT INTO "userquestion" VALUES(2,'2016-07-24 17:31:03.943000',2,8,1,5);
INSERT INTO "userquestion" VALUES(3,'2016-07-24 17:31:03.953000',2,8,1,23);
INSERT INTO "userquestion" VALUES(4,'2016-07-27 17:28:29.799000',2,8,2,29);
INSERT INTO "userquestion" VALUES(5,'2016-07-27 17:28:29.838000',2,8,2,8);
INSERT INTO "userquestion" VALUES(6,'2016-07-27 17:28:29.851000',2,8,2,21);
INSERT INTO "userquestion" VALUES(7,'2016-07-29 06:47:06.968000',2,19,3,43);
INSERT INTO "userquestion" VALUES(8,'2016-07-29 10:15:41.118000',2,8,4,32);
INSERT INTO "userquestion" VALUES(9,'2016-07-29 10:15:41.129000',2,2,4,5);
INSERT INTO "userquestion" VALUES(10,'2016-07-29 10:15:41.139000',2,6,4,22);
COMMIT;
