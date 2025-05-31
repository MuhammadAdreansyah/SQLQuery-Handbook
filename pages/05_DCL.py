"""
MySQL DCL (Data Control Language) Module

This module covers Data Control Language operations in MySQL including:
- User Management (CREATE USER, DROP USER, ALTER USER)
- Grant and Revoke Privileges (GRANT, REVOKE)
- Role Management
- Security and Authentication
- Privilege Levels and Types
- Access Control Best Practices

Author: MySQL Handbook
Version: 1.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import json

# Plotly imports with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.sidebar.warning("Plotly not available. Some visualizations will be disabled.")

# =============================================================================
# DATA MANAGEMENT FUNCTIONS
# =============================================================================

def get_sample_users():
    """Generate sample user data for demonstrations"""
    return [
        {
            'username': 'app_user',
            'host': 'localhost',
            'privileges': ['SELECT', 'INSERT', 'UPDATE'],
            'databases': ['ecommerce'],
            'created_date': '2024-01-15',
            'status': 'Active',
            'role': 'Application User'
        },
        {
            'username': 'analyst',
            'host': '%',
            'privileges': ['SELECT'],
            'databases': ['ecommerce', 'analytics'],
            'created_date': '2024-01-20',
            'status': 'Active',
            'role': 'Data Analyst'
        },
        {
            'username': 'backup_user',
            'host': '192.168.1.%',
            'privileges': ['SELECT', 'LOCK TABLES', 'SHOW VIEW'],
            'databases': ['*'],
            'created_date': '2024-01-10',
            'status': 'Active',
            'role': 'Backup Operator'
        },
        {
            'username': 'dev_user',
            'host': 'localhost',
            'privileges': ['ALL PRIVILEGES'],
            'databases': ['dev_db'],
            'created_date': '2024-02-01',
            'status': 'Active',
            'role': 'Developer'
        },
        {
            'username': 'guest_user',
            'host': '%',
            'privileges': ['SELECT'],
            'databases': ['public_data'],
            'created_date': '2024-02-10',
            'status': 'Locked',
            'role': 'Guest'
        }
    ]

def get_privilege_types():
    """Get MySQL privilege types categorized"""
    return {
        'Database Privileges': [
            'CREATE', 'DROP', 'GRANT OPTION', 'LOCK TABLES',
            'REFERENCES', 'EVENT', 'ALTER', 'DELETE', 'INDEX',
            'INSERT', 'SELECT', 'UPDATE', 'CREATE TEMPORARY TABLES',
            'TRIGGER', 'CREATE VIEW', 'SHOW VIEW', 'ALTER ROUTINE',
            'CREATE ROUTINE', 'EXECUTE'
        ],
        'Table Privileges': [
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE',
            'DROP', 'GRANT OPTION', 'INDEX', 'ALTER', 'REFERENCES',
            'TRIGGER', 'CREATE VIEW', 'SHOW VIEW'
        ],
        'Column Privileges': [
            'SELECT', 'INSERT', 'UPDATE', 'REFERENCES'
        ],
        'Global Privileges': [
            'ALL PRIVILEGES', 'CREATE USER', 'FILE', 'PROCESS',
            'RELOAD', 'REPLICATION CLIENT', 'REPLICATION SLAVE',
            'SHOW DATABASES', 'SHUTDOWN', 'SUPER', 'CREATE TABLESPACE',
            'CREATE ROLE', 'DROP ROLE'
        ],
        'Administrative Privileges': [
            'SUPER', 'PROCESS', 'RELOAD', 'SHUTDOWN', 'FILE',
            'CREATE USER', 'REPLICATION SLAVE', 'REPLICATION CLIENT',
            'SHOW DATABASES'
        ]
    }

def get_sample_roles():
    """Get sample role configurations"""
    return [
        {
            'role_name': 'db_reader',
            'description': 'Read-only access to specific databases',
            'privileges': ['SELECT', 'SHOW VIEW'],
            'scope': 'Database Level',
            'use_case': 'Data analysts, reporting users'
        },
        {
            'role_name': 'db_writer',
            'description': 'Read and write access to application tables',
            'privileges': ['SELECT', 'INSERT', 'UPDATE', 'DELETE'],
            'scope': 'Table Level',
            'use_case': 'Application users, data entry'
        },
        {
            'role_name': 'db_admin',
            'description': 'Full administrative access',
            'privileges': ['ALL PRIVILEGES'],
            'scope': 'Global Level',
            'use_case': 'Database administrators'
        },
        {
            'role_name': 'app_service',
            'description': 'Application service account',
            'privileges': ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE TEMPORARY TABLES'],
            'scope': 'Database Level',
            'use_case': 'Application backend services'
        },
        {
            'role_name': 'backup_operator',
            'description': 'Backup and maintenance operations',
            'privileges': ['SELECT', 'LOCK TABLES', 'SHOW VIEW', 'EVENT'],
            'scope': 'Global Level',
            'use_case': 'Backup systems, maintenance scripts'
        }
    ]

# =============================================================================
# THEORY SECTIONS
# =============================================================================

def show_dcl_introduction():
    """Introduction to DCL concepts"""
    st.header("🔐 Data Control Language (DCL) Introduction")
    
    st.markdown("""
    **Data Control Language (DCL)** adalah subset dari SQL yang digunakan untuk mengontrol akses ke data dalam database. 
    DCL memungkinkan administrator database untuk:
    
    - **Mengelola User dan Role** - Membuat, mengubah, dan menghapus user accounts
    - **Mengatur Privileges** - Memberikan dan mencabut hak akses
    - **Implementasi Security** - Mengatur authentication dan authorization
    - **Access Control** - Mengontrol siapa yang bisa mengakses data apa
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 DCL Commands")
        st.code("""
-- User Management
CREATE USER
ALTER USER
DROP USER
RENAME USER

-- Privilege Management
GRANT
REVOKE
SHOW GRANTS

-- Role Management (MySQL 8.0+)
CREATE ROLE
DROP ROLE
SET ROLE
        """, language="sql")
    
    with col2:
        st.subheader("🔑 Key Concepts")
        st.markdown("""
        **Authentication vs Authorization:**
        - **Authentication**: Memverifikasi identitas user
        - **Authorization**: Menentukan apa yang boleh dilakukan user
        
        **Privilege Levels:**
        - **Global**: Berlaku untuk seluruh server
        - **Database**: Berlaku untuk database tertentu
        - **Table**: Berlaku untuk tabel tertentu
        - **Column**: Berlaku untuk kolom tertentu
        - **Routine**: Berlaku untuk stored procedures/functions
        """)

def show_user_management():
    """User management concepts and examples"""
    st.header("👤 User Management")
    
    # User Creation Section
    st.subheader("1. Creating Users")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Basic User Creation:**")
        st.code("""
-- Create user with password
CREATE USER 'username'@'host' 
IDENTIFIED BY 'password';

-- Examples:
CREATE USER 'app_user'@'localhost' 
IDENTIFIED BY 'strong_password123';

CREATE USER 'remote_user'@'%' 
IDENTIFIED BY 'secure_pwd';

CREATE USER 'network_user'@'192.168.1.%' 
IDENTIFIED BY 'network_pwd';
        """, language="sql")
    
    with col2:
        st.markdown("**Advanced User Creation:**")
        st.code("""
-- With authentication plugin
CREATE USER 'auth_user'@'localhost' 
IDENTIFIED WITH mysql_native_password 
BY 'password';

-- With password expiration
CREATE USER 'temp_user'@'localhost' 
IDENTIFIED BY 'temp_pwd' 
PASSWORD EXPIRE INTERVAL 30 DAY;

-- Account locking
CREATE USER 'locked_user'@'localhost' 
IDENTIFIED BY 'password' 
ACCOUNT LOCK;
        """, language="sql")
    
    # User Modification Section
    st.subheader("2. Modifying Users")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Password Management:**")
        st.code("""
-- Change password
ALTER USER 'username'@'host' 
IDENTIFIED BY 'new_password';

-- Set password expiration
ALTER USER 'username'@'host' 
PASSWORD EXPIRE INTERVAL 60 DAY;

-- Never expire password
ALTER USER 'username'@'host' 
PASSWORD EXPIRE NEVER;

-- Force password change on next login
ALTER USER 'username'@'host' 
PASSWORD EXPIRE;
        """, language="sql")
    
    with col2:
        st.markdown("**Account Status:**")
        st.code("""
-- Lock account
ALTER USER 'username'@'host' 
ACCOUNT LOCK;

-- Unlock account
ALTER USER 'username'@'host' 
ACCOUNT UNLOCK;

-- Rename user
RENAME USER 'old_name'@'host' 
TO 'new_name'@'host';

-- Drop user
DROP USER 'username'@'host';
        """, language="sql")

def show_privilege_management():
    """Privilege management concepts and examples"""
    st.header("🎫 Privilege Management")
    
    # Grant Privileges Section
    st.subheader("1. Granting Privileges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Global Privileges:**")
        st.code("""
-- Grant global privileges
GRANT ALL PRIVILEGES ON *.* 
TO 'admin'@'localhost';

GRANT CREATE USER ON *.* 
TO 'user_manager'@'localhost';

GRANT REPLICATION SLAVE ON *.* 
TO 'replication_user'@'%';

-- Show global privileges
SHOW GRANTS FOR 'admin'@'localhost';
        """, language="sql")
    
    with col2:
        st.markdown("**Database Privileges:**")
        st.code("""
-- Grant database privileges
GRANT ALL PRIVILEGES ON ecommerce.* 
TO 'app_user'@'localhost';

GRANT SELECT, INSERT, UPDATE ON sales.* 
TO 'sales_user'@'%';

GRANT SELECT ON analytics.* 
TO 'analyst'@'%';

-- Multiple databases
GRANT SELECT ON db1.*, db2.* 
TO 'reader'@'localhost';
        """, language="sql")
    
    # Table and Column Privileges
    st.subheader("2. Table and Column Privileges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Table Level:**")
        st.code("""
-- Grant table privileges
GRANT SELECT, INSERT ON ecommerce.users 
TO 'app_user'@'localhost';

GRANT UPDATE (email, phone) ON ecommerce.users 
TO 'profile_updater'@'%';

GRANT DELETE ON ecommerce.orders 
TO 'order_manager'@'localhost';

-- With grant option
GRANT SELECT ON ecommerce.products 
TO 'product_viewer'@'%' 
WITH GRANT OPTION;
        """, language="sql")
    
    with col2:
        st.markdown("**Column Level:**")
        st.code("""
-- Grant column-specific privileges
GRANT SELECT (id, name, email) ON ecommerce.users 
TO 'limited_reader'@'%';

GRANT UPDATE (status) ON ecommerce.orders 
TO 'status_updater'@'localhost';

-- Insert specific columns
GRANT INSERT (name, email, phone) ON ecommerce.users 
TO 'registration_service'@'%';

-- Multiple columns with different privileges
GRANT SELECT (id, name), UPDATE (email) ON ecommerce.users 
TO 'profile_service'@'localhost';
        """, language="sql")
    
    # Revoke Privileges Section
    st.subheader("3. Revoking Privileges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Basic Revoke:**")
        st.code("""
-- Revoke specific privileges
REVOKE INSERT, UPDATE ON ecommerce.* 
FROM 'app_user'@'localhost';

-- Revoke all privileges on database
REVOKE ALL PRIVILEGES ON sales.* 
FROM 'sales_user'@'%';

-- Revoke global privileges
REVOKE CREATE USER ON *.* 
FROM 'user_manager'@'localhost';
        """, language="sql")
    
    with col2:
        st.markdown("**Advanced Revoke:**")
        st.code("""
-- Revoke grant option
REVOKE GRANT OPTION ON ecommerce.products 
FROM 'product_viewer'@'%';

-- Revoke column privileges
REVOKE SELECT (email, phone) ON ecommerce.users 
FROM 'limited_reader'@'%';

-- Revoke all privileges and grant option
REVOKE ALL PRIVILEGES, GRANT OPTION ON *.* 
FROM 'former_admin'@'localhost';
        """, language="sql")

def show_role_management():
    """Role management (MySQL 8.0+) concepts and examples"""
    st.header("🎭 Role Management (MySQL 8.0+)")
    
    st.info("**Note:** Role management is available in MySQL 8.0 and later versions.")
    
    # Role Creation Section
    st.subheader("1. Creating and Managing Roles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Role Creation:**")
        st.code("""
-- Create roles
CREATE ROLE 'db_reader';
CREATE ROLE 'db_writer';
CREATE ROLE 'db_admin';
CREATE ROLE 'app_service';

-- Grant privileges to roles
GRANT SELECT ON ecommerce.* TO 'db_reader';

GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.* 
TO 'db_writer';

GRANT ALL PRIVILEGES ON ecommerce.* TO 'db_admin';

-- Show role grants
SHOW GRANTS FOR 'db_reader';
        """, language="sql")
    
    with col2:
        st.markdown("**Role Assignment:**")
        st.code("""
-- Grant roles to users
GRANT 'db_reader' TO 'analyst'@'%';
GRANT 'db_writer' TO 'app_user'@'localhost';
GRANT 'db_admin' TO 'admin'@'localhost';

-- Grant multiple roles
GRANT 'db_reader', 'db_writer' 
TO 'power_user'@'localhost';

-- Set default roles
ALTER USER 'analyst'@'%' 
DEFAULT ROLE 'db_reader';

-- Activate roles for session
SET ROLE 'db_writer';
        """, language="sql")
    
    # Role Hierarchies
    st.subheader("2. Role Hierarchies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Nested Roles:**")
        st.code("""
-- Create role hierarchy
CREATE ROLE 'junior_dev';
CREATE ROLE 'senior_dev';
CREATE ROLE 'team_lead';

-- Grant basic privileges
GRANT SELECT ON dev_db.* TO 'junior_dev';

-- Build hierarchy
GRANT 'junior_dev' TO 'senior_dev';
GRANT SELECT, INSERT, UPDATE ON dev_db.* 
TO 'senior_dev';

GRANT 'senior_dev' TO 'team_lead';
GRANT ALL PRIVILEGES ON dev_db.* TO 'team_lead';
        """, language="sql")
    
    with col2:
        st.markdown("**Role Management:**")
        st.code("""
-- Check current roles
SELECT CURRENT_ROLE();

-- Show all roles for user
SHOW GRANTS FOR 'user'@'host' USING 'role_name';

-- Revoke role from user
REVOKE 'db_writer' FROM 'app_user'@'localhost';

-- Drop role
DROP ROLE 'old_role';

-- Mandatory roles (global setting)
SET GLOBAL mandatory_roles = 'db_reader';
        """, language="sql")

def show_security_best_practices():
    """Security best practices and guidelines"""
    st.header("🛡️ Security Best Practices")
    
    # Account Security
    st.subheader("1. Account Security")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Password Policies:**")
        st.code("""
-- Strong password requirements
ALTER USER 'username'@'host' 
IDENTIFIED BY 'Complex_Pass123!' 
PASSWORD REQUIRE CURRENT;

-- Password validation
INSTALL COMPONENT 'file://component_validate_password';

-- Set password policy
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 2;
SET GLOBAL validate_password.number_count = 2;
SET GLOBAL validate_password.special_char_count = 2;
        """, language="sql")
    
    with col2:
        st.markdown("**Connection Security:**")
        st.code("""
-- SSL requirements
ALTER USER 'secure_user'@'%' 
REQUIRE SSL;

-- Specific SSL requirements
ALTER USER 'cert_user'@'%' 
REQUIRE X509;

-- IP restriction
CREATE USER 'restricted_user'@'192.168.1.10' 
IDENTIFIED BY 'password';

-- Connection limits
ALTER USER 'limited_user'@'%' 
WITH MAX_CONNECTIONS_PER_HOUR 100 
MAX_USER_CONNECTIONS 5;
        """, language="sql")
    
    # Privilege Guidelines
    st.subheader("2. Privilege Guidelines")
    
    st.markdown("""
    **Principle of Least Privilege:**
    - Grant only the minimum privileges necessary
    - Use database-specific privileges instead of global
    - Regular privilege audits and cleanup
    - Separate accounts for different functions
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Good Practices:**")
        st.code("""
-- Application user - minimal privileges
CREATE USER 'app'@'localhost' 
IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* 
TO 'app'@'localhost';

-- Read-only analyst
CREATE USER 'analyst'@'%' 
IDENTIFIED BY 'secure_pwd';
GRANT SELECT ON reporting.* TO 'analyst'@'%';

-- Service account with specific privileges
CREATE USER 'backup_service'@'localhost' 
IDENTIFIED BY 'backup_pwd';
GRANT SELECT, LOCK TABLES ON *.* 
TO 'backup_service'@'localhost';
        """, language="sql")
    
    with col2:
        st.markdown("**❌ Bad Practices:**")
        st.code("""
-- Don't do this - too permissive
GRANT ALL PRIVILEGES ON *.* 
TO 'app_user'@'%' WITH GRANT OPTION;

-- Avoid weak passwords
CREATE USER 'user'@'%' 
IDENTIFIED BY '123456';

-- Don't use wildcards unnecessarily
CREATE USER 'admin'@'%' 
IDENTIFIED BY 'password';

-- Avoid shared accounts
CREATE USER 'shared_account'@'%' 
IDENTIFIED BY 'everyone_knows';
        """, language="sql")

# =============================================================================
# INTERACTIVE TOOLS
# =============================================================================

def user_management_tool():
    """Interactive user management tool"""
    st.header("🛠️ Interactive User Management Tool")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create User", "Manage Privileges", "Role Assignment", "User Audit"])
    
    with tab1:
        st.subheader("Create New User")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", value="new_user")
            host = st.selectbox("Host", ["localhost", "%", "192.168.1.%", "specific_ip"], index=0)
            if host == "specific_ip":
                host = st.text_input("Specific IP/Host", value="192.168.1.100")
            
            password = st.text_input("Password", type="password", value="")
            auth_plugin = st.selectbox("Authentication Plugin", 
                                     ["mysql_native_password", "caching_sha2_password", "sha256_password"])
        
        with col2:
            password_expire = st.selectbox("Password Expiration", 
                                         ["Default", "Never", "Custom Interval", "Immediate"])
            if password_expire == "Custom Interval":
                expire_days = st.number_input("Days until expiration", min_value=1, value=90)
            
            account_lock = st.checkbox("Lock Account Initially")
            max_connections = st.number_input("Max Connections Per Hour", min_value=0, value=0)
            max_user_connections = st.number_input("Max Concurrent Connections", min_value=0, value=0)
        
        if st.button("Generate CREATE USER Statement"):
            create_sql = f"CREATE USER '{username}'@'{host}'"
            
            if auth_plugin != "mysql_native_password":
                create_sql += f" IDENTIFIED WITH {auth_plugin}"
            
            if password:
                create_sql += f" BY '{'*' * len(password)}'"  # Hide actual password
            
            if password_expire == "Never":
                create_sql += " PASSWORD EXPIRE NEVER"
            elif password_expire == "Custom Interval":
                create_sql += f" PASSWORD EXPIRE INTERVAL {expire_days} DAY"
            elif password_expire == "Immediate":
                create_sql += " PASSWORD EXPIRE"
            
            if account_lock:
                create_sql += " ACCOUNT LOCK"
            
            if max_connections > 0:
                create_sql += f" WITH MAX_CONNECTIONS_PER_HOUR {max_connections}"
            
            if max_user_connections > 0:
                create_sql += f" MAX_USER_CONNECTIONS {max_user_connections}"
            
            create_sql += ";"
            
            st.code(create_sql, language="sql")
            
            st.success(f"✅ CREATE USER statement generated for '{username}'@'{host}'")
    
    with tab2:
        st.subheader("Privilege Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**User Selection:**")
            target_user = st.text_input("Username", value="app_user", key="priv_user")
            target_host = st.text_input("Host", value="localhost", key="priv_host")
            
            operation = st.radio("Operation", ["Grant", "Revoke"])
            
            privilege_level = st.selectbox("Privilege Level", 
                                         ["Global", "Database", "Table", "Column"])
        
        with col2:
            st.markdown("**Privilege Selection:**")
            
            if privilege_level == "Global":
                available_privs = get_privilege_types()["Global Privileges"]
                database = "*"
                table = "*"
            elif privilege_level == "Database":
                available_privs = get_privilege_types()["Database Privileges"]
                database = st.text_input("Database Name", value="ecommerce")
                table = "*"
            elif privilege_level == "Table":
                available_privs = get_privilege_types()["Table Privileges"]
                database = st.text_input("Database Name", value="ecommerce", key="table_db")
                table = st.text_input("Table Name", value="users")
            else:  # Column
                available_privs = get_privilege_types()["Column Privileges"]
                database = st.text_input("Database Name", value="ecommerce", key="col_db")
                table = st.text_input("Table Name", value="users", key="col_table")
                columns = st.text_input("Columns (comma-separated)", value="id, name, email")
            
            selected_privs = st.multiselect("Privileges", available_privs)
            with_grant_option = st.checkbox("WITH GRANT OPTION")
        
        if st.button("Generate Privilege Statement"):
            if selected_privs:
                privs_str = ", ".join(selected_privs)
                
                if privilege_level == "Column" and columns:
                    col_list = f" ({columns})"
                    target = f"{database}.{table}{col_list}"
                elif privilege_level in ["Table", "Database"]:
                    if table == "*":
                        target = f"{database}.*"
                    else:
                        target = f"{database}.{table}"
                else:  # Global
                    target = "*.*"
                
                if operation == "Grant":
                    sql = f"GRANT {privs_str} ON {target} TO '{target_user}'@'{target_host}'"
                    if with_grant_option:
                        sql += " WITH GRANT OPTION"
                else:
                    sql = f"REVOKE {privs_str} ON {target} FROM '{target_user}'@'{target_host}'"
                
                sql += ";"
                
                st.code(sql, language="sql")
                st.success(f"✅ {operation.upper()} statement generated")
            else:
                st.warning("⚠️ Please select at least one privilege")
    
    with tab3:
        st.subheader("Role Assignment")
        
        roles_data = get_sample_roles()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Available Roles:**")
            roles_df = pd.DataFrame(roles_data)
            st.dataframe(roles_df[['role_name', 'description', 'use_case']], use_container_width=True)
        
        with col2:
            st.markdown("**Role Assignment:**")
            role_user = st.text_input("Username", value="new_user", key="role_user")
            role_host = st.text_input("Host", value="localhost", key="role_host")
            
            selected_roles = st.multiselect("Select Roles", 
                                          [role['role_name'] for role in roles_data])
            
            set_default = st.checkbox("Set as Default Roles")
            
            if st.button("Generate Role Assignment"):
                if selected_roles:
                    roles_str = "', '".join(selected_roles)
                    grant_sql = f"GRANT '{roles_str}' TO '{role_user}'@'{role_host}';"
                    
                    st.code(grant_sql, language="sql")
                    
                    if set_default:
                        default_sql = f"ALTER USER '{role_user}'@'{role_host}' DEFAULT ROLE '{roles_str}';"
                        st.code(default_sql, language="sql")
                    
                    st.success("✅ Role assignment statements generated")
                else:
                    st.warning("⚠️ Please select at least one role")
    
    with tab4:
        st.subheader("User Audit Dashboard")
        
        users_data = get_sample_users()
        users_df = pd.DataFrame(users_data)
        
        # User Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", len(users_df))
        
        with col2:
            active_users = len(users_df[users_df['status'] == 'Active'])
            st.metric("Active Users", active_users)
        
        with col3:
            locked_users = len(users_df[users_df['status'] == 'Locked'])
            st.metric("Locked Users", locked_users)
        
        with col4:
            admin_users = len(users_df[users_df['role'].str.contains('Admin|admin')])
            st.metric("Admin Users", admin_users)
        
        # User Details Table
        st.markdown("**User Details:**")
        st.dataframe(users_df, use_container_width=True)
        
        # Privilege Distribution
        if PLOTLY_AVAILABLE:
            st.markdown("**Privilege Distribution:**")
            
            # Count privileges per user
            priv_counts = []
            for user in users_data:
                priv_counts.append({
                    'user': f"{user['username']}@{user['host']}",
                    'privilege_count': len(user['privileges']),
                    'role': user['role']
                })
            
            priv_df = pd.DataFrame(priv_counts)
            
            fig = px.bar(priv_df, x='user', y='privilege_count', 
                        color='role', title="Privileges per User")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

def privilege_analyzer():
    """Interactive privilege analyzer"""
    st.header("🔍 Privilege Analyzer")
    
    st.markdown("""
    Analyze and visualize privilege distributions across users and databases.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Privilege Matrix", "Security Assessment", "Recommendation Engine"])
    
    with tab1:
        st.subheader("User-Privilege Matrix")
        
        users_data = get_sample_users()
        privilege_types = get_privilege_types()
        
        # Create privilege matrix
        matrix_data = []
        all_privileges = set()
        
        for user in users_data:
            user_key = f"{user['username']}@{user['host']}"
            for priv in user['privileges']:
                all_privileges.add(priv)
                matrix_data.append({
                    'User': user_key,
                    'Privilege': priv,
                    'Database': ', '.join(user['databases']),
                    'Role': user['role'],
                    'Status': user['status']
                })
        
        if matrix_data:
            matrix_df = pd.DataFrame(matrix_data)
            
            # Pivot table for heatmap
            pivot_df = matrix_df.pivot_table(
                index='User', 
                columns='Privilege', 
                values='Status',
                aggfunc='count',
                fill_value=0
            )
            
            if PLOTLY_AVAILABLE:
                fig = px.imshow(pivot_df.values, 
                              x=pivot_df.columns, 
                              y=pivot_df.index,
                              title="User-Privilege Matrix",
                              color_continuous_scale='Blues')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Detailed Privilege Assignments:**")
            st.dataframe(matrix_df, use_container_width=True)
    
    with tab2:
        st.subheader("Security Assessment")
        
        # Security metrics
        users_data = get_sample_users()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Security Indicators:**")
            
            # Calculate security scores
            total_users = len(users_data)
            high_priv_users = 0
            weak_host_users = 0
            locked_users = 0
            
            for user in users_data:
                if 'ALL PRIVILEGES' in user['privileges']:
                    high_priv_users += 1
                if user['host'] == '%':
                    weak_host_users += 1
                if user['status'] == 'Locked':
                    locked_users += 1
            
            security_data = [
                {"Metric": "Users with ALL PRIVILEGES", "Count": high_priv_users, "Risk": "High"},
                {"Metric": "Users with wildcard host (%)", "Count": weak_host_users, "Risk": "Medium"},
                {"Metric": "Locked accounts", "Count": locked_users, "Risk": "Low"},
                {"Metric": "Active admin accounts", "Count": total_users - locked_users, "Risk": "Medium"}
            ]
            
            security_df = pd.DataFrame(security_data)
            st.dataframe(security_df, use_container_width=True)
        
        with col2:
            st.markdown("**Risk Assessment:**")
            
            if PLOTLY_AVAILABLE:
                risk_counts = security_df['Risk'].value_counts()
                
                fig = px.pie(values=risk_counts.values, 
                           names=risk_counts.index,
                           title="Risk Distribution",
                           color_discrete_map={
                               'High': '#ff4444',
                               'Medium': '#ffaa00', 
                               'Low': '#44ff44'
                           })
                st.plotly_chart(fig, use_container_width=True)
        
        # Security recommendations
        st.markdown("**Security Recommendations:**")
        
        recommendations = []
        
        if high_priv_users > 1:
            recommendations.append("🔴 **High Risk**: Multiple users have ALL PRIVILEGES. Consider using specific privileges instead.")
        
        if weak_host_users > 0:
            recommendations.append("🟡 **Medium Risk**: Users with wildcard hosts (%) detected. Consider restricting to specific IP ranges.")
        
        if locked_users == 0:
            recommendations.append("🟡 **Medium Risk**: No locked accounts found. Ensure unused accounts are properly locked.")
        
        recommendations.extend([
            "✅ **Best Practice**: Implement regular privilege audits",
            "✅ **Best Practice**: Use roles instead of direct privilege assignments", 
            "✅ **Best Practice**: Enable password expiration policies",
            "✅ **Best Practice**: Monitor failed login attempts"
        ])
        
        for rec in recommendations:
            st.markdown(rec)
    
    with tab3:
        st.subheader("Recommendation Engine")
        
        st.markdown("**Role-Based Access Control Recommendations:**")
        
        # Analyze current privileges and suggest roles
        users_data = get_sample_users()
        privilege_patterns = {}
        
        for user in users_data:
            pattern = tuple(sorted(user['privileges']))
            if pattern not in privilege_patterns:
                privilege_patterns[pattern] = []
            privilege_patterns[pattern].append(user)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Common Privilege Patterns:**")
            
            pattern_data = []
            for i, (pattern, users) in enumerate(privilege_patterns.items()):
                pattern_data.append({
                    'Pattern': f"Pattern {i+1}",
                    'Privileges': ', '.join(pattern),
                    'User Count': len(users),
                    'Suggested Role': f"role_pattern_{i+1}"
                })
            
            pattern_df = pd.DataFrame(pattern_data)
            st.dataframe(pattern_df, use_container_width=True)
        
        with col2:
            st.markdown("**Suggested Role Definitions:**")
            
            for i, (pattern, users) in enumerate(privilege_patterns.items()):
                if len(users) > 1:  # Only suggest roles for patterns used by multiple users
                    role_name = f"role_pattern_{i+1}"
                    st.code(f"""
-- Create role for {len(users)} users
CREATE ROLE '{role_name}';
GRANT {', '.join(pattern)} ON database.* TO '{role_name}';

-- Assign to users:
{chr(10).join([f"GRANT '{role_name}' TO '{user['username']}'@'{user['host']}';" for user in users])}
                    """, language="sql")
        
        # Migration recommendations
        st.markdown("**Migration Strategy:**")
        
        st.markdown("""
        **Phase 1: Role Creation**
        1. Create roles based on identified patterns
        2. Test roles with limited users
        3. Validate privilege inheritance
        
        **Phase 2: User Migration**
        1. Grant roles to users
        2. Set default roles
        3. Revoke direct privileges gradually
        
        **Phase 3: Cleanup**
        1. Remove unused direct privileges
        2. Consolidate similar roles
        3. Document role hierarchy
        """)

# =============================================================================
# PRACTICE LAB
# =============================================================================

def dcl_practice_lab():
    """Interactive practice lab for DCL operations"""
    st.header("🧪 DCL Practice Lab")
    
    st.markdown("""
    **Welcome to the DCL Practice Lab!** 
    
    Practice user management, privilege assignment, and security scenarios in a safe environment.
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Basic User Management", "Privilege Scenarios", "Role Implementation", "Security Challenges"])
    
    with tab1:
        st.subheader("Exercise 1: Basic User Management")
        
        st.markdown("""
        **Scenario:** You need to create user accounts for a new e-commerce application.
        
        **Requirements:**
        - Application user for localhost access
        - Analyst user for remote access
        - Backup user with restricted IP range
        - Service account with connection limits
        """)
        
        with st.expander("📝 Exercise Instructions"):
            st.markdown("""
            1. Create an application user 'ecomm_app' that can connect from localhost
            2. Create an analyst user 'data_analyst' that can connect from anywhere
            3. Create a backup user 'backup_svc' that can only connect from 192.168.1.0/24 network
            4. Set connection limits for the service account
            5. Lock the backup account initially for security
            """)
        
        exercise1_answer = st.text_area("Your SQL Solution:", height=200, key="ex1_dcl")
        
        if st.button("Check Exercise 1 Solution"):
            correct_solution = """-- Exercise 1 Solution:
CREATE USER 'ecomm_app'@'localhost' IDENTIFIED BY 'app_secure_password';

CREATE USER 'data_analyst'@'%' IDENTIFIED BY 'analyst_password' 
PASSWORD EXPIRE INTERVAL 60 DAY;

CREATE USER 'backup_svc'@'192.168.1.%' IDENTIFIED BY 'backup_password' 
WITH MAX_CONNECTIONS_PER_HOUR 10 
MAX_USER_CONNECTIONS 2 
ACCOUNT LOCK;

-- Unlock backup account when ready
ALTER USER 'backup_svc'@'192.168.1.%' ACCOUNT UNLOCK;"""
            
            st.code(correct_solution, language="sql")
            
            # Simple validation
            if "ecomm_app" in exercise1_answer and "localhost" in exercise1_answer:
                st.success("✅ Good! You created the application user correctly.")
            if "data_analyst" in exercise1_answer and "%" in exercise1_answer:
                st.success("✅ Excellent! Analyst user with wildcard host.")
            if "192.168.1.%" in exercise1_answer:
                st.success("✅ Perfect! Network-restricted backup user.")
            if "ACCOUNT LOCK" in exercise1_answer.upper():
                st.success("✅ Great security practice! Initially locked account.")
    
    with tab2:
        st.subheader("Exercise 2: Privilege Assignment Scenarios")
        
        scenarios = [
            {
                'title': "Application Database Access",
                'description': "Grant appropriate privileges for an e-commerce application",
                'requirements': [
                    "Read/write access to products, orders, customers tables",
                    "Read-only access to configuration tables",
                    "No access to admin or audit tables",
                    "No structural modification privileges"
                ]
            },
            {
                'title': "Data Analyst Access",
                'description': "Provide analytics access while maintaining security",
                'requirements': [
                    "Read-only access to all data tables",
                    "Access to create temporary tables for analysis",
                    "View access to reporting views",
                    "No modification or deletion privileges"
                ]
            },
            {
                'title': "Backup Service Account",
                'description': "Minimal privileges for backup operations",
                'requirements': [
                    "Read access to all databases",
                    "Lock tables privilege for consistent backups",
                    "Show view privilege for view definitions",
                    "No write or modification privileges"
                ]
            }
        ]
        
        selected_scenario = st.selectbox("Choose a scenario:", 
                                       [s['title'] for s in scenarios])
        
        scenario = next(s for s in scenarios if s['title'] == selected_scenario)
        
        st.markdown(f"**Scenario:** {scenario['description']}")
        st.markdown("**Requirements:**")
        for req in scenario['requirements']:
            st.markdown(f"- {req}")
        
        scenario_answer = st.text_area("Your privilege assignment solution:", 
                                     height=150, key=f"scenario_{selected_scenario}")
        
        if st.button("Show Scenario Solution"):
            if selected_scenario == "Application Database Access":
                solution = """-- Application Database Access Solution:
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.products TO 'ecomm_app'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.orders TO 'ecomm_app'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.customers TO 'ecomm_app'@'localhost';
GRANT SELECT ON ecommerce.config TO 'ecomm_app'@'localhost';
GRANT CREATE TEMPORARY TABLES ON ecommerce.* TO 'ecomm_app'@'localhost';"""
            
            elif selected_scenario == "Data Analyst Access":
                solution = """-- Data Analyst Access Solution:
GRANT SELECT ON ecommerce.* TO 'data_analyst'@'%';
GRANT CREATE TEMPORARY TABLES ON ecommerce.* TO 'data_analyst'@'%';
GRANT SHOW VIEW ON ecommerce.* TO 'data_analyst'@'%';
-- Explicitly deny sensitive tables if needed
-- REVOKE SELECT ON ecommerce.user_passwords FROM 'data_analyst'@'%';"""
            
            else:  # Backup Service Account
                solution = """-- Backup Service Account Solution:
GRANT SELECT ON *.* TO 'backup_svc'@'192.168.1.%';
GRANT LOCK TABLES ON *.* TO 'backup_svc'@'192.168.1.%';
GRANT SHOW VIEW ON *.* TO 'backup_svc'@'192.168.1.%';
GRANT EVENT ON *.* TO 'backup_svc'@'192.168.1.%';
GRANT TRIGGER ON *.* TO 'backup_svc'@'192.168.1.%';"""
            
            st.code(solution, language="sql")
    
    with tab3:
        st.subheader("Exercise 3: Role-Based Access Control")
        
        st.markdown("""
        **Challenge:** Implement a role-based access control system for a multi-tenant application.
        
        **Requirements:**
        - Create roles for different user types
        - Implement role hierarchy
        - Assign roles to users
        - Set up default roles
        """)
        
        role_exercise = st.text_area("Design your RBAC system:", height=250, key="rbac_exercise")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Show Role Hierarchy Example"):
                st.code("""
-- Role Hierarchy Implementation
CREATE ROLE 'tenant_reader';
CREATE ROLE 'tenant_writer'; 
CREATE ROLE 'tenant_admin';
CREATE ROLE 'system_admin';

-- Base privileges
GRANT SELECT ON app.* TO 'tenant_reader';

-- Build hierarchy
GRANT 'tenant_reader' TO 'tenant_writer';
GRANT SELECT, INSERT, UPDATE, DELETE ON app.tenant_data TO 'tenant_writer';

GRANT 'tenant_writer' TO 'tenant_admin';
GRANT CREATE, DROP ON app.tenant_data TO 'tenant_admin';

GRANT 'tenant_admin' TO 'system_admin';
GRANT ALL PRIVILEGES ON app.* TO 'system_admin';
                """, language="sql")
        
        with col2:
            if st.button("Show User Assignment Example"):
                st.code("""
-- User Role Assignments
GRANT 'tenant_reader' TO 'analyst'@'%';
GRANT 'tenant_writer' TO 'app_user'@'localhost';
GRANT 'tenant_admin' TO 'tenant_mgr'@'%';
GRANT 'system_admin' TO 'sys_admin'@'localhost';

-- Set default roles
ALTER USER 'analyst'@'%' DEFAULT ROLE 'tenant_reader';
ALTER USER 'app_user'@'localhost' DEFAULT ROLE 'tenant_writer';
ALTER USER 'tenant_mgr'@'%' DEFAULT ROLE 'tenant_admin';
ALTER USER 'sys_admin'@'localhost' DEFAULT ROLE 'system_admin';
                """, language="sql")
    
    with tab4:
        st.subheader("Exercise 4: Security Challenges")
        
        st.markdown("""
        **Security Audit Challenge:** You've inherited a MySQL system with poor security practices. 
        Identify and fix the security issues.
        """)
        
        with st.expander("📋 Current System State"):
            st.code("""
-- Current problematic setup:
CREATE USER 'admin'@'%' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;

CREATE USER 'app'@'%' IDENTIFIED BY 'app';
GRANT ALL PRIVILEGES ON *.* TO 'app'@'%';

CREATE USER 'backup'@'%' IDENTIFIED BY '';
GRANT SELECT ON *.* TO 'backup'@'%';

CREATE USER 'test'@'%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'%';

-- Additional issues:
-- No password expiration
-- No connection limits
-- Overprivileged accounts
-- Weak passwords
-- Wildcard hosts everywhere
            """, language="sql")
        
        security_fixes = st.text_area("Your security improvements:", height=300, key="security_fixes")
        
        if st.button("Show Security Fix Recommendations"):
            st.code("""
-- Security Improvements:

-- 1. Fix admin account
DROP USER 'admin'@'%';
CREATE USER 'db_admin'@'localhost' IDENTIFIED BY 'StrongAdminPass123!';
GRANT ALL PRIVILEGES ON app_db.* TO 'db_admin'@'localhost';
ALTER USER 'db_admin'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;

-- 2. Fix application account
DROP USER 'app'@'%';
CREATE USER 'app_service'@'192.168.1.%' IDENTIFIED BY 'SecureAppPassword456!';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_service'@'192.168.1.%';
ALTER USER 'app_service'@'192.168.1.%' 
WITH MAX_CONNECTIONS_PER_HOUR 1000 MAX_USER_CONNECTIONS 10;

-- 3. Fix backup account
DROP USER 'backup'@'%';
CREATE USER 'backup_service'@'192.168.1.100' IDENTIFIED BY 'BackupSecure789!';
GRANT SELECT, LOCK TABLES ON *.* TO 'backup_service'@'192.168.1.100';
ALTER USER 'backup_service'@'192.168.1.100' 
WITH MAX_CONNECTIONS_PER_HOUR 24 MAX_USER_CONNECTIONS 1;

-- 4. Remove test account
DROP USER 'test'@'%';

-- 5. Implement role-based access
CREATE ROLE 'app_role';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_role';
GRANT 'app_role' TO 'app_service'@'192.168.1.%';

-- 6. Enable audit logging and monitoring
-- SET GLOBAL general_log = 'ON';
-- Install audit plugin for production
            """, language="sql")
            
            st.markdown("""
            **Key Security Improvements Made:**
            
            1. **Strong Passwords**: Replaced weak passwords with complex ones
            2. **Host Restrictions**: Limited access to specific IP ranges instead of wildcards
            3. **Privilege Minimization**: Granted only necessary privileges
            4. **Connection Limits**: Added resource limitations
            5. **Password Policies**: Implemented password expiration
            6. **Account Cleanup**: Removed unnecessary test accounts
            7. **Role-Based Access**: Implemented RBAC for better management
            8. **Audit Trail**: Recommended audit logging for monitoring
            """)

# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Main function to run the DCL module"""
    st.set_page_config(
        page_title="MySQL DCL - Data Control Language",
        page_icon="🔐",
        layout="wide"
    )
    
    # Sidebar Navigation
    st.sidebar.title("🔐 DCL Navigation")
    
    section = st.sidebar.radio(
        "Choose Section:",
        [
            "📚 Introduction",
            "👤 User Management", 
            "🎫 Privilege Management",
            "🎭 Role Management",
            "🛡️ Security Best Practices",
            "🛠️ Interactive Tools",
            "🔍 Privilege Analyzer",
            "🧪 Practice Lab"
        ]
    )
    
    # Sidebar Tips
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 DCL Tips")
    st.sidebar.info("""
    **Best Practices:**
    - Use principle of least privilege
    - Implement strong password policies
    - Regular privilege audits
    - Use roles for better management
    - Monitor authentication attempts
    """)
    
    st.sidebar.markdown("### 🔗 Quick References")
    st.sidebar.markdown("""
    - [MySQL User Management](https://dev.mysql.com/doc/refman/8.0/en/user-management.html)
    - [Privilege System](https://dev.mysql.com/doc/refman/8.0/en/privilege-system.html)
    - [Role Management](https://dev.mysql.com/doc/refman/8.0/en/roles.html)
    - [Security Guidelines](https://dev.mysql.com/doc/refman/8.0/en/security-guidelines.html)
    """)
    
    # Main Content
    if section == "📚 Introduction":
        show_dcl_introduction()
    elif section == "👤 User Management":
        show_user_management()
    elif section == "🎫 Privilege Management":
        show_privilege_management()
    elif section == "🎭 Role Management":
        show_role_management()
    elif section == "🛡️ Security Best Practices":
        show_security_best_practices()
    elif section == "🛠️ Interactive Tools":
        user_management_tool()
    elif section == "🔍 Privilege Analyzer":
        privilege_analyzer()
    elif section == "🧪 Practice Lab":
        dcl_practice_lab()

if __name__ == "__main__":
    main()