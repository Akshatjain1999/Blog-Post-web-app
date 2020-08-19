import sqlite3
conn = sqlite3.connect("data2.db", check_same_thread=False)
c = conn.cursor()


def create_user_table():
    c.execute('create table users if not exist')


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogTable(\
        author text , title text , article text , postDate DATE)')


def add_data(author, title, article, postDate):
    c.execute("insert into blogTable(author,title,article,postDate)\
        values (?,?,?,?)", (author, title, article, postDate))
    conn.commit()


def view_all_notes():
    c.execute("select * from blogTable")
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute('select distinct title from blogTable')
    return c.fetchall()


def get_blog_by_title(title):
    c.execute('select * from blogTable where title="{}"'.format(title))
    return c.fetchall()


def get_blog_by_author(author):
    c.execute('select * from blogTable where author="{}"'.format(author))
    return c.fetchall()


def delete_data(title):
    c.execute('Delete from blogTable where title="{}"'.format(title))
    conn.commit()


def owner_article(author='Akshat Jain'):
    c.execute('select * from blogTable where author="{}"'.format(author))
    return c.fetchall()
