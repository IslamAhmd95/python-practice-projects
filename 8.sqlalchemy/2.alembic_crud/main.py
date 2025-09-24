from app.crud.user_crud import *



if __name__ == '__main__':

    create_user({'name': 'islam', 'email': 'islam@gmail.com', 'password': '51215'})

    for user in get_users():
        print(user)