import openpyxl

def load_test_cases(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    test_steps = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        test_steps.append({
            "TestCaseID": row[0],
            "StepNo": row[1],
            "Keyword": row[2],
            "Locator": row[3],
            "InputData": row[4],
            "ExpectedResult": row[5],
        })
    return test_steps
