
import streamlit as st

st.title("My First Dockerized Streamlit App with [codanics](www.codanics.com)")
st.write("Hello from inside Docker!")
st.write("This is a simple Streamlit app running inside a Docker container.")
st.write("You can use this template to build your own Streamlit apps.")
st.write("To run this app, use the following command:")
st.code("docker run -p 8501:8501 my-first-app")
st.write("You can also use the following command to build and run the app:")
