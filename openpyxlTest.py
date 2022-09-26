# 导入openpyxl package
import openpyxl

# 创建一个工作簿
f = openpyxl.Workbook()
table = f.active
table.title = '结果'


table.cell(row=3, column=1).value = 10


# 保存文件
f.save('demo.xlsx')
