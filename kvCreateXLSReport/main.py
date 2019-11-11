import pyOTDR
import json
import os
import re
import xlsxwriter

filename = os.path.normpath("D:\Develop\PythonProjects\pyOTDR\Пионерская 14 [1] - АТС Светлый 1 4 [19].SOR")




def createReflReports(filenames = None):
    if filenames is None:
        return "Error"



    workbook = xlsxwriter.Workbook('filename.xlsx')



    for filename in filenames:
        regexp = r'(.*)\[(.*)\].*[!-](.*)\[(.*)\](.*)'
        addressPackage = re.findall(regexp, os.path.split(filename)[-1], re.IGNORECASE)[0][:-1]
        worksheet1 = workbook.add_worksheet(addressPackage[1])
        Addr1, Port1, Addr2, Port2 = addressPackage
        worksheet1.write('A1', Addr1)
        worksheet1.write('A2', Port1)
        worksheet1.write('A3', Addr2)
        worksheet1.write('A4', Port2)

#        writeWorksheet(filename)

    workbook.close()


def writeWorksheet(worksheet, filename = None):
    if filename is None:
        return "Error"

    status, reports, tracedata = pyOTDR.ConvertSORtoTPL(filename)
    print(status)

    data = reports

    fnameStart, fnameEnd = re.split('-', data['filename'].strip(".SOR"))

    addrStart, numStart = tuple(re.split('\[', fnameStart))
    numStart = numStart[:len(numStart) - 2]
    print(addrStart, numStart)
    addrEnd, numEnd = tuple(re.split('\[', fnameEnd))
    numEnd = numEnd[:len(numEnd) - 2]
    print(addrEnd.lstrip(" "), numEnd)
    return worksheet



#createReflReport(filename)
