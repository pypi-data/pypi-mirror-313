import pandas as pd


def do_read_and_write_xlsx(file_path):
    # 读取 Excel 文件
    xls = pd.ExcelFile(file_path)

    # 读取工作表1的第一列和第二列
    sheet1 = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    column1_sheet1 = sheet1.iloc[:, 0]
    column2_sheet1 = sheet1.iloc[:, 1]

    # 将工作表1的第一列和第二列分别写入A.txt和B.txt
    with open('./A.txt', 'w', encoding='utf-8') as file_a:
        for item in column1_sheet1:
            file_a.write(f"{item}\n")

    with open('./B.txt', 'w', encoding='utf-8') as file_b:
        for item in column2_sheet1:
            file_b.write(f"{item}\n")

    # 读取工作表2的第一列
    sheet2 = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
    column1_sheet2 = sheet2.iloc[:, 0]

    # 将工作表2的第一列写入C.txt
    with open('./C.txt', 'w', encoding='utf-8') as file_c:
        for item in column1_sheet2:
            file_c.write(f"{item}\n")

    # 读取工作表3的第一列
    sheet3 = pd.read_excel(xls, sheet_name=xls.sheet_names[2])
    column1_sheet3 = sheet3.iloc[:, 0]

    # 将工作表3的第一列写入D.txt
    with open('./D.txt', 'w', encoding='utf-8') as file_d:
        for item in column1_sheet3:
            file_d.write(f"{item}\n")

if __name__ == '__main__':
    # 调用函数，并传入 xlsx 文件的路径
    file_path = "./youtube_url.xlsx"
    do_read_and_write_xlsx(file_path)
