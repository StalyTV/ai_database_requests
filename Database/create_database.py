#!/usr/bin/env python3
"""
Construction Project Database Creation Script
Creates a SQLite database for a building construction project with stories and elements.
"""

import sqlite3
import os

def create_construction_database():
    """Create and populate the construction project database."""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'construction_project.db')
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Connect to database (creates file if not exists)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Stories table
    cursor.execute('''
        CREATE TABLE stories (
            story_id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_code TEXT UNIQUE NOT NULL,
            story_name TEXT NOT NULL,
            floor_level INTEGER NOT NULL,
            description TEXT
        )
    ''')
    
    # Create Elements table
    cursor.execute('''
        CREATE TABLE elements (
            element_id INTEGER PRIMARY KEY AUTOINCREMENT,
            element_code TEXT UNIQUE NOT NULL,
            element_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Create Story_Elements junction table
    cursor.execute('''
        CREATE TABLE story_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            element_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (story_id) REFERENCES stories (story_id),
            FOREIGN KEY (element_id) REFERENCES elements (element_id),
            UNIQUE(story_id, element_id)
        )
    ''')
    
    # Insert Stories
    stories_data = [
        ('2OG', '2. Obergeschoss', 2, 'Zweites Obergeschoss'),
        ('1OG', '1. Obergeschoss', 1, 'Erstes Obergeschoss'),
        ('EG', 'Erdgeschoss', 0, 'Erdgeschoss/Parterre'),
        ('1UG', '1. Untergeschoss', -1, 'Erstes Untergeschoss')
    ]
    
    cursor.executemany('''
        INSERT INTO stories (story_code, story_name, floor_level, description)
        VALUES (?, ?, ?, ?)
    ''', stories_data)
    
    # Insert Elements (50+ construction elements)
    elements_data = [
        # Fire Safety
        ('BM001', 'Brandmelder', 'Brandschutz', 'Stück', 'Rauchmelder für Brandschutz'),
        ('BM002', 'Brandmelder Hitze', 'Brandschutz', 'Stück', 'Hitzemelder für Küchen/Keller'),
        ('FLL001', 'Fluchtleuchte', 'Brandschutz', 'Stück', 'Notausgangsbeleuchtung'),
        ('FE001', 'Feuerlöscher 6kg', 'Brandschutz', 'Stück', 'Pulverlöscher 6kg'),
        ('FE002', 'Feuerlöscher 12kg', 'Brandschutz', 'Stück', 'Pulverlöscher 12kg'),
        
        # Doors
        ('T001', 'Türe Typ 1', 'Türen', 'Stück', 'Standard Innentür 80cm'),
        ('T002', 'Türe Typ 2', 'Türen', 'Stück', 'Standard Innentür 90cm'),
        ('T003', 'Türe Typ 3', 'Türen', 'Stück', 'Eingangstür Holz'),
        ('T004', 'Türe Typ 4', 'Türen', 'Stück', 'Sicherheitstür Metall'),
        ('T005', 'Schiebetür', 'Türen', 'Stück', 'Schiebetür für Terrasse'),
        ('TZ001', 'Türzarge Holz', 'Türen', 'Stück', 'Holztürzarge standard'),
        ('TZ002', 'Türzarge Metall', 'Türen', 'Stück', 'Metalltürzarge verstärkt'),
        
        # Communication/Data
        ('UKV001', 'UKV Dose', 'Elektro', 'Stück', 'Unterhaltung/Kommunikation/Versorgung Dose'),
        ('LAN001', 'LAN Dose', 'Elektro', 'Stück', 'Netzwerkdose CAT6'),
        ('TEL001', 'Telefondose', 'Elektro', 'Stück', 'Telefonanschluss'),
        ('SAT001', 'SAT Dose', 'Elektro', 'Stück', 'Satellitenanschluss'),
        
        # Electrical
        ('SD001', 'Steckdose Standard', 'Elektro', 'Stück', 'Schuko Steckdose 230V'),
        ('SD002', 'Steckdose Feuchtraum', 'Elektro', 'Stück', 'IP65 Steckdose'),
        ('LS001', 'Lichtschalter', 'Elektro', 'Stück', 'Wechselschalter'),
        ('LS002', 'Dimmer', 'Elektro', 'Stück', 'Dimmer für LED'),
        ('LS003', 'Bewegungsmelder', 'Elektro', 'Stück', 'PIR Bewegungsmelder'),
        ('UV001', 'Unterverteilung', 'Elektro', 'Stück', 'Sicherungskasten 12 Module'),
        
        # Lighting
        ('LED001', 'LED Deckenleuchte', 'Beleuchtung', 'Stück', 'LED Deckenleuchte 18W'),
        ('LED002', 'LED Spots', 'Beleuchtung', 'Stück', 'Einbauspots 7W'),
        ('LED003', 'LED Streifen', 'Beleuchtung', 'Meter', 'LED Strip 24V'),
        ('AUL001', 'Außenleuchte', 'Beleuchtung', 'Stück', 'Wandleuchte außen'),
        
        # HVAC
        ('HK001', 'Heizkörper 600x800', 'Heizung', 'Stück', 'Plattenheizkörper'),
        ('HK002', 'Heizkörper 600x1200', 'Heizung', 'Stück', 'Plattenheizkörper groß'),
        ('HKV001', 'Heizkörperventil', 'Heizung', 'Stück', 'Thermostatventil'),
        ('FBH001', 'Fußbodenheizung', 'Heizung', 'qm', 'Warmwasser Fußbodenheizung'),
        ('LUF001', 'Lüftungsanlage', 'Lüftung', 'Stück', 'Zentrale Lüftungsanlage'),
        ('LUG001', 'Lüftungsgitter', 'Lüftung', 'Stück', 'Zuluftgitter'),
        ('LUA001', 'Lüftungsauslass', 'Lüftung', 'Stück', 'Abluftauslass'),
        
        # Plumbing
        ('WC001', 'WC Keramik', 'Sanitär', 'Stück', 'Wandhängendes WC'),
        ('WB001', 'Waschbecken', 'Sanitär', 'Stück', 'Keramikwaschbecken 60cm'),
        ('DU001', 'Dusche', 'Sanitär', 'Stück', 'Duschtasse 90x90cm'),
        ('BW001', 'Badewanne', 'Sanitär', 'Stück', 'Acryl Badewanne 170cm'),
        ('ARM001', 'Armatur WC', 'Sanitär', 'Stück', 'WC Spülarmatur'),
        ('ARM002', 'Armatur Waschbecken', 'Sanitär', 'Stück', 'Einhebelmischer'),
        ('ARM003', 'Armatur Dusche', 'Sanitär', 'Stück', 'Duscharmatur'),
        
        # Windows
        ('F001', 'Fenster 120x100', 'Fenster', 'Stück', 'Kunststofffenster 3-fach'),
        ('F002', 'Fenster 140x120', 'Fenster', 'Stück', 'Kunststofffenster groß'),
        ('F003', 'Dachfenster', 'Fenster', 'Stück', 'Velux Dachfenster'),
        ('FB001', 'Fensterbank innen', 'Fenster', 'Stück', 'Marmor Fensterbank'),
        ('FB002', 'Fensterbank außen', 'Fenster', 'Stück', 'Blech Fensterbank'),
        ('RO001', 'Rolladen', 'Fenster', 'Stück', 'Elektrischer Rolladen'),
        
        # Flooring
        ('PF001', 'Parkett Eiche', 'Bodenbelag', 'qm', 'Eiche Massivparkett'),
        ('FLT001', 'Fliesen 60x60', 'Bodenbelag', 'qm', 'Feinsteinzeug Fliesen'),
        ('FLT002', 'Fliesen 30x60', 'Bodenbelag', 'qm', 'Wandfliesen Bad'),
        ('LM001', 'Laminat', 'Bodenbelag', 'qm', 'Laminat Eiche Optik'),
        ('TE001', 'Teppich', 'Bodenbelag', 'qm', 'Teppichboden Büro'),
        
        # Insulation & Materials
        ('DA001', 'Dämmung Außenwand', 'Dämmung', 'qm', 'Mineralwolle 16cm'),
        ('DA002', 'Dämmung Dach', 'Dämmung', 'qm', 'Steinwolle 20cm'),
        ('DA003', 'Trittschalldämmung', 'Dämmung', 'qm', 'PE Schaum 5mm'),
        
        # Miscellaneous
        ('BR001', 'Briefkasten', 'Sonstiges', 'Stück', 'Edelstahl Briefkasten'),
        ('KL001', 'Klingel', 'Sonstiges', 'Stück', 'Video Türklingel'),
        ('GA001', 'Garagentor', 'Sonstiges', 'Stück', 'Sektionaltor elektrisch'),
        ('ZA001', 'Zaun', 'Sonstiges', 'Meter', 'Doppelstabmattenzaun'),
        ('TR001', 'Treppe Holz', 'Sonstiges', 'Stück', 'Holztreppe gedrechselt')
    ]
    
    cursor.executemany('''
        INSERT INTO elements (element_code, element_name, category, unit, description)
        VALUES (?, ?, ?, ?, ?)
    ''', elements_data)
    
    # Get story and element IDs for relationships
    cursor.execute('SELECT story_id, story_code FROM stories')
    stories_rows = cursor.fetchall()
    stories = {row[1]: row[0] for row in stories_rows}
    
    cursor.execute('SELECT element_id, element_code FROM elements')
    elements_rows = cursor.fetchall()
    elements = {row[1]: row[0] for row in elements_rows}
    
    # Insert Story-Element relationships with realistic quantities
    story_element_data = []
    
    # 2. Obergeschoss (2OG) - Residential floors typically have fewer elements
    story_2og = stories['2OG']
    story_element_data.extend([
        (story_2og, elements['BM001'], 6, 'Brandmelder in allen Räumen'),
        (story_2og, elements['T001'], 4, 'Innentüren Schlafzimmer'),
        (story_2og, elements['T002'], 2, 'Innentüren Bad/WC'),
        (story_2og, elements['UKV001'], 8, 'TV/Internet Anschlüsse'),
        (story_2og, elements['LAN001'], 6, 'Netzwerkdosen'),
        (story_2og, elements['SD001'], 20, 'Standard Steckdosen'),
        (story_2og, elements['LS001'], 12, 'Lichtschalter'),
        (story_2og, elements['LED001'], 8, 'Deckenleuchten'),
        (story_2og, elements['LED002'], 16, 'LED Spots'),
        (story_2og, elements['HK001'], 4, 'Heizkörper mittel'),
        (story_2og, elements['HK002'], 2, 'Heizkörper groß'),
        (story_2og, elements['F001'], 6, 'Fenster standard'),
        (story_2og, elements['F002'], 2, 'Fenster groß'),
        (story_2og, elements['RO001'], 8, 'Rolladen'),
        (story_2og, elements['WC001'], 2, 'WCs'),
        (story_2og, elements['WB001'], 2, 'Waschbecken'),
        (story_2og, elements['DU001'], 1, 'Dusche'),
        (story_2og, elements['PF001'], 80, 'Parkett Wohnbereich'),
        (story_2og, elements['FLT001'], 25, 'Fliesen Nassbereiche')
    ])
    
    # 1. Obergeschoss (1OG)
    story_1og = stories['1OG']
    story_element_data.extend([
        (story_1og, elements['BM001'], 8, 'Brandmelder alle Räume'),
        (story_1og, elements['T001'], 5, 'Innentüren standard'),
        (story_1og, elements['T002'], 3, 'Innentüren breit'),
        (story_1og, elements['UKV001'], 10, 'TV/Internet'),
        (story_1og, elements['LAN001'], 8, 'Netzwerk'),
        (story_1og, elements['SD001'], 25, 'Steckdosen'),
        (story_1og, elements['LS001'], 15, 'Schalter'),
        (story_1og, elements['LS002'], 3, 'Dimmer Wohnbereich'),
        (story_1og, elements['LED001'], 10, 'Deckenleuchten'),
        (story_1og, elements['LED002'], 20, 'Spots'),
        (story_1og, elements['HK001'], 6, 'Heizkörper'),
        (story_1og, elements['HK002'], 2, 'Heizkörper groß'),
        (story_1og, elements['F001'], 8, 'Fenster'),
        (story_1og, elements['F002'], 3, 'Fenster groß'),
        (story_1og, elements['RO001'], 11, 'Rolladen'),
        (story_1og, elements['WC001'], 2, 'WCs'),
        (story_1og, elements['WB001'], 3, 'Waschbecken'),
        (story_1og, elements['DU001'], 1, 'Dusche'),
        (story_1og, elements['BW001'], 1, 'Badewanne'),
        (story_1og, elements['PF001'], 100, 'Parkett'),
        (story_1og, elements['FLT001'], 30, 'Fliesen')
    ])
    
    # Erdgeschoss (EG) - Main floor with more elements
    story_eg = stories['EG']
    story_element_data.extend([
        (story_eg, elements['BM001'], 10, 'Brandmelder'),
        (story_eg, elements['FLL001'], 4, 'Fluchtleuchten'),
        (story_eg, elements['FE001'], 2, 'Feuerlöscher'),
        (story_eg, elements['T001'], 6, 'Innentüren'),
        (story_eg, elements['T002'], 2, 'Innentüren breit'),
        (story_eg, elements['T003'], 1, 'Eingangstür'),
        (story_eg, elements['T005'], 2, 'Schiebetür Terrasse'),
        (story_eg, elements['UKV001'], 12, 'UKV Dosen'),
        (story_eg, elements['LAN001'], 10, 'LAN Dosen'),
        (story_eg, elements['TEL001'], 3, 'Telefon'),
        (story_eg, elements['SD001'], 30, 'Steckdosen'),
        (story_eg, elements['SD002'], 4, 'Feuchtraum Steckdosen'),
        (story_eg, elements['LS001'], 18, 'Lichtschalter'),
        (story_eg, elements['LS002'], 5, 'Dimmer'),
        (story_eg, elements['LS003'], 2, 'Bewegungsmelder'),
        (story_eg, elements['LED001'], 12, 'Deckenleuchten'),
        (story_eg, elements['LED002'], 25, 'LED Spots'),
        (story_eg, elements['AUL001'], 4, 'Außenleuchten'),
        (story_eg, elements['HK001'], 5, 'Heizkörper'),
        (story_eg, elements['HK002'], 3, 'Heizkörper groß'),
        (story_eg, elements['FBH001'], 60, 'Fußbodenheizung Küche/Bad'),
        (story_eg, elements['F001'], 10, 'Fenster'),
        (story_eg, elements['F002'], 4, 'Fenster groß'),
        (story_eg, elements['RO001'], 14, 'Rolladen'),
        (story_eg, elements['WC001'], 2, 'Gäste-WC + Bad'),
        (story_eg, elements['WB001'], 2, 'Waschbecken'),
        (story_eg, elements['DU001'], 1, 'Dusche'),
        (story_eg, elements['PF001'], 120, 'Parkett Wohnbereich'),
        (story_eg, elements['FLT001'], 40, 'Fliesen Küche/Bad'),
        (story_eg, elements['BR001'], 1, 'Briefkasten'),
        (story_eg, elements['KL001'], 1, 'Türklingel')
    ])
    
    # 1. Untergeschoss (1UG) - Technical floors, storage
    story_1ug = stories['1UG']
    story_element_data.extend([
        (story_1ug, elements['BM002'], 4, 'Hitzemelder Keller'),
        (story_1ug, elements['FLL001'], 6, 'Fluchtleuchten'),
        (story_1ug, elements['FE001'], 1, 'Feuerlöscher'),
        (story_1ug, elements['FE002'], 1, 'Feuerlöscher groß'),
        (story_1ug, elements['T001'], 3, 'Innentüren'),
        (story_1ug, elements['T004'], 1, 'Sicherheitstür'),
        (story_1ug, elements['LAN001'], 4, 'Netzwerk Technikraum'),
        (story_1ug, elements['SD001'], 15, 'Steckdosen'),
        (story_1ug, elements['SD002'], 8, 'Feuchtraum Steckdosen'),
        (story_1ug, elements['LS001'], 8, 'Lichtschalter'),
        (story_1ug, elements['LS003'], 4, 'Bewegungsmelder'),
        (story_1ug, elements['UV001'], 1, 'Hauptverteiler'),
        (story_1ug, elements['LED001'], 8, 'Kellerbeleuchtung'),
        (story_1ug, elements['AUL001'], 2, 'Außenleuchten'),
        (story_1ug, elements['HK001'], 2, 'Heizkörper Hobbyraum'),
        (story_1ug, elements['LUF001'], 1, 'Lüftungsanlage'),
        (story_1ug, elements['LUG001'], 6, 'Lüftungsgitter'),
        (story_1ug, elements['LUA001'], 6, 'Lüftungsauslässe'),
        (story_1ug, elements['F001'], 3, 'Kellerfenster'),
        (story_1ug, elements['WC001'], 1, 'Keller-WC'),
        (story_1ug, elements['WB001'], 1, 'Waschbecken'),
        (story_1ug, elements['FLT001'], 60, 'Fliesen Keller'),
        (story_1ug, elements['TE001'], 20, 'Teppich Hobbyraum'),
        (story_1ug, elements['GA001'], 1, 'Garagentor'),
        (story_1ug, elements['DA001'], 200, 'Außenwanddämmung'),
        (story_1ug, elements['DA003'], 150, 'Trittschalldämmung')
    ])
    
    # Insert all story-element relationships
    cursor.executemany('''
        INSERT INTO story_elements (story_id, element_id, quantity, notes)
        VALUES (?, ?, ?, ?)
    ''', story_element_data)
    
    # Create useful views
    cursor.execute('''
        CREATE VIEW story_elements_view AS
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
        ORDER BY s.floor_level DESC, e.category, e.element_name
    ''')
    
    cursor.execute('''
        CREATE VIEW element_totals_view AS
        SELECT 
            e.element_code,
            e.element_name,
            e.category,
            e.unit,
            SUM(se.quantity) as total_quantity
        FROM elements e
        LEFT JOIN story_elements se ON e.element_id = se.element_id
        GROUP BY e.element_id, e.element_code, e.element_name, e.category, e.unit
        ORDER BY e.category, e.element_name
    ''')
    
    cursor.execute('''
        CREATE VIEW story_summary_view AS
        SELECT 
            s.story_code,
            s.story_name,
            COUNT(se.element_id) as element_count,
            SUM(se.quantity) as total_items
        FROM stories s
        LEFT JOIN story_elements se ON s.story_id = se.story_id
        GROUP BY s.story_id, s.story_code, s.story_name
        ORDER BY s.floor_level DESC
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print("\nDatabase structure:")
    print("- stories: Building levels/floors")
    print("- elements: Construction elements/materials")
    print("- story_elements: Quantities per story")
    print("\nViews created:")
    print("- story_elements_view: Complete overview")
    print("- element_totals_view: Total quantities per element")
    print("- story_summary_view: Summary per story")

if __name__ == "__main__":
    create_construction_database()
