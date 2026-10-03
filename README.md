# FilePal Relay

سرور رلهٔ کوچک برای اتصال دستگاه‌های FilePal از راه دور (بدون وای‌فای مشترک).
فقط پایتون استاندارد؛ وابستگی ندارد.

## اجرا روی Railway
1. این پوشه را در یک مخزن GitHub بگذار.
2. در Railway: **New Project → Deploy from GitHub repo** و مخزن را انتخاب کن (Dockerfile خودکار شناخته می‌شود).
3. داخل سرویس: **Settings → Networking → TCP Proxy** را بزن و پورت **9000** را وارد کن.
4. Railway یک آدرس مثل `xxxx.proxy.rlwy.net:12345` می‌دهد. همین را در تنظیمات اپ FilePal (فیلد «سرور رله») روی هر دو دستگاه بنویس.

نکته: «Generate Domain» (HTTP) لازم نیست؛ این سرور TCP خام است و فقط TCP Proxy کار می‌کند.

## اجرای محلی / روی هر سرور
    python relay.py          # پورت 9000
    RELAY_PORT=7000 python relay.py
