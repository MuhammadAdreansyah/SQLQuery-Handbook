"""
MySQL Handbook - Data Manipulation Language (DML) Module

This module provides comprehensive coverage of MySQL DML operations including:
- INSERT operations (single, multiple, bulk)
- UPDATE operations (single, multiple, conditional)
- DELETE operations (conditional, bulk, soft delete)
- Data import/export operations
- Performance optimization for DML operations

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import json

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

def get_dml_sample_data():
    """Generate sample data for DML demonstrations."""
    
    # Sample customers data
    customers = []
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Anna']
    last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller', 'Moore', 'Taylor']
    
    for i in range(1, 21):
        customers.append({
            'customer_id': i,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'user{i}@example.com',
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'status': random.choice(['active', 'inactive', 'pending'])
        })
    
    # Sample products data
    products = []
    product_names = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'Tablet', 'Phone']
    
    for i in range(1, 16):
        products.append({
            'product_id': i,
            'name': f"{random.choice(product_names)} {random.choice(['Pro', 'Max', 'Plus', 'Mini'])}",
            'price': round(random.uniform(29.99, 1999.99), 2),
            'stock_quantity': random.randint(0, 100),
            'category': random.choice(['Electronics', 'Computers', 'Accessories', 'Mobile']),
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d')
        })
    
    # Sample orders data
    orders = []
    for i in range(1, 31):
        orders.append({
            'order_id': i,
            'customer_id': random.randint(1, 20),
            'order_date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            'total_amount': round(random.uniform(50.00, 2000.00), 2),
            'status': random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled'])
        })
    
    return {
        'customers': customers,
        'products': products,
        'orders': orders
    }


# ================================
# INSERT OPERATIONS
# ================================

def show_insert_operations():
    """Display INSERT operation examples and interactive tools."""
    st.header("➕ INSERT Operations")
    
    # Theory section
    show_insert_theory()
    
    # Interactive examples
    show_insert_interactive()
    
    # Sidebar content
    show_insert_sidebar()


def show_insert_theory():
    """Show INSERT operations theory."""
    st.subheader("Data Insertion Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Single Row INSERT:**")
        st.code("""
INSERT INTO customers (first_name, last_name, email)
VALUES ('John', 'Doe', 'john.doe@email.com');
        """, language="sql")
        
        st.write("**Multiple Rows INSERT:**")
        st.code("""
INSERT INTO customers (first_name, last_name, email)
VALUES 
    ('Jane', 'Smith', 'jane.smith@email.com'),
    ('Mike', 'Johnson', 'mike.johnson@email.com'),
    ('Sarah', 'Davis', 'sarah.davis@email.com');
        """, language="sql")
    
    with col2:
        st.write("**INSERT with SELECT:**")
        st.code("""
INSERT INTO archived_customers (customer_id, full_name, email)
SELECT customer_id, 
       CONCAT(first_name, ' ', last_name),
       email
FROM customers 
WHERE status = 'inactive';
        """, language="sql")
        
        st.write("**INSERT IGNORE:**")
        st.code("""
INSERT IGNORE INTO customers (email, first_name, last_name)
VALUES ('existing@email.com', 'Test', 'User');

-- Prevents duplicate key errors
        """, language="sql")


def show_insert_interactive():
    """Show interactive INSERT operations."""
    st.subheader("🔧 Interactive Data Insertion")
    
    with st.expander("Customer Data Entry Form", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name:", value="John")
            last_name = st.text_input("Last Name:", value="Doe")
            email = st.text_input("Email:", value="john.doe@example.com")
            
        with col2:
            phone = st.text_input("Phone:", value="+1-555-123-4567")
            status = st.selectbox("Status:", ["active", "inactive", "pending"])
            
        if st.button("Generate INSERT Statement"):
            insert_sql = f"""INSERT INTO customers (first_name, last_name, email, phone, status, created_at)
VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{status}', NOW());"""
            st.code(insert_sql, language="sql")
    
    with st.expander("Bulk Data Generator", expanded=False):
        num_records = st.slider("Number of records to generate:", 1, 100, 10)
        
        if st.button("Generate Bulk INSERT"):
            bulk_sql = generate_bulk_insert(num_records)
            st.code(bulk_sql, language="sql")
            
        st.info("💡 **Performance Tip:** Use bulk INSERT for better performance when inserting multiple rows.")


def generate_bulk_insert(num_records):
    """Generate bulk INSERT statement."""
    data = get_dml_sample_data()
    customers = data['customers'][:num_records]
    
    sql_parts = ["INSERT INTO customers (first_name, last_name, email, phone, status, created_at)"]
    sql_parts.append("VALUES")
    
    value_parts = []
    for customer in customers:
        value_part = f"('{customer['first_name']}', '{customer['last_name']}', '{customer['email']}', '{customer['phone']}', '{customer['status']}', '{customer['created_at']}')"
        value_parts.append(value_part)
    
    sql_parts.append(",\n".join(value_parts))
    sql_parts.append(";")
    
    return "\n".join(sql_parts)


def show_insert_sidebar():
    """Show INSERT operations sidebar content."""
    with st.sidebar:
        st.write("**➕ INSERT Best Practices:**")
        st.success("""
        • Use bulk INSERT for multiple rows
        • Specify column names explicitly
        • Use prepared statements for security
        • Consider INSERT IGNORE for duplicates
        • Use REPLACE for upsert operations
        """)


# ================================
# UPDATE OPERATIONS
# ================================

def show_update_operations():
    """Display UPDATE operation examples and interactive tools."""
    st.header("✏️ UPDATE Operations")
    
    # Theory section
    show_update_theory()
    
    # Interactive examples
    show_update_interactive()
    
    # Sidebar content
    show_update_sidebar()


def show_update_theory():
    """Show UPDATE operations theory."""
    st.subheader("Data Modification Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Simple UPDATE:**")
        st.code("""
UPDATE customers 
SET phone = '+1-555-999-8888'
WHERE customer_id = 1;
        """, language="sql")
        
        st.write("**Multiple Column UPDATE:**")
        st.code("""
UPDATE customers 
SET first_name = 'Jonathan',
    last_name = 'Smith',
    updated_at = NOW()
WHERE customer_id = 1;
        """, language="sql")
    
    with col2:
        st.write("**Conditional UPDATE:**")
        st.code("""
UPDATE products 
SET price = price * 0.9
WHERE category = 'Electronics' 
  AND stock_quantity > 50;
        """, language="sql")
        
        st.write("**UPDATE with JOIN:**")
        st.code("""
UPDATE customers c
JOIN orders o ON c.customer_id = o.customer_id
SET c.status = 'vip'
WHERE o.total_amount > 1000;
        """, language="sql")


def show_update_interactive():
    """Show interactive UPDATE operations."""
    st.subheader("🔧 Interactive Data Updates")
    
    data = get_dml_sample_data()
    
    with st.expander("Customer Update Tool", expanded=True):
        # Display current data
        df_customers = pd.DataFrame(data['customers'][:10])
        st.write("**Current Customer Data:**")
        st.dataframe(df_customers)
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_id = st.selectbox("Select Customer ID:", df_customers['customer_id'].tolist())
            update_field = st.selectbox("Field to Update:", 
                                      ['first_name', 'last_name', 'email', 'phone', 'status'])
            new_value = st.text_input("New Value:")
            
        with col2:
            condition_type = st.selectbox("Update Type:", 
                                        ["Single Record", "Conditional Update", "Bulk Update"])
            
            if condition_type != "Single Record":
                condition = st.text_input("WHERE Condition:", 
                                        value="status = 'inactive'" if condition_type == "Conditional Update" else "1=1")
            
        if st.button("Generate UPDATE Statement"):
            if condition_type == "Single Record":
                update_sql = f"""UPDATE customers 
SET {update_field} = '{new_value}',
    updated_at = NOW()
WHERE customer_id = {customer_id};"""
            else:
                where_clause = condition if condition_type == "Conditional Update" else "1=1"
                update_sql = f"""UPDATE customers 
SET {update_field} = '{new_value}',
    updated_at = NOW()
WHERE {where_clause};"""
            
            st.code(update_sql, language="sql")
    
    with st.expander("Batch Price Update Simulator", expanded=False):
        st.write("**Product Price Management:**")
        df_products = pd.DataFrame(data['products'][:10])
        st.dataframe(df_products)
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category:", df_products['category'].unique())
            adjustment_type = st.selectbox("Adjustment:", ["Percentage", "Fixed Amount"])
            
        with col2:
            if adjustment_type == "Percentage":
                adjustment = st.slider("Percentage Change:", -50, 50, 10)
                multiplier = 1 + (adjustment / 100)
                update_sql = f"""UPDATE products 
SET price = price * {multiplier}
WHERE category = '{category}';"""
            else:
                adjustment = st.number_input("Fixed Amount:", value=10.0)
                update_sql = f"""UPDATE products 
SET price = price + {adjustment}
WHERE category = '{category}';"""
        
        st.code(update_sql, language="sql")


def show_update_sidebar():
    """Show UPDATE operations sidebar content."""
    with st.sidebar:
        st.write("**✏️ UPDATE Safety Tips:**")
        st.warning("""
        • Always use WHERE clause (avoid accidental mass updates)
        • Test with SELECT first
        • Use transactions for critical updates
        • Backup data before bulk updates
        • Consider UPDATE limits
        """)


# ================================
# DELETE OPERATIONS
# ================================

def show_delete_operations():
    """Display DELETE operation examples and interactive tools."""
    st.header("🗑️ DELETE Operations")
    
    # Theory section
    show_delete_theory()
    
    # Interactive examples
    show_delete_interactive()
    
    # Sidebar content
    show_delete_sidebar()


def show_delete_theory():
    """Show DELETE operations theory."""
    st.subheader("Data Removal Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Simple DELETE:**")
        st.code("""
DELETE FROM customers 
WHERE customer_id = 1;
        """, language="sql")
        
        st.write("**Conditional DELETE:**")
        st.code("""
DELETE FROM orders 
WHERE order_date < '2023-01-01' 
  AND status = 'cancelled';
        """, language="sql")
        
        st.write("**Soft DELETE (Recommended):**")
        st.code("""
-- Mark as deleted instead of removing
UPDATE customers 
SET deleted_at = NOW(),
    status = 'deleted'
WHERE customer_id = 1;
        """, language="sql")
    
    with col2:
        st.write("**DELETE with JOIN:**")
        st.code("""
DELETE c FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date < '2022-01-01'
  AND o.status = 'cancelled';
        """, language="sql")
        
        st.write("**Truncate vs DELETE:**")
        st.code("""
-- DELETE (slower, logged, can rollback)
DELETE FROM temp_table;

-- TRUNCATE (faster, minimal logging)
TRUNCATE TABLE temp_table;
        """, language="sql")


def show_delete_interactive():
    """Show interactive DELETE operations."""
    st.subheader("🔧 Interactive Data Removal")
    
    data = get_dml_sample_data()
    
    with st.expander("Safe Delete Simulator", expanded=True):
        tab1, tab2 = st.tabs(["🎯 Targeted Delete", "🧹 Cleanup Operations"])
        
        with tab1:
            df_orders = pd.DataFrame(data['orders'][:15])
            st.write("**Orders Data:**")
            st.dataframe(df_orders)
            
            col1, col2 = st.columns(2)
            with col1:
                delete_type = st.selectbox("Delete Operation:", 
                                         ["Single Order", "By Status", "By Date Range", "By Customer"])
                
                if delete_type == "Single Order":
                    order_id = st.selectbox("Order ID:", df_orders['order_id'].tolist())
                elif delete_type == "By Status":
                    status = st.selectbox("Status:", df_orders['status'].unique())
                elif delete_type == "By Date Range":
                    start_date = st.date_input("Start Date:")
                    end_date = st.date_input("End Date:")
                else:  # By Customer
                    customer_id = st.selectbox("Customer ID:", df_orders['customer_id'].unique())
            
            with col2:
                deletion_method = st.radio("Deletion Method:", 
                                         ["Hard Delete", "Soft Delete (Recommended)"])
                
                if st.button("Generate DELETE Statement"):
                    delete_sql = generate_delete_statement(delete_type, deletion_method, locals())
                    st.code(delete_sql, language="sql")
        
        with tab2:
            st.write("**Database Cleanup Operations:**")
            
            cleanup_operations = {
                "Remove old logs": "DELETE FROM system_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);",
                "Clear cancelled orders": "DELETE FROM orders WHERE status = 'cancelled' AND created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);",
                "Remove inactive users": "UPDATE users SET deleted_at = NOW() WHERE last_login < DATE_SUB(NOW(), INTERVAL 1 YEAR);",
                "Clean temporary data": "TRUNCATE TABLE temp_processing_data;"
            }
            
            selected_cleanup = st.selectbox("Select Cleanup Operation:", list(cleanup_operations.keys()))
            st.code(cleanup_operations[selected_cleanup], language="sql")
            
            if st.button("Simulate Cleanup Impact"):
                simulate_cleanup_impact(selected_cleanup)


def generate_delete_statement(delete_type, deletion_method, context):
    """Generate DELETE statement based on parameters."""
    if deletion_method == "Soft Delete (Recommended)":
        base_sql = "UPDATE orders SET deleted_at = NOW(), status = 'deleted'"
    else:
        base_sql = "DELETE FROM orders"
    
    if delete_type == "Single Order":
        where_clause = f"WHERE order_id = {context['order_id']}"
    elif delete_type == "By Status":
        where_clause = f"WHERE status = '{context['status']}'"
    elif delete_type == "By Date Range":
        where_clause = f"WHERE order_date BETWEEN '{context['start_date']}' AND '{context['end_date']}'"
    else:  # By Customer
        where_clause = f"WHERE customer_id = {context['customer_id']}"
    
    return f"{base_sql}\n{where_clause};"


def simulate_cleanup_impact(operation):
    """Simulate the impact of cleanup operations."""
    impact_data = {
        "Remove old logs": {"rows_affected": 15420, "space_freed_mb": 245, "performance_impact": "Low"},
        "Clear cancelled orders": {"rows_affected": 892, "space_freed_mb": 12, "performance_impact": "Low"},
        "Remove inactive users": {"rows_affected": 1205, "space_freed_mb": 8, "performance_impact": "Medium"},
        "Clean temporary data": {"rows_affected": 50000, "space_freed_mb": 1200, "performance_impact": "High"}
    }
    
    impact = impact_data.get(operation, {"rows_affected": 0, "space_freed_mb": 0, "performance_impact": "Unknown"})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows Affected", f"{impact['rows_affected']:,}")
    with col2:
        st.metric("Space Freed", f"{impact['space_freed_mb']} MB")
    with col3:
        st.metric("Performance Impact", impact['performance_impact'])


def show_delete_sidebar():
    """Show DELETE operations sidebar content."""
    with st.sidebar:
        st.write("**🗑️ DELETE Safety Guidelines:**")
        st.error("""
        **CRITICAL WARNINGS:**
        • DELETE is irreversible!
        • Always backup before mass deletes
        • Use transactions for safety
        • Test with SELECT first
        • Consider soft delete for important data
        """)


# ================================
# DATA IMPORT/EXPORT
# ================================

def show_import_export():
    """Display data import/export examples and tools."""
    st.header("📥📤 Data Import/Export")
    
    # Theory section
    show_import_export_theory()
    
    # Interactive examples
    show_import_export_interactive()
    
    # Sidebar content
    show_import_export_sidebar()


def show_import_export_theory():
    """Show import/export theory."""
    st.subheader("Data Import and Export Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**LOAD DATA INFILE:**")
        st.code("""
LOAD DATA INFILE '/path/to/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS
(first_name, last_name, email, phone);
        """, language="sql")
        
        st.write("**INSERT from CSV Logic:**")
        st.code("""
-- For applications without LOAD DATA privilege
INSERT INTO customers (first_name, last_name, email)
SELECT 
    SUBSTRING_INDEX(SUBSTRING_INDEX(csv_row, ',', 1), ',', -1),
    SUBSTRING_INDEX(SUBSTRING_INDEX(csv_row, ',', 2), ',', -1),
    SUBSTRING_INDEX(SUBSTRING_INDEX(csv_row, ',', 3), ',', -1)
FROM temp_csv_table;
        """, language="sql")
    
    with col2:
        st.write("**SELECT INTO OUTFILE:**")
        st.code("""
SELECT customer_id, first_name, last_name, email
INTO OUTFILE '/path/to/export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
FROM customers
WHERE status = 'active';
        """, language="sql")
        
        st.write("**Backup Data:**")
        st.code("""
-- Create backup table
CREATE TABLE customers_backup AS
SELECT * FROM customers
WHERE created_at >= '2024-01-01';

-- Or use mysqldump
-- mysqldump -u user -p database_name > backup.sql
        """, language="sql")


def show_import_export_interactive():
    """Show interactive import/export tools."""
    st.subheader("🔧 Interactive Data Transfer")
    
    with st.expander("CSV Import Simulator", expanded=True):
        st.write("**Upload and Import Data:**")
        
        # File upload simulation
        import_type = st.selectbox("Import Method:", 
                                 ["LOAD DATA INFILE", "INSERT statements", "Bulk INSERT"])
        
        # Sample CSV data
        sample_csv = """first_name,last_name,email,phone
John,Doe,john.doe@email.com,+1-555-123-4567
Jane,Smith,jane.smith@email.com,+1-555-234-5678
Mike,Johnson,mike.johnson@email.com,+1-555-345-6789"""
        
        st.text_area("Sample CSV Data:", value=sample_csv, height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            has_header = st.checkbox("CSV has header row", value=True)
            delimiter = st.selectbox("Field Separator:", [",", ";", "\\t", "|"])
            
        with col2:
            quote_char = st.selectbox("Text Qualifier:", ['"', "'", "None"])
            encoding = st.selectbox("Encoding:", ["UTF-8", "Latin1", "Windows-1252"])
        
        if st.button("Generate Import Statement"):
            import_sql = generate_import_statement(import_type, delimiter, quote_char, has_header)
            st.code(import_sql, language="sql")
    
    with st.expander("Data Export Tool", expanded=False):
        st.write("**Export Configuration:**")
        
        col1, col2 = st.columns(2)
        with col1:
            export_table = st.selectbox("Table to Export:", ["customers", "products", "orders"])
            export_format = st.selectbox("Export Format:", ["CSV", "JSON", "SQL INSERT"])
            
        with col2:
            include_header = st.checkbox("Include Header", value=True)
            where_condition = st.text_input("WHERE Condition (optional):", 
                                          placeholder="status = 'active'")
        
        if st.button("Generate Export Statement"):
            export_sql = generate_export_statement(export_table, export_format, include_header, where_condition)
            st.code(export_sql, language="sql")


def generate_import_statement(import_type, delimiter, quote_char, has_header):
    """Generate import statement based on parameters."""
    if import_type == "LOAD DATA INFILE":
        quote_part = f"ENCLOSED BY '{quote_char}'" if quote_char != "None" else ""
        ignore_part = "IGNORE 1 ROWS" if has_header else ""
        
        return f"""LOAD DATA INFILE '/path/to/data.csv'
INTO TABLE customers
FIELDS TERMINATED BY '{delimiter}'
{quote_part}
LINES TERMINATED BY '\\n'
{ignore_part}
(first_name, last_name, email, phone);"""
    
    elif import_type == "INSERT statements":
        return """-- Process each row individually
INSERT INTO customers (first_name, last_name, email, phone)
VALUES ('John', 'Doe', 'john.doe@email.com', '+1-555-123-4567');

INSERT INTO customers (first_name, last_name, email, phone)
VALUES ('Jane', 'Smith', 'jane.smith@email.com', '+1-555-234-5678');"""
    
    else:  # Bulk INSERT
        return """INSERT INTO customers (first_name, last_name, email, phone)
VALUES 
    ('John', 'Doe', 'john.doe@email.com', '+1-555-123-4567'),
    ('Jane', 'Smith', 'jane.smith@email.com', '+1-555-234-5678'),
    ('Mike', 'Johnson', 'mike.johnson@email.com', '+1-555-345-6789');"""


def generate_export_statement(table, format_type, include_header, where_condition):
    """Generate export statement based on parameters."""
    where_clause = f"WHERE {where_condition}" if where_condition else ""
    
    if format_type == "CSV":
        return f"""SELECT {table}.*
INTO OUTFILE '/path/to/{table}_export.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
FROM {table}
{where_clause};"""
    
    elif format_type == "JSON":
        return f"""SELECT JSON_OBJECT(
    'customer_id', customer_id,
    'name', CONCAT(first_name, ' ', last_name),
    'email', email,
    'phone', phone
) as json_data
FROM {table}
{where_clause};"""
    
    else:  # SQL INSERT
        return f"""SELECT CONCAT(
    'INSERT INTO {table} VALUES (',
    QUOTE(customer_id), ',',
    QUOTE(first_name), ',',
    QUOTE(last_name), ',',
    QUOTE(email), ',',
    QUOTE(phone), ');'
) as insert_statement
FROM {table}
{where_clause};"""


def show_import_export_sidebar():
    """Show import/export sidebar content."""
    with st.sidebar:
        st.write("**📥📤 Import/Export Tips:**")
        st.info("""
        • Validate data before importing
        • Use transactions for large imports
        • Check file permissions and paths
        • Monitor disk space during operations
        • Test with small datasets first
        """)


# ================================
# PRACTICE LAB
# ================================

def show_practice_lab():
    """Show DML practice lab with exercises."""
    st.header("🧪 DML Practice Lab")
    
    tab1, tab2, tab3 = st.tabs(["📚 Guided Exercises", "🎯 Real-world Scenarios", "🏆 Performance Challenge"])
    
    with tab1:
        show_guided_dml_exercises()
    
    with tab2:
        show_realworld_scenarios()
    
    with tab3:
        show_performance_challenge()


def show_guided_dml_exercises():
    """Show guided DML exercises."""
    st.subheader("📚 Step-by-Step DML Exercises")
    
    exercises = [
        {
            'title': "E-commerce Order Processing",
            'description': "Practice INSERT, UPDATE, and DELETE operations for an e-commerce system",
            'tasks': [
                "Insert new customer records",
                "Add products to the catalog",
                "Create orders and order items",
                "Update order status as it progresses",
                "Handle order cancellations",
                "Update inventory after sales"
            ],
            'sample_solution': """
-- Step 1: Insert new customer
INSERT INTO customers (first_name, last_name, email, phone, created_at)
VALUES ('Alice', 'Wilson', 'alice.wilson@email.com', '+1-555-999-0000', NOW());

-- Step 2: Add new product
INSERT INTO products (name, price, category, stock_quantity, created_at)
VALUES ('Wireless Headphones Pro', 199.99, 'Electronics', 50, NOW());

-- Step 3: Create order
INSERT INTO orders (customer_id, order_date, status, total_amount)
VALUES (LAST_INSERT_ID(), NOW(), 'pending', 199.99);

-- Step 4: Update order status
UPDATE orders 
SET status = 'processing', updated_at = NOW()
WHERE order_id = LAST_INSERT_ID();

-- Step 5: Handle cancellation (soft delete)
UPDATE orders 
SET status = 'cancelled', 
    cancelled_at = NOW(),
    cancellation_reason = 'Customer request'
WHERE order_id = 123;

-- Step 6: Update inventory after sale
UPDATE products 
SET stock_quantity = stock_quantity - 1,
    updated_at = NOW()
WHERE product_id = 1 AND stock_quantity > 0;
            """
        }
    ]
    
    for i, exercise in enumerate(exercises):
        with st.expander(f"Exercise {i+1}: {exercise['title']}", expanded=True):
            st.write(exercise['description'])
            st.write("**Tasks to Complete:**")
            for task in exercise['tasks']:
                st.write(f"• {task}")
            
            user_solution = st.text_area(f"Your Solution {i+1}:", height=200, key=f"dml_exercise_{i}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Show Solution {i+1}"):
                    st.code(exercise['sample_solution'], language="sql")
            
            with col2:
                if st.button(f"Validate Solution {i+1}"):
                    if user_solution.strip():
                        st.success("Solution submitted! Review the sample solution for comparison.")
                    else:
                        st.warning("Please provide a solution before validating.")


def show_realworld_scenarios():
    """Show real-world DML scenarios."""
    st.subheader("🎯 Real-world Data Management Scenarios")
    
    scenarios = [
        {
            'title': "User Account Migration",
            'description': "Migrate user accounts from old system to new system with data transformation",
            'challenge': "Handle duplicate emails, normalize phone numbers, and update user preferences"
        },
        {
            'title': "Inventory Synchronization",
            'description': "Sync inventory data between warehouse and online store",
            'challenge': "Handle stock discrepancies, update prices, and manage product variations"
        },
        {
            'title': "Order Status Batch Update",
            'description': "Process shipping notifications and update order statuses",
            'challenge': "Update multiple orders, handle partial shipments, and notify customers"
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        with st.expander(f"Scenario {i+1}: {scenario['title']}", expanded=False):
            st.write(f"**Description:** {scenario['description']}")
            st.write(f"**Challenge:** {scenario['challenge']}")
            
            # Provide sample data for the scenario
            if i == 0:  # User migration
                st.write("**Sample Data to Process:**")
                sample_data = [
                    {'old_id': 1, 'email': 'JOHN.DOE@EXAMPLE.COM', 'phone': '555.123.4567', 'name': 'john doe'},
                    {'old_id': 2, 'email': 'jane@example.com', 'phone': '(555) 234-5678', 'name': 'Jane Smith'},
                ]
                st.dataframe(pd.DataFrame(sample_data))
            
            solution_area = st.text_area(f"Your Solution for Scenario {i+1}:", 
                                       height=150, key=f"scenario_{i}")
            
            if st.button(f"Submit Scenario {i+1} Solution"):
                if solution_area.strip():
                    st.success("Scenario solution submitted!")
                    # In a real application, this would be evaluated
                else:
                    st.warning("Please provide a solution.")


def show_performance_challenge():
    """Show DML performance optimization challenge."""
    st.subheader("🏆 DML Performance Optimization Challenge")
    
    st.write("**Challenge:** Optimize the following slow DML operations")
    
    slow_queries = [
        {
            'operation': 'Slow UPDATE',
            'query': """UPDATE products 
SET price = price * 1.1 
WHERE category = 'Electronics';""",
            'problem': 'No index on category column',
            'solution': 'CREATE INDEX idx_category ON products(category);'
        },
        {
            'operation': 'Inefficient INSERT',
            'query': """-- Individual inserts in a loop
INSERT INTO orders (customer_id, total) VALUES (1, 100.00);
INSERT INTO orders (customer_id, total) VALUES (2, 150.00);
-- ... thousands more""",
            'problem': 'Multiple individual INSERT statements',
            'solution': """INSERT INTO orders (customer_id, total) VALUES 
(1, 100.00), (2, 150.00), (3, 200.00) -- batch insert"""
        }
    ]
    
    for i, query_info in enumerate(slow_queries):
        with st.expander(f"Optimization Challenge {i+1}: {query_info['operation']}", expanded=True):
            st.write("**Problematic Query:**")
            st.code(query_info['query'], language="sql")
            
            st.write(f"**Problem:** {query_info['problem']}")
            
            user_optimization = st.text_area(f"Your Optimization {i+1}:", 
                                           height=100, key=f"optimization_{i}")
            
            if st.button(f"Show Optimal Solution {i+1}"):
                st.write("**Optimized Solution:**")
                st.code(query_info['solution'], language="sql")
    
    # Performance metrics simulation
    st.write("**Performance Impact Simulation:**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Before Optimization", "45.2 seconds", delta=None)
        st.metric("Rows Processed", "1,000,000", delta=None)
    
    with col2:
        st.metric("After Optimization", "2.8 seconds", delta="-42.4 seconds", delta_color="inverse")
        st.metric("Performance Gain", "16x faster", delta="+1500%", delta_color="normal")


# ================================
# MAIN FUNCTION
# ================================

def main():
    """Main function to display DML module content."""
    try:
        st.title("✏️ Data Manipulation Language (DML)")
        st.markdown("Master the art of data manipulation with INSERT, UPDATE, DELETE, and data transfer operations.")
        
        # Create tabs for different DML topics
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "➕ INSERT Operations",
            "✏️ UPDATE Operations", 
            "🗑️ DELETE Operations",
            "📥📤 Import/Export",
            "🧪 Practice Lab"
        ])
        
        with tab1:
            show_insert_operations()
        
        with tab2:
            show_update_operations()
        
        with tab3:
            show_delete_operations()
        
        with tab4:
            show_import_export()
        
        with tab5:
            show_practice_lab()
        
        # Footer
        st.markdown("---")
        st.markdown("**⚠️ Safety First:** Always backup your data before performing bulk DML operations!")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your database connection and try again.")


if __name__ == "__main__":
    main()