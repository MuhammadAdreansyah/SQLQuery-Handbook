#!/usr/bin/env python3
"""
Test script to verify all MySQL Handbook modules load correctly
"""

import sys
import os
from pathlib import Path

# Add pages directory to path
pages_dir = Path(__file__).parent / "pages"
sys.path.append(str(pages_dir))

def test_module_imports():
    """Test that all modules can be imported successfully."""
    modules_to_test = [
        "01_Home",
        "02_BasicQuery", 
        "03_DDL",
        "04_DML",
        "05_DCL",
        "06_TCL",
        "07_AggregateQuery",
        "SQLQueryEditor"
    ]
    
    results = {}
    
    for module_name in modules_to_test:
        try:
            module = __import__(module_name)
            results[module_name] = "✅ SUCCESS"
            print(f"✅ {module_name}: Successfully imported")
        except Exception as e:
            results[module_name] = f"❌ ERROR: {str(e)}"
            print(f"❌ {module_name}: {str(e)}")
    
    return results

def test_main_functions():
    """Test that modules have expected main functions."""
    import importlib
    
    function_map = {
        "01_Home": "show_home",
        "02_BasicQuery": "show_basic_query",
        "03_DDL": "main",
        "04_DML": "main", 
        "05_DCL": "main",
        "06_TCL": "main",
        "07_AggregateQuery": "main",
        "SQLQueryEditor": "main"
    }
    
    results = {}
    
    for module_name, expected_function in function_map.items():
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, expected_function):
                results[module_name] = f"✅ Has {expected_function}()"
                print(f"✅ {module_name}: Has {expected_function}() function")
            else:
                results[module_name] = f"❌ Missing {expected_function}()"
                print(f"❌ {module_name}: Missing {expected_function}() function")
        except Exception as e:
            results[module_name] = f"❌ ERROR: {str(e)}"
            print(f"❌ {module_name}: {str(e)}")
    
    return results

if __name__ == "__main__":
    print("🧪 Testing MySQL Handbook Modules")
    print("=" * 50)
    
    print("\n1. Testing Module Imports:")
    print("-" * 30)
    import_results = test_module_imports()
    
    print("\n2. Testing Main Functions:")
    print("-" * 30)
    function_results = test_main_functions()
    
    print("\n📊 Summary:")
    print("-" * 30)
    total_modules = len(import_results)
    success_imports = sum(1 for result in import_results.values() if "SUCCESS" in result)
    success_functions = sum(1 for result in function_results.values() if "✅" in result)
    
    print(f"Modules imported successfully: {success_imports}/{total_modules}")
    print(f"Functions found successfully: {success_functions}/{total_modules}")
    
    if success_imports == total_modules and success_functions == total_modules:
        print("🎉 All modules are ready!")
    else:
        print("⚠️ Some issues found. Check the details above.")
