import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3

from database import *


def readingTime(mytext):
    total_words = len([token for token in mytext.split(" ")])
    estimatedTime = total_words / 200.0
    return estimatedTime


title_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author: {}</h6>
	<br/>
	<br/>	
	<p style="text-align:center">{}</p>
	</div>
	"""
title_temp_1 = """
	<div style="background-color:#464e6f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<h6>Author: {}</h6>
	<br/>
	<br/>	
	<p style="text-align:center">{}</p>
	</div>
	"""
article_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<h6>Author:{}</h6> 
	<h6>Post Date: {}</h6>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>
	<p style="text-align:justify">{}</p>
	</div>
	"""
head_message_temp = """
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<h4 style="color:white;text-align:center;">{}</h1>
	<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
	<h6>Author:{}</h6> 		
	<h6>Post Date: {}</h6>		
	</div>
	"""
full_message_temp = """
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""


def main():
    st.title("Simple Blog")
    st.markdown(
        """##### [By Akshat jain](https://www.github.com/akshatjain1999)""")
    menu = ['Home', 'View Posts', 'Add Post', 'Search', 'Manage Blog']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.subheader('Home')
        result = view_all_notes()
        index_to_view = np.random.randint(
            low=0, high=len(result), size=9, dtype=int)
        imp = owner_article()
        o_author = imp[0][0]
        o_tite = imp[0][1]
        o_article = imp[0][2]
        o_date = imp[0][3]
        st.markdown(title_temp_1.format(o_tite, o_author,
                                        o_article, o_date), unsafe_allow_html=True)
        for i in index_to_view:
            b_author = result[i][0]
            b_title = result[i][1]
            b_article = str(result[i][2])[0:30]  # Text Summarization
            b_post_date = result[i][3]
            st.markdown(title_temp.format(b_title, b_author,
                                          b_article, b_post_date), unsafe_allow_html=True)

    elif choice == 'View Posts':
        st.subheader("View Articles")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Posts", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.text("Reading Time:{}".format(readingTime(b_article)))
            st.markdown(head_message_temp.format(
                b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(
                b_article), unsafe_allow_html=True)

    elif choice == 'Add Post':
        st.subheader("Add Articles")
        create_table()
        blog_author = st.text_input("Enter Author Name", max_chars=50)
        blog_title = st.text_input("Enter Post Title", max_chars=50)
        blog_article = st.text_area("Post Article", height=200)
        blog_date = st.date_input("Date")
        if st.button("ADD"):
            add_data(blog_author, blog_title, blog_article, blog_date)
            st.success("Post :{} saved ".format(blog_title))

    elif choice == 'Search':
        st.subheader("Search Articles")
        search_term = st.text_input("Enter Search Term")
        search_choice = st.radio("Feild to search by", ("title", "author"))
        if search_choice == 'title':
            artice_result = get_blog_by_title(search_term)
        elif search_choice == 'author':
            artice_result = get_blog_by_author(search_term)

        for i in artice_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.text("Reading Time:{}".format(readingTime(b_article)))
            st.markdown(head_message_temp.format(
                b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(
                b_article), unsafe_allow_html=True)

    elif choice == 'Manage Blog':
        st.subheader("Manage Articles")

        result = view_all_notes()
        clean_db = pd.DataFrame(
            result, columns=['Author', 'Title', 'Articles', 'Post Date'])
        st.dataframe(clean_db, width=1500)
        unique_titles = [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.selectbox("Delete Blog", unique_titles)

        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted: '{}'".format(delete_blog_by_title))
            st.write("Refresh the page to view update data")


if __name__ == '__main__':
    main()
