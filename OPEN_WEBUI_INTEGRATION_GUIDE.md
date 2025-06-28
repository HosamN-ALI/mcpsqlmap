# دليل ربط خادم MCP مع Open WebUI

## 📋 معلومات الاتصال

**Open WebUI Admin Panel:**
- **الرابط:** http://172.245.232.168:3000/admin/settings/general
- **البريد الإلكتروني:** deepgaza@hotmail.com
- **كلمة المرور:** 123Zaq!@#

**خادم MCP:**
- **الرابط المحلي:** http://0.0.0.0:8000
- **الرابط العام:** http://a36599630488ccf5d3.blackbx.ai

## 🔧 خطوات الربط

### الخطوة 1: الدخول إلى Open WebUI Admin Panel

1. افتح المتصفح واذهب إلى: http://172.245.232.168:3000/admin/settings/general
2. قم بتسجيل الدخول باستخدام:
   - البريد الإلكتروني: `deepgaza@hotmail.com`
   - كلمة المرور: `123Zaq!@#`

### الخطوة 2: إعداد External API في Open WebUI

1. في لوحة الإدارة، اذهب إلى **Settings** > **External**
2. أضف API جديد مع التفاصيل التالية:

```json
{
  "name": "MCP SQLMap Server",
  "base_url": "http://a36599630488ccf5d3.blackbx.ai",
  "api_key": "sk-1bd5de3f31db429cb8cbe73875537c5c",
  "model": "mcp-sqlmap",
  "enabled": true
}
```

### الخطوة 3: إعداد Model في Open WebUI

1. اذهب إلى **Settings** > **Models**
2. أضف نموذج جديد:

```json
{
  "id": "mcp-sqlmap",
  "name": "MCP SQLMap Security Scanner",
  "owned_by": "mcp-server",
  "object": "model",
  "created": 1640995200,
  "permission": [],
  "root": "mcp-sqlmap",
  "parent": null
}
```

### الخطوة 4: إعداد Functions في Open WebUI

أضف الوظائف التالية في **Settings** > **Functions**:

#### وظيفة فحص SQL Injection
```json
{
  "name": "sql_injection_scan",
  "description": "Scan for SQL injection vulnerabilities",
  "parameters": {
    "type": "object",
    "properties": {
      "target_url": {
        "type": "string",
        "description": "Target URL to scan"
      },
      "options": {
        "type": "object",
        "description": "Scan options"
      }
    },
    "required": ["target_url"]
  },
  "endpoint": "http://a36599630488ccf5d3.blackbx.ai/api/v1/scan"
}
```

#### وظيفة تحليل Payload
```json
{
  "name": "analyze_payload",
  "description": "Analyze SQL injection payload",
  "parameters": {
    "type": "object",
    "properties": {
      "payload": {
        "type": "string",
        "description": "SQL injection payload to analyze"
      }
    },
    "required": ["payload"]
  },
  "endpoint": "http://a36599630488ccf5d3.blackbx.ai/api/v1/analyze"
}
```

#### وظيفة WAF Bypass
```json
{
  "name": "waf_bypass",
  "description": "Generate WAF bypass techniques",
  "parameters": {
    "type": "object",
    "properties": {
      "payload": {
        "type": "string",
        "description": "Original payload"
      },
      "techniques": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Bypass techniques to apply"
      }
    },
    "required": ["payload"]
  },
  "endpoint": "http://a36599630488ccf5d3.blackbx.ai/api/v1/bypass"
}
```

## 🔗 إعداد Webhook للتحديثات التلقائية

### في Open WebUI:
1. اذهب إلى **Settings** > **Webhooks**
2. أضف webhook جديد:

```json
{
  "name": "MCP Server Updates",
  "url": "http://172.245.232.168:3000/api/webhooks/mcp-updates",
  "events": ["scan_complete", "vulnerability_found", "analysis_complete"],
  "headers": {
    "Authorization": "Bearer YOUR_WEBHOOK_TOKEN",
    "Content-Type": "application/json"
  }
}
```

## 📡 نقاط النهاية المتاحة

### نقاط نهاية خادم MCP:

| النقطة | الطريقة | الوصف |
|--------|---------|--------|
| `/` | GET | معلومات الخادم |
| `/status` | GET | حالة الخادم |
| `/api/v1/health` | GET | فحص الصحة |
| `/api/v1/scan` | POST | بدء فحص SQL injection |
| `/api/v1/inject` | POST | تنفيذ هجوم SQL injection |
| `/api/v1/bypass` | POST | تطبيق تقنيات WAF bypass |
| `/api/v1/payloads` | GET | الحصول على payloads |
| `/api/v1/payloads/custom` | POST | إضافة payload مخصص |
| `/api/v1/analyze` | POST | تحليل البيانات |

### أمثلة على الطلبات:

#### فحص SQL Injection:
```bash
curl -X POST "http://a36599630488ccf5d3.blackbx.ai/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "http://example.com/login.php",
    "options": {
      "depth": 2,
      "threads": 5
    }
  }'
```

#### تحليل Payload:
```bash
curl -X POST "http://a36599630488ccf5d3.blackbx.ai/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "integration_type": "deepseek",
    "data": {
      "payload": "\' OR \'1\'=\'1",
      "context": "login form"
    }
  }'
```

## 🔐 إعداد المصادقة

### في ملف .env:
```env
# DeepSeek API Configuration
DEEPSEEK_API_KEY=sk-1bd5de3f31db429cb8cbe73875537c5c
DEEPSEEK_API_URL=https://api.deepseek.com/v1

# Open WebUI Configuration
OPENWEBUI_URL=http://172.245.232.168:3000
OPENWEBUI_API_KEY=your_openwebui_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
API_SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://172.245.232.168:3000,http://localhost:3000
```

## 🧪 اختبار الاتصال

### 1. اختبار خادم MCP:
```bash
# فحص حالة الخادم
curl http://a36599630488ccf5d3.blackbx.ai/status

# فحص الصحة
curl http://a36599630488ccf5d3.blackbx.ai/api/v1/health
```

### 2. اختبار Open WebUI:
```bash
# فحص الاتصال
curl -X GET "http://172.245.232.168:3000/api/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🔄 تدفق العمل المتكامل

### 1. المستخدم يطلب فحص أمني في Open WebUI
### 2. Open WebUI يرسل طلب إلى خادم MCP
### 3. خادم MCP ينفذ الفحص باستخدام SQLMap
### 4. النتائج تُحلل باستخدام DeepSeek API
### 5. التقرير النهائي يُرسل إلى Open WebUI
### 6. المستخدم يحصل على النتائج في واجهة Open WebUI

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة وحلولها:

#### 1. خطأ في الاتصال:
```bash
# تحقق من حالة الخادم
curl -I http://a36599630488ccf5d3.blackbx.ai/

# تحقق من السجلات
tail server.log
```

#### 2. خطأ في المصادقة:
- تأكد من صحة مفتاح DeepSeek API
- تحقق من إعدادات CORS
- راجع رموز الاستجابة HTTP

#### 3. مشاكل في الأداء:
- راقب استخدام الذاكرة والمعالج
- تحقق من عدد الطلبات المتزامنة
- راجع إعدادات timeout

## 📞 الدعم والمساعدة

في حالة وجود مشاكل:
1. راجع سجلات الخادم: `tail server.log`
2. تحقق من حالة الخدمات: `curl http://a36599630488ccf5d3.blackbx.ai/status`
3. راجع إعدادات Open WebUI في لوحة الإدارة
4. تأكد من صحة متغيرات البيئة في ملف `.env`

## 🎯 الخطوات التالية

بعد إكمال الربط:
1. اختبر جميع الوظائف
2. قم بإعداد مراقبة للأداء
3. أضف المزيد من نماذج الأمان
4. قم بتخصيص واجهة المستخدم حسب الحاجة
