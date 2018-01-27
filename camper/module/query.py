import module.model


class User():
    def __init__(self, db_session):
        self. db_session = db_session


    _user = None

    def _to_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d

    def _retrieve(self, id):
        user = module.model.User.query.get(id)
        self._user = user

        return user


    def add(self, first_name=None, last_name=None, email=None, password=None):
        user_new = module.model.User(first_name=first_name, last_name=last_name, email=email, password=password)
        self.db_session.session.add(user_new)
        self.db_session.session.commit()

        user = self._retrieve(user_new.id)

        return self._to_dict(user)


    def delete(self, id):
        user_to_delete = module.model.User.query.get(id)
        self.db_session.session.delete(user_to_delete)


    def get(self, id):
        user = self._retrieve(id)

        return self._to_dict(user)


    def all(self):
        users_all = module.model.User.query.all()

        output = {}
        for user in users_all:
            output[user.id] = self._to_dict(user)

        return output

        


    def modify(self, id):
        user_to_modify = self._retrieve(id)
        
        return self._to_dict(user_to_modify)


    def __repr__(self):
        return f'<User ...>'


