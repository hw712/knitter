# -*- coding: utf-8 -*-

import xlrd

import env, log


class ExcelSheet:
    def __init__(self, excel, sheet):
        self.excel = xlrd.open_workbook(r"%s\data\%s" % (env.PROJECT_PATH, excel))
        self.sheet = self.excel.sheet_by_name(sheet)
    
    def nrows(self):
        return self.sheet.nrows
    
    def ncols(self):
        return self.sheet.ncols
    
    def cellxy(self, rowx, colx):
        '''
        Description:
            If the cell value is number, 1234 will get as 1234.0, so fix this issue.
        
        Reference:
            http://stackoverflow.com/questions/2739989/reading-numeric-excel-data-as-text-using-xlrd-in-python
            http://www.lexicon.net/sjmachin/xlrd.html  (Search for "ctype")
            
            self.sheet.cell(rowx, colx).ctype:
                Type symbol    Type number    Python value
                XL_CELL_EMPTY    0           empty string u''
                XL_CELL_TEXT     1           a Unicode string
                XL_CELL_NUMBER   2           float
                XL_CELL_DATE     3           float
                XL_CELL_BOOLEAN  4           int; 1 means TRUE, 0 means FALSE
                ......
        '''
        
        cell_value = self.sheet.cell(rowx, colx).value
        
        if self.sheet.cell(rowx, colx).ctype in (2,3) and int(cell_value) == cell_value:
            cell_value = int(cell_value)
        
        return str(cell_value)
    
    
    def cell(self, rowx, col_name):
        for colx in range(0, self.ncols()):
            if self.cellxy(0, colx) == col_name:
                log.step_normal("ExcelSheet.cellx(%s, %s)=[%s]" % (rowx, col_name, self.cellxy(rowx, colx)))
                return self.cellxy(rowx, colx)
    



