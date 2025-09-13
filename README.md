Django Notes App
A Django-based web application for authenticated users to create, edit, delete, and manage notes with rich-text descriptions, file attachments, pagination, search capabilities. The app includes user authentication with JWT, a secure password reset flow, and a clean, responsive frontend using Tailwind CSS and Summernote.
Features

User Authentication:
Register, login, and logout using JSON Web Tokens (JWT).
Secure password reset via email with expiring tokens.


Note Management:
Create, edit, and delete notes with title, rich-text description (via Summernote), and optional file attachments.
Notes are user-specific and stored in a database.


Pagination:
Notes are paginated (10 notes per page) with Previous/Next controls.


Search :
Search notes by title or description.


Responsive UI:
Built with Tailwind CSS for a modern, responsive design.
Rich-text editing with Summernote for note descriptions.


Security:
JWT-based authentication with access and refresh tokens.
CSRF protection for forms and AJAX requests.
Rate limiting on password reset requests (5/minute).
Secure password requirements (8+ characters, one uppercase).


Prerequisites

Python: 3.8 or higher
Django: 4.x or compatible
Git: For cloning the repository
Virtual Environment: Recommended (e.g., venv)

Setup Instructions
1. Clone the Repository
git clone [https://github.com/beemamk/django-notes-app.git]
Replace yourusername with your GitHub username.

cd django-notes-app

3. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install Dependencies
Install required Python packages:
pip install -r requirements.txt

Common dependencies (ensure they’re in requirements.txt):
django>=4.2
djangorestframework>=3.14
djangorestframework-simplejwt>=5.3
pillow>=10.0  # For file uploads

5. Apply Migrations
Set up the database:
python manage.py makemigrations
python manage.py migrate

6. Create a Superuser (Optional)
For admin access:
python manage.py createsuperuser

Admin Panel: Access http://127.0.0.1:8000/admin/ with superuser credentials to manage users and notes.

8. Run the Development Server
python manage.py runserver

Access the app at http://127.0.0.1:8000.

Usage

Register: Go to /register/ to create an account.
Login: Use /login/ to authenticate and receive JWT tokens.
Notes Page:
Access /notes/ to view, create, edit, or delete notes.
Use search to find notes by title or description.
Navigate pages using Previous/Next buttons.


Password Reset:
Go to /forgot-password/ to request a reset link.
Check the console (development) for the link.
Follow the link to reset your password.

API Endpoints

POST /api/token/: Get access and refresh tokens (login).
POST /api/token/refresh/: Refresh access token.
POST /api/logout/: Invalidate refresh token.
GET/POST /api/notes/: List or create notes (paginated, authenticated).
GET/PUT/PATCH/DELETE /api/notes//: Retrieve, update, or delete a note.
POST /api/password-reset/request/: Request password reset link.
POST /api/password-reset/confirm///: Reset password.
