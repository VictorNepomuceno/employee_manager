#ROTAS
from app import app, db
import bcrypt
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Admin, Employees
from sqlalchemy.exc import IntegrityError
import datetime

def check_password(password, hash_password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)


@app.route('/register', methods=['GET','POST'])
def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['pwd']

            new_user = Admin(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário registrado com sucesso, realize seu login para prosseguir.', 'success')
            return redirect(url_for('login'))
        
    except IntegrityError:
        db.session.rollback()
        flash('Usuário ou email já existente, tente novamente.', 'error')
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pwd']
        user = Admin.query.filter_by(name=name).first()

        if user and check_password(password, user.password):
            login_user(user)
            flash('Sucesso ao entrar', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorreta', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    current_time = datetime.datetime.now().strftime("%d/%m/%Y")
    employees = Employees.query.all()
    return render_template('dashboard.html', username=current_user.name, employees=employees, current_time=current_time)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        new_emloyee = Employees(name=name, email=email, phone=phone)
        db.session.add(new_emloyee)
        db.session.commit()
        flash('Usuário adicionado com sucesso', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Erro ao cadastrar usuário, tente novamente', 'error')
        return redirect(url_for('dashboard'))

@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        edited_employee = Employees.query.get(request.form.get('id'))

        if edited_employee:
            edited_employee.name = request.form['name']
            edited_employee.email = request.form['email']
            edited_employee.phone = request.form['phone']

            db.session.commit()
            flash('Usuário editado com sucesso!')
            return redirect(url_for('dashboard'))
        else:
            flash('Erro: Funcionário não encontrado com o ID fornecido.', 'error')
            return redirect(url_for('dashboard'))


@app.route('/delete/<id>/', methods=['GET', 'DELETE'])
@login_required
def delete(id):
    delete_employee = Employees.query.get(id)
    db.session.delete(delete_employee)
    db.session.commit()
    flash('Usuário removido com sucesso', 'error')
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)