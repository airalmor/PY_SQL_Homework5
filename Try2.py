import psycopg2


def delete_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            drop table if exists phones;
            drop table if exists clients;
            """)


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            create table if not exists clients(
            id serial primary key,
            name varchar(80),
            surname varchar(80),
            email varchar(100) unique not null);
            """)

    with conn.cursor() as cur:
        cur.execute("""
            create table if not exists phones(
            id serial primary key,
            client_id int references clients(id),
            phone varchar(100) default ('Ask phone')
            );
            """)


def add_client(conn, name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
            insert into clients(name,surname,email)
            values (%s,%s,%s);
            """, (name, surname, email))


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            insert into phones (client_id,phone)
            values (%s,%s);
            """, (client_id, phone))


def change_client_phone(conn, client_id, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            update phones
            set phone = %s
            where client_id =%s;
            """, (phone, client_id))


def change_client(conn, id, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            update clients
            set name = %s, surname = %s, email = %s
            where id = %s;
            """, (name, surname, email, id))


def delete_phone_by_client_id(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                delete 	
                from phones using clients
                where client_id=%s;""", (client_id,))


def delete_phone_by_phone_id(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
                delete
                from phones
                where id=%s;""", (id,))


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                delete
                from phones
                where client_id=%s;
                """, (client_id,))

        cur.execute("""
                delete
                from clients
                where id=%s;""", (client_id,))


def find_client(conn):
    question = str(input('Введите что вы ищеете :'))

    with conn.cursor() as cur:
        cur.execute("""
            select name,surname,email,phones.phone
            from clients 
            join phones on phones.client_id = clients.id
            where name ilike %s or surname ilike %s or email ilike %s or phones.phone ilike %s;""",
                    (question, question, question, question))
        print(cur.fetchall())


def find_all(conn):
    with conn.cursor() as cur:
        cur.execute("""
            select name,surname,email, phones.phone
            from clients 
            join phones on phones.client_id = clients.id
            ;""")
        print(cur.fetchall())


if __name__ == '__main__':
    import psycopg2

    with psycopg2.connect(database="netology_db", user="postgres", password="postgres") as conn:
        delete_tables(conn)
        create_table(conn)
        add_client(conn, 'Harry', 'Potter', 'mag@hogwards.magic')
        add_client(conn, 'Draco', 'Malfoy', 'draco@slytherin.magic')
        add_client(conn, 'Ron', 'Weasley', 'ron@hogwards.magic')
        add_client(conn, 'Albus', 'Dumbledore', 'director@hofwards.magic')
        add_phone(conn, 4, '999-999-999')
        add_phone(conn, 1, '+444-444-444')
        add_phone(conn, 1, '+111-111-111')
        add_phone(conn, 2, '+222-222-222')
        add_phone(conn, 3, '+333-333-333')
        change_client(conn, 1, 'Big Harry', 'Not Potter', 'no mail')
        change_client_phone(conn, 2, '666-666-666')
        delete_phone_by_phone_id(conn, 2)
        delete_phone_by_client_id(conn, 3)
        delete_client(conn, 2)
        find_client(conn)
        find_all(conn)
