from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db = SQLAlchemy(app)
'''migrate = Migrate(app, db)  # Integrando o Flask-Migrate'''

# Modelo de exemplo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
   # birthdate = db.Column(db.Date, nullable=True)  # Novo campo adicionado

# Criar o banco de dados
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Criar novo usuário e adicionar ao banco de dados
        new_user = User(name=name, address=address, phone=phone, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('list_users'))

    return render_template('form.html')


@app.route('/list')
def list_users():
    # Recuperar todos os usuários do banco de dados
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.address = request.form.get('address')
        user.phone = request.form.get('phone')
        user.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for('list_users'))

    return render_template('edit.html', user=user)


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))


if __name__ == '__main__':
    app.run(debug=True)