# VDAcademy - Backend API

VDAcademy is a Learning Management System (LMS) backend built with **Django** and **Django REST Framework**. It handles the core logic for managing online courses, user enrollments, and structured educational content.

## 🛠 Features
- **Course Hierarchy:** Manage Categories, Courses, Modules, and Lessons.
- **Role-based Access:** Different permissions for Teachers (Instructors) and Students.
- **Secure Auth:** JWT-based authentication for mobile and web clients.
- **PostgreSQL Ready:** Optimized for relational data and complex queries.

## 🚀 Quick Start

1. **Clone & Virtualenv:**
   ```bash
   git clone https://github.com/naazriin/vdacademy.git
   cd vdacademy
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

2. Install:
pip install -r requirements.txt

3. Database:
Create a .env file based on the environment needs.
python manage.py migrate
python manage.py createsuperuser

4. Run:
   python manage.py runserver

🏗 Project Structure
courses/: Core models for educational content.

users/: Custom user models and authentication logic.

api/: API routing and serializers.
