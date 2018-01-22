import os

from flask import Flask, render_template, abort, redirect, url_for, request
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers

import module.model

app = Flask(__name__)
app.config.from_object('config')

module.model.db.init_app(app)
module.model.db.create_all(app=app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(module.model.db, module.model.User, module.model.Role)
security = Security(app, user_datastore)

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False


    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Flask views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/role')
def role():
    return render_template('role.html')

@app.route('/trip')
def trip():
    return render_template('trip.html')

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/comment')
def comment():
    return render_template('comment.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/rank')
def rank():
    return render_template('rank.html')






# Create admin
admin = flask_admin.Admin(
    app,
    'Example: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(module.model.Role, module.model.db.session))
admin.add_view(MyModelView(module.model.User, module.model.db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    # module.model.db.drop_all()
    # module.model.db.create_all()

    with app.app_context():
        user_role = module.model.Role(name='user')
        super_user_role = module.model.Role(name='superuser')
        module.model.db.session.add(user_role)
        module.model.db.session.add(super_user_role)
        module.model.db.session.commit()

        user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        module.model.db.session.commit()

    return

# build_sample_db()

if __name__ == '__main__':
    app.run(debug=True)