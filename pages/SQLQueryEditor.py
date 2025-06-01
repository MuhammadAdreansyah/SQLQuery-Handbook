"""
MySQL Handbook - SQL Query Editor Module

Interactive SQL Query Editor with syntax highlighting, query validation,
result visualization, and educational features.

Features:
- Syntax-highlighted SQL editor
- Query execution simulation
- Result set visualization
- Query optimization suggestions
- Educational examples and templates
- Query history and favorites

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
import random

# Check for plotly availability
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ================================
# SAMPLE DATA GENERATION
# ================================

def get_sample_database():
    """Generate sample database with multiple tables for query testing."""
    
    # Customers table
    customers = []
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Tom', 'Anna', 'Chris', 'Emma']
    last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller', 'Moore', 'Taylor', 'Anderson', 'Thomas']
    
    for i in range(1, 51):
        customers.append({
            'customer_id': i,
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'customer{i}@email.com',
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            'state': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
            'registration_date': datetime.now() - timedelta(days=random.randint(1, 365)),
            'status': random.choice(['Active', 'Inactive', 'Suspended'])
        })
    
    # Products table
    products = []
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys']
    product_names = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress'],
        'Books': ['Fiction Novel', 'Programming Book', 'History Book', 'Science Book', 'Art Book'],
        'Home & Garden': ['Chair', 'Table', 'Lamp', 'Plant', 'Vase'],
        'Sports': ['Basketball', 'Tennis Racket', 'Running Shoes', 'Yoga Mat', 'Dumbbells'],
        'Toys': ['Action Figure', 'Puzzle', 'Board Game', 'Doll', 'RC Car']
    }
    
    for i in range(1, 101):
        category = random.choice(categories)
        products.append({
            'product_id': i,
            'product_name': random.choice(product_names[category]),
            'category': category,
            'price': round(random.uniform(10, 500), 2),
            'stock_quantity': random.randint(0, 100),
            'supplier_id': random.randint(1, 10),
            'created_date': datetime.now() - timedelta(days=random.randint(1, 180))
        })
    
    # Orders table
    orders = []
    for i in range(1, 201):
        order_date = datetime.now() - timedelta(days=random.randint(1, 90))
        orders.append({
            'order_id': i,
            'customer_id': random.randint(1, 50),
            'order_date': order_date,
            'total_amount': round(random.uniform(20, 1000), 2),
            'status': random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']),
            'shipping_address': f'{random.randint(100, 9999)} Main St',
            'payment_method': random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])
        })
    
    # Order Items table
    order_items = []
    for i in range(1, 401):
        order_items.append({
            'order_item_id': i,
            'order_id': random.randint(1, 200),
            'product_id': random.randint(1, 100),
            'quantity': random.randint(1, 5),
            'unit_price': round(random.uniform(10, 500), 2)
        })
    
    # Suppliers table
    suppliers = []
    company_types = ['Corp', 'Inc', 'LLC', 'Ltd']
    for i in range(1, 11):
        suppliers.append({
            'supplier_id': i,
            'company_name': f'Supplier {i} {random.choice(company_types)}',
            'contact_name': f'{random.choice(first_names)} {random.choice(last_names)}',
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'email': f'contact@supplier{i}.com',
            'country': random.choice(['USA', 'Canada', 'Mexico', 'UK', 'Germany'])
        })
    
    return {
        'customers': pd.DataFrame(customers),
        'products': pd.DataFrame(products),
        'orders': pd.DataFrame(orders),
        'order_items': pd.DataFrame(order_items),
        'suppliers': pd.DataFrame(suppliers)
    }

# ================================
# QUERY TEMPLATES AND EXAMPLES
# ================================

def get_query_templates():
    """Get predefined query templates for education."""
    return {
        'Basic SELECT': {
            'description': 'Simple SELECT statement',
            'template': 'SELECT column1, column2 FROM table_name;',
            'example': 'SELECT first_name, last_name, email FROM customers;'
        },
        'SELECT with WHERE': {
            'description': 'Filtered SELECT with conditions',
            'template': 'SELECT * FROM table_name WHERE condition;',
            'example': "SELECT * FROM products WHERE category = 'Electronics' AND price > 100;"
        },
        'JOIN Query': {
            'description': 'Inner join between tables',
            'template': 'SELECT t1.col, t2.col FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id;',
            'example': '''SELECT c.first_name, c.last_name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;'''
        },
        'GROUP BY': {
            'description': 'Aggregation with grouping',
            'template': 'SELECT column, COUNT(*) FROM table_name GROUP BY column;',
            'example': '''SELECT category, COUNT(*) as product_count, AVG(price) as avg_price
FROM products 
GROUP BY category;'''
        },
        'Subquery': {
            'description': 'Query with subquery',
            'template': 'SELECT * FROM table1 WHERE column IN (SELECT column FROM table2);',
            'example': '''SELECT product_name, price 
FROM products 
WHERE product_id IN (
    SELECT DISTINCT product_id 
    FROM order_items
);'''
        },
        'Window Function': {
            'description': 'Query with window functions',
            'template': 'SELECT column, ROW_NUMBER() OVER (PARTITION BY col ORDER BY col) FROM table;',
            'example': '''SELECT 
    customer_id, 
    order_date, 
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_number
FROM orders;'''
        }
    }

def get_sample_queries():
    """Get sample queries for different difficulty levels."""
    return {
        'Beginner': [
            "SELECT * FROM customers LIMIT 10;",
            "SELECT first_name, last_name FROM customers WHERE city = 'New York';",
            "SELECT COUNT(*) FROM products;",
            "SELECT * FROM orders WHERE status = 'Delivered';"
        ],
        'Intermediate': [
            '''SELECT c.first_name, c.last_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;''',
            
            '''SELECT p.category, AVG(p.price) as avg_price
FROM products p
WHERE p.stock_quantity > 0
GROUP BY p.category
HAVING AVG(p.price) > 50;''',
            
            '''SELECT o.order_id, o.order_date, SUM(oi.quantity * oi.unit_price) as calculated_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date;'''
        ],
        'Advanced': [
            '''WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    first_name,
    last_name,
    total_orders,
    total_spent,
    CASE 
        WHEN total_spent > 500 THEN 'Gold'
        WHEN total_spent > 200 THEN 'Silver'
        ELSE 'Bronze'
    END as customer_tier
FROM customer_stats
ORDER BY total_spent DESC;''',
            
            '''SELECT 
    p.product_name,
    p.category,
    p.price,
    AVG(p.price) OVER (PARTITION BY p.category) as category_avg_price,
    p.price - AVG(p.price) OVER (PARTITION BY p.category) as price_difference
FROM products p
ORDER BY p.category, p.price DESC;'''
        ]
    }

# ================================
# QUERY ANALYZER AND VALIDATOR
# ================================

class QueryAnalyzer:
    """Analyze and validate SQL queries."""
    
    @staticmethod
    def analyze_query(query):
        """Analyze SQL query and provide insights."""
        query_upper = query.upper().strip()
        
        analysis = {
            'query_type': QueryAnalyzer.get_query_type(query_upper),
            'tables_used': QueryAnalyzer.extract_tables(query),
            'complexity': QueryAnalyzer.assess_complexity(query_upper),
            'suggestions': QueryAnalyzer.get_suggestions(query_upper),
            'estimated_performance': QueryAnalyzer.estimate_performance(query_upper)
        }
        
        return analysis
    
    @staticmethod
    def get_query_type(query_upper):
        """Determine the type of SQL query."""
        if query_upper.startswith('SELECT'):
            return 'SELECT'
        elif query_upper.startswith('INSERT'):
            return 'INSERT'
        elif query_upper.startswith('UPDATE'):
            return 'UPDATE'
        elif query_upper.startswith('DELETE'):
            return 'DELETE'
        elif query_upper.startswith('CREATE'):
            return 'CREATE'
        elif query_upper.startswith('ALTER'):
            return 'ALTER'
        elif query_upper.startswith('DROP'):
            return 'DROP'
        else:
            return 'UNKNOWN'
    
    @staticmethod
    def extract_tables(query):
        """Extract table names from query."""
        # Simple regex to find table names (not perfect but good for demo)
        patterns = [
            r'FROM\s+(\w+)',
            r'JOIN\s+(\w+)',
            r'UPDATE\s+(\w+)',
            r'INSERT\s+INTO\s+(\w+)',
            r'DELETE\s+FROM\s+(\w+)'
        ]
        
        tables = set()
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tables.update(matches)
        
        return list(tables)
    
    @staticmethod
    def assess_complexity(query_upper):
        """Assess query complexity based on keywords."""
        complexity_score = 0
        
        # Basic complexity indicators
        if 'JOIN' in query_upper:
            complexity_score += 2
        if 'SUBQUERY' in query_upper or '(' in query_upper:
            complexity_score += 3
        if 'WINDOW' in query_upper or 'OVER' in query_upper:
            complexity_score += 4
        if 'WITH' in query_upper:  # CTE
            complexity_score += 3
        if 'UNION' in query_upper:
            complexity_score += 2
        if 'GROUP BY' in query_upper:
            complexity_score += 1
        if 'ORDER BY' in query_upper:
            complexity_score += 1
        
        if complexity_score <= 2:
            return 'Simple'
        elif complexity_score <= 5:
            return 'Intermediate'
        else:
            return 'Complex'
    
    @staticmethod
    def get_suggestions(query_upper):
        """Generate optimization suggestions."""
        suggestions = []
        
        if 'SELECT *' in query_upper:
            suggestions.append("⚠️ Consider specifying column names instead of SELECT * for better performance")
        
        if 'WHERE' not in query_upper and 'SELECT' in query_upper:
            suggestions.append("💡 Consider adding WHERE clause to filter results")
        
        if 'LIMIT' not in query_upper and 'SELECT' in query_upper:
            suggestions.append("💡 Consider adding LIMIT clause for large datasets")
        
        if 'INDEX' not in query_upper and 'WHERE' in query_upper:
            suggestions.append("🔍 Ensure columns in WHERE clause are indexed")
        
        if query_upper.count('JOIN') > 3:
            suggestions.append("⚠️ Multiple JOINs detected - consider query optimization")
        
        return suggestions
    
    @staticmethod
    def estimate_performance(query_upper):
        """Estimate query performance."""
        if 'JOIN' in query_upper and 'WHERE' not in query_upper:
            return 'Poor - JOINs without WHERE clauses can be slow'
        elif query_upper.count('JOIN') > 2:
            return 'Moderate - Multiple JOINs may impact performance'
        elif 'SELECT *' in query_upper:
            return 'Moderate - SELECT * may return unnecessary data'
        else:
            return 'Good - Query looks optimized'

# ================================
# QUERY EXECUTOR (SIMULATION)
# ================================

class QueryExecutor:
    """Simulate query execution on sample data."""
    
    def __init__(self, database):
        self.database = database
    
    def execute_query(self, query):
        """Execute SQL query on sample data (simulation)."""
        try:
            # Simple query parsing and execution simulation
            query_clean = query.strip().rstrip(';')
            
            if query_clean.upper().startswith('SELECT'):
                return self.execute_select(query_clean)
            elif query_clean.upper().startswith('SHOW TABLES'):
                return self.show_tables()
            elif query_clean.upper().startswith('DESCRIBE') or query_clean.upper().startswith('DESC'):
                return self.describe_table(query_clean)
            else:
                return {
                    'success': False,
                    'error': 'Only SELECT, SHOW TABLES, and DESCRIBE queries are supported in this demo',
                    'result': None
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'result': None
            }
    
    def execute_select(self, query):
        """Execute SELECT query simulation."""
        # This is a simplified simulation - real implementation would use SQL parser
        query_upper = query.upper()
        
        # Extract table name (simplified)
        if 'FROM' in query_upper:
            parts = query.split()
            from_index = -1
            for i, part in enumerate(parts):
                if part.upper() == 'FROM':
                    from_index = i
                    break
            
            if from_index != -1 and from_index + 1 < len(parts):
                table_name = parts[from_index + 1].replace(',', '').replace(';', '')
                
                if table_name in self.database:
                    df = self.database[table_name].copy()
                    
                    # Apply LIMIT if present
                    if 'LIMIT' in query_upper:
                        limit_match = re.search(r'LIMIT\s+(\d+)', query, re.IGNORECASE)
                        if limit_match:
                            limit_val = int(limit_match.group(1))
                            df = df.head(limit_val)
                    
                    # If no specific columns mentioned, return first 10 rows
                    if df.shape[0] > 10 and 'LIMIT' not in query_upper:
                        df = df.head(10)
                        note = f"Showing first 10 rows of {df.shape[0]} total rows"
                    else:
                        note = f"Returned {df.shape[0]} rows"
                    
                    return {
                        'success': True,
                        'result': df,
                        'rows_affected': len(df),
                        'note': note
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Table '{table_name}' not found",
                        'result': None
                    }
        
        return {
            'success': False,
            'error': 'Could not parse query',
            'result': None
        }
    
    def show_tables(self):
        """Show available tables."""
        tables_df = pd.DataFrame({
            'Table': list(self.database.keys()),
            'Rows': [len(df) for df in self.database.values()],
            'Columns': [len(df.columns) for df in self.database.values()]
        })
        
        return {
            'success': True,
            'result': tables_df,
            'rows_affected': len(tables_df)
        }
    
    def describe_table(self, query):
        """Describe table structure."""
        parts = query.split()
        if len(parts) >= 2:
            table_name = parts[1].replace(';', '')
            
            if table_name in self.database:
                df = self.database[table_name]
                
                # Create table description
                desc_data = []
                for col in df.columns:
                    dtype = str(df[col].dtype)
                    desc_data.append({
                        'Column': col,
                        'Type': dtype,
                        'Null': 'YES',  # Simplified
                        'Key': '',      # Simplified
                        'Default': None,
                        'Extra': ''
                    })
                
                desc_df = pd.DataFrame(desc_data)
                
                return {
                    'success': True,
                    'result': desc_df,
                    'rows_affected': len(desc_df)
                }
            else:
                return {
                    'success': False,
                    'error': f"Table '{table_name}' not found",
                    'result': None
                }
        
        return {
            'success': False,
            'error': 'Invalid DESCRIBE syntax',
            'result': None
        }

# ================================
# MAIN UI COMPONENTS
# ================================

def show_query_editor():
    """Main query editor interface."""
    st.header("💻 Interactive SQL Query Editor")
    st.markdown("Practice your MySQL skills with our interactive query environment!")
    
    # Initialize database
    if 'database' not in st.session_state:
        st.session_state.database = get_sample_database()
        st.session_state.query_history = []
        st.session_state.favorites = []
    
    # Create executor
    executor = QueryExecutor(st.session_state.database)
    
    # Sidebar
    show_editor_sidebar()
    
    # Main editor area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_main_editor(executor)
    
    with col2:
        show_query_assistant()

def show_main_editor(executor):
    """Main SQL editor interface."""
    st.subheader("📝 SQL Query Editor")
    
    # Query input
    query = st.text_area(
        "Enter your SQL query:",
        height=200,
        placeholder="SELECT * FROM customers LIMIT 10;",
        help="Write your SQL query here. Use Ctrl+Enter to execute."
    )
    
    # Execute button and options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        execute_button = st.button("🚀 Execute Query", type="primary")
    
    with col2:
        analyze_button = st.button("🔍 Analyze Query")
    
    with col3:
        save_button = st.button("💾 Save Query")
    
    # Execute query
    if execute_button and query.strip():
        with st.spinner("Executing query..."):
            result = executor.execute_query(query)
            show_query_results(result)
            
            # Add to history
            if query not in st.session_state.query_history:
                st.session_state.query_history.append({
                    'query': query,
                    'timestamp': datetime.now(),
                    'success': result['success']
                })
    
    # Analyze query
    if analyze_button and query.strip():
        show_query_analysis(query)
    
    # Save query
    if save_button and query.strip():
        st.session_state.favorites.append({
            'query': query,
            'name': f"Query {len(st.session_state.favorites) + 1}",
            'timestamp': datetime.now()
        })
        st.success("✅ Query saved to favorites!")

def show_query_results(result):
    """Display query execution results."""
    st.subheader("📊 Query Results")
    
    if result['success']:
        st.success(f"✅ Query executed successfully")
        
        if result['result'] is not None:
            # Show result dataframe
            st.dataframe(result['result'], use_container_width=True)
            
            # Show additional info
            if 'note' in result:
                st.info(result['note'])
            
            # Visualization option
            if len(result['result']) > 0 and PLOTLY_AVAILABLE:
                show_result_visualization(result['result'])
        
        else:
            st.info("Query executed but returned no results")
    
    else:
        st.error(f"❌ Query failed: {result['error']}")

def show_result_visualization(df):
    """Show visualization options for query results."""
    with st.expander("📈 Visualize Results", expanded=False):
        if len(df) == 0:
            st.warning("No data to visualize")
            return
        
        # Detect numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.info("No numeric columns found for visualization")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            chart_type = st.selectbox("Chart Type:", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
        
        with col2:
            if chart_type in ["Bar Chart", "Pie Chart"] and categorical_cols:
                x_col = st.selectbox("Category Column:", categorical_cols)
            else:
                x_col = st.selectbox("X Column:", df.columns.tolist())
        
        if len(numeric_cols) > 0:
            y_col = st.selectbox("Y Column:", numeric_cols)
            
            try:
                if chart_type == "Bar Chart":
                    if x_col in categorical_cols:
                        # Group by categorical column and sum numeric
                        chart_data = df.groupby(x_col)[y_col].sum().reset_index()
                        fig = px.bar(chart_data, x=x_col, y=y_col)
                    else:
                        fig = px.bar(df, x=x_col, y=y_col)
                
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_col, y=y_col)
                
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_col, y=y_col)
                
                elif chart_type == "Pie Chart" and x_col in categorical_cols:
                    chart_data = df.groupby(x_col)[y_col].sum().reset_index()
                    fig = px.pie(chart_data, names=x_col, values=y_col)
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating visualization: {str(e)}")

def show_query_analysis(query):
    """Show query analysis results."""
    st.subheader("🔍 Query Analysis")
    
    analyzer = QueryAnalyzer()
    analysis = analyzer.analyze_query(query)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Query Type", analysis['query_type'])
        st.metric("Complexity", analysis['complexity'])
        
        if analysis['tables_used']:
            st.write("**Tables Used:**")
            for table in analysis['tables_used']:
                st.write(f"- {table}")
    
    with col2:
        st.write("**Performance Estimate:**")
        st.write(analysis['estimated_performance'])
        
        if analysis['suggestions']:
            st.write("**Suggestions:**")
            for suggestion in analysis['suggestions']:
                st.write(suggestion)

def show_editor_sidebar():
    """Show query editor sidebar."""
    with st.sidebar:
        st.markdown("### 📚 Quick Reference")
        
        # Database schema
        with st.expander("🗃️ Database Schema", expanded=True):
            st.markdown("""
            **Available Tables:**
            - `customers` (50 rows)
            - `products` (100 rows)  
            - `orders` (200 rows)
            - `order_items` (400 rows)
            - `suppliers` (10 rows)
            
            **Quick Commands:**
            - `SHOW TABLES;`
            - `DESCRIBE table_name;`
            """)
        
        # Query templates
        with st.expander("📋 Query Templates"):
            templates = get_query_templates()
            
            selected_template = st.selectbox(
                "Choose template:",
                list(templates.keys())
            )
            
            if selected_template:
                template_info = templates[selected_template]
                st.markdown(f"**{template_info['description']}**")
                st.code(template_info['example'], language="sql")
        
        # Sample queries
        with st.expander("💡 Sample Queries"):
            difficulty = st.selectbox("Difficulty:", ["Beginner", "Intermediate", "Advanced"])
            
            sample_queries = get_sample_queries()
            if difficulty in sample_queries:
                for i, query in enumerate(sample_queries[difficulty]):
                    if st.button(f"Load Query {i+1}", key=f"sample_{difficulty}_{i}"):
                        st.session_state.selected_query = query

def show_query_assistant():
    """Show query assistant panel."""
    st.subheader("🤖 Query Assistant")
    
    # Query history
    with st.expander("📜 Query History", expanded=False):
        if st.session_state.query_history:
            for i, hist in enumerate(reversed(st.session_state.query_history[-10:])):
                status_icon = "✅" if hist['success'] else "❌"
                timestamp = hist['timestamp'].strftime("%H:%M:%S")
                
                if st.button(f"{status_icon} {timestamp}", key=f"hist_{i}"):
                    st.session_state.selected_query = hist['query']
                
                # Show truncated query
                query_preview = hist['query'][:50] + "..." if len(hist['query']) > 50 else hist['query']
                st.caption(query_preview)
        else:
            st.info("No query history yet")
    
    # Favorites
    with st.expander("⭐ Favorite Queries", expanded=False):
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(fav['name'], key=f"fav_{i}"):
                        st.session_state.selected_query = fav['query']
                
                with col2:
                    if st.button("🗑️", key=f"del_fav_{i}"):
                        st.session_state.favorites.pop(i)
                        st.rerun()
        else:
            st.info("No saved queries yet")
    
    # Learning resources
    with st.expander("📖 Learning Resources"):
        st.markdown("""
        **SQL Basics:**
        - SELECT statements
        - WHERE conditions
        - JOIN operations
        - GROUP BY aggregation
        
        **Advanced Topics:**
        - Window functions
        - Common Table Expressions (CTEs)
        - Subqueries
        - Performance optimization
        """)

# ================================
# ADDITIONAL FEATURES
# ================================

def show_query_builder():
    """Visual query builder interface."""
    st.subheader("🔧 Visual Query Builder")
    st.info("Visual query builder is under development. Coming soon!")
    
    # Placeholder for visual query builder
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Select Table:**")
        tables = ['customers', 'products', 'orders', 'order_items', 'suppliers']
        selected_table = st.selectbox("Table:", tables)
        
        st.markdown("**Select Columns:**")
        if selected_table == 'customers':
            columns = ['customer_id', 'first_name', 'last_name', 'email', 'city', 'state']
        elif selected_table == 'products':
            columns = ['product_id', 'product_name', 'category', 'price', 'stock_quantity']
        else:
            columns = ['*']
        
        selected_columns = st.multiselect("Columns:", columns, default=columns[:3])
    
    with col2:
        st.markdown("**Add Conditions:**")
        add_where = st.checkbox("Add WHERE clause")
        
        if add_where:
            where_column = st.selectbox("Column:", columns)
            operator = st.selectbox("Operator:", ['=', '>', '<', '>=', '<=', 'LIKE'])
            where_value = st.text_input("Value:")
        
        add_limit = st.checkbox("Add LIMIT")
        if add_limit:
            limit_value = st.number_input("Limit:", min_value=1, value=10)
    
    if st.button("🏗️ Build Query"):
        # Generate query based on selections
        query_parts = []
        
        if selected_columns:
            columns_str = ', '.join(selected_columns)
        else:
            columns_str = '*'
        
        query_parts.append(f"SELECT {columns_str}")
        query_parts.append(f"FROM {selected_table}")
        
        if add_where and where_column and where_value:
            if operator == 'LIKE':
                query_parts.append(f"WHERE {where_column} LIKE '%{where_value}%'")
            else:
                query_parts.append(f"WHERE {where_column} {operator} '{where_value}'")
        
        if add_limit:
            query_parts.append(f"LIMIT {limit_value}")
        
        built_query = '\n'.join(query_parts) + ';'
        
        st.markdown("**Generated Query:**")
        st.code(built_query, language="sql")

# ================================
# MAIN FUNCTION
# ================================

def main():
    """Main function for SQL Query Editor."""
    st.set_page_config(
        page_title="MySQL Handbook - Query Editor",
        page_icon="💻",
        layout="wide"
    )
    
    # Main navigation
    tab1, tab2, tab3 = st.tabs([
        "💻 Query Editor",
        "🔧 Query Builder", 
        "📊 Data Explorer"
    ])
    
    with tab1:
        show_query_editor()
    
    with tab2:
        show_query_builder()
    
    with tab3:
        show_data_explorer()

def show_data_explorer():
    """Data explorer interface."""
    st.subheader("📊 Database Explorer")
    
    # Initialize database if not exists
    if 'database' not in st.session_state:
        st.session_state.database = get_sample_database()
    
    # Table selection
    tables = list(st.session_state.database.keys())
    selected_table = st.selectbox("Select table to explore:", tables)
    
    if selected_table:
        df = st.session_state.database[selected_table]
        
        # Table info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Data preview
        st.markdown("**Data Preview:**")
        st.dataframe(df.head(20), use_container_width=True)
        
        # Column information
        with st.expander("📋 Column Information"):
            col_info = []
            for col in df.columns:
                col_info.append({
                    'Column': col,
                    'Type': str(df[col].dtype),
                    'Non-Null Count': df[col].count(),
                    'Null Count': df[col].isnull().sum(),
                    'Unique Values': df[col].nunique()
                })
            
            st.dataframe(pd.DataFrame(col_info), use_container_width=True)
        
        # Basic statistics
        if len(df.select_dtypes(include=['number']).columns) > 0:
            with st.expander("📈 Statistical Summary"):
                st.dataframe(df.describe(), use_container_width=True)

if __name__ == "__main__":
    main()
