# 导入openpyxl package
import openpyxl

# 创建一个工作簿
f = openpyxl.Workbook()

table = f['Sheet1']


table.cell(row=3, column=1).value = 10


# 保存文件
f.template = True  # 存为模板
f.save('demo.xlsx')
