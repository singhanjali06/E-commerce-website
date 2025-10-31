A fully functional **E-commerce website** built with **Python, Django, and XAMPP**, integrated with **Stripe payment gateway**. The project includes **customer and vendor dashboards**, shopping cart, checkout flow, and order management.

## 🚀 Features

### Customer
- ✅ User registration & login
- ✅ Browse products & search
- ✅ Add products to cart
- ✅ Checkout with Stripe
- ✅ View order history

### Vendor
- ✅ Vendor registration & login
- ✅ Add, edit, products

### General
- 🔹 Responsive design (desktop & mobile)
- 🔹 Secure password handling with Django auth
- 🔹 Stripe payment integration
- 🔹 Admin interface to manage users & products

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Backend |
| Django 4.x | Web Framework |
| SQLite3 / MySQL | Database |
| HTML5, CSS3, JS | Frontend |
| Stripe API | Payments |
| Git & GitHub | Version Control |

---

## 🎨 Screenshots

 
[Home Page]
<img width="872" height="704" alt="Screenshot 2025-10-31 121024" src="https://github.com/user-attachments/assets/9768ceb2-b073-4f7a-a68b-48b4534bb1f0" />

*Registration*
[Customer Registration]
<img width="682" height="916" alt="Screenshot 2025-10-31 121043" src="https://github.com/user-attachments/assets/370ecae2-980d-44a3-b9b7-a1f337217892" />

*login*
[login page]
<img width="798" height="735" alt="Screenshot 2025-10-31 121130" src="https://github.com/user-attachments/assets/bac08ddb-28c8-4257-b84a-fb33da6f5798" />

*Dashboard* 
[Customer Dashboard]
<img width="1834" height="909" alt="Screenshot 2025-10-31 121150" src="https://github.com/user-attachments/assets/bd810944-43b0-47f3-8ee9-e8b10e89a3f8" />

*Cart*
[Customer cart]
<img width="1335" height="550" alt="Screenshot 2025-10-31 121216" src="https://github.com/user-attachments/assets/1e305224-4bbd-4611-955b-801defdc8a96" />


## ⚡ Installation

1. Clone the repo
git clone https://github.com/singhanjali06/E-commerce-website.git
cd E-commerce-website

2. Create a virtual environment
python -m venv venv

3. Activate it
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Set up environment variables
 Create a `.env` file in the project root
# Example:
 SECRET_KEY=your_django_secret_key_here
 DEBUG=True
 STRIPE_PUBLISHABLE_KEY=pk_test_YourPublishableKeyHere
 STRIPE_SECRET_KEY=sk_test_YourSecretKeyHere

6. Apply migrations
python manage.py makemigrations
python manage.py migrate

7. Run the development server
python manage.py runserver


