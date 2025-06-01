"""
MySQL Handbook - Transaction Control Language (TCL) Module

This module provides comprehensive coverage of MySQL TCL operations including:
- Transaction fundamentals and ACID properties
- COMMIT and ROLLBACK operations
- SAVEPOINT and nested transactions
- Isolation levels and concurrency control
- Deadlock handling and prevention
- Performance optimization for transactions

Author: MySQL Handbook Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
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
# DATA MANAGEMENT
# ================================

def get_tcl_sample_data():
    """Generate sample data for TCL demonstrations."""
    
    # Sample transaction log data
    transaction_log = []
    transaction_types = ['BEGIN', 'INSERT', 'UPDATE', 'DELETE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT']
    
    for i in range(1, 51):
        transaction_log.append({
            'log_id': i,
            'transaction_id': f'TXN_{random.randint(1000, 9999)}',
            'operation_type': random.choice(transaction_types),
            'table_name': random.choice(['customers', 'orders', 'products', 'payments']),
            'timestamp': datetime.now() - timedelta(minutes=random.randint(1, 1440)),
            'status': random.choice(['SUCCESS', 'FAILED', 'PENDING']),
            'isolation_level': random.choice(['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE'])
        })
    
    # Sample account data for banking scenario
    accounts = []
    for i in range(1, 11):
        accounts.append({
            'account_id': i,
            'account_number': f'ACC{1000 + i}',
            'account_holder': f'Customer {i}',
            'balance': random.uniform(1000, 50000),
            'account_type': random.choice(['Savings', 'Checking', 'Business']),
            'created_date': datetime.now() - timedelta(days=random.randint(30, 365))
        })
    
    # Sample transfer data
    transfers = []
    for i in range(1, 21):
        from_acc = random.randint(1, 10)
        to_acc = random.randint(1, 10)
        while to_acc == from_acc:
            to_acc = random.randint(1, 10)
        
        transfers.append({
            'transfer_id': i,
            'from_account': from_acc,
            'to_account': to_acc,
            'amount': random.uniform(100, 5000),
            'transfer_date': datetime.now() - timedelta(days=random.randint(1, 30)),
            'status': random.choice(['COMPLETED', 'PENDING', 'FAILED', 'CANCELLED']),
            'transaction_id': f'TXN_{random.randint(1000, 9999)}'
        })
    
    return {
        'transaction_log': transaction_log,
        'accounts': accounts,
        'transfers': transfers
    }

# ================================
# TRANSACTION FUNDAMENTALS
# ================================

def show_transaction_fundamentals():
    """Display transaction fundamentals and ACID properties."""
    st.header("🔄 Transaction Fundamentals")
    
    # ACID Properties section
    show_acid_properties()
    
    # Basic transaction syntax
    show_basic_transaction_syntax()
    
    # Interactive transaction demo
    show_transaction_demo()
    
    # Sidebar content
    show_fundamentals_sidebar()

def show_acid_properties():
    """Show ACID properties explanation."""
    st.subheader("🧪 ACID Properties")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **ACID adalah fondasi dari sistem database yang reliable:**
        
        - **Atomicity (Atomisitas)** - All or nothing principle
        - **Consistency (Konsistensi)** - Data integrity maintained
        - **Isolation (Isolasi)** - Concurrent transactions don't interfere
        - **Durability (Durabilitas)** - Changes survive system failures
        """)
        
        # ACID visualization
        if PLOTLY_AVAILABLE:
            fig = go.Figure(data=go.Scatter(
                x=[1, 2, 3, 4],
                y=[1, 1, 1, 1],
                mode='markers+text',
                marker=dict(size=100, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']),
                text=['A', 'C', 'I', 'D'],
                textposition="middle center",
                textfont=dict(size=20, color='white')
            ))
            fig.update_layout(
                title="ACID Properties",
                showlegend=False,
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False),
                height=200
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("""
        **💡 Contoh ACID dalam kehidupan nyata:**
        
        **Transfer Bank (Atomicity):**
        - Debit dari rekening A: ✅
        - Credit ke rekening B: ✅
        - Jika salah satu gagal → ROLLBACK semua
        
        **Consistency:**
        - Total uang sebelum = Total uang sesudah
        
        **Isolation:**
        - Transfer A tidak melihat transfer B yang belum selesai
        
        **Durability:**
        - Setelah COMMIT, data tersimpan permanen
        """)

def show_basic_transaction_syntax():
    """Show basic transaction syntax."""
    st.subheader("📝 Basic Transaction Syntax")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Basic Transaction Structure:**")
        st.code("""
-- Start transaction
START TRANSACTION;
-- atau
BEGIN;

-- Your SQL operations
UPDATE accounts SET balance = balance - 1000 
WHERE account_id = 1;

UPDATE accounts SET balance = balance + 1000 
WHERE account_id = 2;

-- Commit changes
COMMIT;

-- Or rollback if error
-- ROLLBACK;
        """, language="sql")
    
    with col2:
        st.markdown("**Transaction with Error Handling:**")
        st.code("""
-- Start transaction with error handling
START TRANSACTION;

-- Check if sufficient balance
SELECT balance FROM accounts 
WHERE account_id = 1 AND balance >= 1000;

-- If balance sufficient, proceed
UPDATE accounts SET balance = balance - 1000 
WHERE account_id = 1;

UPDATE accounts SET balance = balance + 1000 
WHERE account_id = 2;

-- Commit if all operations successful
COMMIT;

-- Rollback on any error
-- ROLLBACK;
        """, language="sql")

def show_transaction_demo():
    """Show interactive transaction demonstration."""
    st.subheader("🎮 Interactive Transaction Demo")
    
    with st.expander("Bank Transfer Simulator", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Transfer Configuration:**")
            from_account = st.selectbox("From Account:", ['ACC1001', 'ACC1002', 'ACC1003'])
            to_account = st.selectbox("To Account:", ['ACC1004', 'ACC1005', 'ACC1006'])
            amount = st.number_input("Transfer Amount:", min_value=1.0, value=1000.0, step=100.0)
            
            # Simulate conditions
            simulate_error = st.checkbox("Simulate Error Condition")
            use_savepoint = st.checkbox("Use Savepoint")
            
        with col2:
            st.markdown("**Account Balances (Before):**")
            account_data = {
                'Account': ['ACC1001', 'ACC1002', 'ACC1003', 'ACC1004', 'ACC1005', 'ACC1006'],
                'Balance': [5000, 7500, 3200, 8900, 4500, 6700]
            }
            st.dataframe(pd.DataFrame(account_data), use_container_width=True)
        
        if st.button("🚀 Execute Transfer", type="primary"):
            show_transfer_execution(from_account, to_account, amount, simulate_error, use_savepoint)

def show_transfer_execution(from_account, to_account, amount, simulate_error, use_savepoint):
    """Show the execution of a transfer transaction."""
    st.markdown("**🔄 Transaction Execution Log:**")
    
    # Generate transaction SQL
    if use_savepoint:
        sql_code = f"""
START TRANSACTION;

-- Create savepoint before transfer
SAVEPOINT before_transfer;

-- Check source account balance
SELECT balance FROM accounts WHERE account_number = '{from_account}';

-- Debit from source account
UPDATE accounts 
SET balance = balance - {amount}
WHERE account_number = '{from_account}';

-- Credit to destination account
UPDATE accounts 
SET balance = balance + {amount}
WHERE account_number = '{to_account}';

"""
        if simulate_error:
            sql_code += """
-- Simulate error condition
-- ERROR: Insufficient funds or constraint violation

-- Rollback to savepoint
ROLLBACK TO SAVEPOINT before_transfer;
ROLLBACK;
"""
        else:
            sql_code += """
-- All operations successful
COMMIT;
"""
    else:
        sql_code = f"""
START TRANSACTION;

-- Check source account balance
SELECT balance FROM accounts WHERE account_number = '{from_account}';

-- Debit from source account
UPDATE accounts 
SET balance = balance - {amount}
WHERE account_number = '{from_account}';

-- Credit to destination account
UPDATE accounts 
SET balance = balance + {amount}
WHERE account_number = '{to_account}';

"""
        if simulate_error:
            sql_code += """
-- Simulate error condition
ROLLBACK;
"""
        else:
            sql_code += """
COMMIT;
"""
    
    st.code(sql_code, language="sql")
    
    # Show result
    if simulate_error:
        st.error("❌ Transaction Failed - All changes rolled back")
        result_status = "ROLLED BACK"
    else:
        st.success("✅ Transaction Completed Successfully")
        result_status = "COMMITTED"
    
    # Show updated balances
    st.markdown("**Account Balances (After):**")
    if not simulate_error:
        # Simulate updated balances
        updated_data = {
            'Account': ['ACC1001', 'ACC1002', 'ACC1003', 'ACC1004', 'ACC1005', 'ACC1006'],
            'Balance': [4000 if from_account == 'ACC1001' else 5000,
                       6500 if from_account == 'ACC1002' else 7500,
                       2200 if from_account == 'ACC1003' else 3200,
                       9900 if to_account == 'ACC1004' else 8900,
                       5500 if to_account == 'ACC1005' else 4500,
                       7700 if to_account == 'ACC1006' else 6700]
        }
    else:
        # Original balances (no change)
        updated_data = {
            'Account': ['ACC1001', 'ACC1002', 'ACC1003', 'ACC1004', 'ACC1005', 'ACC1006'],
            'Balance': [5000, 7500, 3200, 8900, 4500, 6700]
        }
    
    st.dataframe(pd.DataFrame(updated_data), use_container_width=True)

def show_fundamentals_sidebar():
    """Show fundamentals sidebar content."""
    with st.sidebar:
        st.markdown("### 🎯 Transaction Key Points")
        
        with st.expander("Transaction States"):
            st.markdown("""
            - **ACTIVE** - Transaction is executing
            - **PARTIALLY COMMITTED** - After final statement
            - **COMMITTED** - After successful completion
            - **FAILED** - After discovering normal execution cannot proceed
            - **ABORTED** - After rollback and database restored
            """)
        
        with st.expander("Best Practices"):
            st.markdown("""
            - Keep transactions short
            - Acquire locks in same order
            - Handle deadlocks gracefully
            - Use appropriate isolation levels
            - Always handle errors properly
            """)

# ================================
# SAVEPOINTS & NESTED TRANSACTIONS
# ================================

def show_savepoints_nested():
    """Display savepoints and nested transactions functionality."""
    st.header("📍 Savepoints & Nested Transactions")
    
    # Theory section
    st.subheader("🎯 Understanding Savepoints")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Savepoints** allow you to set intermediate points within a transaction 
        that you can rollback to without aborting the entire transaction.
        
        ### Key Benefits:
        - **Partial Rollback**: Undo only specific operations
        - **Error Recovery**: Handle errors without losing all work
        - **Complex Logic**: Implement sophisticated transaction flows
        - **Performance**: Reduce transaction restart overhead
        """)
        
        # Savepoint syntax
        st.code("""
-- Creating savepoints
START TRANSACTION;
INSERT INTO accounts (id, balance) VALUES (1, 1000);
SAVEPOINT after_insert;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT after_update;

-- Rollback to specific savepoint
ROLLBACK TO SAVEPOINT after_insert;

-- Release savepoint (optional)
RELEASE SAVEPOINT after_insert;

COMMIT;
        """, language="sql")
    
    with col2:
        st.info("""
        💡 **Savepoint Rules**
        
        - Savepoints are transaction-scoped
        - Names must be unique within transaction
        - Nested savepoints are supported
        - Released automatically on COMMIT/ROLLBACK
        """)
    
    # Interactive savepoint simulator
    st.subheader("🧪 Interactive Savepoint Simulator")
    
    if 'savepoint_demo' not in st.session_state:
        st.session_state.savepoint_demo = {
            'balance': 1000,
            'savepoints': [],
            'operations': [],
            'transaction_active': False
        }
    
    demo = st.session_state.savepoint_demo
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 START TRANSACTION"):
            demo['transaction_active'] = True
            demo['operations'] = ["START TRANSACTION"]
            st.success("Transaction started!")
    
    with col2:
        if st.button("💾 CREATE SAVEPOINT") and demo['transaction_active']:
            savepoint_name = f"sp_{len(demo['savepoints']) + 1}"
            demo['savepoints'].append({
                'name': savepoint_name,
                'balance': demo['balance'],
                'operation_count': len(demo['operations'])
            })
            demo['operations'].append(f"SAVEPOINT {savepoint_name}")
            st.success(f"Savepoint '{savepoint_name}' created!")
    
    with col3:
        if st.button("🔴 COMMIT") and demo['transaction_active']:
            demo['transaction_active'] = False
            demo['savepoints'] = []
            demo['operations'].append("COMMIT")
            st.success("Transaction committed!")
    
    if demo['transaction_active']:
        st.subheader("💰 Account Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount", min_value=1, max_value=500, value=100)
            
            if st.button("➕ DEPOSIT"):
                demo['balance'] += amount
                demo['operations'].append(f"DEPOSIT +${amount}")
                st.success(f"Deposited ${amount}")
            
            if st.button("➖ WITHDRAW"):
                if demo['balance'] >= amount:
                    demo['balance'] -= amount
                    demo['operations'].append(f"WITHDRAW -${amount}")
                    st.success(f"Withdrew ${amount}")
                else:
                    st.error("Insufficient funds!")
        
        with col2:
            st.metric("Current Balance", f"${demo['balance']}")
            
            if demo['savepoints']:
                st.selectbox(
                    "Rollback to Savepoint:",
                    options=[sp['name'] for sp in demo['savepoints']],
                    key="rollback_target"
                )
                
                if st.button("⏪ ROLLBACK TO SAVEPOINT"):
                    target = st.session_state.rollback_target
                    for sp in demo['savepoints']:
                        if sp['name'] == target:
                            demo['balance'] = sp['balance']
                            demo['operations'] = demo['operations'][:sp['operation_count']]
                            demo['operations'].append(f"ROLLBACK TO SAVEPOINT {target}")
                            # Remove later savepoints
                            demo['savepoints'] = [s for s in demo['savepoints'] 
                                                if s['operation_count'] <= sp['operation_count']]
                            st.success(f"Rolled back to {target}")
                            break
    
    # Transaction log
    if demo['operations']:
        st.subheader("📋 Transaction Log")
        for i, op in enumerate(demo['operations'], 1):
            st.text(f"{i:2d}. {op}")

# ================================
# ISOLATION LEVELS & CONCURRENCY
# ================================

def show_isolation_levels():
    """Display isolation levels and concurrency control."""
    st.header("🔒 Isolation Levels & Concurrency")
    
    # Isolation levels overview
    st.subheader("🎯 Understanding Isolation Levels")
    
    levels_data = {
        'Isolation Level': [
            'READ UNCOMMITTED',
            'READ COMMITTED', 
            'REPEATABLE READ',
            'SERIALIZABLE'
        ],
        'Dirty Read': ['❌ Possible', '✅ Prevented', '✅ Prevented', '✅ Prevented'],
        'Non-Repeatable Read': ['❌ Possible', '❌ Possible', '✅ Prevented', '✅ Prevented'],
        'Phantom Read': ['❌ Possible', '❌ Possible', '❌ Possible', '✅ Prevented'],
        'Performance': ['🟢 Highest', '🟡 High', '🟡 Medium', '🔴 Lowest']
    }
    
    st.dataframe(pd.DataFrame(levels_data), use_container_width=True)
    
    # Interactive isolation level demo
    st.subheader("🧪 Isolation Level Simulator")
    
    selected_level = st.selectbox(
        "Select Isolation Level:",
        ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔵 Transaction A**")
        st.code(f"""
SET TRANSACTION ISOLATION LEVEL {selected_level};
START TRANSACTION;

-- Read account balance
SELECT balance FROM accounts WHERE id = 1;
-- Result: $1000

-- Wait for Transaction B...

-- Read again
SELECT balance FROM accounts WHERE id = 1;
-- Result depends on isolation level!

COMMIT;
        """, language="sql")
    
    with col2:
        st.markdown("**🟠 Transaction B**")
        st.code("""
START TRANSACTION;

-- Update account balance
UPDATE accounts 
SET balance = balance - 500 
WHERE id = 1;

-- Transaction A might see this change
-- depending on isolation level

COMMIT;
        """, language="sql")
    
    # Explain behavior for selected level
    st.subheader(f"📊 Behavior with {selected_level}")
    
    behaviors = {
        'READ UNCOMMITTED': {
            'description': "Lowest isolation level - allows dirty reads",
            'behavior': "Transaction A will see the uncommitted change from Transaction B",
            'risk': "⚠️ High risk of inconsistent data",
            'use_case': "Analytics on non-critical data"
        },
        'READ COMMITTED': {
            'description': "Prevents dirty reads but allows non-repeatable reads", 
            'behavior': "Transaction A will only see committed changes",
            'risk': "⚠️ Data may change between reads",
            'use_case': "Most web applications"
        },
        'REPEATABLE READ': {
            'description': "Prevents dirty and non-repeatable reads",
            'behavior': "Transaction A will see consistent data throughout",
            'risk': "⚠️ May experience phantom reads",
            'use_case': "Financial applications"
        },
        'SERIALIZABLE': {
            'description': "Highest isolation level - prevents all phenomena",
            'behavior': "Transactions execute as if they were serial",
            'risk': "⚠️ Higher chance of deadlocks and timeouts",
            'use_case': "Critical systems requiring absolute consistency"
        }
    }
    
    behavior = behaviors[selected_level]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Description:** {behavior['description']}")
        st.success(f"**Behavior:** {behavior['behavior']}")
    
    with col2:
        st.warning(behavior['risk'])
        st.info(f"**Typical Use Case:** {behavior['use_case']}")

# ================================
# PRACTICE LAB
# ================================

def show_practice_lab():
    """Display interactive practice exercises for TCL."""
    st.header("🧪 TCL Practice Lab")
    
    # Exercise selection
    exercise = st.selectbox(
        "Choose a practice exercise:",
        [
            "1. Basic Transaction Management",
            "2. Savepoint Operations", 
            "3. Isolation Level Testing",
            "4. Deadlock Resolution",
            "5. Performance Optimization"
        ]
    )
    
    if "1. Basic" in exercise:
        show_basic_transaction_exercise()
    elif "2. Savepoint" in exercise:
        show_savepoint_exercise() 
    elif "3. Isolation" in exercise:
        show_isolation_exercise()
    elif "4. Deadlock" in exercise:
        show_deadlock_exercise()
    elif "5. Performance" in exercise:
        show_performance_exercise()

def show_basic_transaction_exercise():
    """Basic transaction management exercise."""
    st.subheader("📝 Exercise 1: Basic Transaction Management")
    
    st.markdown("""
    **Scenario:** You need to transfer $500 from Account A to Account B.
    Write the transaction code to ensure ACID properties.
    """)
    
    # Show account data
    accounts_df = pd.DataFrame({
        'Account ID': ['A001', 'B001'],
        'Account Name': ['Alice Johnson', 'Bob Smith'],
        'Current Balance': [1500, 800]
    })
    
    st.dataframe(accounts_df, use_container_width=True)
    
    # User input area
    user_solution = st.text_area(
        "Write your transaction code:",
        placeholder="START TRANSACTION;\n-- Your code here\nCOMMIT;",
        height=200
    )
    
    # Solution
    with st.expander("💡 View Solution"):
        st.code("""
START TRANSACTION;

-- Check sufficient funds
SELECT balance FROM accounts WHERE account_id = 'A001';

-- Debit from source account
UPDATE accounts 
SET balance = balance - 500 
WHERE account_id = 'A001' AND balance >= 500;

-- Check if update affected any rows
-- If no rows affected, rollback

-- Credit to destination account  
UPDATE accounts 
SET balance = balance + 500 
WHERE account_id = 'B001';

-- Verify both operations succeeded
-- If any issues, ROLLBACK
-- Otherwise, COMMIT

COMMIT;
        """, language="sql")

def show_savepoint_exercise():
    """Savepoint operations exercise."""
    st.subheader("📝 Exercise 2: Savepoint Operations")
    
    st.markdown("""
    **Scenario:** Process a batch of 5 orders. If any order fails validation,
    rollback only that order and continue with the rest.
    """)
    
    # Mock order data
    orders_df = pd.DataFrame({
        'Order ID': [1001, 1002, 1003, 1004, 1005],
        'Product': ['Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Webcam'],
        'Quantity': [1, 2, 1, 1, 3],
        'Price': [999.99, 25.50, 299.99, 79.99, 89.99],
        'Stock Available': [5, 10, 3, 8, 1]  # Order 1005 will fail
    })
    
    st.dataframe(orders_df, use_container_width=True)
    
    user_solution = st.text_area(
        "Write your savepoint transaction:",
        placeholder="START TRANSACTION;\n-- Process orders with savepoints\nCOMMIT;",
        height=250
    )
    
    with st.expander("💡 View Solution"):
        st.code("""
START TRANSACTION;

-- Process Order 1001
SAVEPOINT order_1001;
INSERT INTO order_items (order_id, product, quantity, price) 
VALUES (1001, 'Laptop', 1, 999.99);
UPDATE inventory SET stock = stock - 1 WHERE product = 'Laptop';

-- Process Order 1002  
SAVEPOINT order_1002;
INSERT INTO order_items (order_id, product, quantity, price)
VALUES (1002, 'Mouse', 2, 25.50);
UPDATE inventory SET stock = stock - 2 WHERE product = 'Mouse';

-- Continue for each order...
-- When Order 1005 fails:
SAVEPOINT order_1005;
-- Validation fails (insufficient stock)
ROLLBACK TO SAVEPOINT order_1005;
-- Continue with next order or commit successful ones

COMMIT;
        """, language="sql")

def show_isolation_exercise():
    """Isolation level testing exercise."""
    st.subheader("📝 Exercise 3: Isolation Level Testing")
    
    st.markdown("""
    **Scenario:** Test different isolation levels with concurrent transactions
    accessing the same data.
    """)
    
    # Simplified for space - implement similar pattern

def show_deadlock_exercise():
    """Deadlock resolution exercise.""" 
    st.subheader("📝 Exercise 4: Deadlock Resolution")
    
    st.markdown("""
    **Scenario:** Identify and resolve a deadlock situation between two transactions.
    """)
    
    # Simplified for space

def show_performance_exercise():
    """Performance optimization exercise."""
    st.subheader("📝 Exercise 5: Performance Optimization")
    
    st.markdown("""
    **Scenario:** Optimize transaction performance while maintaining data integrity.
    """)
    
    # Simplified for space

# ================================
# MAIN FUNCTION
# ================================

def main():
    """Main function for TCL module."""
    
    # Main header
    st.title("🔄 Transaction Control Language (TCL)")
    st.markdown("### Master MySQL Transaction Management")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Fundamentals", 
        "📍 Savepoints", 
        "🔒 Isolation Levels",
        "🧪 Practice Lab"    ])
    
    with tab1:
        show_transaction_fundamentals()
    
    with tab2:
        show_savepoints_nested()
    
    with tab3:
        show_isolation_levels()
    
    with tab4:
        show_practice_lab()

if __name__ == "__main__":
    main()