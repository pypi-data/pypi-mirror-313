from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from casmodel_func import compute_fluorescence


class FluorescenceSimulationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluorescence Simulation")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Input fields
        self.input_layout = QGridLayout()
        self.layout.addLayout(self.input_layout)

        self.forwardDNA_label = QLabel("Forward DNA:")
        self.forwardDNA_input = QLineEdit()
        self.forwardDNA_input.setText("TTTTTTTTTTTTTGATGATGTGAAGGTGTTGTCGTTTATTTATTTATTTATTTATTTCTATCTTTCCTCTTAATTCGACG")

        self.TemplateConc_label = QLabel("Template Concentration (nM):")
        self.TemplateConc_input = QDoubleSpinBox()
        self.TemplateConc_input.setRange(0, 1e6)
        self.TemplateConc_input.setDecimals(2)
        self.TemplateConc_input.setValue(5.0)

        self.PrimerConc_label = QLabel("Primer Concentration (nM):")
        self.PrimerConc_input = QDoubleSpinBox()
        self.PrimerConc_input.setRange(0, 1e6)
        self.PrimerConc_input.setDecimals(2)
        self.PrimerConc_input.setValue(50.0)

        self.dNTPConc_label = QLabel("dNTP Concentration (nM):")
        self.dNTPConc_input = QDoubleSpinBox()
        self.dNTPConc_input.setRange(0, 1e6)
        self.dNTPConc_input.setDecimals(2)
        self.dNTPConc_input.setValue(100.0)

        self.Kaff_label = QLabel("Kaff:")
        self.Kaff_input = QDoubleSpinBox()
        self.Kaff_input.setRange(0, 1e6)
        self.Kaff_input.setDecimals(2)
        self.Kaff_input.setValue(0.3)

        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)

        # Add widgets to the input layout
        self.input_layout.addWidget(self.forwardDNA_label, 0, 0)
        self.input_layout.addWidget(self.forwardDNA_input, 0, 1)
        self.input_layout.addWidget(self.TemplateConc_label, 1, 0)
        self.input_layout.addWidget(self.TemplateConc_input, 1, 1)
        self.input_layout.addWidget(self.PrimerConc_label, 2, 0)
        self.input_layout.addWidget(self.PrimerConc_input, 2, 1)
        self.input_layout.addWidget(self.dNTPConc_label, 3, 0)
        self.input_layout.addWidget(self.dNTPConc_input, 3, 1)
        self.input_layout.addWidget(self.Kaff_label, 4, 0)
        self.input_layout.addWidget(self.Kaff_input, 4, 1)
        self.input_layout.addWidget(self.run_button, 5, 0, 1, 2)

        # Matplotlib canvas for plotting
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def run_simulation(self):
        # Get inputs
        forwardDNA = self.forwardDNA_input.text()
        TemplateConc_nM = self.TemplateConc_input.value()
        PrimerConc_nM = self.PrimerConc_input.value()
        dNTPConc_nM = self.dNTPConc_input.value()
        Kaff = self.Kaff_input.value()

        # Validate inputs
        if not all(base in "ATCG" for base in forwardDNA.upper()):
            QMessageBox.critical(self, "Error", "Forward DNA sequence contains invalid characters.")
            return

        try:
            # Compute fluorescence
            results = compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM, Kaff)

            # Pass fixed NRTI concentrations
            nrti_concs = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
            self.plot_fluorescence(results, nrti_concs)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def plot_fluorescence(self, results, nrti_concs):
        """Plot the fluorescence on the embedded Matplotlib canvas."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for (time_mins, fluorescence), nrti_conc in zip(results, nrti_concs):
            ax.plot(time_mins, fluorescence, label=f"NRTI_Conc = {nrti_conc:.1e}")
        ax.set_title("Combined Kinetics of RT Incorporation and Cas12a Cleavage")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Fluorescence (RFU)")
        ax.set_xlim(0, 120)
        ax.legend()
        ax.grid(True)
        self.canvas.draw()



# Main loop
def main():
    app = QApplication(sys.argv)
    window = FluorescenceSimulationApp()
    window.show()
    sys.exit(app.exec_())


# Uncomment the line below to run the application locally:
main()
