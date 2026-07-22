import csv
import os

output_dir = "Test_Cases_Excel_Sheets"
os.makedirs(output_dir, exist_ok=True)

headers = ["Test Case ID", "Module", "Description", "Steps to Execute", "Expected Result", "Status (Pass/Fail)"]

def generate_selenium_tests():
    cases = []
    # 1. Login permutations (50)
    for i in range(1, 51):
        cases.append([f"WEB_{i:03d}", "Authentication", f"Login boundary test #{i}", f"Enter credentials variation {i}", "System handles login appropriately", ""])
    # 2. Add Faculty permutations (50)
    for i in range(51, 101):
        cases.append([f"WEB_{i:03d}", "Faculty Management", f"Add faculty with data variation {i}", "Submit faculty form", "Validation or success as expected", ""])
    # 3. Add Student permutations (50)
    for i in range(101, 151):
        cases.append([f"WEB_{i:03d}", "Student Management", f"Student profile data variation {i}", "Submit student form", "Record saved correctly", ""])
    # 4. Rooms permutations (50)
    for i in range(151, 201):
        cases.append([f"WEB_{i:03d}", "Room Management", f"Room capacity edge case {i}", "Submit room form", "Room capacity validated", ""])
    # 5. Seating Plan & Dashboard permutations (100)
    for i in range(201, 301):
        cases.append([f"WEB_{i:03d}", "Seating Plan", f"Generate plan for exam type variation {i}", "Click generate seating plan", "Plan is mapped correctly to UI", ""])
    return cases

def generate_appium_tests():
    cases = []
    orientations = ["Portrait", "Landscape"]
    networks = ["WiFi", "4G", "3G", "Offline"]
    for i in range(1, 301):
        orient = orientations[i % 2]
        net = networks[i % 4]
        cases.append([f"APP_{i:03d}", "Mobile UI", f"App test #{i} - {orient} on {net}", f"Launch app in {orient} under {net}", "UI adapts correctly without crashing", ""])
    return cases

def generate_api_tests():
    cases = []
    endpoints = ["GET /students", "POST /students", "GET /rooms", "POST /rooms", "POST /final-reports", "PUT /profile"]
    for i in range(1, 301):
        ep = endpoints[i % len(endpoints)]
        cases.append([f"API_{i:03d}", "Backend Routes", f"API Test #{i} for {ep}", f"Send HTTP request with payload variation {i}", "Endpoint returns correct HTTP status code", ""])
    return cases

def generate_validation_tests():
    cases = []
    fields = ["Email", "Name", "Reg No", "Branch", "Capacity", "Experience", "Phone"]
    for i in range(1, 301):
        field = fields[i % len(fields)]
        cases.append([f"VAL_{i:03d}", "Form Validation", f"Validation test #{i} for {field}", f"Submit form with invalid {field} data pattern {i}", "Frontend blocks submission with error message", ""])
    return cases

def generate_load_tests():
    cases = []
    for i in range(1, 301):
        users = 10 * i
        cases.append([f"PERF_{i:03d}", "Load Testing", f"Load test #{i} with {users} concurrent users", f"Run JMeter script with {users} threads", f"System handles {users} users without crashing", ""])
    return cases

tests = {
    "Selenium_Website_Tests.csv": generate_selenium_tests(),
    "Appium_Android_Tests.csv": generate_appium_tests(),
    "Unit_Tests_API.csv": generate_api_tests(),
    "Validation_Tests.csv": generate_validation_tests(),
    "Load_Testing_Performance.csv": generate_load_tests()
}

for filename, rows in tests.items():
    new_filename = filename.replace('.csv', '_300_cases.csv')
    file_path = os.path.join(output_dir, new_filename)
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

print("Generated 300 test cases for each category.")
