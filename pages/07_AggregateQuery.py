"""
MySQL Handbook - Aggregate Queries Module

This module provides comprehensive coverage of MySQL aggregate functions and operations including:
- Basic aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- GROUP BY operations and grouping strategies
- HAVING clause for filtering grouped data
- Window functions for advanced analytics
- Complex aggregation scenarios and optimizations

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# Check for plotly availability
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# ================================
# DATA MANAGEMENT
# ================================

def get_aggregate_sample_data():
    """Generate comprehensive sample data for aggregate function demonstrations."""
    
    # Sales data with realistic patterns
    sales_data = []
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    for i in range(1, 501):  # 500 sales records
        sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
        sales_data.append({
            'sale_id': i,
            'product_category': random.choice(categories),
            'region': random.choice(regions),
            'sale_amount': round(random.uniform(10.0, 1000.0), 2),
            'quantity_sold': random.randint(1, 20),
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'month': sale_date.strftime('%Y-%m'),
            'quarter': f"Q{((sale_date.month - 1) // 3) + 1} {sale_date.year}",
            'year': sale_date.year,
            'salesperson_id': random.randint(1, 25)
    })
    
    # Employee data
    employees = []
    departments = ['Sales', 'Marketing', 'IT', 'HR', 'Finance']
    for i in range(1, 26):
        employees.append({
            'employee_id': i,
            'name': f'Employee {i}',
            'department': random.choice(departments),
            'salary': random.randint(40000, 120000),
            'hire_date': (datetime.now() - timedelta(days=random.randint(30, 2000))).strftime('%Y-%m-%d'),
            'age': random.randint(22, 65)
        })
    
    # Customer data
    customers = []
    for i in range(1, 101):
        customers.append({
            'customer_id': i,
            'age_group': random.choice(['18-25', '26-35', '36-45', '46-55', '56+']),
            'total_orders': random.randint(1, 50),
            'total_spent': round(random.uniform(50.0, 5000.0), 2),
            'registration_date': (datetime.now() - timedelta(days=random.randint(1, 730))).strftime('%Y-%m-%d')
        })
    
    return {
        'sales': sales_data,
        'employees': employees,
        'customers': customers
    }


# ================================
# BASIC AGGREGATE FUNCTIONS
# ================================

def show_basic_aggregates():
    """Display basic aggregate function examples and interactive tools."""
    st.header("🔢 Basic Aggregate Functions")
    
    # Theory section
    show_aggregate_theory()
    
    # Interactive examples
    show_aggregate_interactive()
    
    # Sidebar content
    show_aggregate_sidebar()


def show_aggregate_theory():
    """Show basic aggregate functions theory."""
    st.subheader("Essential Aggregate Functions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**COUNT Functions:**")
        st.code("""
-- Count all rows
SELECT COUNT(*) FROM sales;

-- Count non-null values
SELECT COUNT(customer_id) FROM sales;

-- Count distinct values
SELECT COUNT(DISTINCT customer_id) FROM sales;
        """, language="sql")
        
        st.write("**SUM and AVG:**")
        st.code("""
-- Total sales amount
SELECT SUM(sale_amount) FROM sales;

-- Average sale amount
SELECT AVG(sale_amount) FROM sales;

-- Average with rounding
SELECT ROUND(AVG(sale_amount), 2) as avg_sale
FROM sales;
        """, language="sql")
    
    with col2:
        st.write("**MIN and MAX:**")
        st.code("""
-- Find minimum and maximum
SELECT 
    MIN(sale_amount) as min_sale,
    MAX(sale_amount) as max_sale,
    MAX(sale_date) as latest_sale
FROM sales;
        """, language="sql")
        
        st.write("**Combined Aggregates:**")
        st.code("""
-- Multiple aggregates in one query
SELECT 
    COUNT(*) as total_sales,
    SUM(sale_amount) as total_revenue,
    AVG(sale_amount) as avg_sale,
    MIN(sale_amount) as min_sale,
    MAX(sale_amount) as max_sale
FROM sales;
        """, language="sql")


def show_aggregate_interactive():
    """Show interactive aggregate function examples."""
    st.subheader("🔧 Interactive Aggregate Calculator")
    
    data = get_aggregate_sample_data()
    df_sales = pd.DataFrame(data['sales'])
    
    with st.expander("Sales Data Overview", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Sample Sales Data:**")
            st.dataframe(df_sales.head(10))
            
        with col2:
            st.write("**Quick Statistics:**")
            total_sales = len(df_sales)
            total_revenue = df_sales['sale_amount'].sum()
            avg_sale = df_sales['sale_amount'].mean()
            
            st.metric("Total Sales", f"{total_sales:,}")
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
            st.metric("Average Sale", f"${avg_sale:.2f}")
    
    with st.expander("Custom Aggregate Query Builder", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            aggregate_function = st.selectbox("Aggregate Function:", 
                                            ["COUNT", "SUM", "AVG", "MIN", "MAX"])
            column_name = st.selectbox("Column:", 
                                     ["sale_amount", "quantity_sold", "sale_id"])
        
        with col2:
            use_distinct = st.checkbox("Use DISTINCT", key="aggregate_distinct")
            use_where = st.checkbox("Add WHERE condition", key="aggregate_where")
            
            if use_where:
                where_column = st.selectbox("WHERE Column:", 
                                          ["product_category", "region", "year"])
                where_value = st.text_input("WHERE Value:")
        
        with col3:
            if st.button("Generate Query"):
                query = generate_aggregate_query(aggregate_function, column_name, 
                                               use_distinct, use_where, 
                                               locals().get('where_column', ''), 
                                               locals().get('where_value', ''))
                st.code(query, language="sql")
                
                # Calculate and show result
                if where_value:
                    result = calculate_aggregate_result(df_sales, aggregate_function, 
                                                      column_name, use_distinct, 
                                                      use_where, where_column, where_value)
                    st.success(f"Result: {result}")


def generate_aggregate_query(func, column, distinct, use_where, where_col, where_val):
    """Generate aggregate query based on parameters."""
    distinct_part = "DISTINCT " if distinct else ""
    
    if func == "COUNT" and column == "sale_id":
        select_part = f"SELECT COUNT({distinct_part}*)"
    else:
        select_part = f"SELECT {func}({distinct_part}{column})"
    
    query = f"{select_part} FROM sales"
    
    if use_where and where_col and where_val:
        if where_col in ['product_category', 'region']:
            query += f"\nWHERE {where_col} = '{where_val}'"
        else:
            query += f"\nWHERE {where_col} = {where_val}"
    
    query += ";"
    return query


def calculate_aggregate_result(df, func, column, distinct, use_where, where_col, where_val):
    """Calculate actual result for demonstration."""
    try:
        # Apply WHERE condition if specified
        if use_where and where_col and where_val:
            if where_col in ['product_category', 'region']:
                df = df[df[where_col] == where_val]
            else:
                df = df[df[where_col] == int(where_val)]
        
        # Apply DISTINCT if specified
        if distinct:
            values = df[column].drop_duplicates()
        else:
            values = df[column]
        
        # Calculate aggregate
        if func == "COUNT":
            return len(values)
        elif func == "SUM":
            return f"{values.sum():,.2f}"
        elif func == "AVG":
            return f"{values.mean():.2f}"
        elif func == "MIN":
            return f"{values.min():.2f}"
        elif func == "MAX":
            return f"{values.max():.2f}"
    except Exception as e:
        return f"Error: {str(e)}"


def show_aggregate_sidebar():
    """Show aggregate functions sidebar content."""
    with st.sidebar:
        st.write("**🔢 Aggregate Function Tips:**")
        st.info("""
        • COUNT(*) counts all rows including NULLs
        • COUNT(column) ignores NULL values
        • Use DISTINCT to count unique values
        • AVG ignores NULL values
        • Combine multiple aggregates in one query
        """)


# ================================
# GROUP BY OPERATIONS
# ================================

def show_group_by_operations():
    """Display GROUP BY operation examples and interactive tools."""
    st.header("📊 GROUP BY Operations")
    
    # Theory section
    show_group_by_theory()
    
    # Interactive examples
    show_group_by_interactive()
    
    # Sidebar content
    show_group_by_sidebar()


def show_group_by_theory():
    """Show GROUP BY operations theory."""
    st.subheader("Grouping and Aggregating Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Basic GROUP BY:**")
        st.code("""
-- Sales by category
SELECT 
    product_category,
    COUNT(*) as total_sales,
    SUM(sale_amount) as total_revenue
FROM sales
GROUP BY product_category;
        """, language="sql")
        
        st.write("**Multiple Grouping Columns:**")
        st.code("""
-- Sales by category and region
SELECT 
    product_category,
    region,
    COUNT(*) as sales_count,
    AVG(sale_amount) as avg_sale
FROM sales
GROUP BY product_category, region
ORDER BY product_category, region;
        """, language="sql")
    
    with col2:
        st.write("**GROUP BY with DATE functions:**")
        st.code("""
-- Monthly sales summary
SELECT 
    YEAR(sale_date) as year,
    MONTH(sale_date) as month,
    COUNT(*) as sales_count,
    SUM(sale_amount) as monthly_revenue
FROM sales
GROUP BY YEAR(sale_date), MONTH(sale_date)
ORDER BY year, month;
        """, language="sql")
        
        st.write("**Advanced Grouping:**")
        st.code("""
-- Quarterly performance
SELECT 
    CONCAT('Q', QUARTER(sale_date), ' ', YEAR(sale_date)) as quarter,
    COUNT(DISTINCT salesperson_id) as active_salespeople,
    SUM(sale_amount) as quarterly_revenue,
    AVG(sale_amount) as avg_sale_amount
FROM sales
GROUP BY YEAR(sale_date), QUARTER(sale_date)
ORDER BY YEAR(sale_date), QUARTER(sale_date);
        """, language="sql")


def show_group_by_interactive():
    """Show interactive GROUP BY examples."""
    st.subheader("🔧 Interactive GROUP BY Builder")
    
    data = get_aggregate_sample_data()
    df_sales = pd.DataFrame(data['sales'])
    
    with st.expander("GROUP BY Query Generator", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Grouping Options:**")
            group_columns = st.multiselect("Group By Columns:", 
                                         ["product_category", "region", "year", "month", "quarter"],
                                         default=["product_category"])
        
        with col2:
            st.write("**Aggregate Functions:**")
            agg_functions = st.multiselect("Select Aggregates:",
                                         ["COUNT(*) as count", 
                                          "SUM(sale_amount) as total_revenue",
                                          "AVG(sale_amount) as avg_sale",
                                          "MIN(sale_amount) as min_sale",
                                          "MAX(sale_amount) as max_sale"],                                         default=["COUNT(*) as count", "SUM(sale_amount) as total_revenue"])
        
        with col3:
            st.write("**Options:**")
            use_order_by = st.checkbox("Add ORDER BY", value=True, key="group_by_order")
            limit_results = st.checkbox("Limit Results", key="group_by_limit")
            
            if limit_results:
                limit_count = st.slider("Limit to:", 5, 50, 10)
        
        if st.button("Generate GROUP BY Query"):
            if group_columns and agg_functions:
                query = generate_group_by_query(group_columns, agg_functions, 
                                              use_order_by, limit_results, 
                                              locals().get('limit_count', 10))
                st.code(query, language="sql")
                
                # Show result preview
                result_df = calculate_group_by_result(df_sales, group_columns, agg_functions)
                if not result_df.empty:
                    st.write("**Result Preview:**")
                    st.dataframe(result_df.head(limit_count if limit_results else 20))
    
    with st.expander("Visual GROUP BY Analysis", expanded=False):
        if PLOTLY_AVAILABLE:
            show_group_by_visualizations(df_sales)
        else:
            st.info("Install plotly for interactive visualizations")
            show_basic_group_by_charts(df_sales)


def generate_group_by_query(group_cols, agg_funcs, use_order, limit_results, limit_count):
    """Generate GROUP BY query based on parameters."""
    select_parts = group_cols + agg_funcs
    query = f"SELECT \n    {',\n    '.join(select_parts)}\nFROM sales"
    
    if group_cols:
        query += f"\nGROUP BY {', '.join(group_cols)}"
    
    if use_order:
        query += f"\nORDER BY {group_cols[0]}" if group_cols else "\nORDER BY COUNT(*) DESC"
    
    if limit_results:
        query += f"\nLIMIT {limit_count}"
    
    query += ";"
    return query


def calculate_group_by_result(df, group_cols, agg_funcs):
    """Calculate GROUP BY result for demonstration."""
    try:
        if not group_cols:
            return pd.DataFrame()
        
        # Convert aggregate function strings to actual operations
        agg_dict = {}
        result_cols = {}
        
        for func in agg_funcs:
            if "COUNT(*)" in func:
                agg_dict['sale_id'] = 'count'
                result_cols['sale_id'] = 'count'
            elif "SUM(sale_amount)" in func:
                agg_dict['sale_amount'] = 'sum'
                result_cols['sale_amount'] = 'total_revenue'
            elif "AVG(sale_amount)" in func:
                if 'sale_amount' not in agg_dict:
                    agg_dict['sale_amount'] = ['mean']
                else:
                    agg_dict['sale_amount'].append('mean')
                result_cols['sale_amount'] = 'avg_sale'
            elif "MIN(sale_amount)" in func:
                if 'sale_amount' not in agg_dict:
                    agg_dict['sale_amount'] = ['min']
                else:
                    agg_dict['sale_amount'].append('min')
            elif "MAX(sale_amount)" in func:
                if 'sale_amount' not in agg_dict:
                    agg_dict['sale_amount'] = ['max']
                else:
                    agg_dict['sale_amount'].append('max')
        
        # Perform groupby operation
        grouped = df.groupby(group_cols).agg(agg_dict).round(2)
        grouped.columns = ['_'.join(col).strip() if col[1] else col[0] for col in grouped.columns.values]
        
        return grouped.reset_index()
    
    except Exception as e:
        st.error(f"Error calculating result: {str(e)}")
        return pd.DataFrame()


def show_group_by_visualizations(df):
    """Show interactive visualizations for GROUP BY data."""
    st.write("**Sales by Category:**")
    category_sales = df.groupby('product_category')['sale_amount'].agg(['count', 'sum', 'mean']).reset_index()
    category_sales.columns = ['Category', 'Count', 'Total Revenue', 'Average Sale']
    
    fig = px.bar(category_sales, x='Category', y='Total Revenue', 
                title='Total Revenue by Product Category')
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("**Monthly Sales Trend:**")
    monthly_sales = df.groupby('month')['sale_amount'].sum().reset_index()
    fig2 = px.line(monthly_sales, x='month', y='sale_amount', 
                  title='Monthly Sales Trend')
    st.plotly_chart(fig2, use_container_width=True)


def show_basic_group_by_charts(df):
    """Show basic charts when plotly is not available."""
    st.write("**Sales by Category:**")
    category_sales = df.groupby('product_category')['sale_amount'].sum()
    st.bar_chart(category_sales)
    
    st.write("**Monthly Sales:**")
    monthly_sales = df.groupby('month')['sale_amount'].sum()
    st.line_chart(monthly_sales)


def show_group_by_sidebar():
    """Show GROUP BY sidebar content."""
    with st.sidebar:
        st.write("**📊 GROUP BY Guidelines:**")
        st.success("""
        • All non-aggregate columns must be in GROUP BY
        • Use meaningful aliases for aggregates
        • Consider performance with large datasets
        • Combine with ORDER BY for sorted results
        • Use HAVING for filtering grouped results
        """)


# ================================
# HAVING CLAUSE
# ================================

def show_having_clause():
    """Display HAVING clause examples and interactive tools."""
    st.header("🔍 HAVING Clause")
    
    # Theory section
    show_having_theory()
    
    # Interactive examples
    show_having_interactive()
    
    # Sidebar content
    show_having_sidebar()


def show_having_theory():
    """Show HAVING clause theory."""
    st.subheader("Filtering Grouped Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**HAVING vs WHERE:**")
        st.code("""
-- WHERE filters before grouping
SELECT product_category, COUNT(*)
FROM sales
WHERE sale_amount > 100
GROUP BY product_category;

-- HAVING filters after grouping
SELECT product_category, COUNT(*)
FROM sales
GROUP BY product_category
HAVING COUNT(*) > 50;
        """, language="sql")
        
        st.write("**Complex HAVING Conditions:**")
        st.code("""
-- Multiple conditions in HAVING
SELECT 
    product_category,
    COUNT(*) as sales_count,
    AVG(sale_amount) as avg_sale
FROM sales
GROUP BY product_category
HAVING COUNT(*) > 20 
   AND AVG(sale_amount) > 200;
        """, language="sql")
    
    with col2:
        st.write("**HAVING with Aggregate Functions:**")
        st.code("""
-- Find high-performing regions
SELECT 
    region,
    SUM(sale_amount) as total_revenue,
    COUNT(*) as sales_count
FROM sales
GROUP BY region
HAVING SUM(sale_amount) > 10000
ORDER BY total_revenue DESC;
        """, language="sql")
        
        st.write("**Combining WHERE and HAVING:**")
        st.code("""
-- Filter recent high-volume categories
SELECT 
    product_category,
    COUNT(*) as recent_sales,
    SUM(sale_amount) as recent_revenue
FROM sales
WHERE sale_date >= '2024-01-01'
GROUP BY product_category
HAVING COUNT(*) > 10
   AND SUM(sale_amount) > 5000;
        """, language="sql")


def show_having_interactive():
    """Show interactive HAVING clause examples."""
    st.subheader("🔧 Interactive HAVING Filter Builder")
    
    data = get_aggregate_sample_data()
    df_sales = pd.DataFrame(data['sales'])
    
    with st.expander("HAVING Clause Generator", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**GROUP BY Setup:**")
            group_column = st.selectbox("Group By:", ["product_category", "region", "year"])
            
            st.write("**SELECT Aggregates:**")
            select_aggregates = st.multiselect("Select Functions:",
                                             ["COUNT(*)", "SUM(sale_amount)", "AVG(sale_amount)", 
                                              "MIN(sale_amount)", "MAX(sale_amount)"],                                             default=["COUNT(*)", "SUM(sale_amount)"])
        
        with col2:
            st.write("**HAVING Conditions:**")
            having_function = st.selectbox("HAVING Function:", 
                                         ["COUNT(*)", "SUM(sale_amount)", "AVG(sale_amount)"])
            having_operator = st.selectbox("Operator:", [">", ">=", "<", "<=", "="])
            having_value = st.number_input("Value:", value=50.0)
            
            add_where = st.checkbox("Add WHERE condition", key="having_where")
            if add_where:
                where_condition = st.text_input("WHERE clause:", 
                                              placeholder="year = 2024")
        
        if st.button("Generate HAVING Query"):
            query = generate_having_query(group_column, select_aggregates, 
                                        having_function, having_operator, having_value,
                                        add_where, locals().get('where_condition', ''))
            st.code(query, language="sql")
            
            # Show result
            result_df = calculate_having_result(df_sales, group_column, select_aggregates,
                                              having_function, having_operator, having_value)
            if not result_df.empty:
                st.write("**Filtered Results:**")
                st.dataframe(result_df)
    
    with st.expander("Common HAVING Patterns", expanded=False):
        show_having_patterns()


def generate_having_query(group_col, aggregates, having_func, operator, value, use_where, where_cond):
    """Generate HAVING query based on parameters."""
    # Build SELECT clause
    select_parts = [group_col] + aggregates
    query = f"SELECT \n    {',\n    '.join(select_parts)}\nFROM sales"
    
    # Add WHERE clause if specified
    if use_where and where_cond:
        query += f"\nWHERE {where_cond}"
    
    # Add GROUP BY
    query += f"\nGROUP BY {group_col}"
    
    # Add HAVING clause
    query += f"\nHAVING {having_func} {operator} {value}"
    
    # Add ORDER BY
    query += f"\nORDER BY {group_col};"
    
    return query


def calculate_having_result(df, group_col, aggregates, having_func, operator, value):
    """Calculate HAVING result for demonstration."""
    try:
        # Group the data
        grouped = df.groupby(group_col).agg({
            'sale_id': 'count',
            'sale_amount': ['sum', 'mean', 'min', 'max']
        }).round(2)
        
        # Flatten column names
        grouped.columns = ['count', 'sum_amount', 'avg_amount', 'min_amount', 'max_amount']
        grouped = grouped.reset_index()
        
        # Apply HAVING filter
        if having_func == "COUNT(*)":
            filter_col = 'count'
        elif having_func == "SUM(sale_amount)":
            filter_col = 'sum_amount'
        elif having_func == "AVG(sale_amount)":
            filter_col = 'avg_amount'
        
        # Apply operator
        if operator == ">":
            filtered = grouped[grouped[filter_col] > value]
        elif operator == ">=":
            filtered = grouped[grouped[filter_col] >= value]
        elif operator == "<":
            filtered = grouped[grouped[filter_col] < value]
        elif operator == "<=":
            filtered = grouped[grouped[filter_col] <= value]
        else:  # "="
            filtered = grouped[grouped[filter_col] == value]
        
        return filtered
    
    except Exception as e:
        st.error(f"Error calculating result: {str(e)}")
        return pd.DataFrame()


def show_having_patterns():
    """Show common HAVING clause patterns."""
    patterns = [
        {
            'title': "High Volume Categories",
            'description': "Find product categories with many sales",
            'query': """SELECT product_category, COUNT(*) as sales_count
FROM sales
GROUP BY product_category
HAVING COUNT(*) > 50
ORDER BY sales_count DESC;"""
        },
        {
            'title': "Top Revenue Regions",
            'description': "Identify regions generating high revenue",
            'query': """SELECT region, SUM(sale_amount) as total_revenue
FROM sales
GROUP BY region
HAVING SUM(sale_amount) > 10000
ORDER BY total_revenue DESC;"""
        },
        {
            'title': "Premium Categories",
            'description': "Categories with high average sale amounts",
            'query': """SELECT product_category, AVG(sale_amount) as avg_sale
FROM sales
GROUP BY product_category
HAVING AVG(sale_amount) > 200
ORDER BY avg_sale DESC;"""
        }
    ]
    
    for pattern in patterns:
        st.write(f"**{pattern['title']}:**")
        st.write(pattern['description'])
        st.code(pattern['query'], language="sql")
        st.write("---")


def show_having_sidebar():
    """Show HAVING clause sidebar content."""
    with st.sidebar:
        st.write("**🔍 HAVING Clause Rules:**")
        st.warning("""
        • HAVING filters grouped results
        • WHERE filters before grouping
        • Use aggregate functions in HAVING
        • HAVING comes after GROUP BY
        • Can combine multiple conditions
        """)


# ================================
# WINDOW FUNCTIONS
# ================================

def show_window_functions():
    """Display window function examples and interactive tools."""
    st.header("🪟 Window Functions")
    
    # Theory section
    show_window_theory()
    
    # Interactive examples
    show_window_interactive()
    
    # Sidebar content
    show_window_sidebar()


def show_window_theory():
    """Show window functions theory."""
    st.subheader("Advanced Analytics with Window Functions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**ROW_NUMBER and RANK:**")
        st.code("""
-- Rank sales by amount within each category
SELECT 
    product_category,
    sale_amount,
    ROW_NUMBER() OVER (
        PARTITION BY product_category 
        ORDER BY sale_amount DESC
    ) as row_num,
    RANK() OVER (
        PARTITION BY product_category 
        ORDER BY sale_amount DESC
    ) as rank_num
FROM sales;
        """, language="sql")
        
        st.write("**Running Totals:**")
        st.code("""
-- Calculate running total of sales
SELECT 
    sale_date,
    sale_amount,
    SUM(sale_amount) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM sales
ORDER BY sale_date;
        """, language="sql")
    
    with col2:
        st.write("**LAG and LEAD:**")
        st.code("""
-- Compare with previous and next sales
SELECT 
    sale_date,
    sale_amount,
    LAG(sale_amount) OVER (ORDER BY sale_date) as prev_sale,
    LEAD(sale_amount) OVER (ORDER BY sale_date) as next_sale,
    sale_amount - LAG(sale_amount) OVER (ORDER BY sale_date) as change
FROM sales
ORDER BY sale_date;
        """, language="sql")
        
        st.write("**Percentiles and Distribution:**")
        st.code("""
-- Calculate percentiles within categories
SELECT 
    product_category,
    sale_amount,
    PERCENT_RANK() OVER (
        PARTITION BY product_category 
        ORDER BY sale_amount
    ) as percentile_rank,
    NTILE(4) OVER (
        PARTITION BY product_category 
        ORDER BY sale_amount
    ) as quartile
FROM sales;
        """, language="sql")


def show_window_interactive():
    """Show interactive window function examples."""
    st.subheader("🔧 Interactive Window Functions")
    
    data = get_aggregate_sample_data()
    df_sales = pd.DataFrame(data['sales'][:50])  # Limit for better display
    
    with st.expander("Window Function Builder", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            window_function = st.selectbox("Window Function:", 
                                         ["ROW_NUMBER()", "RANK()", "DENSE_RANK()", 
                                          "SUM(sale_amount)", "AVG(sale_amount)", 
                                          "LAG(sale_amount)", "LEAD(sale_amount)"])
        
        with col2:
            partition_by = st.selectbox("PARTITION BY:", 
                                      ["None", "product_category", "region", "year"])
            order_by = st.selectbox("ORDER BY:", 
                                  ["sale_amount DESC", "sale_date", "sale_amount ASC"])
        
        with col3:
            if "SUM" in window_function or "AVG" in window_function:
                frame_clause = st.selectbox("Frame Clause:",
                                          ["Default", "ROWS UNBOUNDED PRECEDING", 
                                           "ROWS 2 PRECEDING", "RANGE UNBOUNDED PRECEDING"])
        
        if st.button("Generate Window Function Query"):
            query = generate_window_query(window_function, partition_by, order_by,
                                        locals().get('frame_clause', 'Default'))
            st.code(query, language="sql")
            
            # Show result preview
            result_df = calculate_window_result(df_sales, window_function, partition_by, order_by)
            if not result_df.empty:
                st.write("**Result Preview:**")
                st.dataframe(result_df.head(15))
    
    with st.expander("Window Function Examples", expanded=False):
        show_window_examples(df_sales)


def generate_window_query(func, partition, order, frame):
    """Generate window function query."""
    # Build OVER clause
    over_parts = []
    if partition != "None":
        over_parts.append(f"PARTITION BY {partition}")
    if order:
        over_parts.append(f"ORDER BY {order}")
    if frame != "Default" and ("SUM" in func or "AVG" in func):
        over_parts.append(frame)
    
    over_clause = " ".join(over_parts)
    
    # Build SELECT clause
    base_columns = ["sale_id", "product_category", "sale_amount", "sale_date"]
    window_column = f"{func} OVER ({over_clause}) as window_result"
    
    query = f"""SELECT 
    {', '.join(base_columns)},
    {window_column}
FROM sales
ORDER BY {order if order else 'sale_id'}
LIMIT 20;"""
    
    return query


def calculate_window_result(df, func, partition, order):
    """Calculate window function result for demonstration."""
    try:
        # Sort dataframe based on order
        if "sale_amount DESC" in order:
            df_sorted = df.sort_values('sale_amount', ascending=False)
        elif "sale_amount ASC" in order:
            df_sorted = df.sort_values('sale_amount', ascending=True)
        else:
            df_sorted = df.sort_values('sale_date')
        
        # Apply window function
        if partition != "None":
            if "ROW_NUMBER" in func:
                df_sorted['window_result'] = df_sorted.groupby(partition).cumcount() + 1
            elif "RANK" in func:
                df_sorted['window_result'] = df_sorted.groupby(partition)['sale_amount'].rank(method='min', ascending=False)
            elif "SUM" in func:
                df_sorted['window_result'] = df_sorted.groupby(partition)['sale_amount'].cumsum()
            elif "AVG" in func:
                df_sorted['window_result'] = df_sorted.groupby(partition)['sale_amount'].expanding().mean().values
        else:
            if "ROW_NUMBER" in func:
                df_sorted['window_result'] = range(1, len(df_sorted) + 1)
            elif "RANK" in func:
                df_sorted['window_result'] = df_sorted['sale_amount'].rank(method='min', ascending=False)
            elif "SUM" in func:
                df_sorted['window_result'] = df_sorted['sale_amount'].cumsum()
            elif "AVG" in func:
                df_sorted['window_result'] = df_sorted['sale_amount'].expanding().mean()
            elif "LAG" in func:
                df_sorted['window_result'] = df_sorted['sale_amount'].shift(1)
            elif "LEAD" in func:
                df_sorted['window_result'] = df_sorted['sale_amount'].shift(-1)
        
        return df_sorted[['sale_id', 'product_category', 'sale_amount', 'sale_date', 'window_result']].round(2)
    
    except Exception as e:
        st.error(f"Error calculating window result: {str(e)}")
        return pd.DataFrame()


def show_window_examples(df):
    """Show practical window function examples."""
    st.write("**Top 3 Sales per Category:**")
    # Simulate top 3 sales per category
    top_sales = df.groupby('product_category').apply(
        lambda x: x.nlargest(3, 'sale_amount')
    ).reset_index(drop=True)
    st.dataframe(top_sales[['product_category', 'sale_amount']].head(9))
    
    st.write("**Sales Comparison with Previous:**")
    # Simulate LAG function
    df_sorted = df.sort_values('sale_date')
    df_sorted['prev_sale'] = df_sorted['sale_amount'].shift(1)
    df_sorted['change'] = df_sorted['sale_amount'] - df_sorted['prev_sale']
    st.dataframe(df_sorted[['sale_date', 'sale_amount', 'prev_sale', 'change']].head(10))


def show_window_sidebar():
    """Show window functions sidebar content."""
    with st.sidebar:
        st.write("**🪟 Window Function Benefits:**")
        st.info("""
        • No need for self-joins
        • Maintain detail while adding aggregates
        • Powerful for rankings and comparisons
        • Support for complex analytical queries
        • Better performance than subqueries
        """)


# ================================
# PRACTICE LAB
# ================================

def show_practice_lab():
    """Show aggregate functions practice lab."""
    st.header("🧪 Aggregate Functions Practice Lab")
    
    tab1, tab2, tab3 = st.tabs(["📚 Progressive Exercises", "🎯 Business Intelligence", "🏆 Advanced Analytics"])
    
    with tab1:
        show_progressive_exercises()
    
    with tab2:
        show_bi_scenarios()
    
    with tab3:
        show_advanced_analytics()


def show_progressive_exercises():
    """Show progressive aggregate exercises."""
    st.subheader("📚 Progressive Learning Path")
    
    exercises = [
        {
            'level': 'Beginner',
            'title': 'Basic Aggregations',
            'tasks': [
                'Count total number of sales',
                'Calculate total revenue',
                'Find average sale amount',
                'Identify highest and lowest sales'
            ],
            'sample_solution': """
-- Basic aggregate functions
SELECT 
    COUNT(*) as total_sales,
    SUM(sale_amount) as total_revenue,
    AVG(sale_amount) as average_sale,
    MIN(sale_amount) as lowest_sale,
    MAX(sale_amount) as highest_sale
FROM sales;
            """
        },
        {
            'level': 'Intermediate',
            'title': 'GROUP BY Analysis',
            'tasks': [
                'Sales summary by product category',
                'Monthly revenue trends',
                'Regional performance comparison',
                'Top performing categories using HAVING'
            ],
            'sample_solution': """
-- Sales by category with performance filter
SELECT 
    product_category,
    COUNT(*) as sales_count,
    SUM(sale_amount) as total_revenue,
    AVG(sale_amount) as avg_sale_amount,
    ROUND(SUM(sale_amount) / COUNT(*), 2) as revenue_per_sale
FROM sales
GROUP BY product_category
HAVING COUNT(*) > 20 AND SUM(sale_amount) > 5000
ORDER BY total_revenue DESC;
            """
        },
        {
            'level': 'Advanced',
            'title': 'Window Functions',
            'tasks': [
                'Rank products by sales within each category',
                'Calculate running totals',
                'Compare current vs previous period',
                'Identify top 10% performers'
            ],
            'sample_solution': """
-- Advanced window function analysis
SELECT 
    product_category,
    sale_amount,
    ROW_NUMBER() OVER (PARTITION BY product_category ORDER BY sale_amount DESC) as category_rank,
    SUM(sale_amount) OVER (ORDER BY sale_date ROWS UNBOUNDED PRECEDING) as running_total,
    LAG(sale_amount) OVER (PARTITION BY product_category ORDER BY sale_date) as prev_sale,
    NTILE(10) OVER (ORDER BY sale_amount DESC) as decile
FROM sales;
            """
        }
    ]
    
    for i, exercise in enumerate(exercises):
        with st.expander(f"{exercise['level']}: {exercise['title']}", expanded=i==0):
            st.write("**Learning Objectives:**")
            for task in exercise['tasks']:
                st.write(f"• {task}")
            
            user_solution = st.text_area(f"Your Solution ({exercise['level']}):", 
                                       height=150, key=f"agg_exercise_{i}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Show Solution ({exercise['level']})"):
                    st.code(exercise['sample_solution'], language="sql")
            
            with col2:
                if st.button(f"Validate ({exercise['level']})"):
                    if user_solution.strip():
                        st.success(f"{exercise['level']} solution submitted!")
                    else:
                        st.warning("Please provide a solution.")


def show_bi_scenarios():
    """Show business intelligence scenarios."""
    st.subheader("🎯 Business Intelligence Scenarios")
    
    data = get_aggregate_sample_data()
    
    scenarios = [
        {
            'title': 'Sales Performance Dashboard',
            'description': 'Create KPIs for executive dashboard',
            'requirements': [
                'Total revenue and growth rate',
                'Top 5 product categories',
                'Regional performance rankings',
                'Sales target achievement analysis'
            ]
        },
        {
            'title': 'Customer Segmentation',
            'description': 'Analyze customer purchasing behavior',
            'requirements': [
                'Customer lifetime value calculation',
                'Purchase frequency analysis',
                'High-value customer identification',
                'Churn risk assessment'
            ]
        },
        {
            'title': 'Inventory Optimization',
            'description': 'Optimize inventory based on sales patterns',
            'requirements': [
                'Product velocity analysis',
                'Seasonal demand patterns',
                'Stock level recommendations',
                'Supplier performance metrics'
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        with st.expander(f"BI Scenario {i+1}: {scenario['title']}", expanded=False):
            st.write(f"**Description:** {scenario['description']}")
            st.write("**Key Requirements:**")
            for req in scenario['requirements']:
                st.write(f"• {req}")
            
            if i == 0:  # Show sample data for first scenario
                st.write("**Sample KPI Dashboard:**")
                df_sales = pd.DataFrame(data['sales'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_revenue = df_sales['sale_amount'].sum()
                    st.metric("Total Revenue", f"${total_revenue:,.2f}")
                
                with col2:
                    total_sales = len(df_sales)
                    st.metric("Total Sales", f"{total_sales:,}")
                
                with col3:
                    avg_sale = df_sales['sale_amount'].mean()
                    st.metric("Average Sale", f"${avg_sale:.2f}")
            
            solution_area = st.text_area(f"Your BI Solution {i+1}:", 
                                       height=200, key=f"bi_scenario_{i}")
            
            if st.button(f"Submit BI Solution {i+1}"):
                if solution_area.strip():
                    st.success("BI solution submitted for review!")
                else:
                    st.warning("Please provide your analysis.")


def show_advanced_analytics():
    """Show advanced analytics challenges."""
    st.subheader("🏆 Advanced Analytics Challenge")
    
    st.write("**Challenge: Comprehensive Sales Analytics**")
    st.write("Create a complete analytical solution combining multiple aggregate techniques.")
    
    requirements = [
        "**Descriptive Analytics**: Historical performance summary",
        "**Trend Analysis**: Month-over-month growth patterns", 
        "**Comparative Analysis**: Regional and category benchmarking",
        "**Predictive Insights**: Seasonal forecasting indicators",
        "**Performance Rankings**: Top performers across multiple dimensions"
    ]
    
    for req in requirements:
        st.write(f"• {req}")
    
    with st.expander("Advanced Challenge Workspace", expanded=True):
        challenge_solution = st.text_area("Your Comprehensive Solution:", 
                                        height=300, 
                                        placeholder="""
-- Your solution should include:
-- 1. Descriptive statistics
-- 2. Time-based analysis
-- 3. Comparative rankings
-- 4. Window functions for trends
-- 5. Complex aggregations

SELECT ...
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Advanced Solution"):
                if challenge_solution.strip():
                    st.success("🎉 Advanced analytics solution submitted!")
                    st.balloons()
                else:
                    st.warning("Please provide your comprehensive solution.")
        
        with col2:
            if st.button("Show Example Approach"):
                example_solution = """
-- Comprehensive Sales Analytics Solution
WITH monthly_stats AS (
    SELECT 
        DATE_FORMAT(sale_date, '%Y-%m') as month,
        product_category,
        COUNT(*) as sales_count,
        SUM(sale_amount) as revenue,
        AVG(sale_amount) as avg_sale
    FROM sales
    GROUP BY DATE_FORMAT(sale_date, '%Y-%m'), product_category
),
category_rankings AS (
    SELECT 
        product_category,
        SUM(sale_amount) as total_revenue,
        RANK() OVER (ORDER BY SUM(sale_amount) DESC) as revenue_rank,
        COUNT(*) as total_sales,
        AVG(sale_amount) as avg_sale_amount
    FROM sales
    GROUP BY product_category
),
growth_analysis AS (
    SELECT 
        month,
        product_category,
        revenue,
        LAG(revenue) OVER (PARTITION BY product_category ORDER BY month) as prev_revenue,
        (revenue - LAG(revenue) OVER (PARTITION BY product_category ORDER BY month)) / 
        LAG(revenue) OVER (PARTITION BY product_category ORDER BY month) * 100 as growth_rate
    FROM monthly_stats
)
SELECT 
    cr.product_category,
    cr.total_revenue,
    cr.revenue_rank,
    cr.avg_sale_amount,
    AVG(ga.growth_rate) as avg_growth_rate
FROM category_rankings cr
LEFT JOIN growth_analysis ga ON cr.product_category = ga.product_category
GROUP BY cr.product_category, cr.total_revenue, cr.revenue_rank, cr.avg_sale_amount
ORDER BY cr.revenue_rank;
                """
                st.code(example_solution, language="sql")


# ================================
# MAIN FUNCTION
# ================================

def main():
    """Main function to display Aggregate Queries module content."""
    try:
        st.title("📊 Aggregate Queries & Analytics")
        st.markdown("Master MySQL aggregate functions, GROUP BY operations, and advanced analytics with window functions.")
        
        # Create tabs for different aggregate topics
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔢 Basic Aggregates",
            "📊 GROUP BY Operations", 
            "🔍 HAVING Clause",
            "🪟 Window Functions",
            "🧪 Practice Lab"
        ])
        
        with tab1:
            show_basic_aggregates()
        
        with tab2:
            show_group_by_operations()
        
        with tab3:
            show_having_clause()
        
        with tab4:
            show_window_functions()
        
        with tab5:
            show_practice_lab()
        
        # Footer
        st.markdown("---")
        st.markdown("**💡 Pro Tip:** Combine aggregate functions with proper indexing for optimal query performance!")
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your database connection and try again.")


if __name__ == "__main__":
    main()