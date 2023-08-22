# Bot-FloweShop

## Setup

### 1. Install requirements

```bash
pip install -r requirements.txt
```
### 2. Run the migration to configure the SQLite database:

```bash
python3 manage.py migrate
```

### 3. Create a superuser to gain access to the admin panel:

```bash
python3 manage.py createsuperuser
```

### 4. Starts the admin panel:

```bash
python3 manage.py runserver
```
The address of the admin panel: http://127.0.0.1:8000/admin/

### 5. Create .env and add token:
TELEGRAM_TOKEN=...


### 6. Start Bot
```bash
python3 bot.py
```

You will find bot at t.me/flower_shop_dvmn_bot

