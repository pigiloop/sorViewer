import pyOTDR
#pyOTDR/main.py

if __name__ == '__main__':

    input("Привет")

    status, results, tracedata = pyOTDR.main()

    print(status)


    if status != "Writed to file":

        with open("report.txt", "w") as f:
            f.write(results["filename"])

        print(results, tracedata)

        input("Вводи")


