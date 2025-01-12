import random
import datetime

import psycopg
import faker

fake = faker.Faker(["fa_IR"])

def get_connection():
    return psycopg.connect(
        dbname="mydb",
        user="postgres",
        password="password",
        host="localhost",
        options="-c search_path=mydb,public",  # Setting schema search path at the connection level
        port=5432
    )


def create_faculties(curr):
    college_terms = [
        'دانشکده علوم انسانی', 'دانشکده مهندسی', 'دانشکده پزشکی', 'دانشکده علوم پایه',
        'دانشکده علوم کامپیوتر', 'دانشکده هنر', 'دانشکده علوم اجتماعی',
        'دانشکده حقوق', 'دانشکده کشاورزی', 'دانشکده زبان و ادبیات', 'دانشکده مدیریت'
    ]
    for faculty_name in college_terms:
        # Insert faculty name using single quotes around the name to ensure it is treated as a string literal
        curr.execute(f'INSERT INTO "Faculty" ("name") VALUES (%s)', (faculty_name,))
        #print(curr.execute('SELECT * FROM "Faculty"').fetchall())


def create_departments(curr):
    faculties = curr.execute('select * from "Faculty"').fetchall()

    academic_groups = {
        'دانشکده علوم انسانی': [
            'روانشناسی', 'فلسفه', 'تاریخ', 'جامعه‌شناسی', 'زبان‌شناسی',
            'ادبیات فارسی', 'حقوق', 'علوم سیاسی'
        ],
        'دانشکده مهندسی': [
            'مهندسی برق', 'مهندسی مکانیک', 'مهندسی عمران', 'مهندسی کامپیوتر',
            'مهندسی صنایع', 'مهندسی شیمی', 'مهندسی مواد', 'مهندسی معماری'
        ],
        'دانشکده پزشکی': [
            'پزشکی عمومی', 'پرستاری', 'داروسازی', 'دندانپزشکی',
            'توانبخشی', 'علوم آزمایشگاهی', 'بهداشت عمومی'
        ],
        'دانشکده علوم پایه': [
            'ریاضیات', 'فیزیک', 'شیمی', 'زیست‌شناسی', 'زمین‌شناسی'
        ],
        'دانشکده علوم کامپیوتر': [
            'علم داده', 'هوش مصنوعی', 'مهندسی نرم‌افزار', 'شبکه‌های کامپیوتری',
            'برنامه‌نویسی', 'تحلیل سیستم‌ها'
        ],
        'دانشکده هنر': [
            'نقاشی', 'طراحی گرافیک', 'سینما', 'تئاتر', 'موسیقی',
            'معماری داخلی', 'هنرهای تجسمی'
        ],
        'دانشکده علوم اجتماعی': [
           'مردم‌شناسی', 'مددکاری اجتماعی', 'جغرافیا', 'برنامه‌ریزی شهری'
        ],
        'دانشکده کشاورزی': [
            'کشاورزی', 'باغبانی', 'علوم دامی', 'علوم خاک', 'مهندسی آب و خاک'
        ],
        'دانشکده زبان و ادبیات': [
            'زبان و ادبیات فارسی', 'زبان انگلیسی', 'زبان عربی', 'زبان‌های خارجی دیگر', 'ترجمه'
        ],
        'دانشکده مدیریت': [
            'مدیریت کسب‌وکار', 'مدیریت منابع انسانی', 'مدیریت مالی',
            'مدیریت بازاریابی', 'مدیریت سیستم‌ها'
        ],
        'دانشکده حقوق': [
            'حقوق عمومی', 'حقوق خصوصی', 'حقوق بین‌الملل', 'حقوق جزا', 'حقوق تجارت'
        ]
    }

    for faculty_id, faculty_name  in faculties:
        for group_name in academic_groups[faculty_name]:
            curr.execute(f'INSERT INTO "Department" ("faculty_id", "name") VALUES (%s, %s)', (faculty_id, group_name))
    #print(curr.execute('SELECT * FROM "Department"').fetchall())

def create_professors(curr):

    users = curr.execute(f'select user_id from "User" limit 50').fetchall()
    departments = curr.execute('select department_id from "Department"').fetchall()
    departments = [i[0] for i in departments]
    ranks = ["استادیار", "دانشیار", "استاد", "مربی"]

    for user_id in users:
        user_id = user_id[0]
        selected_department = random.choice(departments)
        curr.execute(f'INSERT INTO "Professor" ("user_id", "department_id", "room_number", "academic_rank") VALUES (%s, %s, %s, %s)', (user_id, selected_department, str(random.randint(1, 100)), random.choice(ranks)))
    #print(curr.execute('SELECT * FROM "Professor"').fetchall())

def create_students(curr):
    users = curr.execute(f'select user_id from "User" where "user_id" NOT IN (select user_id from "User" limit 50)').fetchall()
    users = [i[0] for i in users]
    departments = curr.execute('select department_id from "Department"').fetchall()
    departments = [i[0] for i in departments]
    degrees = ["کارشناسی", "کارشناسی ارشد", "دکتری"]
    status = ["در حال تحصیل", "فارغ التحصیل"]
    for user_id in users:
        selected_department = random.choice(departments)
        selected_degree = random.choice(degrees)
        selected_status = random.choice(status)
        curr.execute(f'INSERT INTO "Student" ("user_id", "department_id", "degree_status", "status") VALUES (%s, %s, %s, %s)', (user_id, selected_department, selected_degree, selected_status))
    #print(curr.execute('select * from "Student"').fetchall())

def create_lessons(curr):
    department_lessons = {
        'روانشناسی': [
            {"lesson_name": "مبانی روانشناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "روانشناسی اجتماعی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'فلسفه': [
            {"lesson_name": "مبانی فلسفه", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "فلسفه اخلاق", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'تاریخ': [
            {"lesson_name": "مبانی تاریخ", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "تاریخ ایران", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'جامعه‌شناسی': [
            {"lesson_name": "مبانی جامعه‌شناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "جامعه‌شناسی توسعه", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'زبان‌شناسی': [
            {"lesson_name": "مبانی زبان‌شناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "زبان‌شناسی اجتماعی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'ادبیات فارسی': [
            {"lesson_name": "مبانی ادبیات فارسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "ادبیات معاصر", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق': [
            {"lesson_name": "حقوق عمومی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "حقوق خصوصی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'علوم سیاسی': [
            {"lesson_name": "مبانی علوم سیاسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مباحث سیاسی ایران", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مهندسی برق': [
            {"lesson_name": "مبانی مهندسی برق", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مدارهای الکتریکی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی مکانیک': [
            {"lesson_name": "مبانی مهندسی مکانیک", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "دینامیک", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی عمران': [
            {"lesson_name": "مبانی مهندسی عمران", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مقاومت مصالح", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی کامپیوتر': [
            {"lesson_name": "مبانی مهندسی کامپیوتر", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "الگوریتم‌ها", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی صنایع': [
            {"lesson_name": "مبانی مهندسی صنایع", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مدیریت تولید", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مهندسی شیمی': [
            {"lesson_name": "مبانی مهندسی شیمی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "فرآیندهای شیمیایی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی مواد': [
            {"lesson_name": "مبانی مهندسی مواد", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "خواص مواد", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مهندسی معماری': [
            {"lesson_name": "مبانی معماری", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "تاریخ معماری", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'پزشکی عمومی': [
            {"lesson_name": "مبانی پزشکی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "فیزیولوژی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'پرستاری': [
            {"lesson_name": "مبانی پرستاری", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "پرستاری اورژانس", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'داروسازی': [
            {"lesson_name": "مبانی داروسازی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "داروسازی بالینی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'دندانپزشکی': [
            {"lesson_name": "مبانی دندانپزشکی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "ترمیم دندان", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'توانبخشی': [
            {"lesson_name": "مبانی توانبخشی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "توانبخشی حرکتی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'علوم آزمایشگاهی': [
            {"lesson_name": "مبانی علوم آزمایشگاهی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "بیوشیمی بالینی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'بهداشت عمومی': [
            {"lesson_name": "مبانی بهداشت عمومی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "سلامت جامعه", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'ریاضیات': [
            {"lesson_name": "مبانی ریاضیات", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "جبر خطی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'فیزیک': [
            {"lesson_name": "مبانی فیزیک", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مکانیک کلاسیک", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'شیمی': [
            {"lesson_name": "مبانی شیمی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "شیمی آلی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'زیست‌شناسی': [
            {"lesson_name": "مبانی زیست‌شناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "زیست‌شناسی مولکولی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'زمین‌شناسی': [
            {"lesson_name": "مبانی زمین‌شناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "زمین‌شناسی فیزیکی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'علم داده': [
            {"lesson_name": "مبانی علم داده", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "یادگیری ماشین", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'هوش مصنوعی': [
            {"lesson_name": "مبانی هوش مصنوعی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "الگوریتم‌های هوش مصنوعی", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'مهندسی نرم‌افزار': [
            {"lesson_name": "مبانی مهندسی نرم‌افزار", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "توسعه نرم‌افزار", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'شبکه‌های کامپیوتری': [
            {"lesson_name": "مبانی شبکه‌های کامپیوتری", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "شبکه‌های بی‌سیم", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'برنامه‌نویسی': [
            {"lesson_name": "مبانی برنامه‌نویسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "برنامه‌نویسی پیشرفته", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'تحلیل سیستم‌ها': [
            {"lesson_name": "مبانی تحلیل سیستم‌ها", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مدل‌سازی سیستم‌ها", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'نقاشی': [
            {"lesson_name": "مبانی نقاشی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "رنگ‌شناسی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'طراحی گرافیک': [
            {"lesson_name": "مبانی طراحی گرافیک", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "طراحی پوستر", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'سینما': [
            {"lesson_name": "مبانی سینما", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "تاریخ سینما", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'تئاتر': [
            {"lesson_name": "مبانی تئاتر", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "درام نویسی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'موسیقی': [
            {"lesson_name": "مبانی موسیقی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "تئوری موسیقی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'معماری داخلی': [
            {"lesson_name": "مبانی معماری داخلی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "طراحی داخلی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'هنرهای تجسمی': [
            {"lesson_name": "مبانی هنرهای تجسمی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "نقد هنری", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مردم‌شناسی': [
            {"lesson_name": "مبانی مردم‌شناسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مردم‌شناسی فرهنگی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مددکاری اجتماعی': [
            {"lesson_name": "مبانی مددکاری اجتماعی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مددکاری روانشناختی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'جغرافیا': [
            {"lesson_name": "مبانی جغرافیا", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "جغرافیای انسانی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'برنامه‌ریزی شهری': [
            {"lesson_name": "مبانی برنامه‌ریزی شهری", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "برنامه‌ریزی حمل و نقل", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'کشاورزی': [
            {"lesson_name": "مبانی کشاورزی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "کشاورزی پایدار", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'باغبانی': [
            {"lesson_name": "مبانی باغبانی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "باغبانی میوه", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'علوم دامی': [
            {"lesson_name": "مبانی علوم دامی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "علوم تغذیه دام", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'علوم خاک': [
            {"lesson_name": "مبانی علوم خاک", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "خاک‌شناسی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مهندسی آب و خاک': [
            {"lesson_name": "مبانی مهندسی آب و خاک", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مدیریت منابع آب", "credits": 4, "lesson_type": "تخصصی"}
        ],
        'زبان و ادبیات فارسی': [
            {"lesson_name": "مبانی زبان و ادبیات فارسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "ادبیات کلاسیک فارسی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'زبان انگلیسی': [
            {"lesson_name": "مبانی زبان انگلیسی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مبانی ترجمه انگلیسی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'زبان عربی': [
            {"lesson_name": "مبانی زبان عربی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "زبان عربی پیشرفته", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'زبان‌های خارجی دیگر': [
            {"lesson_name": "مبانی زبان‌های خارجی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "زبان فرانسه", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'ترجمه': [
            {"lesson_name": "مبانی ترجمه", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "ترجمه متن‌های تخصصی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مدیریت کسب‌وکار': [
            {"lesson_name": "مبانی مدیریت کسب‌وکار", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "استراتژی کسب‌وکار", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مدیریت منابع انسانی': [
            {"lesson_name": "مبانی مدیریت منابع انسانی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "مدیریت تعارضات", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مدیریت مالی': [
            {"lesson_name": "مبانی مدیریت مالی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "تحلیل صورت‌های مالی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مدیریت بازاریابی': [
            {"lesson_name": "مبانی مدیریت بازاریابی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "استراتژی بازاریابی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'مدیریت سیستم‌ها': [
            {"lesson_name": "مبانی مدیریت سیستم‌ها", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "طراحی سیستم‌های اطلاعاتی", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق عمومی': [
            {"lesson_name": "مبانی حقوق عمومی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "حقوق اداری", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق خصوصی': [
            {"lesson_name": "مبانی حقوق خصوصی", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "حقوق قراردادها", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق بین‌الملل': [
            {"lesson_name": "مبانی حقوق بین‌الملل", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "حقوق بین‌الملل بشر", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق جزا': [
            {"lesson_name": "مبانی حقوق جزا", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "جرایم سازمان‌یافته", "credits": 3, "lesson_type": "تخصصی"}
        ],
        'حقوق تجارت': [
            {"lesson_name": "مبانی حقوق تجارت", "credits": 3, "lesson_type": "عمومی"},
            {"lesson_name": "حقوق شرکت‌ها", "credits": 3, "lesson_type": "تخصصی"}
        ]
    }

    for department in department_lessons.keys():
        department_id = curr.execute(f'SELECT department_id from "Department" where name = %s', (department,)).fetchone()
        department_id = department_id[0]
        for lesson in department_lessons[department]:
            lesson_name = lesson['lesson_name']
            lesson_credits = lesson['credits']
            lesson_type = lesson['lesson_type']
            curr.execute(f'INSERT INTO "Lesson" ("department_id", "type", "title", "credits") VALUES (%s, %s, %s, %s)', (department_id, lesson_type, lesson_name, lesson_credits))
    #print(curr.execute('SELECT * FROM "Lesson"').fetchall())


def create_semesters(curr):
    start_date = []
    end_date = []
    for i in range(2015,2025):
        start = datetime.date(year=i, month=7, day=random.randint(1, 29))
        start_date.append(start)
        end = start + datetime.timedelta(days=120)
        end_date.append(end)
        start = end + datetime.timedelta(days=14)
        start_date.append(start)
        end = start + datetime.timedelta(days=120)
        end_date.append(end)
    dates = zip(start_date, end_date)
    for i, date in enumerate(dates):
        type = "پاییز" if i%2==0 else "بهار"
        start , end = date
        curr.execute('INSERT INTO "Semester" ("start_date", "end_date", "type") VALUES (%s, %s, %s)', (str(start), str(end), type))
    #print(curr.execute('SELECT * FROM "Semester"').fetchall())

def create_courses(curr):
    semesters = curr.execute(f'SELECT semester_id FROM "Semester"').fetchall()
    semesters = [i[0] for i in semesters]
    lessons = curr.execute(f'SELECT lesson_id FROM "Lesson"').fetchall()
    lessons = [i[0] for i in lessons]
    for semester in semesters:
        for lesson in lessons:
            curr.execute('INSERT INTO "Course" ("semester_id", "lesson_id", "maximum_capacity") VALUES (%s, %s, %s)', (semester, lesson, 6))
    #print(curr.execute('SELECT * FROM "Course"').fetchall())

def create_enrolments(curr):
    # courses = curr.execute(f'SELECT course_id, student_id, c.lesson_id, COUNT(lesson_id) FROM "Course" c JOIN (SELECT student_id,lesson_id FROM "Student" s JOIN "Lesson" l ON l.department_id = s.department_id) t ON c.lesson_id = t.lesson_id GROUP BY lesson_id')
    courses = curr.execute(f"""
        SELECT 
            c.course_id, 
            t.student_id 
        FROM "Course" c
        JOIN (
            SELECT s.student_id, l.lesson_id
            FROM "Student" s
            JOIN "Lesson" l ON l.department_id = s.department_id
        ) t ON c.lesson_id = t.lesson_id
    """).fetchall()
    for course_id, student_id in courses:
        curr.execute(f'INSERT INTO "Enrollment" ("course_id", "student_id", "final_grade") VALUES (%s, %s, %s)', (course_id, student_id, random.choice(list(map(lambda x:x/100, list(range(0, 2000, 25)))))) )

    #print(curr.execute('SELECT * FROM "Enrollment"').fetchall())

def create_advisements(curr):
    courses = curr.execute('SELECT course_id FROM "Course"').fetchall()
    professors = curr.execute(f'SELECT professor_id FROM "Professor"').fetchall()
    professors = [i[0] for i in professors]
    for course in courses:
        curr.execute(f'INSERT INTO "Advisement" (course_id, professor_id) VALUES (%s, %s)', (course[0], random.choice(professors)))
    #print(curr.execute('SELECT * FROM "Advisement"').fetchall())

def create_requirement(curr):
    lesson_dependency = ["پیشنیاز", "همنیاز"]
    departments = curr.execute('SELECT department_id FROM "Department"').fetchall()
    departments = [i[0] for i in departments]
    for department in departments:
        lessons = curr.execute('SELECT lesson_id, type FROM "Lesson" WHERE department_id=%s', (department,)).fetchall()
        general_lessons = list(filter(lambda x:True if x[1] == "عمومی" else False, lessons))
        general_lessons = [i[0] for i in general_lessons]
        specialized_lessons = list(filter(lambda x: True if x[1] == "تخصصی" else False, lessons))
        specialized_lessons = [i[0] for i in specialized_lessons]
        if len(specialized_lessons) == 0 or len(general_lessons) == 0:
            continue
        curr.execute('INSERT INTO "Requirement" (dependent_lesson_id, independent_lesson_id, lesson_dependency) VALUES (%s, %s, %s)', (random.choice(general_lessons), random.choice(specialized_lessons), random.choice(lesson_dependency)))

    #print(curr.execute('SELECT * FROM "Requirement"').fetchall())

def create_specialized(curr):
    curr.execute("""
    INSERT INTO "Specialized" (department_id, course_id)
    SELECT department_id, course_id
    FROM "Lesson" l
    JOIN "Course" c ON l.lesson_id = c.lesson_id;
    """)

    print(curr.execute('SELECT * FROM "Specialized"').fetchall())


# Get the connection and cursor
conn = get_connection()
curr = conn.cursor()
# create_faculties(curr)
# create_departments(curr)
# create_professors(curr)
# create_students(curr)
# create_lessons(curr)
# create_semesters(curr)
# create_courses(curr)
# create_enrolments(curr)
# create_advisements(curr)
# create_specialized(curr)
# create_requirement(curr)
curr.execute('ALTER TABLE "Lesson" DROP CONSTRAINT "Lesson_department_id_fkey"')
curr.execute('ALTER TABLE "Lesson" DROP COLUMN "department_id"')
conn.commit()
