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
import pandas as pd
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
# Module Import Helper Functions
# ============================================================================

def load_module(module_file, module_name):
    """Load a module from file path with error handling"""
    try:
        spec = importlib.util.spec_from_file_location(
            module_name, 
            pages_dir / module_file
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"⚠️ Failed to load {module_name}: {str(e)}")
        return None

def safe_call_function(module, function_name, fallback_title, fallback_description):
    """Safely call a function from a module with fallback content"""
    try:
        if module and hasattr(module, function_name):
            getattr(module, function_name)()
        else:
            # Fallback content
            st.title(fallback_title)
            st.markdown(fallback_description)
            st.info("This module is under development. Please check back later.")
    except Exception as e:
        st.error(f"⚠️ Error in {function_name}: {str(e)}")
        st.title(fallback_title)
        st.markdown(fallback_description)

# ============================================================================
# Page Functions
# ============================================================================
def show_home():
    """Display the home page content"""
    # Load and call home module
    home_module = load_module("01_Home.py", "home_module")
    safe_call_function(home_module, "show_home", 
                      "🏠 Welcome to MySQL Handbook",
                      """
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
            
def show_basic_query():
    """Display basic queries learning module"""
    basic_query_module = load_module("02_BasicQuery.py", "basic_query_module")
    safe_call_function(basic_query_module, "show_basic_query",
                      "🔍 Basic Queries",
                      """
                      Learn the fundamental MySQL query operations including SELECT, WHERE, 
                      ORDER BY, and more.
                      """)

def show_ddl():
    """Display DDL commands learning module"""
    ddl_module = load_module("03_DDL.py", "ddl_module")
    safe_call_function(ddl_module, "main",
                      "📋 DDL Commands",
                      """
                      Master Data Definition Language commands for creating and modifying 
                      database structures.
                      """)

def show_dml():
    """Display DML operations learning module"""
    dml_module = load_module("04_DML.py", "dml_module")
    safe_call_function(dml_module, "main",
                      "✏️ DML Operations",
                      """
                      Understand Data Manipulation Language for working with data in your tables.
                      """)

def show_dcl():
    """Display DCL controls learning module"""
    dcl_module = load_module("05_DCL.py", "dcl_module")
    safe_call_function(dcl_module, "main",
                      "🔒 DCL Controls",
                      """
                      Learn Data Control Language for managing user permissions and access control.
                      """)

def show_tcl():
    """Display TCL management learning module"""
    tcl_module = load_module("06_TCL.py", "tcl_module")
    safe_call_function(tcl_module, "main",
                      "🔄 TCL Management",
                      """
                      Master Transaction Control Language for managing database transactions.
                      """)

def show_aggregate_query():
    """Display aggregate functions learning module"""
    aggregate_module = load_module("07_AggregateQuery.py", "aggregate_module")
    safe_call_function(aggregate_module, "main",
                      "📊 Aggregate Functions",
                      """
                      Explore MySQL's powerful aggregate functions for data analysis and reporting.
                      """)

def show_query_editor():
    """Display SQL query editor tool"""
    editor_module = load_module("SQLQueryEditor.py", "editor_module")
    safe_call_function(editor_module, "main",
                      "💻 SQL Query Editor",
                      """
                      Practice your MySQL skills with our interactive query editor.
                      """)

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