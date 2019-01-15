import xlrd

A_dic = {}
G_dic = {}
M_dic = {}


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook("./shares.xlsx")

    # 获取A股信息
    A_info = workbook.sheet_by_name("A股")
    A_nrow = A_info.nrows

    for row in range(2, A_nrow):
        title = A_info.cell_value(row, 1)
        code = A_info.cell_value(row, 2)
        nick = None if not A_info.cell_value(row, 3) else A_info.cell_value(row, 3)

        A_dic[code] = {"title": title, "nick": nick}

    # 获取港股信息
    G_info = workbook.sheet_by_name("港股")
    G_nrow = G_info.nrows

    for row in range(2, G_nrow):
        title = G_info.cell_value(row, 1)
        code = G_info.cell_value(row, 2).split(".")[0]
        nick = None if not G_info.cell_value(row, 4) else G_info.cell_value(row, 4)

        G_dic[code] = {"title": title, "nick": nick}

    # 美股
    M_info = workbook.sheet_by_name("美股")
    M_nrow = M_info.nrows

    for row in range(2, M_nrow):
        title = M_info.cell_value(row, 1)
        code = M_info.cell_value(row, 2)
        nick = None if not M_info.cell_value(row, 4) else M_info.cell_value(row, 4)

        M_dic[code] = {"title": title, "nick": nick}

