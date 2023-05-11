import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE `temp_pass` (`name` VARCHAR(30) NOT NULL , `regno` NUMBER  NOT NULL , `student` VARCHAR(20) NOT NULL , `phone` NUMBER NOT NULL , `dept` VARCHAR(10) NOT NULL , `year` INT NOT NULL , `date` DATE NOT NULL , `time` TIME NOT NULL , `purpose` VARCHAR(255) NOT NULL , `indate` DATE NOT NULL , `intime` TIME NOT NULL)
''')
cur.execute('''
CREATE TABLE `pass` (`name` VARCHAR(30) NOT NULL , `regno` NUMBER  NOT NULL , `student` VARCHAR(20) NOT NULL , `phone` NUMBER NOT NULL , `dept` VARCHAR(10) NOT NULL , `year` INT NOT NULL , `date` DATE NOT NULL , `time` TIME NOT NULL , `purpose` VARCHAR(255) NOT NULL , `indate` DATE NOT NULL , `intime` TIME NOT NULL)
''')
conn.commit()
conn.close()