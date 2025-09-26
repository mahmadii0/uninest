# 📚 Uninest – Student Class Manager Bot

A **Telegram bot** for university students to manage their **classes, professors, exams, and files** inside student groups.  
The project integrates a **Django web app** for forms and uses **Redis + Docker** for communication, with **MySQL** as the main database.

---

## 🚀 Features
- **Class management** – create and edit classes  
- **Professors** – assign a professor to each class, with optional profile image  
- **Students** – users can join classes (after starting bot in private chat) to receive notifications  
- **Exams** – schedule exams with date & time; reminders sent automatically  
- **Files** – upload and search files per class, plus global search across all classes  
- **Django forms** – better UX for creating/editing professors, classes, and exams (links are shared by bot)  

---

## 🛠️ Tech Stack
- **Bot framework**: [Telebot](https://github.com/eternnoir/pyTelegramBotAPI) (Python)  
- **Web app**: Django  
- **Database**: MySQL  
- **Message broker**: Redis  
- **Containerization**: Docker & docker-compose  

---

## 📂 Project Structure
uninest/

├── bot/ # Telegram bot (Telebot)

├── webApp/ # Django web application

├── shared/ # Shared utilities & logic

├── locales/ # Translation files

├── docker-compose.yml

├── Dockerfile

└── requirements.txt

---

## ⚡ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mahmadii0/uninest.git
cd uninest
```

### 2. Setup environment
- create a constants.py file on shared directory and write them to it:
```bash
Token='Your bot token'

#Coonection Detail for database
connectionDetail={
    'host':'mysql',
    'port':'3306',
    'user':'yourusername',
    'password':'yourpassword',
    'database':'db_name',
    }

channelID=int('a private channel id for saving files')

#Tables

tables={'groups':'''CREATE TABLE IF NOT EXISTS botgroups(
groupID BIGINT NOT NULL PRIMARY KEY,
group_name varchar(150),
lang varchar(2) NOT NULL
);'''
,'lectures':'''CREATE TABLE IF NOT EXISTS lectures(
lecID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
lec_name varchar(100) NOT NULL,
phone varchar(11),
rate FLOAT NOT NULL,
pic varchar(200),
groupID BIGINT NOT NULL,
CONSTRAINT group_lectures FOREIGN KEY (groupID) REFERENCES botgroups(groupID)
);'''
,'classes':'''CREATE TABLE IF NOT EXISTS classes(
classID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
class_name varchar(100) NOT NULL,
lecID INTEGER NOT NULL,
CONSTRAINT classes_lectures FOREIGN KEY (lecID) REFERENCES lectures(lecID),
groupID BIGINT NOT NULL,
CONSTRAINT group_classes FOREIGN KEY (groupID) REFERENCES botgroups(groupID)
);'''
,'students':'''CREATE TABLE IF NOT EXISTS students(
studentID BIGINT NOT NULL PRIMARY KEY,
std_name varchar(100) NOT NULL,
username varchar(100),
groupID BIGINT NOT NULL,
CONSTRAINT group_students FOREIGN KEY (groupID) REFERENCES botgroups(groupID)
);'''
,'student_class_relation':'''CREATE TABLE IF NOT EXISTS student_class_relation(
classID INTEGER NOT NULL PRIMARY KEY,
studentID BIGINT NOT NULL PRIMARY KEY,
groupID varchar(45) NOT NULL PRIMARY KEY,
CONSTRAINT class_s_c_relation FOREIGN KEY (classID) REFERENCES classes(classID),
CONSTRAINT student_s_c_redaltion FOREIGN KEY (studentID) REFERENCES students(studentID) 
);'''
,'files':'''CREATE TABLE IF NOT EXISTS files(
file_name varchar(120) NOT NULL,
address varchar(100) NOT NULL,
classID INTEGER ,
CONSTRAINT files_classes FOREIGN KEY (classID) REFERENCES classes(classID) 
);'''
,'exams':'''CREATE TABLE IF NOT EXISTS exams(
examID INTEGER NOT NULL PRIMARY KEY,
title varchar(100) NOT NULL,
classID INTEGER NOT NULL ,
date_time DATETIME NOT NULL,
reminder varchar(35) NOT NULL,
CONSTRAINT exams_classes FOREIGN KEY (classID) REFERENCES classes(classID)
);'''
,'exercises':'''CREATE TABLE IF NOT EXISTS exercises(
title varchar(100) NOT NULL,
classID INTEGER NOT NULL,
date_time DATETIME,
CONSTRAINT exercises_classes FOREIGN KEY (classID) REFERENCES classes(classID)
);'''
,'requests':'''CREATE TABLE IF NOT EXISTS requests(
token BIGINT NOT NULL,
groupID BIGINT ,
type varchar(30) 
);'''
}
```
### 3. Run with Docker
```bash
docker-compose up --build
```
### 4. Start Bot
- Once containers are running, start the bot and web app:
  
    Bot: listens for group & private messages
  
    Web app: forms accessible at http://localhost:8000
  
    redis: listen at port 6379
  
    mysql: listen at port 3307(because on my machine, the mysql engine already listen at port 3306)
### 🤝 Contributing
1.Fork the repo

2.Create a feature branch (git checkout -b feature-name)

3.Commit changes (git commit -m "Add feature")

4.Push branch (git push origin feature-name)

5.Open a Pull Request
