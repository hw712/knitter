
from knitter import logger
import xlrd


class ExcelSheet:
    def __init__(self, excel, sheet):
        """
        :param excel: Location of Excel. e.g. "C:/Archive/TestExcel.xlsx"
        :param sheet: Sheet Name. e.g. "Sheet1"
        """
        self.excel = xlrd.open_workbook(excel)
        self.sheet = self.excel.sheet_by_name(sheet)
        
        # something like: [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
        self.data = [["" for x in range(self.sheet.ncols)] for y in range(self.sheet.nrows)] 
        
        for i in range(self.sheet.nrows):
            for j in range(self.sheet.ncols):
                self.data[i][j] = self.cellxy(i, j)

    def nrows(self):
        return self.sheet.nrows
    
    def ncols(self):
        return self.sheet.ncols
    
    def cellxy(self, rowx, colx):
        """
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
        """
        
        cell_value = self.sheet.cell(rowx, colx).value
        
        if self.sheet.cell(rowx, colx).ctype in (2, 3) and int(cell_value) == cell_value:
            cell_value = int(cell_value)
        
        return str(cell_value)

    def cell(self, rowx, col_name):
        for colx in range(0, self.ncols()):
            if self.cellxy(0, colx) == col_name:
                logger.step_normal("ExcelSheet.cellx(%s, %s)=[%s]" % (rowx, col_name, self.cellxy(rowx, colx)))
                return self.cellxy(rowx, colx)

        return None

    def cell_by_colname(self, rowx, col_name):
        for colx in range(0, self.sheet.ncols):
            if self.data[0][colx] == col_name:
                logger.step_normal("[%s][%s]=[%s]" % (colx, col_name, self.data[rowx][colx]))
                return self.data[rowx][colx]
        
        return None

    def cell_by_rowname(self, row_name, colx):
        for rowx in range(0, self.sheet.nrows):
            if self.data[rowx][0] == row_name:
                logger.step_normal("[%s][%s]=[%s]" % (row_name, colx, self.data[rowx][colx]))
                return self.data[rowx][colx]

        return None

    def cell_by_row_and_col_name(self, row_name, col_name):
        for rowx in range(0, self.nrows()):
            if self.cellxy(rowx, 0) == row_name:
                logger.step_normal("row_name=" + row_name + ", col_name=" + col_name + ", value=" + self.cell(rowx, col_name))
                return self.cell(rowx, col_name)

        return None














