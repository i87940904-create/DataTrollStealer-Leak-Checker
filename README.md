# 🔐 DataTrollStealer Leak Checker
أداة فحص شاملة لكشف تسريبات بيانات **DataTrollStealerLogs**

## ℹ️ حول الأداة
أداة آمنة وسهلة الاستخدام للتحقق من:
- ✅ تسريب البريد الإلكتروني
- ✅ تسريب كلمات المرور
- ✅ فحص البيانات الشخصية
- ✅ الحصول على تقارير مفصلة
- ✅ تنبيهات الأمان

## 🌍 المصادر الموثوقة
- [Have I Been Pwned](https://haveibeenpwned.com/)
- [Mozilla Monitor](https://monitor.mozilla.org/)
- [PersProtect](https://persprotect.com/)
- [GitHub Info Stealers Stats](https://github.com/infostealers-stats/data-breach)

## 🚀 البدء السريع

### المتطلبات
- Python 3.8+
- pip

### التثبيت
```bash
git clone https://github.com/i87940904-create/DataTrollStealer-Leak-Checker.git
cd DataTrollStealer-Leak-Checker
pip install -r requirements.txt
```

### الاستخدام

#### 1. فحص البريد الإلكتروني
```bash
python main.py --email your@email.com
```

#### 2. فحص كلمة مرور
```bash
python main.py --password "your_password"
```

#### 3. فحص متقدم (شامل)
```bash
python main.py --email your@email.com --full-scan
```

#### 4. تصدير التقرير
```bash
python main.py --email your@email.com --export json
```

## 📋 الخيارات المتاحة
```
--email EMAIL              البريد الإلكتروني للفحص
--password PASSWORD        كلمة المرور للفحص
--full-scan               فحص شامل متقدم
--export FORMAT           تصدير التقرير (json/csv/html)
--verbose                 عرض تفاصيل كاملة
--check-monitoring        فحص خدمات المراقبة
--timeout SECONDS         وقت انتظار الاتصال
```

## 📊 أمثلة الاستخدام

### مثال 1: فحص بسيط
```bash
python main.py --email user@example.com
```

### مثال 2: فحص مع تقرير JSON
```bash
python main.py --email user@example.com --export json
```

### مثال 3: فحص شامل مع التفاصيل
```bash
python main.py --email user@example.com --full-scan --verbose
```

### مثال 4: فحص كلمة المرور
```bash
python main.py --password "mypassword123"
```

## 🔒 الأمان والخصوصية
- ❌ لا يتم حفظ البيانات الشخصية
- ❌ لا يتم إرسال البيانات الحساسة إلى خوادم خارجية
- ✅ جميع العمليات محلية وآمنة
- ✅ استخدام HTTPS فقط للاتصالات
- ✅ لا يتم تسجيل المعلومات الحساسة

## 📈 المميزات
- 🔍 فحص دقيق من مصادر موثوقة
- 📱 واجهة سهلة الاستخدام
- 📊 تقارير تفصيلية
- 🔔 تنبيهات فورية
- 💾 تصدير متعدد الصيغ
- 🌐 دعم اللغة العربية
- ⚡ سرعة فحص عالية

## 🛠️ الدعم والمساهمة
- 📝 الإبلاغ عن المشاكل: [Issues](https://github.com/i87940904-create/DataTrollStealer-Leak-Checker/issues)
- 🤝 المساهمة: [Pull Requests](https://github.com/i87940904-create/DataTrollStealer-Leak-Checker/pulls)
- 💬 النقاشات: [Discussions](https://github.com/i87940904-create/DataTrollStealer-Leak-Checker/discussions)

## 📜 الترخيص
هذا المشروع مرخص تحت [MIT License](LICENSE)

## ⚠️ إخلاء المسؤولية
هذه الأداة للأغراض التعليمية والأمان الشخصي فقط. استخدمها بمسؤولية وفقاً للقوانين المحلية.

---

**تم التطوير بـ ❤️ من قبل المجتمع**
