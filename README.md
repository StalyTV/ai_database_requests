# Construction Project Database Structure

## Overview
This database represents a construction project for a multi-story building with detailed information about construction elements needed for each floor level.

## Database Structure

### Tables

#### 1. `stories` - Building Levels/Floors
Stores information about each floor/story of the building.

| Column | Type | Description |
|--------|------|-------------|
| story_id | INTEGER PRIMARY KEY | Unique identifier for each story |
| story_code | TEXT UNIQUE | Short code (e.g., "EG", "1OG", "2OG", "1UG") |
| story_name | TEXT | Full name in German |
| floor_level | INTEGER | Numeric floor level (negative for underground) |
| description | TEXT | Detailed description |

**Data:**
- **2OG** - 2. Obergeschoss (Level 2)
- **1OG** - 1. Obergeschoss (Level 1) 
- **EG** - Erdgeschoss (Level 0)
- **1UG** - 1. Untergeschoss (Level -1)

#### 2. `elements` - Construction Elements
Contains all construction materials, equipment, and components.

| Column | Type | Description |
|--------|------|-------------|
| element_id | INTEGER PRIMARY KEY | Unique identifier for each element |
| element_code | TEXT UNIQUE | Short code (e.g., "BM001", "T001") |
| element_name | TEXT | Full name in German |
| category | TEXT | Element category |
| unit | TEXT | Unit of measurement (Stück, qm, Meter) |
| description | TEXT | Detailed description |

**Categories (11 total):**
1. **Brandschutz** (Fire Safety) - Brandmelder, Fluchtleuchten, Feuerlöscher
2. **Türen** (Doors) - Various door types and frames
3. **Elektro** (Electrical) - Outlets, switches, network connections
4. **Beleuchtung** (Lighting) - LED lights, spots, outdoor lighting
5. **Heizung** (Heating) - Radiators, floor heating, valves
6. **Lüftung** (Ventilation) - Ventilation systems and components
7. **Sanitär** (Plumbing) - Toilets, sinks, faucets, shower/bath
8. **Fenster** (Windows) - Windows, blinds, window sills
9. **Bodenbelag** (Flooring) - Parquet, tiles, laminate, carpet
10. **Dämmung** (Insulation) - Wall, roof, and sound insulation
11. **Sonstiges** (Miscellaneous) - Mailbox, doorbell, garage door, fence

#### 3. `story_elements` - Junction Table
Links stories to elements with quantities and notes.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique identifier |
| story_id | INTEGER | Foreign key to stories table |
| element_id | INTEGER | Foreign key to elements table |
| quantity | INTEGER | Number of units needed |
| notes | TEXT | Additional notes or specifications |

### Views

#### 1. `story_elements_view`
Complete view combining all three tables for easy querying.

```sql
SELECT 
    s.story_code,
    s.story_name,
    e.element_code,
    e.element_name,
    e.category,
    se.quantity,
    e.unit,
    se.notes
FROM story_elements se
JOIN stories s ON se.story_id = s.story_id
JOIN elements e ON se.element_id = e.element_id
```

#### 2. `element_totals_view`
Shows total quantities needed across all stories for each element.

```sql
SELECT 
    e.element_code,
    e.element_name,
    e.category,
    e.unit,
    SUM(se.quantity) as total_quantity
FROM elements e
LEFT JOIN story_elements se ON e.element_id = se.element_id
GROUP BY e.element_id
```

#### 3. `story_summary_view`
Provides summary statistics for each story.

```sql
SELECT 
    s.story_code,
    s.story_name,
    COUNT(se.element_id) as element_count,
    SUM(se.quantity) as total_items
FROM stories s
LEFT JOIN story_elements se ON s.story_id = se.story_id
GROUP BY s.story_id
```

## Database Statistics

- **4 Stories** (2 above ground, 1 ground level, 1 underground)
- **59 Construction Elements** across 11 categories
- **1,420 Total Items** across all stories
- **97 Story-Element Relationships**

## Element Distribution by Story

### 2. Obergeschoss (2OG) - 19 element types
- Primarily residential elements
- Focus on living spaces (bedrooms, bathrooms)
- 302 total items

### 1. Obergeschoss (1OG) - 21 element types  
- Main residential floor
- Larger living areas, master bathroom
- 389 total items

### Erdgeschoss (EG) - 31 element types
- Most complex floor with entrance, main living areas
- Kitchen, guest facilities, outdoor connections
- 707 total items

### 1. Untergeschoss (1UG) - 26 element types
- Technical floor with utilities, storage, garage
- Additional insulation and ventilation systems
- 322 total items

## Key Element Types

### Most Common Elements (by total quantity):
1. **Parkett Eiche** (Oak Parquet) - 300 qm
2. **Dämmung Außenwand** (External Wall Insulation) - 200 qm
3. **Fliesen 60x60** (Tiles 60x60cm) - 155 qm
4. **Trittschalldämmung** (Impact Sound Insulation) - 150 qm
5. **Steckdose Standard** (Standard Outlets) - 90 pieces

### Fire Safety Elements:
- **Brandmelder** (Smoke Detectors) - 30 total across all floors
- **Fluchtleuchte** (Emergency Lighting) - 10 total
- **Feuerlöscher** (Fire Extinguishers) - 4 total

### Electrical Infrastructure:
- **90 Standard Outlets** across all floors
- **53 Light Switches** of various types
- **28 Network/Communication Connections** (UKV, LAN, Phone, SAT)

## Usage Examples

The database supports various types of queries:

1. **Material Lists per Floor** - Get all elements needed for specific story
2. **Category-based Queries** - Find all electrical or plumbing elements
3. **Quantity Planning** - Calculate total materials needed
4. **Cost Estimation** - Apply unit costs to calculate project costs
5. **Search Functionality** - Find elements by name or description
6. **Progress Tracking** - Monitor installation progress by story/category

## File Structure

```
Database/
├── create_database.py          # Database creation script
└── construction_project.db     # SQLite database file

API.py                          # Python API for database access
example_queries.py              # SQL query examples
test_nl_queries.py              # Natural language query tests
README.md                       # This documentation file
SETUP.md                        # Environment setup guide
.env.example                    # Environment variables template
.gitignore                      # Git ignore file
```

## Setup

1. **Install Dependencies:**
   ```bash
   pip install openai python-dotenv
   ```

2. **Configure Environment:**
   See [SETUP.md](SETUP.md) for detailed instructions on setting up your OpenAI API key.

3. **Quick Start:**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   python API.py
   ```

## API Usage

The `ConstructionProjectAPI` class provides methods for:
- Querying stories, elements, and relationships
- Searching and filtering data
- Calculating totals and statistics
- Executing custom SQL queries
- Cost estimation functionality

See `API.py` for complete API documentation and usage examples.
