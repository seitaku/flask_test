

# db = SQLAlchemy()


# db.init_app(app)

# class User2(db.Model):
#     __tablename__ = 'user2'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(100), unique=True)
#     update_time = db.Column(db.Date, default=datetime.utcnow)

# class UUser(db.Model):
#     __tablename__ = 'u_user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))

# @app.route('/create_db')
# def index():
#     return 'ok'

# @app.route('/favicon.ico') 
# def favicon(): 
#     print('path:', os.path.join(app.root_path, 'static'))
#     return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon2.ico'
#         , mimetype='image/vnd.microsoft.icon')

# @app.route("/printOrder")
# def printOrder():
#     html = render_template('print_proforma_invoice.html')
#     return html

import os
from dotenv import load_dotenv
# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)


# 切換環境
from app import create_app
app = create_app('dev')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)