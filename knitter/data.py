# -*- coding: utf-8 -*-

import xlrd

import environment


class ExcelSheet(object):
    def __init__(self, excel, sheet):
        self.excel = xlrd.open_workbook("%s\%s" % (environment.PROJECT_PATH, excel))
        self.sheet = self.excel.sheet_by_name(sheet)
    
    def get_value_by_position(self, row, column):
        return unicode(self.sheet.cell(row,column).value)
    
    def row_count(self):
        return self.sheet.nrows
    
    def get_value_by_row_number(self, row_number, col_name):
        collist = []
        
        for col in range(0, self.sheet.ncols):
            collist.append(self.get_value_by_position(0, col))
        
        return self.get_value_by_position(row_number, collist.index(col_name))
        
    
    def get_value_by_row_name(self, row_name, col_name):
        rowlist = []
        collist = []
        
        for row in range(0, self.sheet.nrows):
            rowlist.append(self.get_value_by_position(row, 0))
        
        for col in range(0, self.sheet.ncols):
            collist.append(self.get_value_by_position(0, col))
        
        return self.get_value_by_position(rowlist.index(row_name), collist.index(col_name))



#for testing...
if __name__=="__main__":
    t = ExcelSheet("E:\\WorkSpace\\ODMAutomation\\Data\\BasicSearch.xlsx", "STT Number")
    
    print t.get_value_by_position(16, 0)
    print t.row_count()
    
    








