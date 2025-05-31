"""
MySQL Handbook - Complete Guide to MySQL Database
=================================================
A comprehensive Streamlit application for learning MySQL database concepts,
commands, and best practices.

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import sys
import os
import importlib.util
from pathlib import Path

# ============================================================================
# Configuration and Setup
# ============================================================================

# Configure Streamlit page settings
st.set_page_config(
    page_title="MySQL Handbook",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the pages directory to the Python path
pages_dir = Path(__file__).parent / "pages"
sys.path.append(str(pages_dir))

# ============================================================================
# Page Functions
# ============================================================================

def show_home():
    """Display the home page content"""
    st.title("🏠 Welcome to MySQL Handbook")
    st.markdown("""
    ### Your Complete Guide to MySQL Database
    
    Welcome to the most comprehensive MySQL learning platform! This handbook covers 
    everything from basic queries to advanced database management techniques.
    
    **What you'll learn:**
    - 🔍 Basic and Advanced Queries
    - 📋 Data Definition Language (DDL)
    - ✏️ Data Manipulation Language (DML)
    - 🔒 Data Control Language (DCL)
    - 🔄 Transaction Control Language (TCL)
    - 📊 Aggregate Functions and Analytics
    
    **Start your journey** by selecting a module from the sidebar!
    """)
    
    # Quick start section
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **👋 New to MySQL?**
            Start with Basic Queries to learn the fundamentals.
            """)
        
        with col2:
            st.success("""
            **🚀 Ready to Practice?**
            Use our SQL Query Editor to test your skills.
            """)
        
        with col3:
            st.warning("""
            **📚 Need Reference?**
            Check out our Quick Links for documentation.
            """)

def show_basic_query():
    """Display basic queries learning module"""
    try:
        # Import the restructured module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "basic_query_module", 
            Path(__file__).parent / "pages" / "02_BasicQuery.py"
        )
        basic_query_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(basic_query_module)
        basic_query_module.show_basic_query()
    except Exception as e:
        # Fallback content if module import fails
        st.title("🔍 Basic Queries")
        st.markdown("""
        Learn the fundamental MySQL query operations including SELECT, WHERE, 
        ORDER BY, and more.
        """)
        st.info("This module will teach you essential querying techniques.")
        st.error(f"⚠️ Module loading failed: {str(e)}")

def show_ddl():
    """Display DDL commands learning module"""
    st.title("📋 DDL Commands")
    st.markdown("""
    Master Data Definition Language commands for creating and modifying 
    database structures.
    """)
    st.info("Learn CREATE, ALTER, DROP, and TRUNCATE commands.")

def show_dml():
    """Display DML operations learning module"""
    st.title("✏️ DML Operations")
    st.markdown("""
    Understand Data Manipulation Language for working with data in your tables.
    """)
    st.info("Master INSERT, UPDATE, DELETE, and SELECT operations.")

def show_dcl():
    """Display DCL controls learning module"""
    st.title("🔒 DCL Controls")
    st.markdown("""
    Learn Data Control Language for managing user permissions and access control.
    """)
    st.info("Understand GRANT, REVOKE, and security best practices.")

def show_tcl():
    """Display TCL management learning module"""
    st.title("🔄 TCL Management")
    st.markdown("""
    Master Transaction Control Language for managing database transactions.
    """)
    st.info("Learn COMMIT, ROLLBACK, SAVEPOINT, and transaction handling.")

def show_aggregate_query():
    """Display aggregate functions learning module"""
    st.title("📊 Aggregate Functions")
    st.markdown("""
    Explore MySQL's powerful aggregate functions for data analysis and reporting.
    """)
    st.info("Master COUNT, SUM, AVG, MAX, MIN, and GROUP BY operations.")

def show_query_editor():
    """Display SQL query editor tool"""
    st.title("💻 SQL Query Editor")
    st.markdown("""
    Practice your MySQL skills with our interactive query editor.
    """)
    st.info("Write, test, and execute your SQL queries in a safe environment.")

# ============================================================================
# UI Components
# ============================================================================

def create_header():
    """Create the main header with logo and title"""
    # Create header container
    header_container = st.container()
    
    with header_container:
        # Create columns for logo and title
        col1, col2 = st.columns([1, 4])
        
        with col1:
            # Display logo if it exists
            logo_path = "assets/images/logo.png"
            if os.path.exists(logo_path):
                st.image(logo_path, width=120)
            else:
                st.markdown("🗃️")  # Fallback emoji if logo not found
        
        with col2:
            st.markdown("""
            # 🗃️ MySQL Handbook
            ### *Complete Guide to MySQL Database*
            """)
    
    st.divider()

def create_sidebar_navigation():
    """Create and configure the sidebar navigation"""
    with st.sidebar:
        # Page definitions
        home_page = st.Page(show_home, title="Home", icon="🏠")
        
        learning_pages = [
            st.Page(show_basic_query, title="Basic Queries", icon="🔍"),
            st.Page(show_ddl, title="DDL Commands", icon="📋"),
            st.Page(show_dml, title="DML Operations", icon="✏️"),
            st.Page(show_dcl, title="DCL Controls", icon="🔒"),
            st.Page(show_tcl, title="TCL Management", icon="🔄"),
            st.Page(show_aggregate_query, title="Aggregate Functions", icon="📊")
        ]
        
        tools_pages = [
            st.Page(show_query_editor, title="SQL Query Editor", icon="💻")
        ]
        
        # Create navigation structure
        nav = st.navigation({
            "Home": [home_page],
            "Learning Modules": learning_pages,
            "Tools": tools_pages
        })
        
        return nav

def create_sidebar_content():
    """Create additional sidebar content"""
    with st.sidebar:
        # Quick Links section
        st.subheader("🔗 Quick Links")
        
        with st.expander("📖 Documentation"):
            st.markdown("""
            - [Official MySQL Docs](https://dev.mysql.com/doc/)
            - [SQL Tutorial](https://www.w3schools.com/sql/)
            - [MySQL Workbench](https://www.mysql.com/products/workbench/)
            """)
        
        with st.expander("💡 Tips & Tricks"):
            st.info("💡 **Pro Tip**: Use EXPLAIN to analyze query performance!")
            st.success("✅ **Remember**: Always backup before making schema changes!")
            st.warning("⚠️ **Caution**: Test queries on sample data first!")
        
        with st.expander("🎯 Learning Path"):
            st.markdown("""
            **Recommended learning sequence:**
            1. 🔍 Basic Queries
            2. 📋 DDL Commands  
            3. ✏️ DML Operations
            4. 📊 Aggregate Functions
            5. 🔒 DCL Controls
            6. 🔄 TCL Management
            7. 💻 Practice with Query Editor
            """)
        
        st.divider()
        
        # Footer information
        st.caption("MySQL Handbook v2.0")
        st.caption("Built with ❤️ using Streamlit")

# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application function"""
    try:
        # Create main header with logo and title
        create_header()
        
        # Create sidebar navigation
        nav = create_sidebar_navigation()
        
        # Add additional sidebar content
        create_sidebar_content()
        
        # Run the selected page
        nav.run()
        
    except Exception as e:
        st.error(f"Application error: {e}")
        st.stop()

if __name__ == "__main__":
    main()