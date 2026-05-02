# getmiallist.py — email list reading from Excel files (using openpyxl, no pandas)
import openpyxl

def read_all_rows_specific_sheet(file_path, sheet_index=0):
    """
    Read all values from the first column of an Excel worksheet.
    """
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        if isinstance(sheet_index, int):
            ws = wb.worksheets[sheet_index]
        else:
            ws = wb[sheet_index]

        first_column = []
        for row in ws.iter_rows(min_col=1, max_col=1, values_only=True):
            val = row[0]
            if val is not None:
                first_column.append(str(val).strip())

        wb.close()
        print(f"工作表 '{sheet_index}' 的数据:")
        print(f"总行数: {len(first_column)}")
        return first_column
    except Exception as e:
        print(f"读取工作表时出错: {str(e)}")
        return None
