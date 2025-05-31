"""
MySQL Handbook - Data Definition Language (DDL) Module

This module provides comprehensive coverage of MySQL DDL operations including:
- Database operations (CREATE, DROP, ALTER DATABASE)
- Table operations (CREATE, ALTER, DROP TABLE)
- Index management
- Constraints and relationships
- Storage engines and optimization

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# Check for plotly availability
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# ================================
# DATA MANAGEMENT
# ================================

def get_ddl_sample_data():
    """Generate sample data for DDL demonstrations."""
    return {
        'databases': [
            {'name': 'ecommerce_db', 'created': '2024-01-15', 'size_mb': 245},
            {'name': 'inventory_db', 'created': '2024-02-10', 'size_mb': 128},
            {'name': 'customer_db', 'created': '2024-03-05', 'size_mb': 89}
        ],
        'tables': [
            {'table_name': 'customers', 'engine': 'InnoDB', 'rows': 15430, 'size_mb': 12.5},
            {'table_name': 'products', 'engine': 'InnoDB', 'rows': 8920, 'size_mb': 8.2},
            {'table_name': 'orders', 'engine': 'InnoDB', 'rows': 35670, 'size_mb': 25.8},
            {'table_name': 'order_items', 'engine': 'InnoDB', 'rows': 89450, 'size_mb': 45.3}
        ],
        'columns': [
            {'table': 'customers', 'column': 'customer_id', 'type': 'INT', 'key': 'PRI', 'null': 'NO'},
            {'table': 'customers', 'column': 'email', 'type': 'VARCHAR(100)', 'key': 'UNI', 'null': 'NO'},
            {'table': 'customers', 'column': 'first_name', 'type': 'VARCHAR(50)', 'key': '', 'null': 'NO'},
            {'table': 'customers', 'column': 'last_name', 'type': 'VARCHAR(50)', 'key': '', 'null': 'NO'},
            {'table': 'customers', 'column': 'created_at', 'type': 'TIMESTAMP', 'key': '', 'null': 'NO'}
        ]
    }


# ================================
# DATABASE OPERATIONS
# ================================

def show_database_operations():
    """Display database operation examples and interactive tools."""
    st.header("📊 Database Operations")
    
    # Theory section
    show_database_theory()
    
    # Interactive examples
    show_database_interactive()
    
    # Sidebar content
    show_database_sidebar()


def show_database_theory():
    """Show database operations theory."""
    st.subheader("Creating and Managing Databases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Create Database:**")
        st.code("""
CREATE DATABASE ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
        """, language="sql")
        
        st.write("**Drop Database:**")
        st.code("""
DROP DATABASE IF EXISTS old_database;
        """, language="sql")
    
    with col2:
        st.write("**Alter Database:**")
        st.code("""
ALTER DATABASE ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;
        """, language="sql")
        
        st.write("**Show Databases:**")
        st.code("""
SHOW DATABASES;
SHOW CREATE DATABASE ecommerce_db;
        """, language="sql")


def show_database_interactive():
    """Show interactive database operations."""
    st.subheader("🔧 Interactive Database Builder")
    
    with st.expander("Create Database Interactive Tool", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            db_name = st.text_input("Database Name:", value="my_database")
            charset = st.selectbox("Character Set:", 
                                 ["utf8mb4", "utf8", "latin1", "ascii"])
            collation = st.selectbox("Collation:", 
                                   ["utf8mb4_unicode_ci", "utf8mb4_general_ci", "utf8_general_ci"])
            
            if st.button("Generate CREATE DATABASE Statement"):
                create_sql = f"""CREATE DATABASE {db_name}
CHARACTER SET {charset}
COLLATE {collation};"""
                st.code(create_sql, language="sql")
        
        with col2:
            st.write("**Database Information:**")
            data = get_ddl_sample_data()
            df_databases = pd.DataFrame(data['databases'])
            st.dataframe(df_databases)


def show_database_sidebar():
    """Show database operations sidebar content."""
    with st.sidebar:
        st.write("**💡 Database Tips:**")
        st.info("""
        • Always use utf8mb4 for full Unicode support
        • Include IF NOT EXISTS to avoid errors
        • Choose appropriate collation for your language
        • Regular backups are essential
        """)


# ================================
# TABLE OPERATIONS
# ================================

def show_table_operations():
    """Display table operation examples and interactive tools."""
    st.header("🗂️ Table Operations")
    
    # Theory section
    show_table_theory()
    
    # Interactive examples
    show_table_interactive()
    
    # Sidebar content
    show_table_sidebar()


def show_table_theory():
    """Show table operations theory."""
    st.subheader("Creating and Managing Tables")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Create Table:**")
        st.code("""
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                       ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
        """, language="sql")
    
    with col2:
        st.write("**Alter Table:**")
        st.code("""
-- Add column
ALTER TABLE customers 
ADD COLUMN birth_date DATE;

-- Modify column
ALTER TABLE customers 
MODIFY COLUMN phone VARCHAR(25);

-- Drop column
ALTER TABLE customers 
DROP COLUMN birth_date;

-- Add index
ALTER TABLE customers 
ADD INDEX idx_email (email);
        """, language="sql")


def show_table_interactive():
    """Show interactive table operations."""
    st.subheader("🔧 Interactive Table Builder")
    
    with st.expander("Table Structure Designer", expanded=True):
        table_name = st.text_input("Table Name:", value="my_table")
        
        st.write("**Add Columns:**")
        if 'columns' not in st.session_state:
            st.session_state.columns = []
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            col_name = st.text_input("Column Name:", key="col_name")
        with col2:
            col_type = st.selectbox("Data Type:", 
                                  ["INT", "VARCHAR(50)", "VARCHAR(100)", "TEXT", "DATE", "TIMESTAMP", "DECIMAL(10,2)"],
                                  key="col_type")
        with col3:
            is_null = st.checkbox("Allow NULL", key="is_null")
            is_primary = st.checkbox("Primary Key", key="is_primary")
        with col4:
            is_unique = st.checkbox("Unique", key="is_unique")
            is_auto = st.checkbox("Auto Increment", key="is_auto")
        
        if st.button("Add Column"):
            if col_name:
                column_def = {
                    'name': col_name,
                    'type': col_type,
                    'null': 'NULL' if is_null else 'NOT NULL',
                    'primary': is_primary,
                    'unique': is_unique,
                    'auto': is_auto
                }
                st.session_state.columns.append(column_def)
                st.rerun()
        
        if st.session_state.columns:
            st.write("**Current Table Structure:**")
            df_columns = pd.DataFrame(st.session_state.columns)
            st.dataframe(df_columns)
            
            if st.button("Generate CREATE TABLE Statement"):
                create_sql = generate_create_table_sql(table_name, st.session_state.columns)
                st.code(create_sql, language="sql")
        
        if st.button("Clear All Columns"):
            st.session_state.columns = []
            st.rerun()


def generate_create_table_sql(table_name, columns):
    """Generate CREATE TABLE SQL statement."""
    sql_parts = [f"CREATE TABLE {table_name} ("]
    column_definitions = []
    
    for col in columns:
        col_def = f"    {col['name']} {col['type']}"
        
        if col['auto']:
            col_def += " AUTO_INCREMENT"
        
        col_def += f" {col['null']}"
        
        if col['unique'] and not col['primary']:
            col_def += " UNIQUE"
        
        column_definitions.append(col_def)
    
    # Add primary key
    primary_keys = [col['name'] for col in columns if col['primary']]
    if primary_keys:
        column_definitions.append(f"    PRIMARY KEY ({', '.join(primary_keys)})")
    
    sql_parts.append(",\n".join(column_definitions))
    sql_parts.append(") ENGINE=InnoDB;")
    
    return "\n".join(sql_parts)


def show_table_sidebar():
    """Show table operations sidebar content."""
    with st.sidebar:
        st.write("**🗂️ Table Best Practices:**")
        st.success("""
        • Always define primary keys
        • Use appropriate data types
        • Consider storage requirements
        • Plan for future growth
        • Use meaningful column names
        """)


# ================================
# INDEXES AND CONSTRAINTS
# ================================

def show_indexes_constraints():
    """Display indexes and constraints examples."""
    st.header("🔐 Indexes and Constraints")
    
    # Theory section
    show_indexes_theory()
    
    # Interactive examples
    show_indexes_interactive()
    
    # Sidebar content
    show_indexes_sidebar()


def show_indexes_theory():
    """Show indexes and constraints theory."""
    st.subheader("Database Indexes and Constraints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Index Types:**")
        st.code("""
-- Primary Index (automatically created)
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(100)
);

-- Unique Index
CREATE UNIQUE INDEX idx_email 
ON users (email);

-- Composite Index
CREATE INDEX idx_name_city 
ON users (last_name, city);

-- Full-text Index
CREATE FULLTEXT INDEX idx_content 
ON articles (title, content);
        """, language="sql")
    
    with col2:
        st.write("**Constraints:**")
        st.code("""
-- Foreign Key Constraint
ALTER TABLE orders 
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) 
REFERENCES customers(customer_id);

-- Check Constraint
ALTER TABLE products 
ADD CONSTRAINT chk_price 
CHECK (price > 0);

-- Not Null Constraint
ALTER TABLE customers 
MODIFY email VARCHAR(100) NOT NULL;
        """, language="sql")


def show_indexes_interactive():
    """Show interactive index management."""
    st.subheader("🔧 Index Performance Analyzer")
    
    with st.expander("Index Impact Simulator", expanded=True):
        # Sample data
        data = get_ddl_sample_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Table Information:**")
            df_tables = pd.DataFrame(data['tables'])
            st.dataframe(df_tables)
            
            selected_table = st.selectbox("Select Table:", df_tables['table_name'].tolist())
            
        with col2:
            st.write("**Performance Metrics:**")
            
            # Simulate query performance
            if selected_table:
                rows = df_tables[df_tables['table_name'] == selected_table]['rows'].iloc[0]
                
                # Without index
                scan_time = round(rows / 10000, 2)
                
                # With index
                index_time = round(scan_time * 0.01, 2)
                
                metrics_data = {
                    'Operation': ['Full Table Scan', 'Index Scan'],
                    'Time (seconds)': [scan_time, index_time],
                    'Rows Examined': [rows, min(100, rows)]
                }
                
                df_metrics = pd.DataFrame(metrics_data)
                st.dataframe(df_metrics)
                
                # Visualization
                if PLOTLY_AVAILABLE:
                    fig = px.bar(df_metrics, x='Operation', y='Time (seconds)', 
                               title='Query Performance Comparison')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.bar_chart(df_metrics.set_index('Operation')['Time (seconds)'])


def show_indexes_sidebar():
    """Show indexes sidebar content."""
    with st.sidebar:
        st.write("**⚡ Index Guidelines:**")
        st.warning("""
        • Index frequently queried columns
        • Avoid over-indexing (slows INSERTs)
        • Consider composite indexes for multi-column queries
        • Monitor index usage regularly
        • Drop unused indexes
        """)


# ================================
# STORAGE ENGINES
# ================================

def show_storage_engines():
    """Display storage engines information."""
    st.header("🏗️ Storage Engines")
    
    # Theory section
    show_engines_theory()
    
    # Interactive comparison
    show_engines_interactive()
    
    # Sidebar content
    show_engines_sidebar()


def show_engines_theory():
    """Show storage engines theory."""
    st.subheader("MySQL Storage Engines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**InnoDB (Default):**")
        st.code("""
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10,2)
) ENGINE=InnoDB;

-- Features:
-- ✓ ACID compliance
-- ✓ Foreign keys
-- ✓ Row-level locking
-- ✓ Crash recovery
        """, language="sql")
    
    with col2:
        st.write("**MyISAM:**")
        st.code("""
CREATE TABLE logs (
    log_id INT PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP
) ENGINE=MyISAM;

-- Features:
-- ✓ Fast for read-heavy workloads
-- ✓ Table-level locking
-- ✗ No foreign keys
-- ✗ No transactions
        """, language="sql")


def show_engines_interactive():
    """Show interactive storage engine comparison."""
    st.subheader("🔧 Storage Engine Comparison")
    
    with st.expander("Engine Feature Matrix", expanded=True):
        engine_data = {
            'Feature': ['ACID Compliance', 'Foreign Keys', 'Locking', 'Crash Recovery', 
                       'Full-text Search', 'Memory Usage', 'Best Use Case'],
            'InnoDB': ['✓ Yes', '✓ Yes', 'Row-level', '✓ Yes', '✓ Yes', 'Higher', 'OLTP'],
            'MyISAM': ['✗ No', '✗ No', 'Table-level', '✗ No', '✓ Yes', 'Lower', 'Read-heavy'],
            'Memory': ['✗ No', '✗ No', 'Table-level', '✗ No', '✗ No', 'RAM only', 'Temporary'],
            'Archive': ['✗ No', '✗ No', 'Row-level', '✓ Yes', '✗ No', 'Very low', 'Archival']
        }
        
        df_engines = pd.DataFrame(engine_data)
        st.dataframe(df_engines)
        
        # Performance simulation
        st.write("**Performance Simulation:**")
        workload = st.selectbox("Select Workload Type:", 
                               ["OLTP (Many small transactions)", 
                                "OLAP (Large analytical queries)",
                                "Read-heavy (Mostly SELECT)",
                                "Write-heavy (Many INSERTs/UPDATEs)"])
        
        if workload:
            simulate_engine_performance(workload)


def simulate_engine_performance(workload):
    """Simulate storage engine performance for different workloads."""
    performance_data = {
        "OLTP (Many small transactions)": {
            'InnoDB': 95, 'MyISAM': 60, 'Memory': 100, 'Archive': 20
        },
        "OLAP (Large analytical queries)": {
            'InnoDB': 80, 'MyISAM': 85, 'Memory': 70, 'Archive': 40
        },
        "Read-heavy (Mostly SELECT)": {
            'InnoDB': 85, 'MyISAM': 95, 'Memory': 100, 'Archive': 60
        },
        "Write-heavy (Many INSERTs/UPDATEs)": {
            'InnoDB': 90, 'MyISAM': 70, 'Memory': 95, 'Archive': 30
        }
    }
    
    scores = performance_data[workload]
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_performance = pd.DataFrame(list(scores.items()), 
                                    columns=['Engine', 'Performance Score'])
        st.dataframe(df_performance)
    
    with col2:
        if PLOTLY_AVAILABLE:
            fig = px.bar(df_performance, x='Engine', y='Performance Score',
                        title=f'Performance for {workload}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(df_performance.set_index('Engine'))


def show_engines_sidebar():
    """Show storage engines sidebar content."""
    with st.sidebar:
        st.write("**🏗️ Engine Selection:**")
        st.info("""
        **Use InnoDB for:**
        • E-commerce applications
        • Banking systems
        • Any OLTP workload

        **Use MyISAM for:**
        • Read-only data warehouses
        • Logging systems
        • Legacy applications
        """)


# ================================
# PRACTICE LAB
# ================================

def show_practice_lab():
    """Show DDL practice lab with exercises."""
    st.header("🧪 DDL Practice Lab")
    
    tab1, tab2, tab3 = st.tabs(["📚 Guided Exercises", "🎯 Challenges", "🏆 Schema Designer"])
    
    with tab1:
        show_guided_exercises()
    
    with tab2:
        show_ddl_challenges()
    
    with tab3:
        show_schema_designer()


def show_guided_exercises():
    """Show guided DDL exercises."""
    st.subheader("📚 Step-by-Step DDL Exercises")
    
    exercises = [
        {
            'title': "Create a Blog Database",
            'description': "Create a complete blog database with users, posts, and comments",
            'steps': [
                "Create database 'blog_db'",
                "Create 'users' table with id, username, email, password",
                "Create 'posts' table with id, user_id, title, content, created_at",
                "Create 'comments' table with id, post_id, user_id, content, created_at",
                "Add foreign key constraints"
            ],
            'solution': """
-- Step 1: Create database
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE blog_db;

-- Step 2: Create users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Create posts table
CREATE TABLE posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Step 4: Create comments table
CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 5: Add foreign key constraints
ALTER TABLE posts ADD CONSTRAINT fk_posts_user 
FOREIGN KEY (user_id) REFERENCES users(user_id);

ALTER TABLE comments ADD CONSTRAINT fk_comments_post 
FOREIGN KEY (post_id) REFERENCES posts(post_id);

ALTER TABLE comments ADD CONSTRAINT fk_comments_user 
FOREIGN KEY (user_id) REFERENCES users(user_id);
            """
        }
    ]
    
    for i, exercise in enumerate(exercises):
        with st.expander(f"Exercise {i+1}: {exercise['title']}", expanded=True):
            st.write(exercise['description'])
            st.write("**Steps:**")
            for step in exercise['steps']:
                st.write(f"• {step}")
            
            if st.button(f"Show Solution {i+1}"):
                st.code(exercise['solution'], language="sql")


def show_ddl_challenges():
    """Show DDL challenge problems."""
    st.subheader("🎯 DDL Challenges")
    
    challenges = [
        {
            'title': "E-commerce Database Design",
            'description': "Design a complete e-commerce database with products, orders, inventory, and user management",
            'requirements': [
                "Support multiple product categories",
                "Track inventory levels",
                "Handle complex orders with multiple items",
                "Support user addresses and payment methods",
                "Implement proper indexing strategy"
            ],
            'difficulty': "Advanced"
        },
        {
            'title': "Performance Optimization",
            'description': "Optimize an existing database schema for better performance",
            'requirements': [
                "Analyze existing slow queries",
                "Design appropriate indexes",
                "Partition large tables",
                "Optimize data types",
                "Implement archiving strategy"
            ],
            'difficulty': "Expert"
        }
    ]
    
    for i, challenge in enumerate(challenges):
        with st.expander(f"Challenge {i+1}: {challenge['title']} ({challenge['difficulty']})", expanded=False):
            st.write(challenge['description'])
            st.write("**Requirements:**")
            for req in challenge['requirements']:
                st.write(f"• {req}")
            
            # User input area
            user_solution = st.text_area(f"Your Solution {i+1}:", height=200, key=f"challenge_{i}")
            
            if st.button(f"Validate Solution {i+1}"):
                if user_solution.strip():
                    st.success("Solution submitted! In a real environment, this would be validated against the requirements.")
                else:
                    st.warning("Please provide a solution before validating.")


def show_schema_designer():
    """Show interactive schema designer."""
    st.subheader("🏆 Database Schema Designer")
    
    st.write("Design a complete database schema for your application:")
    
    # Initialize schema in session state
    if 'schema_tables' not in st.session_state:
        st.session_state.schema_tables = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Add New Table:**")
        new_table_name = st.text_input("Table Name:")
        
        if st.button("Add Table") and new_table_name:
            if new_table_name not in st.session_state.schema_tables:
                st.session_state.schema_tables[new_table_name] = []
                st.rerun()
    
    with col2:
        if st.session_state.schema_tables:
            table_to_modify = st.selectbox("Select Table to Modify:", 
                                         list(st.session_state.schema_tables.keys()))
            
            if st.button("Remove Table") and table_to_modify:
                del st.session_state.schema_tables[table_to_modify]
                st.rerun()
    
    # Display current schema
    if st.session_state.schema_tables:
        st.write("**Current Schema:**")
        for table_name, columns in st.session_state.schema_tables.items():
            with st.expander(f"Table: {table_name}"):
                if columns:
                    df_cols = pd.DataFrame(columns)
                    st.dataframe(df_cols)
                else:
                    st.write("No columns defined yet.")
        
        if st.button("Generate Complete DDL"):
            ddl_script = generate_complete_ddl(st.session_state.schema_tables)
            st.code(ddl_script, language="sql")
    
    if st.button("Clear All Tables"):
        st.session_state.schema_tables = {}
        st.rerun()


def generate_complete_ddl(schema_tables):
    """Generate complete DDL script from schema."""
    ddl_parts = []
    
    for table_name, columns in schema_tables.items():
        if columns:
            table_sql = f"CREATE TABLE {table_name} (\n"
            column_definitions = []
            
            for col in columns:
                col_def = f"    {col['name']} {col['type']}"
                if col.get('auto'):
                    col_def += " AUTO_INCREMENT"
                col_def += f" {col['null']}"
                if col.get('unique'):
                    col_def += " UNIQUE"
                column_definitions.append(col_def)
            
            table_sql += ",\n".join(column_definitions)
            table_sql += "\n) ENGINE=InnoDB;"
            ddl_parts.append(table_sql)
    
    return "\n\n".join(ddl_parts)


# ================================
# MAIN FUNCTION
# ================================

def main():
    """Main function to display DDL module content."""
    try:
        st.title("📊 Data Definition Language (DDL)")
        st.markdown("Learn to create, modify, and manage database structures with MySQL DDL operations.")
        
        # Create tabs for different DDL topics
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Database Operations", 
            "🗂️ Table Operations", 
            "🔐 Indexes & Constraints",
            "🏗️ Storage Engines",
            "🧪 Practice Lab"
        ])
        
        with tab1:
            show_database_operations()
        
        with tab2:
            show_table_operations()
        
        with tab3:
            show_indexes_constraints()
        
        with tab4:
            show_storage_engines()
        
        with tab5:
            show_practice_lab()
        
        # Footer
        st.markdown("---")
        st.markdown("**💡 Remember:** DDL operations can't be rolled back in most cases. Always backup before making structural changes!")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your database connection and try again.")


if __name__ == "__main__":
    main()
