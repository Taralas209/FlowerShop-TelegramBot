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

### 3. Load Flowers-Data into your database

```bash
python manage.py loaddata flowers.json```

### 4. Create a superuser to gain access to the admin panel:

```bash
python3 manage.py createsuperuser
```

### 5. Starts the admin panel:

```bash
python3 manage.py runserver
```
The address of the admin panel: http://127.0.0.1:8000/admin/

### 6. Create .env and add token:
TELEGRAM_TOKEN=...


### 7. Start Bot
```bash
python3 bot.py
```

