import xlrd
import xlwt
import os.path
from xlrd import open_workbook
from xlwt import easyxf
from xlutils.copy import copy

#Help function to work with file

def open_file(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)
    max_row = len(first_sheet.col_values(0))
    result_data =[]
    for curr_row in range(1, max_row, 1):
        row_data = []
        for curr_col in range(0, 3, 1):
            data = first_sheet.cell_value(curr_row, curr_col) # Read the data in the current cell
            row_data.append(data)
        result_data.append(row_data)

    for proName in result_data:
        temp = str(proName[0])
        temp = temp.split('.0')
        proName[0] = temp[0]
    return(result_data)

def _getOutCell(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, row, col, value):
    """ Change cell value without changing formatting. """
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK


#use .xls instead of .xlsx
def edit_file(path, elemList):
    rb = open_workbook(path)
    this_sheet = rb.sheet_by_index(0)
    # read a row
    rowNum = this_sheet.nrows
    # print(this_sheet.nrows)

    wb = copy(rb)

    s = wb.get_sheet(0)
    i = 0
    row = rowNum

    for elem in elemList:
        setOutCell(s, row, i, elem)
        i += 1
    wb.save(path)



