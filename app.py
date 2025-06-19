from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airport.db'

# Настройка Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'genuvseznayt@gmail.com'  # Ваш email
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Пароль приложения Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'genuvseznayt@gmail.com'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    terminal = db.Column(db.String(1), nullable=False, default='A')
    aircraft_type = db.Column(db.String(50), nullable=True)
    check_in_counter = db.Column(db.String(10), nullable=True)
    check_in_time = db.Column(db.DateTime, nullable=True)
    boarding_time = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_flights_schedule():
    # Пример расписания на основе фото (можно расширить)
    schedule = [
        {
            'flight_number': 'FV6828', 'airline': 'Россия', 'destination': 'Москва (Шереметьево)',
            'departure_weekdays': [1, 3, 5], 'departure_time': '19:10', 'arrival_time': '21:00', 'terminal': 'A', 'aircraft_type': 'SSJ-100'
        },
        {
            'flight_number': 'A4540', 'airline': 'Азимут', 'destination': 'Сочи',
            'departure_weekdays': [2, 6], 'departure_time': '15:00', 'arrival_time': '17:30', 'terminal': 'A', 'aircraft_type': 'SSJ-100'
        },
        {
            'flight_number': 'WZ2454', 'airline': 'Ред Вингс', 'destination': 'Санкт-Петербург',
            'departure_weekdays': [4], 'departure_time': '18:55', 'arrival_time': '21:15', 'terminal': 'A', 'aircraft_type': 'SSJ-100'
        },
        {
            'flight_number': 'Ю9687', 'airline': 'ЮВТ-Аэро', 'destination': 'Казань',
            'departure_weekdays': [5], 'departure_time': '15:50', 'arrival_time': '17:00', 'terminal': 'A', 'aircraft_type': 'CRJ-200'
        },
        # ... добавьте остальные рейсы по фото ...
    ]
    
    flights = []
    today = datetime.now().date()
    end_date = today + timedelta(days=90)
    for s in schedule:
        for day in range((end_date - today).days + 1):
            date = today + timedelta(days=day)
            if date.isoweekday() in s['departure_weekdays']:
                dep_time = datetime.strptime(f"{date} {s['departure_time']}", "%Y-%m-%d %H:%M")
                arr_time = datetime.strptime(f"{date} {s['arrival_time']}", "%Y-%m-%d %H:%M")
                flights.append(Flight(
                    flight_number=s['flight_number'],
                    airline=s['airline'],
                    destination=s['destination'],
                    departure_time=dep_time,
                    arrival_time=arr_time,
                    status='По расписанию',
                    terminal=s['terminal'],
                    aircraft_type=s['aircraft_type']
                ))
    return flights

def init_test_data():
    Flight.query.delete()
    flights = generate_flights_schedule()
    for flight in flights:
        db.session.add(flight)
    db.session.commit()

# Главная страница: только ближайшие 5 рейсов
@app.route('/')
def index():
    now = datetime.now()
    today = now.date()
    flights = Flight.query.filter(
        db.func.date(Flight.departure_time) == today
    ).order_by(Flight.departure_time).all()
    return render_template('index.html', flights=flights)

@app.route('/about')
def about():
    return render_template('about.html')

# Расписание: по умолчанию ближайшие 2 дня, поиск по дате
@app.route('/schedule')
def schedule():
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    status = request.args.get('status', '')
    query = Flight.query
    if destination:
        query = query.filter(Flight.destination.ilike(f'%{destination}%'))
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        query = query.filter(db.func.date(Flight.departure_time) == date_obj.date())
    if status:
        query = query.filter(Flight.status == status)
    if not date:
        # Если дата не выбрана, показываем рейсы на сегодня и завтра
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        query = query.filter(db.func.date(Flight.departure_time).in_([today, tomorrow]))
    flights = query.order_by(Flight.departure_time).all()
    return render_template('schedule.html', flights=flights)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        privacy = request.form.get('privacy')
        
        if not privacy:
            flash('Необходимо согласиться на обработку персональных данных', 'error')
            return redirect(url_for('contact'))
        
        try:
            # Отправка письма
            msg = Message(
                subject=f'Новое сообщение от {name}: {subject}',
                recipients=['genuvseznayt@gmail.com'],
                body=f'''
                От: {name} <{email}>
                
                Тема: {subject}
                
                Сообщение:
                {message}
                '''
            )
            mail.send(msg)
            flash('Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.', 'success')
        except Exception as e:
            flash('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'error')
            print(f"Ошибка отправки письма: {str(e)}")
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_test_data()  # Инициализируем тестовые данные
    app.run(debug=True) 