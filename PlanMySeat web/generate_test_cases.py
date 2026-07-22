import csv
import os

output_dir = "Test_Cases_Excel_Sheets"
os.makedirs(output_dir, exist_ok=True)

headers = ["Test Case ID", "Module", "Description", "Steps to Execute", "Expected Result", "Status (Pass/Fail)"]

tests = {
    "Selenium_Website_Tests.csv": [
        ["WEB_001", "Authentication", "Verify Admin Login with correct credentials", "1. Go to URL 2. Enter admin@example.com 3. Enter password 4. Click Sign In", "User is redirected to Dashboard", ""],
        ["WEB_002", "Authentication", "Verify Admin Login with incorrect password", "1. Go to URL 2. Enter admin@example.com 3. Enter wrong password 4. Click Sign In", "Error message 'Invalid credentials' is displayed", ""],
        ["WEB_003", "Faculty Management", "Add new faculty member", "1. Navigate to Faculties 2. Click Add Invigilator 3. Fill details 4. Submit", "Faculty is added to the list and success notification shows", ""],
        ["WEB_004", "Faculty Management", "Bulk upload faculty via CSV", "1. Navigate to Faculties 2. Click Upload CSV 3. Select valid CSV 4. Submit", "All faculties in CSV are parsed and added to list", ""],
        ["WEB_005", "Student Management", "Add new student profile", "1. Navigate to Students 2. Click Add Student 3. Fill details 4. Submit", "Student appears in the roster", ""],
        ["WEB_006", "Room Management", "Add new classroom", "1. Navigate to Rooms 2. Click Add Room 3. Enter Capacity & Details", "Room appears in active plan list with correct capacity", ""],
        ["WEB_007", "Seating Plan", "Generate seating plan successfully", "1. Go to Run Seating 2. Select Exam 3. Click Generate", "Seating plan is generated and saved to database without errors", ""],
        ["WEB_008", "Dashboard", "Verify Dashboard charts", "1. Go to Dashboard 2. Check Bar View", "Charts render correctly based on student branches", ""]
    ],
    
    "Appium_Android_Tests.csv": [
        ["APP_001", "App Launch", "Verify app opens without crashing", "1. Tap app icon on Android device", "Splash screen loads, then webview loads", ""],
        ["APP_002", "UI Responsiveness", "Verify UI scales to mobile screen", "1. Open app 2. Navigate through tabs", "Elements are not cut off, text is readable", ""],
        ["APP_003", "Navigation", "Test native back button", "1. Open a sub-menu 2. Press Android physical Back button", "App navigates back to previous screen or prompts to exit", ""],
        ["APP_004", "Offline Mode", "Verify behavior without internet", "1. Turn off WiFi/Data 2. Open App", "Graceful offline error message is shown", ""],
        ["APP_005", "Permissions", "Verify camera/storage permissions", "1. Attempt to upload bug report screenshot", "OS prompts for storage permission", ""]
    ],
    
    "Unit_Tests_API.csv": [
        ["API_001", "GET /students", "Fetch all students for user", "1. Send GET request to /students/{email}", "Returns 200 OK and JSON array of students", ""],
        ["API_002", "POST /rooms", "Create a new room", "1. Send POST request with valid payload", "Returns 200 OK and the created room object with ID", ""],
        ["API_003", "POST /rooms", "Duplicate room handling", "1. Send POST request with existing room_number", "Returns 400 Bad Request with error detail", ""],
        ["API_004", "PUT /rooms/{id}", "Update existing room capacity", "1. Send PUT request to /rooms/1 with new capacity", "Returns 200 OK and updated capacity reflects in response", ""],
        ["API_005", "POST /final-reports", "Save generated plan", "1. Send POST with valid seating array", "Returns 200 OK and successfully inserts to DB", ""]
    ],
    
    "Validation_Tests.csv": [
        ["VAL_001", "Form Inputs", "Submit Add Student with empty name", "1. Click Add Student 2. Leave name empty 3. Click Submit", "HTML5 validation prevents submission", ""],
        ["VAL_002", "Form Inputs", "Submit Room with negative capacity", "1. Click Add Room 2. Enter -10 capacity 3. Click Submit", "Validation prevents negative numbers", ""],
        ["VAL_003", "Data Integrity", "Update student with existing Reg No", "1. Use existing Reg No 2. Change name 3. Submit", "Student record is replaced/updated instead of creating duplicate", ""],
        ["VAL_004", "Business Logic", "Generate plan with 0 capacity rooms", "1. Create room 2. Go to seating 3. Click Generate", "Alert shows 'Insufficient Seating Capacity'", ""]
    ],
    
    "Load_Testing_Performance.csv": [
        ["PERF_001", "API Load", "Simulate 300 concurrent student GET requests", "1. Run JMeter/Locust script for 300 threads to /students", "Average response time < 500ms, 0% error rate", ""],
        ["PERF_002", "Database Load", "Bulk insert 1000 students via API", "1. Execute script to hit POST /students 1000 times", "Database handles inserts without locking or timeout", ""],
        ["PERF_003", "Frontend Performance", "Render 1000 items in Seating Report table", "1. Generate massive seating plan 2. Open View Reports", "Table renders within 2 seconds without freezing browser", ""],
        ["PERF_004", "Algorithm Speed", "Run AI optimization on max students", "1. Setup 5000 students and 100 rooms 2. Click Apply Optimization", "Algorithm calculates and completes within acceptable timeframe (< 5s)", ""]
    ]
}

for filename, rows in tests.items():
    file_path = os.path.join(output_dir, filename)
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

print("Test case spreadsheets generated successfully.")
