# -*- coding: utf-8 -*-

import xlrd

import environment, log


class ExcelSheet(object):
    def __init__(self, excel, sheet):
        self.excel = xlrd.open_workbook(r"%s\data\%s" % (environment.PROJECT_PATH, excel))
        self.sheet = self.excel.sheet_by_name(sheet)
    
    def nrows(self):
        return self.sheet.nrows
    
    def ncols(self):
        return self.sheet.ncols
    
    def cellxy(self, rowx, colx):
        return self.sheet.cell(rowx, colx).value
    
    def cell(self, rowx, col_name):
        for colx in range(0, self.ncols()):
            if self.cellxy(0, colx) == col_name:
                log.step_normal("ExcelSheet.cellx(%s, %s)=[%s]" % (rowx, col_name, self.cellxy(rowx, colx)))
                return self.cellxy(rowx, colx)
    



