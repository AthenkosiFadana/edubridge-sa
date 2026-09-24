"""Seed EduBridge SA with pathways, courses, modules, lessons and quizzes.

Run: python -m app.seed
"""

from sqlalchemy import select

from .database import Base, SessionLocal, engine
from .models import (
    AssessmentQuestion,
    Course,
    JobOpportunity,
    Lesson,
    Module,
    Pathway,
    PathwayLevel,
    QuizQuestion,
    User,
)
from .security import hash_password

Base.metadata.create_all(bind=engine)

COURSES = [
    {
        "title": "Computer Fundamentals",
        "category": "Computer Skills",
        "difficulty": "Beginner",
        "description": "What a computer is, how operating systems work, files, folders and basic troubleshooting.",
        "modules": [
            {
                "title": "Introduction to Computers",
                "description": "Hardware, software and what an operating system does.",
                "lessons": [
                    {
                        "title": "What is a computer?",
                        "content": (
                            "A computer is a machine that takes **input**, processes it, and gives **output**.\n\n"
                            "Key components:\n"
                            "- **CPU** — the brain, executes instructions\n"
                            "- **RAM** — short-term working memory\n"
                            "- **Storage (HDD/SSD)** — long-term files\n"
                            "- **Input devices** — keyboard, mouse\n"
                            "- **Output devices** — screen, speakers\n\n"
                            "An **operating system** (Windows, Linux, macOS) manages all of this. "
                            "It sits between you and the hardware."
                        ),
                        "quiz": [
                            ("Which of the following is an operating system?", "Google", "Windows", "Facebook", "Gmail", "b"),
                            ("What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Program Utility", "a"),
                            ("Which component is short-term memory?", "SSD", "RAM", "Monitor", "Keyboard", "b"),
                        ],
                    },
                    {
                        "title": "Files, folders and storage",
                        "content": (
                            "Files store data. Folders organise files.\n\n"
                            "Common file types:\n"
                            "- `.txt` text\n"
                            "- `.pdf` document\n"
                            "- `.jpg` image\n"
                            "- `.docx` Word document\n\n"
                            "**Storage vs memory:** storage keeps files when the computer is off; "
                            "RAM only holds data while the computer is on.\n\n"
                            "Practical: create a folder `EduBridge` on your device and save a text file inside it."
                        ),
                        "quiz": [
                            ("Which keeps files after the computer is switched off?", "RAM", "Storage (SSD)", "CPU", "Monitor", "b"),
                            ("What does the .pdf extension usually mean?", "A spreadsheet", "A document", "An image", "A program", "b"),
                        ],
                    },
                ],
            },
            {
                "title": "Basic troubleshooting",
                "description": "Fix common problems yourself.",
                "lessons": [
                    {
                        "title": "Solving common computer problems",
                        "content": (
                            "A simple method for any problem:\n\n"
                            "1. **What changed?** (new app, update, cable)\n"
                            "2. **Restart** — solves more than you think\n"
                            "3. **Check connections** — power, cables, Wi-Fi\n"
                            "4. **Read the error message** carefully\n"
                            "5. **Search the exact error** online\n\n"
                            "This method is the same one IT support technicians use every day."
                        ),
                        "quiz": [
                            ("What is usually the FIRST troubleshooting step?", "Buy a new computer", "Restart the device", "Call a friend", "Delete everything", "b"),
                            ("Why read the error message carefully?", "It is entertainment", "It describes the problem", "It is required by law", "It never matters", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Linux Fundamentals",
        "category": "Operating Systems",
        "difficulty": "Beginner",
        "description": "The operating system behind most servers and the cloud. Command line basics.",
        "modules": [
            {
                "title": "Linux basics",
                "description": "Distributions, the shell and essential commands.",
                "lessons": [
                    {
                        "title": "What is Linux?",
                        "content": (
                            "Linux is an open-source operating system. Most AWS services run on Linux.\n\n"
                            "Key ideas:\n"
                            "- **Distribution (distro)** — Ubuntu, Debian, CentOS\n"
                            "- **Shell** — where you type commands (bash)\n"
                            "- **Everything is a file** — even hardware\n"
                            "- **Permissions** — read/write/execute for users\n\n"
                            "Why it matters: EC2 instances, containers and cloud tooling assume Linux knowledge."
                        ),
                        "quiz": [
                            ("Which is a Linux distribution?", "Ubuntu", "Windows 11", "iOS", "Office 365", "a"),
                            ("What is the shell?", "A marine animal", "A command interpreter", "A file type", "A mouse", "b"),
                        ],
                    },
                    {
                        "title": "Essential commands",
                        "content": (
                            "```\n"
                            "pwd           # where am I?\n"
                            "ls            # list files\n"
                            "cd folder     # move into folder\n"
                            "mkdir name    # create folder\n"
                            "touch f.txt   # create file\n"
                            "cat f.txt     # print file contents\n"
                            "cp a b        # copy\n"
                            "rm f.txt      # delete (careful!)\n"
                            "```\n\n"
                            "Practice: create folder `practice`, a file inside it, then list it."
                        ),
                        "quiz": [
                            ("Which command shows your current directory?", "pwd", "ls", "cd", "cat", "a"),
                            ("Which command creates a directory?", "mkdir", "touch", "rm", "cat", "a"),
                            ("Which command lists files?", "cd", "ls", "pwd", "cp", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Networking Fundamentals",
        "category": "Networking",
        "difficulty": "Beginner",
        "description": "IP addresses, DNS, ports and how the internet delivers your data.",
        "modules": [
            {
                "title": "How networks communicate",
                "description": "IP, DNS, ports and protocols.",
                "lessons": [
                    {
                        "title": "IP addresses and DNS",
                        "content": (
                            "Every device on a network has an **IP address** (e.g. `192.168.1.10`).\n\n"
                            "**DNS** translates names to IPs: `google.com` → `142.250.x.x`.\n\n"
                            "Key ports:\n"
                            "- 22 — SSH\n"
                            "- 80 — HTTP\n"
                            "- 443 — HTTPS\n"
                            "- 3306 — MySQL\n\n"
                            "In AWS you will design this with **VPCs** and **security groups**."
                        ),
                        "quiz": [
                            ("What does DNS do?", "Encrypts traffic", "Translates names to IP addresses", "Stores files", "Sends email", "b"),
                            ("Which port is used by HTTPS?", "80", "21", "443", "22", "c"),
                            ("What is an IP address?", "A password", "A device's network address", "An email", "A file", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Python Fundamentals",
        "category": "Programming",
        "difficulty": "Beginner",
        "description": "Variables, control flow, functions and small automation scripts.",
        "modules": [
            {
                "title": "Getting started with Python",
                "description": "Your first programs.",
                "lessons": [
                    {
                        "title": "Variables and data types",
                        "content": (
                            "```python\n"
                            "name = \"Athenkosi\"     # string\n"
                            "age = 25                # integer\n"
                            "data_ok = True          # boolean\n"
                            "print(name, age)\n"
                            "```\n\n"
                            "Python runs top to bottom. Use `input()` to get user data, "
                            "`print()` to show output."
                        ),
                        "quiz": [
                            ("Which is a string in Python?", "42", "\"hello\"", "True", "3.14", "b"),
                            ("Which keyword defines a variable?", "var", "let", "(none — assignment)", "dim", "c"),
                        ],
                    },
                    {
                        "title": "Conditionals and loops",
                        "content": (
                            "```python\n"
                            "score = 75\n"
                            "if score >= 50:\n"
                            "    print(\"Pass\")\n"
                            "else:\n"
                            "    print(\"Fail\")\n\n"
                            "for i in range(3):\n"
                            "    print(i)  # 0 1 2\n"
                            "```\n\n"
                            "This pattern — check, then act — powers quizzes, game logic and automation."
                        ),
                        "quiz": [
                            ("What does `if` do?", "Loops forever", "Makes a decision", "Imports a library", "Ends the program", "b"),
                            ("range(3) produces?", "1,2,3", "0,1,2", "3", "0,1,2,3", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "AWS Cloud Fundamentals",
        "category": "Cloud",
        "difficulty": "Beginner",
        "description": "Cloud concepts, core AWS services and the shared responsibility model.",
        "modules": [
            {
                "title": "Cloud concepts",
                "description": "Why the cloud exists and core services.",
                "lessons": [
                    {
                        "title": "What is cloud computing?",
                        "content": (
                            "Cloud = using someone else's computers on demand, paying for what you use.\n\n"
                            "Service models:\n"
                            "- **IaaS** — virtual machines (EC2)\n"
                            "- **PaaS** — run code without servers (Lambda)\n"
                            "- **SaaS** — software you just use (Gmail)\n\n"
                            "Core AWS services to know:\n"
                            "- **EC2** — virtual servers\n"
                            "- **S3** — file storage\n"
                            "- **RDS** — managed databases\n"
                            "- **Lambda** — serverless functions\n"
                            "- **IAM** — who can access what"
                        ),
                        "quiz": [
                            ("Which AWS service is object storage?", "EC2", "S3", "RDS", "IAM", "b"),
                            ("What does IaaS provide?", "Only software", "Virtual machines and networking", "Email", "Gaming", "b"),
                            ("Which service runs code without servers?", "S3", "EC2", "Lambda", "Route 53", "c"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Email and Digital Safety",
        "category": "Digital Literacy",
        "difficulty": "Beginner",
        "description": "Professional email, Google Workspace basics and staying safe online.",
        "modules": [
            {
                "title": "Communication tools",
                "description": "Email etiquette and online safety.",
                "lessons": [
                    {
                        "title": "Professional email",
                        "content": (
                            "Structure of a good email:\n"
                            "1. Clear subject: `Application: IT Support Role — N. Dlamini`\n"
                            "2. Greeting: `Dear Mr. Nkosi,`\n"
                            "3. Purpose in the first sentence\n"
                            "4. Short body with detail\n"
                            "5. Professional closing: `Kind regards, …`\n\n"
                            "**Safety:** never share passwords; check the sender address; "
                            "don't click suspicious links (phishing)."
                        ),
                        "quiz": [
                            ("Which subject line is best?", "hi", "Application: IT Support Role", "urgent!!!", "asdf", "b"),
                            ("A stranger emails asking for your password. Do you…", "Send it", "Ignore and report it", "Reply with it", "Post it online", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "CV and Job Search Skills",
        "category": "Job Readiness",
        "difficulty": "Beginner",
        "description": "Build a one-page CV, prepare for interviews and find opportunities.",
        "modules": [
            {
                "title": "Getting hired",
                "description": "CV writing and interview basics.",
                "lessons": [
                    {
                        "title": "Building a one-page CV",
                        "content": (
                            "Sections:\n"
                            "1. **Contact** — name, phone, email, location\n"
                            "2. **Summary** — 2 lines about you\n"
                            "3. **Skills** — e.g. Linux, Python basics, MS Office\n"
                            "4. **Education** — schools, courses, certificates\n"
                            "5. **Experience** — jobs, volunteering, projects\n\n"
                            "Tips: one page, no photo (unless asked), "
                            "PDF format, tailor skills to each job advert."
                        ),
                        "quiz": [
                            ("How long should an entry-level CV be?", "5 pages", "One page", "Ten lines with no detail", "It doesn't matter", "b"),
                            ("Which format should you send?", "Word draft with tracked changes", "PDF", "Screenshot", "Voice note", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Cybersecurity Fundamentals",
        "category": "Security",
        "difficulty": "Beginner",
        "description": "Threats, passwords, safe browsing and security mindset.",
        "modules": [
            {
                "title": "Security basics",
                "description": "Protect yourself and your systems.",
                "lessons": [
                    {
                        "title": "Passwords and common attacks",
                        "content": (
                            "Rules:\n"
                            "- Long passphrases beat short passwords (`correct-horse-battery`)\n"
                            "- Unique password per site\n"
                            "- Enable **MFA** everywhere\n\n"
                            "Common attacks:\n"
                            "- **Phishing** — fake emails/links\n"
                            "- **Malware** — malicious software\n"
                            "- **Social engineering** — tricking people\n\n"
                            "In AWS: **IAM least privilege** applies the same idea to cloud access."
                        ),
                        "quiz": [
                            ("Strongest password?", "123456", "password", "kofi-mara-festival-88", "qwerty", "c"),
                            ("MFA means?", "Multi-Factor Authentication", "My File Backup", "Managed Firewall Access", "Many Free Apps", "a"),
                            ("Phishing is…", "A fishing hobby", "Tricking users via fake messages", "A VPN", "A password manager", "b"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "title": "Microsoft Office Fundamentals",
        "category": "Office Productivity",
        "difficulty": "Beginner",
        "description": "Documents, spreadsheets and presentations for the workplace.",
        "modules": [
            {
                "title": "Office essentials",
                "description": "Word, Excel and PowerPoint basics.",
                "lessons": [
                    {
                        "title": "Spreadsheets for everyday work",
                        "content": (
                            "Excel/Sheets essentials:\n"
                            "- Cells, rows, columns\n"
                            "- `=SUM(B1:B10)` — add a range\n"
                            "- `=AVERAGE(…)` — average\n"
                            "- Sorting and filtering tables\n"
                            "- Simple charts\n\n"
                            "Use case: track monthly data costs, small business sales, "
                            "learner attendance at a community centre."
                        ),
                        "quiz": [
                            ("=SUM(B1:B10) does what?", "Counts cells", "Adds values in B1:B10", "Deletes the range", "Sorts the data", "b"),
                            ("A spreadsheet file is also called…", "A slide deck", "A worksheet/workbook", "A database server", "An OS", "b"),
                        ],
                    },
                ],
            },
        ],
    },
]

PATHWAYS = [
    {
        "title": "IT Support Technician",
        "role_title": "IT Support Technician",
        "description": "Hardware, operating systems, networking and the practical project skills helpdesks need.",
        "levels": [
            "Computer Fundamentals",
            "Email and Digital Safety",
            "Linux Fundamentals",
            "Networking Fundamentals",
            "Cybersecurity Fundamentals",
            "Python Fundamentals",
            "AWS Cloud Fundamentals",
            "Practical IT Support Project (hands-on)",
            "CV and Job Search Skills",
        ],
    },
    {
        "title": "Cloud Practitioner",
        "role_title": "Junior Cloud Practitioner",
        "description": "From computer basics to core AWS services, ready for cloud entry roles.",
        "levels": [
            "Computer Fundamentals",
            "Linux Fundamentals",
            "Networking Fundamentals",
            "Python Fundamentals",
            "AWS Cloud Fundamentals",
            "Cybersecurity Fundamentals",
            "CV and Job Search Skills",
        ],
    },
    {
        "title": "Junior Developer",
        "role_title": "Junior Developer",
        "description": "Programming foundations with Python plus the digital literacy to work professionally.",
        "levels": [
            "Computer Fundamentals",
            "Email and Digital Safety",
            "Python Fundamentals",
            "Linux Fundamentals",
            "Networking Fundamentals",
            "AWS Cloud Fundamentals",
            "CV and Job Search Skills",
        ],
    },
    {
        "title": "Cybersecurity Analyst",
        "role_title": "Junior Security Analyst",
        "description": "Security mindset built on systems, networks and cloud fundamentals.",
        "levels": [
            "Computer Fundamentals",
            "Linux Fundamentals",
            "Networking Fundamentals",
            "Cybersecurity Fundamentals",
            "Python Fundamentals",
            "AWS Cloud Fundamentals",
            "CV and Job Search Skills",
        ],
    },
    {
        "title": "Digital Entrepreneur",
        "role_title": "Digital Entrepreneur",
        "description": "Office tools, online communication and cloud basics to run a digital business.",
        "levels": [
            "Computer Fundamentals",
            "Email and Digital Safety",
            "Microsoft Office Fundamentals",
            "AWS Cloud Fundamentals",
            "CV and Job Search Skills",
        ],
    },
]

# 15-question digital skills assessment across 6 categories
ASSESSMENT_QUESTIONS = [
    # Computer Fundamentals (3)
    ("Computer Fundamentals", "Which of the following is an operating system?", "Google", "Windows", "Facebook", "Gmail", "b"),
    ("Computer Fundamentals", "What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Program Utility", "a"),
    ("Computer Fundamentals", "Which component stores files when the computer is off?", "RAM", "Storage (SSD/HDD)", "Monitor", "CPU", "b"),
    # Internet Skills (3)
    ("Internet Skills", "What does DNS do?", "Encrypts messages", "Translates website names to IP addresses", "Stores files", "Sends emails", "b"),
    ("Internet Skills", "Which address type is used to send electronic mail?", "IP address", "Email address", "MAC address", "URL", "b"),
    ("Internet Skills", "An email asking you to click a link and enter your password is most likely…", "A newsletter", "Phishing", "A backup", "Two-factor authentication", "b"),
    # Office Productivity (2)
    ("Office Productivity", "=SUM(B1:B10) in a spreadsheet does what?", "Counts cells", "Adds the values in B1 to B10", "Deletes the range", "Sorts the data", "b"),
    ("Office Productivity", "Which file format is best to send a CV?", "Open scratch file", "PDF", "Screenshot image", "Voice note", "b"),
    # Programming (3)
    ("Programming", "In Python, which line stores a value in a variable?", "print(x)", "x = 10", "if x:", "import x", "b"),
    ("Programming", "What does a for loop do?", "Repeats code for each item in a sequence", "Deletes a file", "Sends an email", "Formats a hard drive", "a"),
    ("Programming", "Which of these is a Python data type?", "integer", "html", "tcp", "pixel", "a"),
    # Networking (2)
    ("Networking", "Which port is used by HTTPS?", "80", "21", "443", "22", "c"),
    ("Networking", "What is an IP address?", "A password", "A device's network address", "An email", "A file extension", "b"),
    # Cloud (2)
    ("Cloud", "Which AWS service is used for object storage?", "EC2", "S3", "IAM", "SNS", "b"),
    ("Cloud", "Cloud computing means…", "Storing files on paper", "Using someone else's computers on demand and paying for what you use", "Only gaming online", "Printing documents remotely", "b"),
]

# Sample South African opportunities (illustrative listings — verify details officially)
OPPORTUNITIES = [
    {
        "title": "AWS re/Start Programme",
        "organisation": "AWS re/Start (via training partners)",
        "opportunity_type": "Certification",
        "location": "Multiple provinces, South Africa",
        "closing_date": "Rolling intakes",
        "description": "Free cloud skills training for unemployed/underemployed learners, ending with resume preparation and interview support.",
        "requirements": "No prior cloud experience required; willingness to commit to the full programme.",
        "url": "https://aws.amazon.com/training/restart/",
    },
    {
        "title": "AWS Cloud Practitioner Essentials",
        "organisation": "Amazon Web Services",
        "opportunity_type": "Certification",
        "location": "Online, South Africa",
        "closing_date": "Always open",
        "description": "Free self-paced course covering cloud concepts, core AWS services, security and pricing.",
        "requirements": "Internet access (low bandwidth mode available).",
        "url": "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials",
    },
    {
        "title": "YES Programme — Technology Stream",
        "organisation": "Youth Employment Service (YES)",
        "opportunity_type": "YES",
        "location": "South Africa",
        "closing_date": "Check YES site for current cycles",
        "description": "Work experience placements for young South Africans in participating companies, including tech roles.",
        "requirements": "SA citizen, 18–35, unemployed and not currently studying full-time.",
        "url": "https://yes.co.za",
    },
    {
        "title": "IT Support / Helpdesk Learnerships",
        "organisation": "Various SETA-accredited providers",
        "opportunity_type": "Learnership",
        "location": "Gauteng, Western Cape, KwaZulu-Natal",
        "closing_date": "Rolling",
        "description": "Structured learnerships combining classroom theory with workplace experience in end-user computing and IT support.",
        "requirements": "Matric recommended; computer basics helpful but often taught from scratch.",
        "url": None,
    },
    {
        "title": "Junior Helpdesk Technician",
        "organisation": "Example SA MSP (sample listing)",
        "opportunity_type": "Job",
        "location": "Johannesburg, Gauteng",
        "closing_date": "Open until filled",
        "description": "Log, triage and resolve first-line IT support tickets: accounts, email, hardware and basic networking.",
        "requirements": "N+ / IT support certificate or equivalent portfolio; customer service attitude.",
        "url": None,
    },
    {
        "title": "Digital Marketing Internship",
        "organisation": "Example agency (sample listing)",
        "opportunity_type": "Internship",
        "location": "Cape Town / Remote",
        "closing_date": "Open until filled",
        "description": "Assist with social media content, basic analytics and email campaigns for local businesses.",
        "requirements": "Basic digital literacy; any EduBridge pathway helps demonstrate initiative.",
        "url": None,
    },
    {
        "title": "Google Career Certificates (IT Support)",
        "organisation": "Google / Coursera",
        "opportunity_type": "Certification",
        "location": "Online, South Africa",
        "closing_date": "Always open (financial aid available)",
        "description": "Industry-recognised IT support certificate with flexible online study; financial aid applications available.",
        "requirements": "English proficiency; device to study on.",
        "url": "https://grow.google/certificates/",
    },
]


def seed():
    db = SessionLocal()
    try:
        # --- Courses / modules / lessons / quizzes ---
        if not db.scalar(select(Course).limit(1)):
            course_map: dict[str, Course] = {}
            for c in COURSES:
                course = Course(
                    title=c["title"],
                    description=c["description"],
                    category=c["category"],
                    difficulty=c["difficulty"],
                )
                db.add(course)
                db.flush()
                course_map[c["title"]] = course
                for mi, m in enumerate(c["modules"], start=1):
                    module = Module(
                        course_id=course.id,
                        title=m["title"],
                        description=m["description"],
                        order_number=mi,
                    )
                    db.add(module)
                    db.flush()
                    for li, l in enumerate(m["lessons"], start=1):
                        lesson = Lesson(
                            module_id=module.id,
                            title=l["title"],
                            content=l["content"],
                            order_number=li,
                        )
                        db.add(lesson)
                        db.flush()
                        for q in l["quiz"]:
                            db.add(
                                QuizQuestion(
                                    lesson_id=lesson.id,
                                    question=q[0],
                                    option_a=q[1],
                                    option_b=q[2],
                                    option_c=q[3],
                                    option_d=q[4],
                                    correct_answer=q[5],
                                )
                            )
            db.commit()

        # --- Pathways ---
        if not db.scalar(select(Pathway).limit(1)):
            course_map = {
                c.title: c for c in db.scalars(select(Course)).all()
            }
            for p in PATHWAYS:
                pathway = Pathway(
                    title=p["title"],
                    description=p["description"],
                    role_title=p["role_title"],
                )
                db.add(pathway)
                db.flush()
                for i, level_title in enumerate(p["levels"], start=1):
                    course = course_map.get(level_title)
                    db.add(
                        PathwayLevel(
                            pathway_id=pathway.id,
                            order_number=i,
                            title=f"LEVEL {i}: {level_title}",
                            course_id=course.id if course else None,
                        )
                    )
            db.commit()

        # --- Assessment questions ---
        if not db.scalar(select(AssessmentQuestion).limit(1)):
            for cat, q, a, b, c, d, ans in ASSESSMENT_QUESTIONS:
                db.add(
                    AssessmentQuestion(
                        category=cat,
                        question=q,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=ans,
                    )
                )
            db.commit()

        # --- Opportunities ---
        if not db.scalar(select(JobOpportunity).limit(1)):
            for o in OPPORTUNITIES:
                db.add(JobOpportunity(**o))
            db.commit()

        # --- Admin user ---
        if not db.scalar(select(User).where(User.email == "admin@edubridge.co.za")):
            db.add(
                User(
                    name="EduBridge Admin",
                    email="admin@edubridge.co.za",
                    password_hash=hash_password("Admin123!"),
                    role="admin",
                    location="Johannesburg",
                )
            )
            db.commit()

        print(
            f"Seed complete: {len(COURSES)} courses, {len(PATHWAYS)} pathways, "
            f"{len(ASSESSMENT_QUESTIONS)} assessment questions, {len(OPPORTUNITIES)} opportunities."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
