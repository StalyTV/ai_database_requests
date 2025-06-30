#!/usr/bin/env python3
"""
Construction Project Database API
Provides SQL query functionality for the construction project database.
Includes natural language to SQL conversion using OpenAI API.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
import json
import openai
from dotenv import load_dotenv

class ConstructionProjectAPI:
    """API class for accessing the construction project database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the API with database path."""
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'Database', 'construction_project.db')
        self.db_path = db_path
        
        # Check if database exists
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at {self.db_path}")
        
        # Load environment variables and set up OpenAI
        # Try multiple locations for .env file
        env_paths = [
            os.path.join(os.path.dirname(__file__), '.env'),  # Project root
            os.path.join(os.path.expanduser('~'), '.env'),    # User home directory
            '.env'  # Current working directory
        ]
        
        env_loaded = False
        for env_path in env_paths:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                env_loaded = True
                break
        
        if not env_loaded:
            load_dotenv()  # Try to load from system environment
        
        # Get API key from environment
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        if not openai.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables.")
            print("Please set it in one of these ways:")
            print("1. Create a .env file in the project root with: OPENAI_API_KEY=your_key_here")
            print("2. Set it as a system environment variable")
            print("3. Export it in your terminal: export OPENAI_API_KEY=your_key_here")
            print("Natural language to SQL functionality will not be available.")
        
        # Get database schema for AI context
        self.db_schema = self._get_database_schema()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def _get_database_schema(self) -> str:
        """Get database schema information for AI context."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get table schemas
            schema_info = []
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table['name']
                schema_info.append(f"\n--- TABLE: {table_name} ---")
                
                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    schema_info.append(f"{col['name']} {col['type']} {'PRIMARY KEY' if col['pk'] else ''} {'NOT NULL' if col['notnull'] else ''}")
                
                # Get sample data (first 3 rows)
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                if sample_data:
                    schema_info.append("Sample data:")
                    for row in sample_data:
                        schema_info.append(str(dict(row)))
            
            # Get views
            cursor.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
            views = cursor.fetchall()
            
            if views:
                schema_info.append("\n--- VIEWS ---")
                for view in views:
                    schema_info.append(f"VIEW: {view['name']}")
            
            return "\n".join(schema_info)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_single_query(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute a SQL query and return single result as dictionary."""
        results = self.execute_query(query, params)
        return results[0] if results else None
    
    # === Story-related queries ===
    
    def get_all_stories(self) -> List[Dict[str, Any]]:
        """Get all building stories."""
        return self.execute_query("""
            SELECT story_id, story_code, story_name, floor_level, description
            FROM stories
            ORDER BY floor_level DESC
        """)
    
    def get_story_by_code(self, story_code: str) -> Optional[Dict[str, Any]]:
        """Get specific story by code."""
        return self.execute_single_query("""
            SELECT story_id, story_code, story_name, floor_level, description
            FROM stories
            WHERE story_code = ?
        """, (story_code,))
    
    def get_story_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all stories with element counts."""
        return self.execute_query("""
            SELECT * FROM story_summary_view
        """)
    
    # === Element-related queries ===
    
    def get_all_elements(self) -> List[Dict[str, Any]]:
        """Get all construction elements."""
        return self.execute_query("""
            SELECT element_id, element_code, element_name, category, unit, description
            FROM elements
            ORDER BY category, element_name
        """)
    
    def get_elements_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get elements by category."""
        return self.execute_query("""
            SELECT element_id, element_code, element_name, category, unit, description
            FROM elements
            WHERE category = ?
            ORDER BY element_name
        """, (category,))
    
    def get_element_by_code(self, element_code: str) -> Optional[Dict[str, Any]]:
        """Get specific element by code."""
        return self.execute_single_query("""
            SELECT element_id, element_code, element_name, category, unit, description
            FROM elements
            WHERE element_code = ?
        """, (element_code,))
    
    def get_element_categories(self) -> List[str]:
        """Get all unique element categories."""
        results = self.execute_query("""
            SELECT DISTINCT category
            FROM elements
            ORDER BY category
        """)
        return [row['category'] for row in results]
    
    def get_element_totals(self) -> List[Dict[str, Any]]:
        """Get total quantities for all elements across all stories."""
        return self.execute_query("""
            SELECT * FROM element_totals_view
            WHERE total_quantity > 0
        """)
    
    # === Story-Element relationship queries ===
    
    # def get_story_elements(self, story_code: str) -> List[Dict[str, Any]]:
    #     """Get all elements for a specific story."""
    #     return self.execute_query("""
    #         SELECT * FROM story_elements_view
    #         WHERE story_code = ?
    #     """, (story_code,))
    
    # def get_element_stories(self, element_code: str) -> List[Dict[str, Any]]:
    #     """Get all stories that use a specific element."""
    #     return self.execute_query("""
    #         SELECT * FROM story_elements_view
    #         WHERE element_code = ?
    #     """, (element_code,))
    
    # def get_story_elements_by_category(self, story_code: str, category: str) -> List[Dict[str, Any]]:
    #     """Get elements of specific category for a story."""
    #     return self.execute_query("""
    #         SELECT * FROM story_elements_view
    #         WHERE story_code = ? AND category = ?
    #         ORDER BY element_name
    #     """, (story_code, category))
    
    # def get_element_quantity(self, story_code: str, element_code: str) -> Optional[int]:
    #     """Get quantity of specific element in specific story."""
    #     result = self.execute_single_query("""
    #         SELECT quantity FROM story_elements_view
    #         WHERE story_code = ? AND element_code = ?
    #     """, (story_code, element_code))
    #     return result['quantity'] if result else None
    
    # === Advanced queries ===
    
    # def get_elements_above_quantity(self, min_quantity: int) -> List[Dict[str, Any]]:
    #     """Get elements with total quantity above specified amount."""
    #     return self.execute_query("""
    #         SELECT * FROM element_totals_view
    #         WHERE total_quantity >= ?
    #         ORDER BY total_quantity DESC
    #     """, (min_quantity,))
    
    # def search_elements(self, search_term: str) -> List[Dict[str, Any]]:
    #     """Search elements by name or description."""
    #     search_pattern = f"%{search_term}%"
    #     return self.execute_query("""
    #         SELECT element_id, element_code, element_name, category, unit, description
    #         FROM elements
    #         WHERE element_name LIKE ? OR description LIKE ?
    #         ORDER BY element_name
    #     """, (search_pattern, search_pattern))
    
    # def get_story_cost_estimate(self, story_code: str, cost_per_unit: Dict[str, float]) -> Dict[str, Any]:
    #     """Calculate estimated cost for a story based on provided unit costs."""
    #     elements = self.get_story_elements(story_code)
    #     total_cost = 0
    #     element_costs = []
        
    #     for element in elements:
    #         element_code = element['element_code']
    #         quantity = element['quantity']
    #         unit_cost = cost_per_unit.get(element_code, 0)
    #         element_total = quantity * unit_cost
    #         total_cost += element_total
            
    #         element_costs.append({
    #             'element_code': element_code,
    #             'element_name': element['element_name'],
    #             'quantity': quantity,
    #             'unit_cost': unit_cost,
    #             'total_cost': element_total
    #         })
        
    #     return {
    #         'story_code': story_code,
    #         'total_cost': total_cost,
    #         'element_costs': element_costs
    #     }
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get general information about the database."""
        story_count = len(self.get_all_stories())
        element_count = len(self.get_all_elements())
        categories = self.get_element_categories()
        
        # Get total quantities
        total_items = self.execute_single_query("""
            SELECT SUM(quantity) as total FROM story_elements
        """)['total']
        
        return {
            'database_path': self.db_path,
            'story_count': story_count,
            'element_count': element_count,
            'categories': categories,
            'total_items': total_items
        }
    
    def custom_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute custom SQL query (use with caution)."""
        return self.execute_query(query, params)
    
    def natural_language_to_sql_with_context(self, natural_query: str) -> Dict[str, Any]:
        """Convert natural language query to SQL and additional context using OpenAI API."""
        if not openai.api_key:
            raise ValueError("OpenAI API key not configured. Cannot convert natural language to SQL.")
        
        system_prompt = f"""You are a SQL expert for a construction project database. Convert natural language queries to SQL and provide additional context.

Database Schema:
{self.db_schema}

Important Context:
- This is a German construction project database
- Stories are building floors: 2OG (2nd floor), 1OG (1st floor), EG (ground floor), 1UG (basement)
- Element categories include: Brandschutz (fire safety), Elektro (electrical), Türen (doors), etc.
- Use German terms like: Brandmelder (smoke detector), Steckdose (outlet), Fenster (window)
- Common views available: story_elements_view, element_totals_view, story_summary_view

Response Format:
Return a JSON object with exactly these two fields:
{{
    "SQL": "the SQL query to execute",
    "additional": "any additional context, calculations, assumptions, or data needed for the final answer"
}}

Rules for SQL:
1. Use proper SQLite syntax
2. Use JOIN operations when needed to combine tables
3. For German terms, match against element_name or category fields
4. Use story_code for floor references (EG, 1OG, 2OG, 1UG)
5. Include appropriate LIMIT clauses for potentially large results
6. Use ORDER BY for better readability

Rules for Additional:
1. Include any assumptions you make (e.g., prices, calculations)
2. Add context that will help interpret the SQL results
3. Include any additional data not available in the database
4. Provide calculation formulas if needed
5. Leave empty string if no additional context is needed

Examples:
- "Show all elements in the ground floor" → {{"SQL": "SELECT * FROM story_elements_view WHERE story_code = 'EG'", "additional": ""}}
- "How much do all doors cost with 500€ each?" → {{"SQL": "SELECT element_name, SUM(quantity) as total_quantity FROM story_elements_view WHERE element_name LIKE '%Türe%' GROUP BY element_name", "additional": "Assumed price per door: 500€. Calculate total cost by multiplying total_quantity * 500€ for each door type."}}
- "What's the value of electrical elements at market prices?" → {{"SQL": "SELECT element_name, SUM(quantity) as total FROM story_elements_view WHERE category = 'Elektro' GROUP BY element_name", "additional": "Market prices (assumed): Steckdose 15€, Lichtschalter 25€, UKV Dose 45€, LAN Dose 35€, Dimmer 55€, Bewegungsmelder 85€, Unterverteilung 350€"}}
"""

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": natural_query}
                ],
                temperature=0.1,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up the response (remove code blocks if present)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON response
            try:
                result = json.loads(response_text.strip())
                
                # Validate required fields
                if "SQL" not in result or "additional" not in result:
                    raise ValueError("Response missing required fields 'SQL' or 'additional'")
                
                return {
                    "sql": result["SQL"].strip(),
                    "additional": result["additional"].strip()
                }
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from AI: {e}\nResponse: {response_text}")
            
        except Exception as e:
            raise ValueError(f"Error converting natural language to SQL: {str(e)}")

    def results_to_natural_language_with_context(self, natural_query: str, sql_query: str, results: List[Dict[str, Any]], additional_context: str) -> str:
        """Convert SQL results back to natural language using additional context."""
        if not openai.api_key:
            return "Cannot generate natural language response: OpenAI API key not configured."
        
        # Prepare results summary
        results_summary = {
            "row_count": len(results),
            "columns": list(results[0].keys()) if results else [],
            "sample_data": results[:10] if results else []  # First 10 rows
        }
        
        system_prompt = """You are a helpful assistant that converts database query results into natural language responses using additional context.

Your task is to:
1. Analyze the SQL results and additional context to create a comprehensive answer
2. Use the additional context for calculations, assumptions, or extra information
3. Provide specific numbers and calculations when applicable
4. Use appropriate German construction terms when relevant
5. Be detailed but concise
6. If additional context contains prices or calculations, perform the math and show the work
7. Format your response using markdown for better readability:
   - Use **bold** for important information, numbers, and totals
   - Use *italics* for assumptions or clarifications
   - Use bullet points (- or *) for lists
   - Use > for important notes or quotes
   - Use `code formatting` for technical terms or element codes

Context: This is a German construction project database with building floors (2OG, 1OG, EG, 1UG) and construction elements."""

        user_prompt = f"""
Original question: "{natural_query}"
SQL query used: {sql_query}
Additional context: {additional_context}
Results summary: {json.dumps(results_summary, indent=2)}

Please provide a comprehensive natural language response that answers the user's question using both the SQL results and the additional context. If the additional context contains prices or calculations, please perform the math and show the calculations.

Format your response with markdown:
- Use **bold** for important numbers, totals, and key information
- Use *italics* for assumptions or clarifications  
- Use bullet points for lists
- Use `code formatting` for element codes or technical terms
- Use > for important notes
- Don't use unnecessary breaks or empty lines

Make the response clear, professional, and keep very short and descriptive.
"""

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating natural language response: {str(e)}"

    def query_from_natural_language(self, natural_query: str) -> Dict[str, Any]:
        """Convert natural language to SQL with context, execute the query, and return natural language response."""
        try:
            # Step 1: Get SQL query and additional context from AI
            ai_response = self.natural_language_to_sql_with_context(natural_query)
            sql_query = ai_response["sql"]
            additional_context = ai_response["additional"]
            
            # Step 2: Execute SQL query
            results = self.execute_query(sql_query)
            
            # Step 3: Convert results back to natural language using context
            natural_response = self.results_to_natural_language_with_context(
                natural_query, sql_query, results, additional_context
            )
            
            return {
                "natural_query": natural_query,
                "sql_query": sql_query,
                "additional_context": additional_context,
                "results": results,
                "natural_response": natural_response,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            return {
                "natural_query": natural_query,
                "sql_query": None,
                "additional_context": None,
                "results": None,
                "natural_response": f"I apologize, but I encountered an error while processing your question: {str(e)}",
                "success": False,
                "error": str(e)
            }


def interactive_query_interface():
    """Interactive interface for natural language queries."""
    try:
        # Initialize API
        api = ConstructionProjectAPI()
        
        print("=== Construction Project Database - Natural Language Query Interface ===")
        print("\nWelcome! You can ask questions about the construction project database in natural language.")
        print("The AI will convert your questions to SQL queries and show you the results.")
        print("\nExamples:")
        print("- 'Show all elements in the ground floor'")
        print("- 'How many smoke detectors are needed in total?'")
        print("- 'List all electrical elements in the basement'")
        print("- 'What fire safety elements are in the second floor?'")
        print("- 'Show me all doors and their quantities'")
        print("\nType 'quit', 'exit', or 'q' to exit.")
        print("Type 'help' to see database structure information.")
        print("Type 'demo' to see the original demo.")
        print("\n" + "="*70 + "\n")
        
        while True:
            try:
                # Get user input
                user_query = input("Enter your question: ").strip()
                
                if not user_query:
                    continue
                
                # Check for exit commands
                if user_query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                # Help command
                if user_query.lower() == 'help':
                    print("\n=== Database Structure ===")
                    db_info = api.get_database_info()
                    print(f"Stories: {db_info['story_count']}")
                    print(f"Elements: {db_info['element_count']}")
                    print(f"Categories: {', '.join(db_info['categories'])}")
                    print(f"Total Items: {db_info['total_items']}")
                    
                    print("\nStory Codes:")
                    stories = api.get_all_stories()
                    for story in stories:
                        print(f"  {story['story_code']}: {story['story_name']}")
                    
                    print("\nElement Categories:")
                    for category in db_info['categories']:
                        print(f"  {category}")
                    print()
                    continue
                
                
                # Process natural language query
                print(f"\nProcessing: '{user_query}'")
                print("Generating SQL query...")
                
                result = api.query_from_natural_language(user_query)
                
                if result['success']:
                    print(f"\nGenerated SQL: {result['sql_query']}")
                    print(f"\nAI Response:")
                    print(f"  {result['natural_response']}")
                    
                    # Also show raw results for transparency
                    print(f"\nRaw Results ({len(result['results'])} rows):")
                    if result['results']:
                        # Display results in a formatted way
                        if len(result['results']) == 1 and len(result['results'][0]) == 1:
                            # Single value result
                            key = list(result['results'][0].keys())[0]
                            value = result['results'][0][key]
                            print(f"  {key}: {value}")
                        else:
                            # Multiple rows/columns
                            for i, row in enumerate(result['results'][:10]):  # Limit to first 10 rows
                                print(f"  Row {i+1}:")
                                for key, value in row.items():
                                    print(f"    {key}: {value}")
                                print()
                            
                            if len(result['results']) > 10:
                                print(f"  ... and {len(result['results']) - 10} more rows")
                    else:
                        print("  No results found.")
                
                else:
                    print(f"\nAI Response: {result['natural_response']}")
                    print(f"\nError Details: {result['error']}")
                
                print("\n" + "-"*70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Please try again or type 'help' for assistance.\n")
                
    except Exception as e:
        print(f"Error initializing API: {e}")


if __name__ == "__main__":
    interactive_query_interface()
