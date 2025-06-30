#!/usr/bin/env python3
"""
Example SQL Queries for Construction Project Database
Demonstrates common use cases and SQL query patterns.
"""

from API import ConstructionProjectAPI
import json

def run_example_queries():
    """Run various example queries to demonstrate database usage."""
    
    api = ConstructionProjectAPI()
    
    print("=== Construction Project Database - SQL Query Examples ===\n")
    
    # Example 1: Basic story information
    print("1. GET ALL STORIES WITH DETAILS")
    print("SQL: SELECT * FROM stories ORDER BY floor_level DESC")
    stories = api.execute_query("SELECT * FROM stories ORDER BY floor_level DESC")
    for story in stories:
        print(f"   {story['story_code']}: {story['story_name']} (Level {story['floor_level']})")
    
    print("\n" + "="*60 + "\n")
    
    # Example 2: Elements by category
    print("2. GET ALL FIRE SAFETY ELEMENTS")
    print("SQL: SELECT * FROM elements WHERE category = 'Brandschutz'")
    fire_elements = api.execute_query("""
        SELECT element_code, element_name, description 
        FROM elements 
        WHERE category = 'Brandschutz'
        ORDER BY element_name
    """)
    for element in fire_elements:
        print(f"   {element['element_code']}: {element['element_name']}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 3: Elements for specific story
    print("3. GET ALL ELEMENTS FOR ERDGESCHOSS (EG)")
    print("SQL: Complex JOIN query using story_elements_view")
    eg_elements = api.execute_query("""
        SELECT element_code, element_name, category, quantity, unit
        FROM story_elements_view
        WHERE story_code = 'EG'
        ORDER BY category, element_name
    """, )
    
    current_category = None
    for element in eg_elements:
        if element['category'] != current_category:
            current_category = element['category']
            print(f"\n   {current_category}:")
        print(f"     {element['element_code']}: {element['element_name']} - {element['quantity']} {element['unit']}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 4: Aggregation query
    print("4. ELEMENT QUANTITIES ACROSS ALL STORIES")
    print("SQL: GROUP BY with SUM aggregation")
    totals = api.execute_query("""
        SELECT 
            e.element_name,
            e.category,
            e.unit,
            SUM(se.quantity) as total_quantity
        FROM elements e
        JOIN story_elements se ON e.element_id = se.element_id
        GROUP BY e.element_id, e.element_name, e.category, e.unit
        HAVING total_quantity >= 20
        ORDER BY total_quantity DESC
        LIMIT 10
    """)
    
    print("   Top 10 elements by total quantity (>=20 units):")
    for element in totals:
        print(f"     {element['element_name']}: {element['total_quantity']} {element['unit']} ({element['category']})")
    
    print("\n" + "="*60 + "\n")
    
    # Example 5: Complex JOIN with filtering
    print("5. ELECTRICAL ELEMENTS BY STORY")
    print("SQL: JOIN with WHERE clause filtering")
    electrical = api.execute_query("""
        SELECT s.story_code, s.story_name, e.element_name, se.quantity, e.unit
        FROM stories s
        JOIN story_elements se ON s.story_id = se.story_id
        JOIN elements e ON se.element_id = e.element_id
        WHERE e.category = 'Elektro'
        ORDER BY s.floor_level DESC, e.element_name
    """)
    
    current_story = None
    for item in electrical:
        if item['story_code'] != current_story:
            current_story = item['story_code']
            print(f"\n   {item['story_code']} - {item['story_name']}:")
        print(f"     {item['element_name']}: {item['quantity']} {item['unit']}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 6: Subquery example
    print("6. STORIES WITH ABOVE-AVERAGE ELEMENT COUNT")
    print("SQL: Subquery to find stories with more elements than average")
    above_avg = api.execute_query("""
        SELECT 
            s.story_code,
            s.story_name,
            COUNT(se.element_id) as element_count
        FROM stories s
        LEFT JOIN story_elements se ON s.story_id = se.story_id
        GROUP BY s.story_id, s.story_code, s.story_name
        HAVING element_count > (
            SELECT AVG(cnt) FROM (
                SELECT COUNT(se2.element_id) as cnt
                FROM stories s2
                LEFT JOIN story_elements se2 ON s2.story_id = se2.story_id
                GROUP BY s2.story_id
            )
        )
        ORDER BY element_count DESC
    """)
    
    for story in above_avg:
        print(f"   {story['story_code']}: {story['element_count']} elements")
    
    print("\n" + "="*60 + "\n")
    
    # Example 7: CASE statement for conditional logic
    print("7. ELEMENT COMPLEXITY CLASSIFICATION")
    print("SQL: CASE statement for conditional categorization")
    complexity = api.execute_query("""
        SELECT 
            element_name,
            category,
            SUM(quantity) as total_qty,
            CASE 
                WHEN SUM(quantity) >= 50 THEN 'High Volume'
                WHEN SUM(quantity) >= 20 THEN 'Medium Volume'
                WHEN SUM(quantity) >= 10 THEN 'Standard Volume'
                ELSE 'Low Volume'
            END as volume_category
        FROM elements e
        LEFT JOIN story_elements se ON e.element_id = se.element_id
        GROUP BY e.element_id, element_name, category
        HAVING total_qty > 0
        ORDER BY total_qty DESC
        LIMIT 15
    """)
    
    for item in complexity:
        print(f"   {item['element_name']}: {item['total_qty']} units - {item['volume_category']}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 8: Window function example (if SQLite version supports it)
    print("8. ELEMENT RANKING WITHIN CATEGORIES")
    print("SQL: ROW_NUMBER() window function")
    try:
        ranking = api.execute_query("""
            SELECT 
                category,
                element_name,
                total_quantity,
                ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_quantity DESC) as rank_in_category
            FROM element_totals_view
            WHERE total_quantity > 0
            ORDER BY category, rank_in_category
        """)
        
        current_cat = None
        for item in ranking:
            if item['category'] != current_cat:
                current_cat = item['category']
                print(f"\n   {current_cat}:")
            if item['rank_in_category'] <= 3:  # Show top 3 per category
                print(f"     #{item['rank_in_category']}: {item['element_name']} ({item['total_quantity']} units)")
                
    except Exception as e:
        print("   Window functions not supported in this SQLite version")
        print(f"   Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 9: Custom business logic query
    print("9. FIRE SAFETY COMPLIANCE CHECK")
    print("SQL: Business logic to check fire safety requirements")
    
    fire_safety_check = api.execute_query("""
        SELECT 
            s.story_code,
            s.story_name,
            COUNT(CASE WHEN e.element_code LIKE 'BM%' THEN 1 END) as smoke_detectors,
            COUNT(CASE WHEN e.element_code LIKE 'FLL%' THEN 1 END) as emergency_lights,
            COUNT(CASE WHEN e.element_code LIKE 'FE%' THEN 1 END) as extinguishers,
            CASE 
                WHEN COUNT(CASE WHEN e.element_code LIKE 'BM%' THEN 1 END) >= 1 
                     AND COUNT(CASE WHEN e.element_code LIKE 'FLL%' THEN 1 END) >= 1
                THEN 'COMPLIANT'
                ELSE 'NEEDS REVIEW'
            END as fire_safety_status
        FROM stories s
        LEFT JOIN story_elements se ON s.story_id = se.story_id
        LEFT JOIN elements e ON se.element_id = e.element_id AND e.category = 'Brandschutz'
        GROUP BY s.story_id, s.story_code, s.story_name
        ORDER BY s.floor_level DESC
    """)
    
    for check in fire_safety_check:
        status_symbol = "✓" if check['fire_safety_status'] == 'COMPLIANT' else "⚠"
        print(f"   {status_symbol} {check['story_code']}: {check['fire_safety_status']}")
        print(f"     Smoke Detectors: {check['smoke_detectors']}, Emergency Lights: {check['emergency_lights']}, Extinguishers: {check['extinguishers']}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    run_example_queries()
