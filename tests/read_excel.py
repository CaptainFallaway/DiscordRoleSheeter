import xlwings

wb = xlwings.Book('checkbox_example.xlsm')

# Get the sheet
sht: xlwings.Sheet = wb.sheets['Roles']

print(sht.range('B2').value)


