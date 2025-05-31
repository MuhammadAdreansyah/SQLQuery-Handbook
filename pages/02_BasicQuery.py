"""
Basic Query Module - MySQL Handbook
===================================
This module covers fundamental SQL SELECT statements and data retrieval techniques.

Topics covered:
- SELECT statement basics
- WHERE clause filtering
- ORDER BY sorting
- LIMIT and OFFSET
- Practice exercises

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Handle plotly imports with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not installed. Some visualizations will be disabled. Install with: pip install plotly")

# ============================================================================
# Data Management
# ============================================================================

def get_sample_data():
    """Generate consistent sample data for examples"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'name': [
            'John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 
            'Charlie Wilson', 'Diana Prince', 'Tom Anderson', 'Sarah Connor'
        ],
        'email': [
            'john@company.com', 'jane@company.com', 'bob@company.com', 
            'alice@company.com', 'charlie@company.com', 'diana@company.com',
            'tom@company.com', 'sarah@company.com'
        ],
        'department': ['IT', 'HR', 'IT', 'Finance', 'IT', 'Marketing', 'Finance', 'HR'],
        'salary': [75000, 65000, 80000, 70000, 72000, 68000, 85000, 62000],
        'hire_date': [
            '2020-01-15', '2019-03-20', '2021-07-10', '2018-11-05', 
            '2020-09-12', '2021-02-28', '2019-08-14', '2022-01-03'
        ],
        'age': [30, 28, 35, 32, 29, 26, 40, 25],
        'status': ['Active', 'Active', 'Active', 'Inactive', 'Active', 'Active', 'Active', 'Active']
    })

def create_query_result(data, query_type, **kwargs):
    """Create query results based on type and parameters"""
    if query_type == "select_all":
        return data.copy()
    elif query_type == "select_columns":
        columns = kwargs.get('columns', ['name', 'department', 'salary'])
        return data[columns].copy()
    elif query_type == "where_filter":
        condition = kwargs.get('condition')
        if condition == 'department_it':
            return data[data['department'] == 'IT'].copy()
        elif condition == 'salary_high':
            return data[data['salary'] > 70000].copy()
        elif condition == 'salary_range':
            return data[(data['salary'] >= 65000) & (data['salary'] <= 75000)].copy()
        elif condition == 'name_starts_j':
            return data[data['name'].str.startswith('J')].copy()
    elif query_type == "order_by":
        column = kwargs.get('column', 'name')
        ascending = kwargs.get('ascending', True)
        return data.sort_values(by=column, ascending=ascending).copy()
    elif query_type == "limit":
        limit = kwargs.get('limit', 3)
        offset = kwargs.get('offset', 0)
        return data.iloc[offset:offset+limit].copy()
    
    return data.copy()

# ============================================================================
# Main Module Function
# ============================================================================

def show_basic_query():
    """Main function for Basic Query learning module"""
    
    # Header section
    st.markdown("# 🔍 Basic SQL Queries")
    st.markdown("### Master the fundamentals of SQL SELECT statements and data retrieval")
    
    # Progress indicator
    create_progress_indicator()
    
    # Learning objectives
    create_learning_objectives()
    
    # Main content tabs
    create_content_tabs()

# ============================================================================
# UI Components
# ============================================================================

def create_progress_indicator():
    """Create a progress indicator for the module"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Topics", "5", help="Number of topics covered")
    with col2:
        st.metric("🎯 Examples", "20+", help="Interactive examples available")
    with col3:
        st.metric("⏱️ Duration", "45 min", help="Estimated completion time")
    with col4:
        st.metric("📊 Difficulty", "Beginner", help="Difficulty level")

def create_learning_objectives():
    """Create the learning objectives section"""
    with st.expander("🎯 Learning Objectives", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **By the end of this module, you will be able to:**
            - ✅ Write basic SELECT statements
            - ✅ Use WHERE clauses for filtering data
            - ✅ Sort results with ORDER BY clause
            """)
        
        with col2:
            st.markdown("""
            **Advanced Skills:**
            - ✅ Apply LIMIT and OFFSET for pagination
            - ✅ Combine multiple conditions with logical operators
            - ✅ Handle NULL values and edge cases
            """)

def create_content_tabs():
    """Create the main content tabs"""
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 SELECT Basics", 
        "🔍 WHERE Clause", 
        "📶 ORDER BY", 
        "🔢 LIMIT & OFFSET", 
        "🧪 Practice Lab"
    ])
    
    with tab1:
        show_select_basics()
    
    with tab2:
        show_where_clause()
    
    with tab3:
        show_order_by()
    
    with tab4:
        show_limit_offset()
    
    with tab5:
        show_practice_lab()

# ============================================================================
# Tab Content Functions
# ============================================================================

def show_select_basics():
    """SELECT statement fundamentals"""
    
    st.markdown("## 📋 SELECT Statement Fundamentals")
    
    # Create main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_select_theory_section()
        create_select_interactive_section()
    
    with col2:
        create_select_sidebar_content()

def create_select_theory_section():
    """Create the theory section for SELECT statements"""
    st.markdown("""
    The SELECT statement is the foundation of SQL data retrieval. It allows you to specify 
    which columns to retrieve and from which tables, making it the most frequently used SQL command.
    """)
    
    st.markdown("### 📚 Basic Syntax")
    st.code("""
-- Basic SELECT syntax
SELECT column1, column2, column3
FROM table_name;

-- Select all columns (use sparingly in production)
SELECT * FROM table_name;

-- Select specific columns with aliases
SELECT name AS employee_name, 
       department AS dept
FROM employees;

-- Select with calculations
SELECT name, 
       salary, 
       salary * 12 AS annual_salary
FROM employees;
    """, language="sql")
    
    # Best practices callout
    st.info("""
    💡 **Best Practice**: Always specify column names instead of using SELECT * 
    in production code for better performance and maintainability.
    """)

def create_select_interactive_section():
    """Create interactive examples for SELECT statements"""
    st.markdown("### 🎮 Interactive SELECT Examples")
    
    # Get sample data
    sample_data = get_sample_data()
    
    # Display sample data
    with st.expander("📊 Sample Data: employees table", expanded=False):
        st.dataframe(sample_data, use_container_width=True)
    
    # Query type selector
    query_type = st.selectbox(
        "Choose a SELECT query type:",
        [
            "SELECT * (All columns)",
            "SELECT specific columns",
            "SELECT with column aliases", 
            "SELECT with calculations",
            "SELECT with string operations"
        ],
        help="Try different types of SELECT statements"
    )
    
    # Generate query and result based on selection
    query, result = generate_select_example(sample_data, query_type)
    
    # Display query and result
    st.markdown("**📝 SQL Query:**")
    st.code(query, language="sql")
    
    st.markdown(f"**📊 Result: {len(result)} rows returned**")
    st.dataframe(result, use_container_width=True)
    
    # Performance tip based on query type
    show_performance_tip(query_type)

def generate_select_example(data, query_type):
    """Generate SQL query and result based on query type"""
    if query_type == "SELECT * (All columns)":
        query = "SELECT * FROM employees;"
        result = data.copy()
        
    elif query_type == "SELECT specific columns":
        query = "SELECT name, department, salary FROM employees;"
        result = data[['name', 'department', 'salary']].copy()
        
    elif query_type == "SELECT with column aliases":
        query = """SELECT name AS employee_name,
       department AS dept,
       salary AS annual_salary,
       hire_date AS start_date
FROM employees;"""
        result = data[['name', 'department', 'salary', 'hire_date']].copy()
        result.columns = ['employee_name', 'dept', 'annual_salary', 'start_date']
        
    elif query_type == "SELECT with calculations":
        query = """SELECT name,
       salary,
       salary * 0.15 AS tax_amount,
       salary * 0.85 AS net_salary,
       salary * 12 AS annual_gross
FROM employees;"""
        result = data[['name', 'salary']].copy()
        result['tax_amount'] = result['salary'] * 0.15
        result['net_salary'] = result['salary'] * 0.85
        result['annual_gross'] = result['salary'] * 12
        
    else:  # SELECT with string operations
        query = """SELECT name,
       UPPER(name) AS name_upper,
       LOWER(department) AS dept_lower,
       CONCAT(name, ' - ', department) AS employee_info
FROM employees;"""
        result = data[['name', 'department']].copy()
        result['name_upper'] = result['name'].str.upper()
        result['dept_lower'] = result['department'].str.lower()
        result['employee_info'] = result['name'] + ' - ' + result['department']
    
    return query, result

def show_performance_tip(query_type):
    """Show performance tips based on query type"""
    if query_type == "SELECT * (All columns)":
        st.warning("⚠️ **Performance Tip**: SELECT * can impact performance with large tables. Always specify needed columns.")
    elif query_type == "SELECT with calculations":
        st.info("💡 **Performance Tip**: Complex calculations can be moved to application layer for better database performance.")
    else:
        st.success("✅ **Good Practice**: Selecting specific columns improves query performance and reduces network traffic.")

def create_select_sidebar_content():
    """Create sidebar content for SELECT section"""
    st.markdown("### 📊 Query Impact")
    
    # Sample data for visualization
    sample_data = get_sample_data()
    
    # Department distribution chart
    if PLOTLY_AVAILABLE:
        dept_counts = sample_data['department'].value_counts()
        fig = px.pie(
            values=dept_counts.values, 
            names=dept_counts.index,
            title="Employee Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback to simple bar chart
        dept_counts = sample_data['department'].value_counts()
        st.bar_chart(dept_counts)
        st.caption("Employee Distribution by Department")
    
    # Key concepts
    st.markdown("### 🔑 Key Concepts")
    
    with st.expander("Column Selection"):
        st.markdown("""
        - **Specific columns**: Better performance
        - **Wildcards (*)**: Use only for exploration
        - **Aliases**: Improve readability
        - **Calculations**: Can be done in SELECT
        """)
    
    with st.expander("Best Practices"):
        st.markdown("""
        - Specify only needed columns
        - Use meaningful aliases
        - Order columns logically
        - Comment complex queries
        - Test with LIMIT first
        """)
    
    with st.expander("Common Errors"):
        st.markdown("""
        - Missing FROM clause
        - Typos in column names
        - Missing commas between columns
        - Incorrect alias syntax
        - Case sensitivity issues
        """)

def show_where_clause():
    """WHERE clause filtering functionality"""
    
    st.markdown("## 🔍 WHERE Clause - Filtering Your Data")
    
    # Create main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_where_theory_section()
        create_where_interactive_section()
    
    with col2:
        create_where_sidebar_content()

def create_where_theory_section():
    """Create theory section for WHERE clause"""
    st.markdown("""
    The WHERE clause is your data filter - it determines which rows are returned by your query. 
    Master the WHERE clause to efficiently retrieve exactly the data you need.
    """)
    
    # Operators reference
    st.markdown("### 🔧 Comparison Operators")
    
    operators_data = {
        'Operator': ['=', '!=', '<>', '>', '<', '>=', '<=', 'IS NULL', 'IS NOT NULL'],
        'Description': [
            'Equal to',
            'Not equal to',
            'Not equal to (alternative)',
            'Greater than',
            'Less than',
            'Greater than or equal',
            'Less than or equal',
            'Is null value',
            'Is not null value'
        ],
        'Example': [
            "department = 'IT'",
            "salary != 70000",
            "status <> 'Inactive'",
            "age > 30",
            "salary < 80000",
            "age >= 25",
            "salary <= 75000",
            "manager IS NULL",
            "email IS NOT NULL"
        ]
    }
    
    operators_df = pd.DataFrame(operators_data)
    st.dataframe(operators_df, use_container_width=True, hide_index=True)
    
    # Logical operators
    st.markdown("### 🧠 Logical Operators")
    st.code("""
-- AND: All conditions must be true
SELECT * FROM employees 
WHERE department = 'IT' AND salary > 70000;

-- OR: Any condition can be true
SELECT * FROM employees
WHERE department = 'IT' OR department = 'HR';

-- NOT: Negates the condition
SELECT * FROM employees
WHERE NOT department = 'Finance';

-- IN: Match any value in a list
SELECT * FROM employees
WHERE department IN ('IT', 'HR', 'Marketing');

-- BETWEEN: Range of values (inclusive)
SELECT * FROM employees
WHERE salary BETWEEN 60000 AND 80000;

-- LIKE: Pattern matching with wildcards
SELECT * FROM employees
WHERE name LIKE 'J%';  -- Names starting with 'J'
    """, language="sql")

def create_where_interactive_section():
    """Create interactive examples for WHERE clause"""
    st.markdown("### 🎮 Interactive WHERE Examples")
    
    sample_data = get_sample_data()
    
    # Filter type selector
    filter_type = st.selectbox(
        "Choose a filter example:",
        [
            "Single condition (department = 'IT')",
            "Numeric comparison (salary > 70000)",
            "Multiple conditions with AND",
            "Multiple conditions with OR",
            "Range filtering (BETWEEN)",
            "List matching (IN operator)",
            "Pattern matching (LIKE)",
            "NULL value checking"
        ],
        help="Explore different types of WHERE conditions"
    )
    
    # Generate query and result
    query, result, explanation = generate_where_example(sample_data, filter_type)
    
    # Display explanation
    st.info(f"📖 **Explanation**: {explanation}")
    
    # Display query
    st.markdown("**📝 SQL Query:**")
    st.code(query, language="sql")
    
    # Display result with metrics
    col_result1, col_result2 = st.columns([3, 1])
    
    with col_result1:
        st.markdown(f"**📊 Result: {len(result)} out of {len(sample_data)} rows**")
        if len(result) > 0:
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("No rows match the specified criteria.")
    
    with col_result2:
        # Show filter effectiveness
        filter_percentage = (len(result) / len(sample_data)) * 100
        st.metric(
            "Filter Effectiveness", 
            f"{filter_percentage:.1f}%",
            help="Percentage of rows that match the filter"
        )

def generate_where_example(data, filter_type):
    """Generate WHERE clause examples"""
    if filter_type == "Single condition (department = 'IT')":
        query = "SELECT * FROM employees WHERE department = 'IT';"
        result = data[data['department'] == 'IT'].copy()
        explanation = "Filters employees who work in the IT department using exact string matching."
        
    elif filter_type == "Numeric comparison (salary > 70000)":
        query = "SELECT * FROM employees WHERE salary > 70000;"
        result = data[data['salary'] > 70000].copy()
        explanation = "Retrieves employees earning more than $70,000 using numeric comparison."
        
    elif filter_type == "Multiple conditions with AND":
        query = "SELECT * FROM employees WHERE department = 'IT' AND salary > 70000;"
        result = data[(data['department'] == 'IT') & (data['salary'] > 70000)].copy()
        explanation = "Both conditions must be true: IT department AND salary above $70,000."
        
    elif filter_type == "Multiple conditions with OR":
        query = "SELECT * FROM employees WHERE department = 'IT' OR department = 'HR';"
        result = data[data['department'].isin(['IT', 'HR'])].copy()
        explanation = "Either condition can be true: IT department OR HR department."
        
    elif filter_type == "Range filtering (BETWEEN)":
        query = "SELECT * FROM employees WHERE salary BETWEEN 65000 AND 75000;"
        result = data[(data['salary'] >= 65000) & (data['salary'] <= 75000)].copy()
        explanation = "Retrieves salaries within the specified range (inclusive of endpoints)."
        
    elif filter_type == "List matching (IN operator)":
        query = "SELECT * FROM employees WHERE department IN ('IT', 'Finance', 'Marketing');"
        result = data[data['department'].isin(['IT', 'Finance', 'Marketing'])].copy()
        explanation = "Matches any department in the specified list - more efficient than multiple ORs."
        
    elif filter_type == "Pattern matching (LIKE)":
        query = "SELECT * FROM employees WHERE name LIKE 'J%';"
        result = data[data['name'].str.startswith('J')].copy()
        explanation = "Finds names starting with 'J' using pattern matching with wildcard (%)."
        
    else:  # NULL value checking
        query = "SELECT * FROM employees WHERE status IS NOT NULL;"
        result = data[data['status'].notna()].copy()
        explanation = "Filters out records where status column contains NULL values."
    
    return query, result, explanation

def create_where_sidebar_content():
    """Create sidebar content for WHERE section"""
    st.markdown("### 📈 Filter Impact Analysis")
    
    sample_data = get_sample_data()
    
    # Create filter impact visualization
    if PLOTLY_AVAILABLE:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = len(sample_data),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Total Records"},
            gauge = {
                'axis': {'range': [None, len(sample_data) + 2]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, len(sample_data)//2], 'color': "lightgray"},
                    {'range': [len(sample_data)//2, len(sample_data)], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': len(sample_data)
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback display
        st.metric("Total Records", len(sample_data))
        st.info("📊 Filter impact visualization requires plotly")
    
    # Pattern matching guide
    st.markdown("### 🎯 LIKE Pattern Guide")
    
    patterns_data = {
        'Pattern': ['%', '_', 'A%', '%son', 'J_n%', '%@company.com'],
        'Description': [
            'Any sequence of characters',
            'Single character',
            'Starts with "A"',
            'Ends with "son"',
            'J + any char + "n" + anything',
            'Ends with "@company.com"'
        ],
        'Example Match': [
            'Any string',
            'A, B, 1, etc.',
            'Alice, Anderson',
            'Johnson, Anderson',
            'John, Jane (if Jen)',
            'john@company.com'
        ]
    }
    
    patterns_df = pd.DataFrame(patterns_data)
    st.dataframe(patterns_df, use_container_width=True, hide_index=True)
    
    # Performance tips
    st.markdown("### ⚡ Performance Tips")
    with st.expander("Query Optimization"):
        st.markdown("""
        - Use indexed columns in WHERE clauses
        - Avoid functions on columns (e.g., WHERE UPPER(name) = 'JOHN')
        - Use specific conditions before general ones
        - Consider using EXISTS instead of IN for subqueries
        - Limit wildcards at the beginning of LIKE patterns
        """)

def show_order_by():
    """ORDER BY sorting functionality"""
    
    st.markdown("## 📶 ORDER BY - Sorting Your Results")
    
    # Create main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_order_by_theory_section()
        create_order_by_interactive_section()
    
    with col2:
        create_order_by_sidebar_content()

def create_order_by_theory_section():
    """Create theory section for ORDER BY"""
    st.markdown("""
    The ORDER BY clause controls how your query results are sorted. Proper sorting makes data 
    more readable and enables efficient pagination and data analysis.
    """)
    
    st.markdown("### 📚 Sorting Fundamentals")
    st.code("""
-- Basic sorting (ascending by default)
SELECT * FROM employees ORDER BY salary;

-- Explicit ascending order
SELECT * FROM employees ORDER BY salary ASC;

-- Descending order
SELECT * FROM employees ORDER BY salary DESC;

-- Multiple column sorting
SELECT * FROM employees 
ORDER BY department ASC, salary DESC;

-- Sorting by column position (not recommended)
SELECT name, salary FROM employees ORDER BY 2 DESC;

-- Sorting with expressions
SELECT name, salary, salary * 12 AS annual_salary
FROM employees
ORDER BY salary * 12 DESC;

-- Sorting with CASE statements
SELECT name, department, salary
FROM employees
ORDER BY 
  CASE department 
    WHEN 'IT' THEN 1
    WHEN 'HR' THEN 2
    ELSE 3
  END,
  salary DESC;
    """, language="sql")

def create_order_by_interactive_section():
    """Create interactive examples for ORDER BY"""
    st.markdown("### 🎮 Interactive Sorting Examples")
    
    sample_data = get_sample_data()
    
    # Sorting configuration
    sort_col1, sort_col2, sort_col3 = st.columns(3)
    
    with sort_col1:
        primary_column = st.selectbox(
            "Primary sort column:",
            ['name', 'department', 'salary', 'age', 'hire_date'],
            help="Choose the main column to sort by"
        )
    
    with sort_col2:
        primary_direction = st.selectbox(
            "Primary sort direction:",
            ['ASC (A→Z, 1→9)', 'DESC (Z→A, 9→1)'],
            help="Choose sorting direction for primary column"
        )
    
    with sort_col3:
        enable_secondary = st.checkbox(
            "Add secondary sort",
            help="Add a second sorting criteria"
        )
    
    # Secondary sorting options
    if enable_secondary:
        sort_col4, sort_col5 = st.columns(2)
        
        with sort_col4:
            secondary_column = st.selectbox(
                "Secondary sort column:",
                [col for col in ['name', 'department', 'salary', 'age', 'hire_date'] 
                 if col != primary_column],
                help="Choose the secondary column to sort by"
            )
        
        with sort_col5:
            secondary_direction = st.selectbox(
                "Secondary sort direction:",
                ['ASC (A→Z, 1→9)', 'DESC (Z→A, 9→1)'],
                key="secondary_dir",
                help="Choose sorting direction for secondary column"
            )
    
    # Generate and execute sort
    primary_asc = primary_direction.startswith('ASC')
    
    if enable_secondary:
        secondary_asc = secondary_direction.startswith('ASC')
        query = f"""SELECT * FROM employees 
ORDER BY {primary_column} {'ASC' if primary_asc else 'DESC'}, 
         {secondary_column} {'ASC' if secondary_asc else 'DESC'};"""
        result = sample_data.sort_values(
            by=[primary_column, secondary_column], 
            ascending=[primary_asc, secondary_asc]
        ).copy()
    else:
        query = f"SELECT * FROM employees ORDER BY {primary_column} {'ASC' if primary_asc else 'DESC'};"
        result = sample_data.sort_values(by=primary_column, ascending=primary_asc).copy()
    
    # Display query and result
    st.markdown("**📝 Generated SQL Query:**")
    st.code(query, language="sql")
    
    st.markdown("**📊 Sorted Results:**")
    st.dataframe(result, use_container_width=True)
    
    # Show sorting insights
    show_sorting_insights(result, primary_column, enable_secondary)

def show_sorting_insights(result, primary_column, has_secondary):
    """Show insights about the sorting results"""
    if primary_column == 'salary':
        min_val = result['salary'].min()
        max_val = result['salary'].max()
        st.info(f"💰 **Salary Range**: ${min_val:,} to ${max_val:,}")
    elif primary_column == 'age':
        min_age = result['age'].min()
        max_age = result['age'].max()
        st.info(f"👥 **Age Range**: {min_age} to {max_age} years old")
    elif primary_column == 'department':
        dept_order = result['department'].unique()
        st.info(f"🏢 **Department Order**: {' → '.join(dept_order)}")
    
    if has_secondary:
        st.success("✅ **Multi-level Sorting**: Results are sorted by primary column first, then by secondary column within each group.")

def create_order_by_sidebar_content():
    """Create sidebar content for ORDER BY section"""
    st.markdown("### 📊 Sorting Visualization")
    
    sample_data = get_sample_data()
    
    # Salary distribution chart
    if PLOTLY_AVAILABLE:
        fig = px.histogram(
            sample_data, 
            x='salary', 
            nbins=10,
            title="Salary Distribution",
            color_discrete_sequence=['#2E86AB']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback visualization
        st.bar_chart(sample_data['salary'])
        st.caption("Salary Distribution")
    
    # Sorting rules
    st.markdown("### 📋 Sorting Rules")
    
    with st.expander("Data Type Sorting"):
        st.markdown("""
        **Numbers**: 1, 2, 10, 100
        **Strings**: A, B, C... a, b, c...
        **Dates**: Older → Newer
        **NULL values**: Usually last (database dependent)
        """)
    
    with st.expander("Performance Considerations"):
        st.markdown("""
        - **Indexed columns** sort faster
        - **Multiple sorts** can be expensive
        - **Large result sets** may need optimization
        - **LIMIT** with ORDER BY is efficient
        """)
    
    with st.expander("Best Practices"):
        st.markdown("""
        - Use column names, not positions
        - Consider creating indexes for frequent sorts
        - Combine with LIMIT for top-N queries
        - Test performance with large datasets
        """)

def show_limit_offset():
    """LIMIT and OFFSET functionality"""
    
    st.markdown("## 🔢 LIMIT & OFFSET - Controlling Result Size")
    
    # Create main layout  
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_limit_theory_section()
        create_limit_interactive_section()
    
    with col2:
        create_limit_sidebar_content()

def create_limit_theory_section():
    """Create theory section for LIMIT and OFFSET"""
    st.markdown("""
    LIMIT and OFFSET clauses control how many rows are returned and enable pagination. 
    They're essential for handling large datasets and implementing user-friendly interfaces.
    """)
    
    st.markdown("### 📚 Pagination Fundamentals")
    st.code("""
-- Limit number of results
SELECT * FROM employees LIMIT 5;

-- Skip rows with OFFSET (MySQL 8.0+)
SELECT * FROM employees LIMIT 5 OFFSET 10;

-- Alternative LIMIT syntax (MySQL specific)
SELECT * FROM employees LIMIT 10, 5;  -- OFFSET, LIMIT

-- Pagination example: Page 2, 5 items per page
SELECT * FROM employees 
ORDER BY hire_date DESC
LIMIT 5 OFFSET 5;

-- Top-N queries
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 3;  -- Top 3 highest paid

-- Combining with WHERE and ORDER BY
SELECT * FROM employees
WHERE department = 'IT'
ORDER BY salary DESC
LIMIT 2;
    """, language="sql")

def create_limit_interactive_section():
    """Create interactive examples for LIMIT and OFFSET"""
    st.markdown("### 🎮 Interactive Pagination Examples")
    
    sample_data = get_sample_data()
    total_records = len(sample_data)
    
    # Pagination controls
    limit_col1, limit_col2, limit_col3 = st.columns(3)
    
    with limit_col1:
        page_size = st.selectbox(
            "Records per page:",
            [3, 5, 8, 10],
            index=1,
            help="Number of records to show per page"
        )
    
    with limit_col2:
        max_pages = (total_records + page_size - 1) // page_size
        current_page = st.selectbox(
            "Current page:",
            list(range(1, max_pages + 1)),
            help=f"Choose page (1 to {max_pages})"
        )
    
    with limit_col3:
        sort_column = st.selectbox(
            "Sort by:",
            ['id', 'name', 'salary', 'hire_date'],
            help="Choose column for consistent pagination"
        )
    
    # Calculate OFFSET
    offset = (current_page - 1) * page_size
    
    # Generate query and result
    query = f"""SELECT * FROM employees 
ORDER BY {sort_column}
LIMIT {page_size} OFFSET {offset};"""
    
    # Apply to data
    sorted_data = sample_data.sort_values(by=sort_column)
    result = sorted_data.iloc[offset:offset + page_size].copy()
    
    # Display query
    st.markdown("**📝 Generated SQL Query:**")
    st.code(query, language="sql")
    
    # Display pagination info
    start_record = offset + 1
    end_record = min(offset + page_size, total_records)
    
    st.markdown(f"**📊 Showing records {start_record}-{end_record} of {total_records}**")
    st.dataframe(result, use_container_width=True)
    
    # Pagination navigation simulation
    st.markdown("### 🧭 Pagination Navigation")
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        st.metric("Current Page", f"{current_page}")
    with nav_col2:
        st.metric("Total Pages", f"{max_pages}")
    with nav_col3:
        st.metric("Records/Page", f"{page_size}")
    with nav_col4:
        st.metric("Total Records", f"{total_records}")

def create_limit_sidebar_content():
    """Create sidebar content for LIMIT section"""
    st.markdown("### 📈 Pagination Metrics")
    
    # Pagination efficiency chart
    if PLOTLY_AVAILABLE:
        page_sizes = [5, 10, 20, 50]
        efficiency_scores = [95, 85, 70, 45]  # Simulated efficiency scores
        
        fig = px.line(
            x=page_sizes, 
            y=efficiency_scores,
            title="Pagination Efficiency by Page Size",
            labels={'x': 'Page Size', 'y': 'Efficiency Score'},
            markers=True
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback display
        page_data = pd.DataFrame({
            'Page Size': [5, 10, 20, 50],
            'Efficiency': [95, 85, 70, 45]
        })
        st.line_chart(page_data.set_index('Page Size'))
        st.caption("Pagination Efficiency by Page Size")
    
    # Best practices
    st.markdown("### 💡 Pagination Best Practices")
    
    with st.expander("Performance Tips"):
        st.markdown("""
        - **Always use ORDER BY** with LIMIT for consistent results
        - **Index the ORDER BY columns** for better performance
        - **Reasonable page sizes** (10-50 records typically)
        - **Avoid large OFFSET values** (consider cursor-based pagination)
        """)
    
    with st.expander("Common Use Cases"):
        st.markdown("""
        - **Web application pagination**
        - **API response limiting**
        - **Top-N analysis** (highest/lowest values)
        - **Data sampling** for analysis
        - **Batch processing** of large datasets
        """)

def show_practice_lab():
    """Practice lab with exercises"""
    
    st.markdown("## 🧪 Practice Lab - Test Your Skills")
    
    st.markdown("""
    Welcome to the practice lab! Here you can test your understanding of basic SQL queries 
    with interactive exercises and challenges.
    """)
    
    # Create practice sections
    create_guided_exercises()
    create_challenge_problems()
    create_query_builder()

def create_guided_exercises():
    """Create guided practice exercises"""
    st.markdown("### 📝 Guided Exercises")
    
    sample_data = get_sample_data()
    
    # Exercise selector
    exercise = st.selectbox(
        "Choose an exercise:",
        [
            "Exercise 1: Select specific columns",
            "Exercise 2: Filter by department", 
            "Exercise 3: Sort by multiple columns",
            "Exercise 4: Combine WHERE and ORDER BY",
            "Exercise 5: Pagination with LIMIT"
        ]
    )
    
    # Exercise content
    if exercise == "Exercise 1: Select specific columns":
        st.markdown("""
        **Task**: Write a query to select only the `name`, `department`, and `salary` columns from the employees table.
        """)
        
        with st.expander("💡 Hint"):
            st.markdown("Use `SELECT column1, column2, column3 FROM table_name;`")
        
        with st.expander("✅ Solution"):
            st.code("SELECT name, department, salary FROM employees;", language="sql")
            st.dataframe(sample_data[['name', 'department', 'salary']], use_container_width=True)
    
    elif exercise == "Exercise 2: Filter by department":
        st.markdown("""
        **Task**: Find all employees who work in the 'Finance' department.
        """)
        
        with st.expander("💡 Hint"):
            st.markdown("Use `WHERE department = 'Finance'`")
        
        with st.expander("✅ Solution"):
            st.code("SELECT * FROM employees WHERE department = 'Finance';", language="sql")
            result = sample_data[sample_data['department'] == 'Finance']
            st.dataframe(result, use_container_width=True)
    
    elif exercise == "Exercise 3: Sort by multiple columns":
        st.markdown("""
        **Task**: Sort employees by department (ascending) and then by salary (descending).
        """)
        
        with st.expander("💡 Hint"):
            st.markdown("Use `ORDER BY column1 ASC, column2 DESC`")
        
        with st.expander("✅ Solution"):
            st.code("SELECT * FROM employees ORDER BY department ASC, salary DESC;", language="sql")
            result = sample_data.sort_values(['department', 'salary'], ascending=[True, False])
            st.dataframe(result, use_container_width=True)
    
    elif exercise == "Exercise 4: Combine WHERE and ORDER BY":
        st.markdown("""
        **Task**: Find IT department employees earning more than $70,000, sorted by salary (highest first).
        """)
        
        with st.expander("💡 Hint"):
            st.markdown("Combine `WHERE department = 'IT' AND salary > 70000` with `ORDER BY salary DESC`")
        
        with st.expander("✅ Solution"):
            st.code("""SELECT * FROM employees 
WHERE department = 'IT' AND salary > 70000 
ORDER BY salary DESC;""", language="sql")
            result = sample_data[
                (sample_data['department'] == 'IT') & 
                (sample_data['salary'] > 70000)
            ].sort_values('salary', ascending=False)
            st.dataframe(result, use_container_width=True)
    
    else:  # Exercise 5
        st.markdown("""
        **Task**: Get the top 3 highest-paid employees using LIMIT.
        """)
        
        with st.expander("💡 Hint"):
            st.markdown("Use `ORDER BY salary DESC LIMIT 3`")
        
        with st.expander("✅ Solution"):
            st.code("SELECT * FROM employees ORDER BY salary DESC LIMIT 3;", language="sql")
            result = sample_data.sort_values('salary', ascending=False).head(3)
            st.dataframe(result, use_container_width=True)

def create_challenge_problems():
    """Create challenge problems for advanced practice"""
    st.markdown("### 🎯 Challenge Problems")
    
    challenges = [
        {
            "title": "Challenge 1: Complex Filtering",
            "description": "Find employees who are either in IT with salary > $70k OR in HR with age < 30",
            "difficulty": "Medium",
            "hint": "Use parentheses to group conditions: (condition1 AND condition2) OR (condition3 AND condition4)"
        },
        {
            "title": "Challenge 2: Advanced Sorting", 
            "description": "Sort employees by department, then by salary descending, but show IT department first",
            "difficulty": "Hard",
            "hint": "Use CASE statement in ORDER BY to prioritize IT department"
        },
        {
            "title": "Challenge 3: Pattern Matching",
            "description": "Find all employees whose email contains 'company' and name starts with a vowel",
            "difficulty": "Medium", 
            "hint": "Combine LIKE patterns: name LIKE 'A%' OR name LIKE 'E%' etc."
        }
    ]
    
    for i, challenge in enumerate(challenges):
        with st.expander(f"{challenge['title']} - {challenge['difficulty']}"):
            st.markdown(f"**Description**: {challenge['description']}")
            st.markdown(f"**Hint**: {challenge['hint']}")
            
            # Let users try to solve it
            user_solution = st.text_area(
                "Your SQL solution:",
                key=f"challenge_{i}",
                placeholder="Write your SQL query here..."
            )
            
            if user_solution.strip():
                st.info("💡 Great effort! In a real environment, this would be executed against the database.")

def create_query_builder():
    """Create an interactive query builder"""
    st.markdown("### 🔧 Interactive Query Builder")
    
    st.markdown("""
    Build your own queries using the controls below. This tool helps you understand 
    how different clauses work together.
    """)
    
    sample_data = get_sample_data()
    
    # Query builder controls
    builder_col1, builder_col2 = st.columns(2)
    
    with builder_col1:
        # SELECT clause
        st.markdown("**SELECT Clause:**")
        select_all = st.checkbox("SELECT * (all columns)", value=True)
        
        if not select_all:
            selected_columns = st.multiselect(
                "Choose columns:",
                sample_data.columns.tolist(),
                default=['name', 'department', 'salary']
            )
        
        # WHERE clause
        st.markdown("**WHERE Clause (optional):**")
        use_where = st.checkbox("Add WHERE condition")
        
        if use_where:
            where_column = st.selectbox("Filter column:", sample_data.columns.tolist())
            where_operator = st.selectbox("Operator:", ['=', '!=', '>', '<', '>=', '<=', 'LIKE'])
            where_value = st.text_input("Value:", placeholder="Enter filter value")
    
    with builder_col2:
        # ORDER BY clause
        st.markdown("**ORDER BY Clause (optional):**")
        use_order = st.checkbox("Add ORDER BY")
        
        if use_order:
            order_column = st.selectbox("Sort column:", sample_data.columns.tolist())
            order_direction = st.selectbox("Direction:", ["ASC", "DESC"])
        
        # LIMIT clause
        st.markdown("**LIMIT Clause (optional):**")
        use_limit = st.checkbox("Add LIMIT")
        
        if use_limit:
            limit_value = st.number_input("Number of rows:", min_value=1, max_value=20, value=5)
    
    # Build and display query
    if st.button("🔨 Build Query", type="primary"):
        query_parts = []
        
        # SELECT
        if select_all:
            query_parts.append("SELECT *")
        else:
            if selected_columns:
                query_parts.append(f"SELECT {', '.join(selected_columns)}")
            else:
                st.error("Please select at least one column or use SELECT *")
                return
        
        # FROM
        query_parts.append("FROM employees")
        
        # WHERE
        if use_where and where_value:
            if where_operator == 'LIKE':
                query_parts.append(f"WHERE {where_column} LIKE '%{where_value}%'")
            else:
                query_parts.append(f"WHERE {where_column} {where_operator} '{where_value}'")
        
        # ORDER BY
        if use_order:
            query_parts.append(f"ORDER BY {order_column} {order_direction}")
        
        # LIMIT
        if use_limit:
            query_parts.append(f"LIMIT {limit_value}")
        
        # Display final query
        final_query = "\n".join(query_parts) + ";"
        
        st.markdown("**🎉 Your Generated Query:**")
        st.code(final_query, language="sql")
        
        # Try to execute the query on sample data (simplified simulation)
        try:
            result = sample_data.copy()
            
            # Apply WHERE filter (simplified)
            if use_where and where_value:
                if where_operator == '=':
                    result = result[result[where_column].astype(str) == where_value]
                elif where_operator == 'LIKE':
                    result = result[result[where_column].astype(str).str.contains(where_value, case=False, na=False)]
                # Add more operators as needed
            
            # Apply ORDER BY
            if use_order:
                result = result.sort_values(by=order_column, ascending=(order_direction == 'ASC'))
            
            # Apply LIMIT
            if use_limit:
                result = result.head(limit_value)
            
            # Apply SELECT
            if not select_all and selected_columns:
                result = result[selected_columns]
            
            st.markdown(f"**📊 Query Result ({len(result)} rows):**")
            st.dataframe(result, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

# ============================================================================
# Module Summary and Navigation
# ============================================================================

def create_module_summary():
    """Create a summary section for the module"""
    st.markdown("### 📋 Module Summary")
    
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.markdown("""
        **What you've learned:**
        - ✅ Basic SELECT statement syntax
        - ✅ WHERE clause for filtering data
        - ✅ ORDER BY for sorting results
        - ✅ LIMIT and OFFSET for pagination
        - ✅ Combining multiple clauses effectively
        """)
    
    with summary_col2:
        st.markdown("""
        **Next steps:**
        - 📋 Explore DDL Commands module
        - ✏️ Practice DML Operations  
        - 📊 Learn Aggregate Functions
        - 💻 Try the SQL Query Editor
        """)

# Call summary at the end of practice lab
if __name__ == "__main__":
    show_basic_query()