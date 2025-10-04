# Indian Court Case Scraper

A web application for fetching and displaying case details from Indian High Courts and District Courts.

## Features

- Search for case details by Case Type, Case Number, and Year
- Support for both High Courts and District Courts
- Fetch case details including parties' names, filing date, next hearing date, and case status
- Download judgments and orders
- View cause lists for specific courts and dates
- Store query history in a database

## Setup and Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Case Search

1. Select the Court Type (High Court or District Court)
2. Select the Court Name
3. Enter the Case Type (e.g., CRL.A, CWP)
4. Enter the Case Number
5. Enter the Year
6. Click "Search Case"

### Cause List

1. Select the Court Type (High Court or District Court)
2. Select the Court Name
3. Select the Date
4. Click "Get Cause List"

## Note

This application uses simulated data for demonstration purposes. In a production environment, you would need to implement actual web scraping logic to fetch real data from the eCourts portals.

## License

MIT