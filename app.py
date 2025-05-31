import streamlit as st
import os
from PIL import Image
import time

# Set page configuration
st.set_page_config(
    page_title="MySQL Handbook",
    page_icon="🐬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and apply custom CSS
with open(os.path.join("assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Configure sidebar
def sidebar():
    # Add logo
    logo_path = os.path.join("assets", "images", "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.sidebar.image(logo, width=200)
    
    st.sidebar.title("MySQL Handbook")
    st.sidebar.caption("Your comprehensive guide to MySQL")
    
    # Add separator
    st.sidebar.markdown("---")
    
    # Display author info
    st.sidebar.markdown("### About")
    st.sidebar.info(
        """
        This app is a comprehensive guide to MySQL database management system.
        Navigate through different sections to learn various aspects of MySQL.
        """
    )
    
    # Add separator
    st.sidebar.markdown("---")
    
    # Version info
    st.sidebar.caption("Version 1.0.0")
    st.sidebar.caption(f"Last updated: May 31, 2025")

# Configure main content for home page
def main():
    # Initialize session state for tracking current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Display the sidebar
    sidebar()
    
    # Add content for the home page
    st.title("Welcome to MySQL Handbook")
    st.subheader("Your Interactive Guide to MySQL Database Management")
    
    # Introduction with animation
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("""
            ### What is MySQL?
            
            MySQL is one of the world's most popular open-source relational database management systems.
            It's known for its reliability, robustness, and performance, making it a top choice for web applications.
            
            ### What will you learn?
            
            This handbook covers everything from basic queries to advanced database administration:
            """)
            
            topics = [
                "Basic SQL Queries",
                "Data Definition Language (DDL)",
                "Data Manipulation Language (DML)",
                "Data Control Language (DCL)",
                "Transaction Control Language (TCL)",
                "Aggregate Functions and Complex Queries",
                "Interactive SQL Query Editor"
            ]
            
            for topic in topics:
                st.markdown(f"- {topic}")
        
        with col2:
            # Show MySQL logo or relevant image
            mysql_image_path = os.path.join("assets", "images", "ChatGPT Image May 29, 2025, 08_26_54 PM.png")
            if os.path.exists(mysql_image_path):
                st.image(mysql_image_path, width=300)
    
    # Add a "Get Started" section
    st.markdown("---")
    with st.container():
        st.header("Get Started")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("### Basic Queries")
            st.write("Learn the fundamental SQL queries for retrieving and filtering data.")
            st.page_link("pages/02_BasicQuery.py", label="Start Learning Basic Queries", icon="📊")
            
        with col2:
            st.success("### Data Manipulation")
            st.write("Master the art of inserting, updating, and deleting data in MySQL.")
            st.page_link("pages/04_DML.py", label="Explore Data Manipulation", icon="✏️")
            
        with col3:
            st.warning("### SQL Query Editor")
            st.write("Practice your SQL skills with our interactive query editor.")
            st.page_link("pages/SQLQueryEdtor.py", label="Open SQL Editor", icon="💻")

    # Add interactive example section
    st.markdown("---")
    with st.container():
        st.header("Quick SQL Example")
        
        code = '''SELECT customer.name, COUNT(orders.id) as order_count
FROM customers
JOIN orders ON customers.id = orders.customer_id
GROUP BY customer.id
HAVING COUNT(orders.id) > 5
ORDER BY order_count DESC
LIMIT 10;'''
        
        st.code(code, language="sql")
        
        if st.button("Explain This Query"):
            with st.spinner("Analyzing query..."):
                time.sleep(1)  # Simulating processing time
            
            st.success("Query Explanation")
            explanation = """
            This query:
            1. Selects customer names and counts their orders
            2. Joins the customers and orders tables
            3. Groups results by customer ID
            4. Filters to only include customers with more than 5 orders
            5. Orders results by order count (descending)
            6. Limits results to the top 10 customers
            """
            st.markdown(explanation)
    
    # Add feedback section
    st.markdown("---")
    with st.container():
        st.subheader("Feedback")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.text_area("Share your thoughts or suggestions:", placeholder="Type your feedback here...")
        
        with col2:
            st.selectbox("Rate this handbook:", options=["Select", "⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
            st.button("Submit Feedback")

if __name__ == "__main__":
    main()