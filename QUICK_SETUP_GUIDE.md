# 🚀 دليل الإعداد السريع - ربط MCP Server مع Open WebUI

## 📋 المعلومات الأساسية

**🔗 الروابط المهمة:**
- **Open WebUI Admin:** http://172.245.232.168:3000/admin/settings/general
- **MCP Server:** http://a36599630488ccf5d3.blackbx.ai
- **البريد الإلكتروني:** deepgaza@hotmail.com
- **كلمة المرور:** 123Zaq!@#

## ⚡ الإعداد التلقائي (الطريقة الأسرع)

```bash
# تشغيل script الإعداد التلقائي
cd /home/user/workspace
python3 setup_openwebui_integration.py
```

## 🔧 الإعداد اليدوي

### الخطوة 1: الدخول إلى Open WebUI
1. اذهب إلى: http://172.245.232.168:3000/admin/settings/general
2. سجل الدخول بـ: deepgaza@hotmail.com / 123Zaq!@#

### الخطوة 2: إضافة External API
في **Settings > External APIs** أضف:
```json
{
  "name": "MCP SQLMap Server",
  "base_url": "http://a36599630488ccf5d3.blackbx.ai",
  "api_key": "sk-1bd5de3f31db429cb8cbe73875537c5c",
  "enabled": true
}
```

### الخطوة 3: إضافة Functions
في **Settings > Functions** أضف الوظائف من ملف `openwebui_config.json`

## 🧪 اختبار الاتصال

```bash
# اختبار خادم MCP
curl http://a36599630488ccf5d3.blackbx.ai/status

# اختبار فحص SQL injection
curl -X POST "http://a36599630488ccf5d3.blackbx.ai/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://example.com"}'
```

## 📱 الاستخدام في Open WebUI

بعد الإعداد، يمكنك استخدام الأوامر التالية في Open WebUI:

1. **فحص SQL Injection:**
   ```
   @sql_injection_scan target_url="http://example.com/login.php"
   ```

2. **تحليل Payload:**
   ```
   @analyze_payload payload="' OR '1'='1"
   ```

3. **WAF Bypass:**
   ```
   @waf_bypass payload="SELECT * FROM users" techniques=["whitespace", "comments"]
   ```

4. **الحصول على Payloads:**
   ```
   @get_payloads source="fuzzdb" category="sql-injection"
   ```

## 🔍 استكشاف الأخطاء

### مشكلة في الاتصال:
```bash
# تحقق من حالة الخادم
curl -I http://a36599630488ccf5d3.blackbx.ai/

# راجع السجلات
tail server.log
```

### مشكلة في المصادقة:
- تأكد من صحة مفتاح DeepSeek API
- راجع إعدادات CORS في Open WebUI

## 📞 الدعم

للمساعدة:
1. راجع الملف الكامل: `OPEN_WEBUI_INTEGRATION_GUIDE.md`
2. استخدم script الإعداد: `setup_openwebui_integration.py`
3. راجع ملف التكوين: `openwebui_config.json`

---
✅ **الخادم جاهز ويعمل على:** http://a36599630488ccf5d3.blackbx.ai
