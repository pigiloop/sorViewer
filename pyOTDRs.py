#!/usr/bin/python
import pyOTDR
import sys
import os
import xlsxwriter
import re
from config import *

import matplotlib.pyplot as plt
import kvCreateXLSReport


def processReports(filenames):
    createXLSReports(filenames)


def convertPair(s):
    return map(float, re.findall(r'(.*)\t(.*)\n', s)[0])
# Первоначальный вариант функции преобразования координат из строк
#    x, y = re.split(r'\t', s.strip('\n'))
#    c = (float(x), float(y))
#   return c


def createXLSReports(filenames):
    print('Старт программы')
    pathReport = os.path.join(os.path.dirname(os.path.normpath(filenames[0])), f'Report {len(filenames)} traces.xlsx')
    print(f'Имя файла отчёта: {pathReport}')
    print('Перед созданием файла')
    #    if not os.path.exists(pathReport) and os.access(pathReport, os.R_OK):
    print('Создание книги')
    workbook = xlsxwriter.Workbook(pathReport)

    prop = {'font_name': 'Arial',
            'font_size': '11'}

    # Задаем параметры форматирования для рабочей книги
    cellFormatHeader = workbook.add_format(prop)
    cellFormatHeader.set_font_size(16)
    cellFormatHeader.set_bold(True)

    cellFormatSubHeader = workbook.add_format(prop)
    cellFormatSubHeader.set_bold(True)

    prop_table = {'font_name': 'Arial',
                  'font_size': '11',
                  'border': 1,
                  'valign': 'center'}

    cellFormatTableHeader = workbook.add_format(prop_table)
    cellFormatTableDataCenter = workbook.add_format(prop_table)
    cellFormatTableDataCenter.set_align('center')
    cellFormatTableDataLeft = workbook.add_format(prop_table)
    cellFormatTableDataLeft.set_align('left')
    cellFormatTableDataRight = workbook.add_format(prop_table)
    cellFormatTableDataRight.set_align('right')

    START_EVENT_ROW = 42

    cellFormatMainText = workbook.add_format(prop)

    print('Перед прогоном файлов')
    c = 1
    width_columns = [9.14, 15, 15, 15, 15, 18.29, 5.29]
    enum_widths = enumerate(width_columns)
    for filename in filenames:
        status, results, tracedata = pyOTDR.ConvertSORtoTPL(filename)

        # Функцию доработать, так как не все файлы именуют с указанием с 2х сторон адресов
        regexp = r'(.*)\[(.*)\].*[!-](.*)\[(.*)\](.*)'
        addressPackage = re.findall(regexp, os.path.split(filename)[-1], re.IGNORECASE)[0][:-1]
        Addr1, Port1, Addr2, Port2 = addressPackage

        if str(results["FxdParams"]["unit"]) == "km (kilometers)":
            unit = "км"
        else:
            unit = "ошибка"

        # Создаём страницу для отчёта
        worksheet = workbook.add_worksheet(f'{c}')
        c += 1
        worksheet.set_portrait()
        worksheet.set_paper(9)

        # устанавливаем ширину колонок
        enum_widths = enumerate(width_columns)
        for col, width in enum_widths:
            print(col, width)
            worksheet.set_column(col, col, width)

        # Заголовок отчёта
        worksheet.write('C2', f'Отчёт OTDR', cellFormatHeader)

        # Подзаголовок параметров
        worksheet.write('C4', f'Параметры', cellFormatSubHeader)

        # Параметры левая колонка
        worksheet.write('A5', f'Начало: {Addr1}', cellFormatMainText)
        worksheet.write('A6', f'Кабель: тип кабеля', cellFormatMainText)
        worksheet.write('A7', f'Диапазон: {results["FxdParams"]["range"]:6.3f} {unit}', cellFormatMainText)
        worksheet.write('A8', f'Длина волны: {results["FxdParams"]["wavelength"]}', cellFormatMainText)
        worksheet.write('A9', f'Порог потерь: {(results["FxdParams"]["loss thr"]).replace("dB", "дБ")}',
                         cellFormatMainText)
        worksheet.write('A10', 'Дата', cellFormatMainText)
        worksheet.write('A11', f'OTDR: {results["SupParams"]["OTDR"]} S/N: {results["SupParams"]["OTDR S/N"]}',
                         cellFormatMainText)
        worksheet.write('A12', f'Модуль: {results["SupParams"]["module"]} S/N: {results["SupParams"]["module S/N"]}',
                         cellFormatMainText)
        worksheet.write('A13', 'Заказчик: ПАО "Ростелеком', cellFormatMainText)
        worksheet.write('A14', 'Подрядчик: АО "ТКТ-Строй', cellFormatMainText)

        # Параметры правая колонка
        worksheet.write('D5', f'Конец: {Addr2}', cellFormatMainText)
        worksheet.write('D6', f'Волокно: {Port2}', cellFormatMainText)
        worksheet.write('D7', f'Импульс: {(results["FxdParams"]["pulse width"]).replace("ns", "нс")}',
                         cellFormatMainText)
        worksheet.write('D8', f'Коэф. преломления: {results["FxdParams"]["index"]}', cellFormatMainText)
        worksheet.write('D9', f'Порог отражения: {results["FxdParams"]["refl thr"]}', cellFormatMainText)
        worksheet.write('D10', f'Файл: {results["filename"]}', cellFormatMainText)

        # Подзаголовок результатов измерений
        worksheet.write('C16', f'Результат измерений', cellFormatSubHeader)

        numEvents = results["KeyEvents"]["num events"]
        distance = results["KeyEvents"][f'event {numEvents}']['distance']
        totalLoss = results["KeyEvents"]["Summary"]['total loss']
        lenghtLoss = float(totalLoss) / float(distance)

        # Результат измерений
        worksheet.write('A17', f'Длина волокна: \t{distance} {unit}', cellFormatMainText)
        worksheet.write('A18', f'Затухание: \t{lenghtLoss:5.3f} дБ/{unit}', cellFormatMainText)
        worksheet.write('E17', f'Полные потери: \t{totalLoss} дБ', cellFormatMainText)

        # Тут будет график рисоваться
#        path = os.path.normpath("D:\develop\python_projects\sorViewer\Гагарина 6а [2]-trace.dat")

        resultTpl = [convertPair(elem) for elem in tracedata]
        xs = []
        ys = []

        for x, y in resultTpl:
            xs.append(x)
            ys.append(y)

        plt.grid(True)

        plt.plot([1.442, 1.442], [17, 15], label='1', color='red')
        plt.plot([3.332, 3.332], [17, 15], label='2', color='red')
        plt.plot(xs, ys, linewidth=0.4, color='black')

        plt.title('Рефлектограмма OTDR')

        plt.axis([-0.05, max(xs), -0.05, max(ys)])
        plt.xlabel('Длина, км')
        plt.ylabel('дБ')


        # Дописать функцию, в зависимости от событий должны чёрточки ставится.
        plt.text(1.1, 14, '1')
        plt.text(1.1, 14, '1')
        plt.text(3.4, 14, '2')
        plt.arrow(3.332, 17, -0.15, 0, color='red', linewidth=0.5, shape='full', head_width=0.4, head_length=0.1)
        plt.arrow(3.332, 15, -0.15, 0, color='red', linewidth=0.5, shape='full', head_width=0.4, head_length=0.1)

        fname, = os.path.splitext(os.path.basename(filename))[:-1]
        pngname = os.path.join(os.path.dirname(filename), fname + '.png')


        plt.savefig(pngname, dpi=300)

        plt.close()

        worksheet.insert_image('A20', pngname, {'x_offset': 40, 'x_scale': 0.9, 'y_scale': 0.9})





        # Тут должна рисоваться таблица
        worksheet.write('C41', 'Таблица событий', cellFormatSubHeader)

        # Рисуем заголовок таблицы
        list_header = ['№', 'Тип', 'Дистанция', 'Потери, дБ', 'Отражение, дБ', 'Затухание, дБ/км']
        enum_header = enumerate(list_header)
        for col_num, col_data in enum_header:
            worksheet.write(START_EVENT_ROW-1, col_num, col_data, cellFormatTableHeader)

        for numEvent in range(numEvents):
            event = results["KeyEvents"][f'event {numEvent + 1}']
            spliceLoss = "---" if float(event["splice loss"]) == 0.00 else event["splice loss"]
            reflectLoss = "---" if event["refl loss"] == "0.000" else event["refl loss"]


            if numEvent + 1 == numEvents:
                typeEvent = "Конец"
            elif float(event["splice loss"]) < 0:
                typeEvent = "Положит. дефект"
            else:
                typeEvent = "Потери"

            list_data = [numEvent + 1, typeEvent, event["distance"], spliceLoss, reflectLoss, event["slope"]]
            enum_data = enumerate(list_data)

            worksheet.write(START_EVENT_ROW + numEvent, 0, numEvent + 1, cellFormatTableDataCenter)
            worksheet.write(START_EVENT_ROW + numEvent, 1, typeEvent, cellFormatTableDataLeft)
            worksheet.write(START_EVENT_ROW + numEvent, 2, event["distance"], cellFormatTableDataRight)
            worksheet.write(START_EVENT_ROW + numEvent, 3, spliceLoss, cellFormatTableDataRight)
            worksheet.write(START_EVENT_ROW + numEvent, 4, reflectLoss, cellFormatTableDataRight)
            worksheet.write(START_EVENT_ROW + numEvent, 5, event["slope"], cellFormatTableDataRight)

        # Задаём область печати
        worksheet.print_area('A1:G57')
        worksheet.fit_to_pages(1, 1)

    workbook.close()
    print('Книга закрылась, запись удалась')


if __name__ == '__main__':
    filenames = sys.argv[1:]

    print(filenames)
    print(filenames.sort())
    processReports(filenames)
