from models import User, Address, Node, sessionLocal


with sessionLocal() as session:
    user_1 = User(name='Islam', age=30)
    user_2 = User(name='abdo', age=31)

    address_1 = Address(city='Cairo', state='Cairo', user=user_1)
    address_2 = Address(city='Mit Ghamr', state='Mansoura', user=user_1)
    address_3 = Address(city='London', state='London', zip_code=123456, user=user_2)

    session.add_all([user_1, user_2])

    session.commit()

    print(f"{user_1.addresses = }")
    print(f"{user_2.addresses = }")
    print(f"{address_1.user = }")


with sessionLocal() as session:
    n1 = Node(value=1)
    n2 = Node(value=2)
    n3 = Node(value=3)

    n1.next_node = n2
    n2.next_node = n3
    # n3.next_node = n1

    session.add_all([n1, n2, n3])
    session.commit()

    print(n1) 
    print(n2)
    print(n3)