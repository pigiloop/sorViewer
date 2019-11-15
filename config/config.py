class Config:
    def __init__(self):
        self.companyBuilder = 'АО "ТКТ-Строй"'
        self.companyCustomer = 'ПАО "Ростелеком"'
        self.reportInfo = {
            'CompanyBuilder': self.companyBuilder,
            'companyCustomer': self.companyBuilder
        }

    def getCompanyBuilder(self):
        return self.companyBuilder

    def getCompanyCustomer(self):
        return self.companyCustomer

    def getReportInfo(self):
        return self.reportInfo
