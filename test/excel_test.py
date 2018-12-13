import xlwt

dic = {'company': 'LinkDoc',
       'education': '本科',
       'experience': '3-5年',
       'name': 'Python开发工程师',
       'position': '北京 海淀区 苏州街',
       'salary': '23k-45k'}

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet("test", cell_overwrite_ok=True)

x = 0
for key, value in dic.items():
    sheet.write(0, x, key)
    sheet.write(1, x, value)
    x += 1

book.save(r'./test1.xls')
