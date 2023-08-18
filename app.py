"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Create the tables based on the defined models
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        bio = request.form['bio']

        # Create a new User object
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, bio=bio)

        # Add the new user to the session and commit changes
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('show_users'))

    return render_template('new.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))

if __name__ == '__main__':
    app.run(debug=True)
