import xlsxwriter
import os
def create_spread(id):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'{id}.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Write some data headers.
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', '116', bold)
    worksheet.write('C1', '117', bold)
    worksheet.write('D1', '118', bold)
    worksheet.write('E1', '119', bold)
    worksheet.write('F1', '120a', bold)
    worksheet.write('G1', '120b', bold)
    worksheet.write('H1', '120c', bold)
    worksheet.write('I1', '121a', bold)
    worksheet.write('J1', '121b', bold)
    worksheet.write('K1', '121c', bold)
    worksheet.write('L1', '121d', bold)
    worksheet.write('M1', '121e', bold)
    worksheet.write('N1', '121f', bold)
    row = 1
    col = 0
    for i in os.listdir('w2_data/corrected_jsondata'):
        worksheet.write(row, col ,i.split('.')[0])
        row += 1
    workbook.close()

create_spread('w2')