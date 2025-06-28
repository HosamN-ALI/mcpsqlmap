# 📋 تعليمات الإعداد اليدوي - ربط MCP Server مع Open WebUI

## ✅ حالة الاتصال
- **✅ خادم MCP:** متصل ويعمل على http://a36599630488ccf5d3.blackbx.ai
- **✅ Open WebUI:** متاح على http://172.245.232.168:3000
- **✅ المصادقة:** تم تسجيل الدخول بنجاح

## 🔧 خطوات الإعداد اليدوي

### الخطوة 1: الدخول إلى Open WebUI Admin Panel

1. **افتح المتصفح** واذهب إلى:
   ```
   http://172.245.232.168:3000/admin/settings/general
   ```

2. **سجل الدخول** باستخدام:
   - **البريد الإلكتروني:** `deepgaza@hotmail.com`
   - **كلمة المرور:** `123Zaq!@#`

### الخطوة 2: إعداد External API Connection

1. في لوحة الإدارة، ابحث عن قسم **"External APIs"** أو **"Connections"**
2. أضف اتصال جديد مع المعلومات التالية:

```
Name: MCP SQLMap Server
Base URL: http://a36599630488ccf5d3.blackbx.ai
API Key: sk-1bd5de3f31db429cb8cbe73875537c5c
Type: Custom API
Enabled: ✅ Yes
```

### الخطوة 3: إعداد Custom Functions

في قسم **Functions** أو **Tools**، أضف الوظائف التالية:

#### 🔍 وظيفة فحص SQL Injection
```javascript
// Function Name: sql_injection_scan
// Description: Scan for SQL injection vulnerabilities
// Endpoint: http://a36599630488ccf5d3.blackbx.ai/api/v1/scan
// Method: POST

function sql_injection_scan(target_url, options = {}) {
    const payload = {
        target_url: target_url,
        options: options
    };
    
    return fetch('http://a36599630488ccf5d3.blackbx.ai/api/v1/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json());
}
```

#### 🧠 وظيفة تحليل Payload
```javascript
// Function Name: analyze_payload
// Description: Analyze SQL injection payload using DeepSeek AI
// Endpoint: http://a36599630488ccf5d3.blackbx.ai/api/v1/analyze
// Method: POST

function analyze_payload(payload, context = "") {
    const data = {
        integration_type: "deepseek",
        data: {
            payload: payload,
            context: context
        }
    };
    
    return fetch('http://a36599630488ccf5d3.blackbx.ai/api/v1/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json());
}
```

#### 🛡️ وظيفة WAF Bypass
```javascript
// Function Name: waf_bypass
// Description: Generate WAF bypass techniques
// Endpoint: http://a36599630488ccf5d3.blackbx.ai/api/v1/bypass
// Method: POST

function waf_bypass(payload, techniques = []) {
    const data = {
        payload: payload,
        techniques: techniques
    };
    
    return fetch('http://a36599630488ccf5d3.blackbx.ai/api/v1/bypass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json());
}
```

#### 📦 وظيفة الحصول على Payloads
```javascript
// Function Name: get_payloads
// Description: Get available SQL injection payloads
// Endpoint: http://a36599630488ccf5d3.blackbx.ai/api/v1/payloads
// Method: GET

function get_payloads(source = "", category = "") {
    let url = 'http://a36599630488ccf5d3.blackbx.ai/api/v1/payloads';
    const params = new URLSearchParams();
    
    if (source) params.append('source', source);
    if (category) params.append('category', category);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json());
}
```

### الخطوة 4: إعداد Model (إذا كان متاحاً)

في قسم **Models**، أضف:
```
Model ID: mcp-sqlmap
Model Name: MCP SQLMap Security Scanner
Provider: Custom
Base URL: http://a36599630488ccf5d3.blackbx.ai
API Key: sk-1bd5de3f31db429cb8cbe73875537c5c
```

### الخطوة 5: اختبار الاتصال

بعد الإعداد، اختبر الوظائف:

1. **اختبار فحص SQL Injection:**
   ```
   sql_injection_scan("http://example.com/login.php", {depth: 2})
   ```

2. **اختبار تحليل Payload:**
   ```
   analyze_payload("' OR '1'='1", "login form")
   ```

3. **اختبار WAF Bypass:**
   ```
   waf_bypass("SELECT * FROM users", ["whitespace", "comments"])
   ```

4. **اختبار الحصول على Payloads:**
   ```
   get_payloads("fuzzdb", "sql-injection")
   ```

## 🔗 إعداد Webhook (اختياري)

إذا كان Open WebUI يدعم webhooks، أضف:
```
Webhook URL: http://172.245.232.168:3000/api/webhooks/mcp-updates
Events: scan_complete, vulnerability_found, analysis_complete
Headers: Content-Type: application/json
```

## 🧪 اختبار شامل

### اختبار من Terminal:
```bash
# اختبار حالة الخادم
curl http://a36599630488ccf5d3.blackbx.ai/status

# اختبار فحص SQL injection
curl -X POST "http://a36599630488ccf5d3.blackbx.ai/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://example.com"}'

# اختبار تحليل payload
curl -X POST "http://a36599630488ccf5d3.blackbx.ai/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "integration_type": "deepseek",
    "data": {
      "payload": "\' OR \'1\'=\'1",
      "context": "test"
    }
  }'
```

## 📱 الاستخدام في Open WebUI

بعد إكمال الإعداد، يمكنك استخدام الوظائف في المحادثات:

### أمثلة على الاستخدام:

1. **"قم بفحص الموقع http://example.com للثغرات الأمنية"**
   - سيستخدم Open WebUI وظيفة `sql_injection_scan`

2. **"حلل هذا الـ payload: ' OR '1'='1"**
   - سيستخدم وظيفة `analyze_payload`

3. **"أنشئ تقنيات تجاوز WAF لهذا الـ payload: SELECT * FROM users"**
   - سيستخدم وظيفة `waf_bypass`

4. **"أعطني قائمة بـ payloads من مصدر fuzzdb"**
   - سيستخدم وظيفة `get_payloads`

## 🔍 استكشاف الأخطاء

### مشاكل شائعة:

1. **خطأ CORS:**
   - تأكد من إضافة `http://172.245.232.168:3000` إلى ALLOWED_ORIGINS

2. **خطأ في المصادقة:**
   - تحقق من صحة مفتاح DeepSeek API

3. **خطأ في الاتصال:**
   - تأكد من أن خادم MCP يعمل على http://a36599630488ccf5d3.blackbx.ai

### فحص السجلات:
```bash
# سجلات خادم MCP
tail server.log

# اختبار الاتصال
curl -I http://a36599630488ccf5d3.blackbx.ai/
```

## 📞 الدعم

للحصول على المساعدة:
1. راجع سجلات الخادم
2. اختبر النقاط النهائية يدوياً
3. تحقق من إعدادات Open WebUI
4. راجع ملف التكوين `openwebui_config.json`

---

## ✅ ملخص المعلومات المهمة

- **Open WebUI Admin:** http://172.245.232.168:3000/admin/settings/general
- **MCP Server:** http://a36599630488ccf5d3.blackbx.ai
- **البريد الإلكتروني:** deepgaza@hotmail.com
- **كلمة المرور:** 123Zaq!@#
- **DeepSeek API Key:** sk-1bd5de3f31db429cb8cbe73875537c5c

**🎯 الهدف:** دمج وظائف الأمان والفحص في Open WebUI لتوفير تجربة متكاملة للمستخدمين.
