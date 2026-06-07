# -*- coding: utf-8 -*-
# سيناريوهات المختبر الحي

LAB_SCENARIOS = [
    {
        "id": "web_basic",
        "name": "اختراق موقع ويب أساسي",
        "desc": "سيناريو بسيط: موقع ويب به ثغرة SQL Injection. حاول استخراج بيانات المستخدمين.",
        "difficulty": "مبتدئ",
        "duration": "15 دقيقة",
        "target": "http://testphp.vulnweb.com",
        "steps": [
            "1. افحص الموقع باستخدام Nmap",
            "2. ابحث عن صفحات ديناميكية (بها بارامترات)",
            "3. جرب حمولة SQLi: ' OR '1'='1",
            "4. استخدم SQLMap للاستخراج التلقائي",
            "5. وثّق النتائج"
        ],
        "tools_needed": ["nmap", "sqli_tester", "sqlmap"],
        "flag": "FLAG{sql_injection_master}",
        "hints": [
            "ابحث عن صفحة بها ?id= أو ?cat=",
            "جرب إضافة فاصلة واحدة ' في نهاية الرابط",
            "إذا ظهر خطأ SQL، فأنت على الطريق الصحيح"
        ]
    },
    {
        "id": "smb_exploit",
        "name": "استغلال ثغرة EternalBlue",
        "desc": "هدف ويندوز قديم معرض لـ EternalBlue. حاول الوصول إلى النظام.",
        "difficulty": "متوسط",
        "duration": "30 دقيقة",
        "target": "192.168.1.50",
        "steps": [
            "1. افحص المنافذ المفتوحة",
            "2. تأكد من وجود المنفذ 445 (SMB)",
            "3. استخدم وحدة ms17_010_scanner للتأكد من الثغرة",
            "4. استخدم EternalBlue exploit",
            "5. احصل على جلسة Meterpreter",
            "6. استخرج الهاشات باستخدام hashdump"
        ],
        "tools_needed": ["nmap", "smb_version", "eternal_blue", "hashdump"],
        "flag": "FLAG{eternal_not_so_eternal}",
        "hints": [
            "nmap -p 445 <target>",
            "use auxiliary/scanner/smb/smb_ms17_010",
            "تأكد من ضبط LHOST على عنوان IP الخاص بك"
        ]
    },
    {
        "id": "password_attack",
        "name": "هجوم تخمين كلمات المرور",
        "desc": "خادم SSH بكلمة مرور ضعيفة. حاول تخمين كلمة المرور والدخول.",
        "difficulty": "مبتدئ",
        "duration": "20 دقيقة",
        "target": "192.168.1.100",
        "steps": [
            "1. تأكد من أن المنفذ 22 مفتوح",
            "2. جهز قائمة كلمات مرور (rockyou.txt)",
            "3. استخدم Hydra لتخمين كلمة المرور",
            "4. سجل الدخول باستخدام SSH",
            "5. ارفع تقرير بالثغرة"
        ],
        "tools_needed": ["nmap", "hydra"],
        "flag": "FLAG{weak_password_found}",
        "hints": [
            "جرب المستخدم root أو admin",
            "استخدم rockyou.txt كقائمة كلمات مرور",
            "hydra -l root -P rockyou.txt ssh://<target>"
        ]
    },
    {
        "id": "web_full_scan",
        "name": "فحص أمني شامل لموقع ويب",
        "desc": "موقع ويب يحتاج فحصاً أمنياً كاملاً. اكتشف كل الثغرات.",
        "difficulty": "متوسط",
        "duration": "45 دقيقة",
        "target": "http://testphp.vulnweb.com",
        "steps": [
            "1. فحص المنافذ والخدمات",
            "2. فحص المسارات المخفية",
            "3. فحص ثغرات XSS",
            "4. فحص ثغرات SQL Injection",
            "5. فحص رؤوس الأمان",
            "6. فحص SSL/TLS",
            "7. كتابة تقرير شامل"
        ],
        "tools_needed": ["nmap", "dirb", "xss_scanner", "sqli_tester", "security_headers", "ssl_scanner"],
        "flag": "FLAG{full_security_audit}",
        "hints": [
            "ابدأ بفحص nmap الشامل",
            "استخدم dirb للعثور على المسارات المخفية",
            "جرب حمولات XSS في أي حقل بحث"
        ]
    },
    {
        "id": "osint_challenge",
        "name": "تحدي جمع المعلومات",
        "desc": "اجمع أكبر قدر من المعلومات عن هدف معين باستخدام أدوات OSINT.",
        "difficulty": "مبتدئ",
        "duration": "15 دقيقة",
        "target": "tesla.com",
        "steps": [
            "1. استخدم theHarvester لجمع الإيميلات",
            "2. استخدم Sherlock للبحث عن اسم المستخدم",
            "3. استخدم WHOIS للحصول على معلومات النطاق",
            "4. استخدم Subfinder لاكتشاف النطاقات الفرعية",
            "5. وثّق كل المعلومات في تقرير"
        ],
        "tools_needed": ["theharvester", "sherlock", "whois", "subfinder"],
        "flag": "FLAG{osint_master}",
        "hints": [
            "theHarvester -d tesla.com -b google",
            "sherlock elonmusk",
            "subfinder -d tesla.com"
        ]
    },
]
