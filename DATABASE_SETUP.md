# 🔐 Database Setup Guide

## ⚠️ المشكلة الحالية

عند النشر على Streamlit Cloud:
- ❌ البيانات في CSV تُحذف عند إعادة التشغيل
- ❌ جميع المستخدمين يرون نفس البيانات
- ❌ لا يوجد backup آمن

## ✅ الحل: PostgreSQL Database

### مميزات الحل:
- ✅ **البيانات دائمة**: لا تُحذف أبداً
- ✅ **آمنة**: مشفرة ومحمية
- ✅ **سريعة**: أداء أفضل من CSV
- ✅ **مجانية**: باستخدام Neon.tech
- ✅ **فصل المستخدمين**: كل user له بياناته

---

## 🚀 خطوات الإعداد

### 1️⃣ إنشاء Database مجانية على Neon

#### أ) اذهب إلى: https://neon.tech

#### ب) سجل حساب جديد (مجاني)

#### ج) أنشئ Project جديد:
- اضغط **"New Project"**
- اسم Project: `Finance_PRO`
- Region: اختر الأقرب لك
- PostgreSQL Version: 15 أو أحدث

#### د) احصل على Connection String:
```
postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

---

### 2️⃣ إعداد Streamlit Cloud

#### أ) اذهب إلى: https://share.streamlit.io

#### ب) افتح تطبيقك

#### ج) اذهب إلى Settings → Secrets

#### د) أضف هذا الكود (مع استبدال الرابط):
```toml
[database]
url = "postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"
```

#### ه) احفظ واضغط **Reboot**

---

### 3️⃣ تهيئة Database (مرة واحدة)

بعد إعادة تشغيل التطبيق:

1. افتح التطبيق على Streamlit Cloud
2. سجل دخول بالحساب العادي
3. Database ستُنشأ تلقائياً!

أو يمكنك تشغيل:
```bash
python setup_database.py
```

---

### 4️⃣ للتطوير المحلي (اختياري)

#### أ) أنشئ ملف `.streamlit/secrets.toml`:
```toml
[database]
url = "postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"
```

#### ب) شغل التطبيق:
```bash
streamlit run app.py
```

---

## 🔍 التحقق من الاتصال

### في التطبيق:
- لو Database متصلة: `🔒 Database: Connected (Secure)` في Sidebar
- لو مش متصلة: `📁 Database: CSV Mode (Local)` في Sidebar

### في Terminal:
```bash
python setup_database.py
```

يجب أن ترى:
```
✅ Database initialized successfully!
```

---

## 📊 هيكل Database

### جدول `users`:
```sql
id          SERIAL PRIMARY KEY
username    VARCHAR(50) UNIQUE
password    VARCHAR(255)
created_at  TIMESTAMP
```

### جدول `transactions`:
```sql
id          SERIAL PRIMARY KEY
user_id     INTEGER (foreign key)
date        DATE
type        VARCHAR(50)
category    VARCHAR(100)
source      VARCHAR(100)
amount      DECIMAL(15, 2)
description TEXT
created_at  TIMESTAMP
```

---

## 🔐 الأمان

### ✅ ما يتم حمايته:
- رابط Database مخفي في Secrets
- كل user له بياناته الخاصة
- الاتصال مشفر (SSL)
- لا يمكن الوصول للبيانات بدون Login

### ⚠️ ملاحظات:
- **لا ترفع** ملف `secrets.toml` على GitHub
- **غير** كلمة السر الافتراضية (saleh109)
- استخدم **Environment Variables** في Production

---

## 🔄 الترحيل من CSV إلى Database

التطبيق يدعم الاثنين تلقائياً:
- لو Database موجودة → يستخدمها
- لو Database مش موجودة → يستخدم CSV

### لنقل البيانات من CSV:
```python
# في terminal
python
>>> from logic.data_loader import load_data
>>> from logic.database import save_transaction_to_db
>>> import pandas as pd
>>> 
>>> # Load from CSV
>>> df = pd.read_csv('data/transactions.csv')
>>> 
>>> # Save to database
>>> for _, row in df.iterrows():
>>>     save_transaction_to_db(
>>>         user_id=1,
>>>         date=row['Date'],
>>>         type_=row['Type'],
>>>         category=row['Category'],
>>>         source=row['Source'],
>>>         amount=row['Amount'],
>>>         description=row.get('Description', '')
>>>     )
```

---

## 🆓 حدود الخطة المجانية (Neon)

- ✅ **Storage**: 512 MB
- ✅ **Compute**: 300 ساعة/شهر
- ✅ **Projects**: 3 مشاريع
- ✅ **Branches**: غير محدود

**كافي لـ:** آلاف المعاملات! 💪

---

## 🌐 بدائل Neon (مجانية أيضاً)

1. **Supabase** (https://supabase.com)
   - 500 MB مجاناً
   - واجهة سهلة

2. **Railway** (https://railway.app)
   - $5 مجاناً شهرياً
   - سهل الربط

3. **ElephantSQL** (https://elephantsql.com)
   - 20 MB مجاناً
   - مناسب للبدء

---

## ❓ حل المشاكل

### مشكلة: لا يتصل بـ Database
```
✅ تحقق من صحة Connection String
✅ تأكد من وضعها في Secrets بشكل صحيح
✅ تأكد من إضافة ?sslmode=require في النهاية
```

### مشكلة: خطأ في Authentication
```
✅ تحقق من username و password في Neon
✅ جرب نسخ Connection String مرة أخرى
```

### مشكلة: البيانات لا تُحفظ
```
✅ تحقق من Sidebar: يجب أن تقول "Connected"
✅ شغل setup_database.py للتأكد من الجداول
```

---

## 📞 الدعم

للمساعدة:
1. تحقق من logs في Streamlit Cloud
2. شغل `setup_database.py` للتشخيص
3. راجع Neon Dashboard للـ Connection Details

---

**الآن بياناتك آمنة ودائمة!** 🎉
