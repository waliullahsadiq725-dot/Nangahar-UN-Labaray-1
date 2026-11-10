# NUDL — Backend Stage 2

دا پړاو د پخواني Frontend د بیا جوړولو پر ځای د FastAPI/PostgreSQL بنسټ برابروي. په دې کاري چاپېریال کې د پخواني Stage 1 فولډر موجود نه و؛ نو Backend په همدې واحد اصلي فولډر کې تنظیم شوی؛ د app او migrations اړین فرعي فولډرونه ساتل شوي دي.

## اړتیاوې
- Python 3.11 یا 3.12
- PostgreSQL 16 (یا Docker Desktop)
- Git اختیاري

## محلي نصب (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
په `.env` کې `SECRET_KEY` د اوږدې تصادفي پټې کلیمې په وسیله بدل کړئ. د `DATABASE_URL` ارزښت د خپل PostgreSQL سره برابر کړئ.

د PostgreSQL ډیټابېس او کارن باید مخکې جوړ وي؛ د Docker طریقه لاندې اسانه ده.

## Docker طریقه
د پروژې په اصلي فولډر کې:
```powershell
Copy-Item .env.example .env
```
په `.env` کې SECRET_KEY بدل کړئ، بیا:
```powershell
docker compose up --build -d
docker compose exec api alembic -c /srv/nudl/alembic.ini upgrade head
```
یادونه: د Dockerfile کاري مسیر `/srv/nudl` دی؛ د migrations اجرا لپاره د API کانتینر کې همدا مسیر کارول کېږي.

## محلي اجرا
```powershell
alembic upgrade head
uvicorn app.main:app --reload
```
API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`
Health check: `http://127.0.0.1:8000/health`

## API لارې
- `POST /api/v1/auth/register` — د محصل یا استاد ثبت؛ نوی حساب `pending` وي.
- `POST /api/v1/auth/login` — فعال حساب ته JWT ورکوي.
- `GET /api/v1/auth/me` — د ننوتلي کاروونکي پروفایل.
- `GET /api/v1/admin/pending-users` — د Admin لپاره د تایید په تمه حسابونه.
- `PATCH /api/v1/admin/users/{id}/activate` — حساب فعالول.
- `PATCH /api/v1/admin/users/{id}/suspend` — حساب ځنډول.

## د Admin حساب
په عامه Registration API کې د Admin رول قصداً بند دی. د لومړي Admin حساب باید د خوندي، یوځلي bootstrap script له لارې جوړ شي؛ دا به د بل پړاو کار وي. تر هغې د Admin endpoints کارول ممکن نه دي.

## امنیت او د پړاو حدود
- د پاسورډ Hash د Argon2 له لارې.
- JWT لاسلیک او د فعال حساب کتنه.
- د رولونو صلاحیتونه په Backend کې ارزول کېږي.
- د محصل/استاد حسابونه د Admin تر تایید مخکې login نه شي کولای.
- CORS د `.env` له لارې محدودېږي.
- دا پړاو لا PDF upload/view/download، د فایل سکین، ایمیل تایید، password reset، rate limiting، audit log او د Admin bootstrap نه لري؛ په راتلونکو پړاوونو کې به ورزیاتېږي.
- د انټرنېټ عامه خپرول تر HTTPS، قوي secrets، backups، firewall، storage او production configuration مخکې مه کوئ.
