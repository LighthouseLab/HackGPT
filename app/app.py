import streamlit as st

def display_app():
  # Simple Hello World App in Streamlit
  st.title("Hello World!")

  # Slider Widget from 0 to 100 in steps of 10
  x = st.slider('Select a value')

  # Display the value
  st.write(x, 'squared is', x * x)

if __name__ == '__main__':
    display_app()