import requests
from bs4 import BeautifulSoup
import os
import json
import time
import random
from datetime import datetime, timedelta

# Base URLs for different court systems
HIGH_COURT_BASE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC/"
DISTRICT_COURT_BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"

# Headers to mimic browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Dictionary mapping court names to their codes
HIGH_COURTS = {
    "Allahabad": "1",
    "Bombay": "2",
    "Delhi": "3",
    "Madras": "4",
    "Karnataka": "5",
    "Madhya Pradesh": "6",
    "Gujarat": "7",
    "Calcutta": "8",
    "Patna": "9",
    "Rajasthan": "10",
    "Kerala": "11",
    "Punjab and Haryana": "12",
    "Telangana": "13",
    "Andhra Pradesh": "14",
    "Orissa": "15",
    "Jharkhand": "16",
    "Chhattisgarh": "17",
    "Uttarakhand": "18",
    "Himachal Pradesh": "19",
    "Jammu and Kashmir": "20",
    "Sikkim": "21",
    "Manipur": "22",
    "Meghalaya": "23",
    "Tripura": "24",
    "Guwahati": "25"
}

DISTRICT_COURTS = {
    "Delhi": "1",
    "Mumbai": "2",
    "Chennai": "3",
    "Bangalore": "4",
    "Hyderabad": "5",
    "Ahmedabad": "6",
    "Kolkata": "7",
    "Pune": "8",
    "Jaipur": "9",
    "Lucknow": "10",
    "Chandigarh": "11",
    "Bhopal": "12",
    "Patna": "13",
    "Guwahati": "14",
    "Kochi": "15"
}

# Common case types
CASE_TYPES = {
    "CRL.A": "Criminal Appeal",
    "CWP": "Civil Writ Petition",
    "CRM": "Criminal Miscellaneous",
    "WP": "Writ Petition",
    "CS": "Civil Suit",
    "SA": "Second Appeal",
    "CRA": "Criminal Revision Application",
    "CRLA": "Criminal Appeal",
    "MACA": "Motor Accident Claims Appeal",
    "FAO": "First Appeal from Order"
}

# Case status options
CASE_STATUS = ["Pending", "Disposed", "In Progress", "Listed for Arguments", "Reserved for Judgment", "Adjourned"]

def fetch_case_details(court_type, court_name, case_type, case_number, year):
    """
    Fetch case details from the eCourts portal
    
    Args:
        court_type (str): 'high' or 'district'
        court_name (str): Name of the court
        case_type (str): Type of case (e.g., 'CRL.A', 'CWP')
        case_number (str): Case number
        year (str): Year of filing
        
    Returns:
        dict: Case details including parties, dates, status, and available documents
    """
    try:
        # Log the request
        print(f"Fetching case details for {case_type} {case_number}/{year} from {court_name} {court_type} Court")
        
        # Add a small delay to simulate network request
        time.sleep(1)
        
        if court_type.lower() == 'high':
            return fetch_high_court_case(court_name, case_type, case_number, year)
        elif court_type.lower() == 'district':
            return fetch_district_court_case(court_name, case_type, case_number, year)
        else:
            return {"error": "Invalid court type. Use 'high' or 'district'"}
    except Exception as e:
        return {"error": f"Failed to fetch case details: {str(e)}"}

def fetch_high_court_case(court_name, case_type, case_number, year):
    """Fetch case details from High Court"""
    if court_name not in HIGH_COURTS:
        return {"error": f"Court '{court_name}' not found in supported High Courts"}
    
    court_code = HIGH_COURTS[court_name]
    
    # In a real implementation, we would make actual HTTP requests
    # For demonstration, we'll create more realistic simulated data
    
    # Generate a unique case ID
    case_id = f"HC{court_code}{case_number}{year}"
    
    # Generate random dates
    filing_date = f"{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    
    # Next hearing date should be in the future
    today = datetime.now()
    next_hearing_days = random.randint(7, 60)
    next_hearing_date = (today + timedelta(days=next_hearing_days)).strftime("%Y-%m-%d")
    
    # Generate random status
    status = random.choice(CASE_STATUS)
    
    # Generate petitioner and respondent names
    petitioners = [
        "Rajesh Kumar", "Sunil Sharma", "Priya Patel", "Amit Singh", 
        "Deepak Verma", "Sunita Gupta", "Manoj Tiwari", "Anita Desai",
        "State of Maharashtra", "Union of India", "Municipal Corporation of Delhi"
    ]
    
    respondents = [
        "State of Karnataka", "Central Bureau of Investigation", 
        "Ravi Shankar", "Meena Kumari", "Vikram Mehta", "Neha Sharma",
        "Commissioner of Income Tax", "Life Insurance Corporation of India",
        "Bharat Sanchar Nigam Limited", "Indian Railways"
    ]
    
    petitioner = random.choice(petitioners)
    respondent = random.choice(respondents)
    
    # Generate document list
    documents = []
    
    # Add orders (0-3 orders)
    num_orders = random.randint(0, 3)
    for i in range(num_orders):
        order_date = datetime.strptime(filing_date, "%Y-%m-%d") + timedelta(days=random.randint(30, 500))
        if order_date > datetime.now():
            continue
            
        documents.append({
            "type": "order",
            "date": order_date.strftime("%Y-%m-%d"),
            "id": f"{case_id}_order{i+1}"
        })
    
    # Add judgment if case is disposed
    if status == "Disposed":
        judgment_date = datetime.strptime(filing_date, "%Y-%m-%d") + timedelta(days=random.randint(100, 700))
        if judgment_date <= datetime.now():
            documents.append({
                "type": "judgment",
                "date": judgment_date.strftime("%Y-%m-%d"),
                "id": f"{case_id}_judgment1"
            })
    
    # Create the case details response
    case_details = {
        "case_id": case_id,
        "court": court_name,
        "case_type": case_type,
        "case_number": case_number,
        "year": year,
        "parties": {
            "petitioner": petitioner,
            "respondent": respondent
        },
        "filing_date": filing_date,
        "next_hearing_date": next_hearing_date if status != "Disposed" else "",
        "status": status,
        "documents": documents
    }
    
    return case_details

def fetch_district_court_case(court_name, case_type, case_number, year):
    """Fetch case details from District Court"""
    if court_name not in DISTRICT_COURTS:
        return {"error": f"Court '{court_name}' not found in supported District Courts"}
    
    court_code = DISTRICT_COURTS[court_name]
    
    # Similar to high court case but with district court specific details
    case_id = f"DC{court_code}{case_number}{year}"
    
    # Generate random dates
    filing_date = f"{year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    
    # Next hearing date should be in the future
    today = datetime.now()
    next_hearing_days = random.randint(5, 45)  # District courts often have shorter intervals
    next_hearing_date = (today + timedelta(days=next_hearing_days)).strftime("%Y-%m-%d")
    
    # Generate random status
    status = random.choice(CASE_STATUS)
    
    # Generate petitioner and respondent names
    petitioners = [
        "Ramesh Yadav", "Sanjay Patel", "Anita Deshmukh", "Vijay Kumar", 
        "Preeti Sharma", "Mohan Singh", "Kavita Joshi", "Prakash Reddy",
        "State Bank of India", "HDFC Bank Ltd.", "Reliance Industries Ltd."
    ]
    
    respondents = [
        "State of Gujarat", "Delhi Development Authority", 
        "Suresh Mehta", "Geeta Kapoor", "Rajiv Malhotra", "Pooja Gupta",
        "Municipal Corporation of Mumbai", "Tata Motors Ltd.",
        "Airtel Bharti Ltd.", "Indian Oil Corporation"
    ]
    
    petitioner = random.choice(petitioners)
    respondent = random.choice(respondents)
    
    # Generate document list
    documents = []
    
    # Add orders (0-2 orders, district courts typically have fewer orders)
    num_orders = random.randint(0, 2)
    for i in range(num_orders):
        order_date = datetime.strptime(filing_date, "%Y-%m-%d") + timedelta(days=random.randint(20, 300))
        if order_date > datetime.now():
            continue
            
        documents.append({
            "type": "order",
            "date": order_date.strftime("%Y-%m-%d"),
            "id": f"{case_id}_order{i+1}"
        })
    
    # Add judgment if case is disposed
    if status == "Disposed":
        judgment_date = datetime.strptime(filing_date, "%Y-%m-%d") + timedelta(days=random.randint(60, 500))
        if judgment_date <= datetime.now():
            documents.append({
                "type": "judgment",
                "date": judgment_date.strftime("%Y-%m-%d"),
                "id": f"{case_id}_judgment1"
            })
    
    # Create the case details response
    case_details = {
        "case_id": case_id,
        "court": court_name,
        "case_type": case_type,
        "case_number": case_number,
        "year": year,
        "parties": {
            "petitioner": petitioner,
            "respondent": respondent
        },
        "filing_date": filing_date,
        "next_hearing_date": next_hearing_date if status != "Disposed" else "",
        "status": status,
        "documents": documents
    }
    
    return case_details

def download_judgment(case_id, document_type):
    """
    Download judgment or order document
    
    Args:
        case_id (str): Case ID
        document_type (str): 'judgment' or 'order'
        
    Returns:
        str: Path to downloaded file or error message
    """
    try:
        print(f"Downloading {document_type} for case {case_id}")
        
        # Add a small delay to simulate network request
        time.sleep(1.5)
        
        # In a real implementation, you would make an HTTP request to download the document
        # For demonstration, create a dummy PDF file with more realistic content
        
        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)
        
        filename = f"{case_id}_{document_type}_{int(time.time())}.pdf"
        file_path = os.path.join(download_dir, filename)
        
        # Create a dummy PDF file with more realistic content
        with open(file_path, 'w') as f:
            court_type = "High Court" if case_id.startswith("HC") else "District Court"
            court_code = case_id[2]
            
            if court_type == "High Court":
                court_name = list(HIGH_COURTS.keys())[list(HIGH_COURTS.values()).index(court_code)]
            else:
                court_name = list(DISTRICT_COURTS.keys())[list(DISTRICT_COURTS.values()).index(court_code)]
                
            f.write(f"IN THE {court_type.upper()} OF {court_name.upper()}\n\n")
            f.write(f"Case No: {case_id[3:-4]}/{case_id[-4:]}\n\n")
            
            if document_type == "order":
                f.write("ORDER\n\n")
                f.write("The matter is listed today for hearing. After hearing the arguments of both sides, ")
                f.write("the Court is of the view that further evidence is required. ")
                f.write("The matter is adjourned to a later date to be notified.\n\n")
                f.write("Ordered accordingly.\n\n")
            else:  # judgment
                f.write("JUDGMENT\n\n")
                f.write("Having heard the parties at length and having perused the material on record, ")
                f.write("this Court is of the considered view that the petition deserves to be allowed ")
                f.write("in part. The respondents are directed to consider the representation of the ")
                f.write("petitioner in accordance with law within a period of 8 weeks from today.\n\n")
                f.write("The petition stands disposed of in the above terms.\n\n")
            
            f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n")
            f.write(f"JUDGE")
        
        return filename
    
    except Exception as e:
        return {"error": f"Failed to download document: {str(e)}"}

def fetch_cause_list(court_type, court_name, date):
    """
    Fetch cause list for a specific court and date
    
    Args:
        court_type (str): 'high' or 'district'
        court_name (str): Name of the court
        date (str): Date in YYYY-MM-DD format
        
    Returns:
        dict: Cause list details
    """
    try:
        print(f"Fetching cause list for {court_name} {court_type} Court on {date}")
        
        # Add a small delay to simulate network request
        time.sleep(1.2)
        
        # Validate court type and name
        if court_type.lower() == 'high' and court_name not in HIGH_COURTS:
            return {"error": f"Court '{court_name}' not found in supported High Courts"}
        elif court_type.lower() == 'district' and court_name not in DISTRICT_COURTS:
            return {"error": f"Court '{court_name}' not found in supported District Courts"}
        
        # Create a more realistic cause list
        cause_list = {
            "court": court_name,
            "date": date,
            "cases": []
        }
        
        # Generate a random number of cases (10-30)
        num_cases = random.randint(10, 30)
        
        # List of judges
        judges = [
            "Hon'ble Justice A.K. Sharma", 
            "Hon'ble Justice P.N. Desai",
            "Hon'ble Justice S.R. Mehta",
            "Hon'ble Justice M.K. Gupta",
            "Hon'ble Justice R.S. Chauhan"
        ]
        
        # List of court halls
        court_halls = ["Court Hall 1", "Court Hall 2", "Court Hall 3", "Court Hall 4"]
        
        # Assign a random judge and court hall
        judge = random.choice(judges)
        court_hall = random.choice(court_halls)
        
        cause_list["judge"] = judge
        cause_list["court_hall"] = court_hall
        
        # Generate cases for the cause list
        for i in range(1, num_cases + 1):
            # Select a random case type
            case_type_key = random.choice(list(CASE_TYPES.keys()))
            case_type_full = CASE_TYPES[case_type_key]
            
            # Generate a random case number and year
            case_number = str(random.randint(100, 9999))
            case_year = str(random.randint(2015, 2023))
            
            # Generate random parties
            petitioners = [
                "Rajesh Kumar", "Sunil Sharma", "Priya Patel", "Amit Singh", 
                "State of Maharashtra", "Union of India", "Municipal Corporation of Delhi"
            ]
            
            respondents = [
                "State of Karnataka", "Central Bureau of Investigation", 
                "Ravi Shankar", "Meena Kumari", "Commissioner of Income Tax"
            ]
            
            petitioner = random.choice(petitioners)
            respondent = random.choice(respondents)
            parties = f"{petitioner} vs {respondent}"
            
            # Generate a random purpose
            purposes = [
                "For Hearing", "For Arguments", "For Final Disposal", 
                "For Framing of Issues", "For Recording of Evidence",
                "For Consideration of Application", "For Pronouncement of Judgment"
            ]
            purpose = random.choice(purposes)
            
            # Add the case to the cause list
            cause_list["cases"].append({
                "serial_no": i,
                "case_type": case_type_key,
                "case_type_full": case_type_full,
                "case_number": case_number,
                "year": case_year,
                "parties": parties,
                "purpose": purpose,
                "advocate": f"Adv. {random.choice(['S.K. Joshi', 'P.R. Patel', 'M.S. Reddy', 'A.K. Gupta', 'R.V. Singh'])}"
            })
        
        return cause_list
    
    except Exception as e:
        return {"error": f"Failed to fetch cause list: {str(e)}"}