# django-ecommerce

A practice Django e-commerce project:  
- 100 sample products  
- Add to cart / remove from cart  
- Checkout (no payment)  
- View previous orders  
- Cart is session‑based  
- Orders & products persisted to DB  

---

## Requirements

- Python 3.x  
- pip  
- (Optional but recommended) virtual environment  
- SQLite (default)  
- Django  

---

## Setup Instructions

1. Clone the repo  
```
git clone https://github.com/ashleighedwards/django-ecommerce.git
cd django-ecommerce
```

2. (Optional) Create & activate a virtual environment  
```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install django
pip install stripe

python manage.py makemigrations
python manage.py migrate

python populate_100.py

python manage.py runserver

navigate to
http://127.0.0.1:8000/


```

