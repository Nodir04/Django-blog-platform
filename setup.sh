#!/bin/bash

# Mini Medium Blog Setup Script
# This script sets up the blog platform automatically

echo "🚀 Setting up Mini Medium Blog Platform..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv blog_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source blog_env/bin/activate

# Install requirements
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Create database
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Create superuser? (y/n)"
read -r create_superuser
if [[ $create_superuser == "y" || $create_superuser == "Y" ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the development server:"
echo "   source blog_env/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📝 Your blog will be available at: http://127.0.0.1:8000/"
echo "🔐 Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "Happy blogging! 🎉"