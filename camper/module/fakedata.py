from faker import Faker

import module.model
import module.query


fake = Faker()

def fake_users(db_session, num_of_users=10):
    
    for _ in range(num_of_users):
        first = fake.first_name()
        second = fake.last_name()
        email = fake.email()
        password = fake.password()

        module.query.User(module.model.db).add(first_name=first, last_name=second, email=email, password=password)

    return True