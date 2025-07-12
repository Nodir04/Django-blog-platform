@echo off
echo 🚀 Setting up Mini Medium Blog Platform...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv blog_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call blog_env\Scripts\activate

REM Install requirements
echo 📋 Installing dependencies...
pip install -r requirements.txt

REM Create database
echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
set /p create_superuser="👤 Create superuser? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo 🎨 Collecting static files...
python manage.py collectstatic --noinput

echo ✅ Setup complete!
echo.
echo 🎯 To start the development server:
echo    blog_env\Scripts\activate
echo    python manage.py runserver
echo.
echo 📝 Your blog will be available at: http://127.0.0.1:8000/
echo 🔐 Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Happy blogging! 🎉
pause