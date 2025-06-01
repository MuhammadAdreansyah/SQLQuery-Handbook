import streamlit as st
import sys
import os
import importlib.util
from pathlib import Path

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
