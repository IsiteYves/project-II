# KURA - Youth Growth & Opportunity Bridge

## Description
KURA is a Python CLI application that serves as a resource bridge for Rwandan rural youth, connecting them to opportunities in tourism, agriculture, and mental health resources.

## Features
1. **Register Portfolio** - Youth can create and export their professional profiles
2. **Explore Opportunities** - Browse tourism jobs and agricultural opportunities
3. **Mental Health Resources** - Find support groups and clinics by district
4. **Admin Outreach Logging** - Ministry officials can track district visits
5. **Resume Export** - Generate .txt files of user portfolios

## Installation & Setup

### Prerequisites
- Python 3.x (Any minor version of python 3) installed on your systems

### Running the Application
```bash
python kura.py
```

### Database Setup
The application automatically creates an SQLite database (`kura.db`) on first run with sample data.

## Usage Instructions

### Main Menu
Run the application and select from the menu:
1. Register Portfolio
2. Explore Opportunities  
3. Mental health and wellbeing resources
4. Admin(MOYA/RDB): Log district outreach
5. Exit

### Admin Access
For option 4 (Admin), use password: `admin123`

### Sample Workflow
1. Register your portfolio with personal details
2. Explore opportunities filtered by your district
3. Find mental health resources nearby
4. Export your resume as a .txt file

## Database Structure
- **users** - Youth portfolios and profiles
- **opportunities** - Tourism and agricultural opportunities
- **mental_health** - Support groups and clinics
- **admin_logs** - District outreach records

## Technical Details
- **Language**: Python 3.x (Any minor version of python 3)
- **Database**: SQLite
- **Interface**: Command-line (CLI)
- **Offline Capability**: Our solution works without needing internet connection

## Project Team
- Yves Isite 
- Louange Kenny Rwigamba Ishimwe
- Ezio Munyengango
- Beza Gashayija Ketia
- Birinda Idriss 

## Submission Date
April 29, 2026
