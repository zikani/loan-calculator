# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDateEdit, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QSpinBox, QInputDialog
from PyQt5.QtCore import QDate,Qt



VERSION = "v1.0"
COMPANY_NAME = "ZMStech"


class LoanCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Loan Calculator {VERSION}")
        self.setGeometry(0, 0, 400, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.companyLabel = QLabel(COMPANY_NAME, self)
        self.companyLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.companyLabel)

        self.loanAmountLabel = QLabel("Loan Amount:", self)
        self.layout.addWidget(self.loanAmountLabel)

        self.loanAmountInput = QLineEdit(self)
        self.layout.addWidget(self.loanAmountInput)

        self.interestRateLabel = QLabel("Interest Rate (%):", self)
        self.layout.addWidget(self.interestRateLabel)

        self.interestRateInput = QLineEdit(self)
        self.layout.addWidget(self.interestRateInput)

        self.loanPeriodLabel = QLabel("Loan Period (years):", self)
        self.layout.addWidget(self.loanPeriodLabel)

        self.loanPeriodInput = QLineEdit(self)
        self.layout.addWidget(self.loanPeriodInput)

        self.numPaymentsLabel = QLabel("Number of Payments per Year:", self)
        self.layout.addWidget(self.numPaymentsLabel)

        self.numPaymentsInput = QSpinBox(self)
        self.numPaymentsInput.setMinimum(1)
        self.numPaymentsInput.setMaximum(12)
        self.numPaymentsInput.setValue(12)
        self.layout.addWidget(self.numPaymentsInput)

        self.startDateLabel = QLabel("Start Date:", self)
        self.layout.addWidget(self.startDateLabel)

        self.startDateInput = QDateEdit(self)
        self.startDateInput.setDate(QDate.currentDate())
        self.layout.addWidget(self.startDateInput)

        self.extraPaymentsLabel = QLabel("Extra Payments per Payment Interval:", self)
        self.layout.addWidget(self.extraPaymentsLabel)

        self.extraPaymentsInput = QLineEdit(self)
        self.layout.addWidget(self.extraPaymentsInput)

        self.calculateButton = QPushButton("Calculate", self)
        self.calculateButton.clicked.connect(self.calculateLoan)
        self.layout.addWidget(self.calculateButton)

        self.scheduledPaymentLabel = QLabel("Scheduled Payment:", self)
        self.layout.addWidget(self.scheduledPaymentLabel)

        self.scheduledPaymentResult = QLabel(self)
        self.layout.addWidget(self.scheduledPaymentResult)

        self.totalPaymentsLabel = QLabel("Total Payments:", self)
        self.layout.addWidget(self.totalPaymentsLabel)

        self.totalPaymentsResult = QLabel(self)
        self.layout.addWidget(self.totalPaymentsResult)

        self.totalInterestLabel = QLabel("Total Interest:", self)
        self.layout.addWidget(self.totalInterestLabel)

        self.totalInterestResult = QLabel(self)
        self.layout.addWidget(self.totalInterestResult)

        self.amortizationTable = QTableWidget()
        self.layout.addWidget(self.amortizationTable)

        self.sendToCompareButton = QPushButton("Send to Compare", self)
        self.sendToCompareButton.clicked.connect(self.sendToCompare)
        self.layout.addWidget(self.sendToCompareButton)

        self.comparisonToolButton = QPushButton("Comparison Tool", self)
        self.comparisonToolButton.clicked.connect(self.openComparisonTool)
        self.layout.addWidget(self.comparisonToolButton)

        self.loanData = []  # Stores the loan data
        
        self.versionLabel = QLabel(f"{VERSION}", self)
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.versionLabel)

    def calculateLoan(self):
        # Retrieve user inputs
        loanAmount = float(self.loanAmountInput.text())
        interestRate = float(self.interestRateInput.text())
        loanPeriod = int(self.loanPeriodInput.text())
        numPayments = int(self.numPaymentsInput.value())
        startDate = self.startDateInput.date().toString("yyyy-MM-dd")
        extraPayments = float(self.extraPaymentsInput.text()) if self.extraPaymentsInput.text() else 0

        # Perform loan calculations
        monthlyInterestRate = interestRate / (100 * numPayments)
        totalPayments = loanPeriod * numPayments
        monthlyPayment = (loanAmount * monthlyInterestRate) / (1 - (1 + monthlyInterestRate) ** -totalPayments)
        totalPaymentAmount = monthlyPayment * totalPayments
        totalInterestPaid = totalPaymentAmount - loanAmount

        # Display results
        self.scheduledPaymentResult.setText(f"${monthlyPayment:.2f}")
        self.totalPaymentsResult.setText(f"${totalPaymentAmount:.2f}")
        self.totalInterestResult.setText(f"${totalInterestPaid:.2f}")

        # Generate amortization schedule
        self.amortizationTable.setRowCount(totalPayments)
        self.amortizationTable.setColumnCount(5)
        self.amortizationTable.setHorizontalHeaderLabels(
            ["Payment Date", "Payment Amount", "Principal Amount", "Interest Amount", "Remaining Balance"]
        )

        remainingBalance = loanAmount
        for i in range(totalPayments):
            paymentDate = QDate.fromString(startDate, "yyyy-MM-dd").addMonths(i)
            paymentAmount = monthlyPayment + extraPayments
            interestAmount = remainingBalance * monthlyInterestRate
            principalAmount = paymentAmount - interestAmount
            remainingBalance -= principalAmount

            self.amortizationTable.setItem(i, 0, QTableWidgetItem(paymentDate.toString("yyyy-MM-dd")))
            self.amortizationTable.setItem(i, 1, QTableWidgetItem(f"${paymentAmount:.2f}"))
            self.amortizationTable.setItem(i, 2, QTableWidgetItem(f"${principalAmount:.2f}"))
            self.amortizationTable.setItem(i, 3, QTableWidgetItem(f"${interestAmount:.2f}"))
            self.amortizationTable.setItem(i, 4, QTableWidgetItem(f"${remainingBalance:.2f}"))

        # Save loan data
        self.loanData.append(
            {
                "Loan Name": "",
                "Loan Amount": loanAmount,
                "Interest Rate": interestRate,
                "Loan Period": loanPeriod,
                "Scheduled Payment": monthlyPayment,
                "Total Payments": totalPaymentAmount,
                "Total Interest": totalInterestPaid,
            }
        )

    def sendToCompare(self):
        loanName, ok = QInputDialog.getText(self, "Loan Name", "Enter Loan Name:")
        if ok:
            self.loanData[-1]["Loan Name"] = loanName
            self.comparisonTool = ComparisonTool(self.loanData)
            self.comparisonTool.setWindowModality(Qt.ApplicationModal)
            self.comparisonTool.show()

    def openComparisonTool(self):
        self.comparisonTool = ComparisonTool(self.loanData)
        self.comparisonTool.setWindowModality(Qt.ApplicationModal)
        self.comparisonTool.show()



class ComparisonTool(QWidget):
    def __init__(self, loanData):
        super().__init__()

        self.setWindowTitle(f"Loan Comparison Tool v{VERSION}")
        self.setGeometry(0, 0, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

        self.populateTable(loanData)

    def populateTable(self, loanData):
        self.table.setRowCount(len(loanData))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "Loan Name",
                "Loan Amount",
                "Interest Rate",
                "Loan Period",
                "Scheduled Payment",
                "Total Payments",
                "Total Interest",
                "Total Paid Amount",
            ]
        )

        for i, loan in enumerate(loanData):
            self.table.setItem(i, 0, QTableWidgetItem(loan["Loan Name"]))
            self.table.setItem(i, 1, QTableWidgetItem(f"${loan['Loan Amount']:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{loan['Interest Rate']:.2f}%"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{loan['Loan Period']} years"))
            self.table.setItem(i, 4, QTableWidgetItem(f"${loan['Scheduled Payment']:.2f}"))
            self.table.setItem(i, 5, QTableWidgetItem(f"${loan['Total Payments']:.2f}"))
            self.table.setItem(i, 6, QTableWidgetItem(f"${loan['Total Interest']:.2f}"))
            self.table.setItem(i, 7, QTableWidgetItem(f"${loan['Total Payments'] + loan['Total Interest']:.2f}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = LoanCalculator()
    calculator.show()
    sys.exit(app.exec_())