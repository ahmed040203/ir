import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QCheckBox,
                             QVBoxLayout,QButtonGroup, QHBoxLayout , QRadioButton , QComboBox , QLabel, QLineEdit,
                             QTextEdit, QScrollArea)
from PyQt5.QtCore import QThread
import Functions

original_Data=Functions.readed # array contains original files that i will display
prep_data=Functions.preprocessed_hotel_data # array contains preprocessed text that i wil process
# folder_path = "hotel_data"
# readed=Functions.read_pdf_content(folder_path)
# preprocessed_hotel_data = Functions.preprocess_folder(readed) #preprocess hotel data

class HotelSearchEngine(QWidget):
    def _init_(self):
        super()._init_()
        self.initUI()
        self.selected_indexing_types = set()

    def initUI(self):
        self.setWindowTitle('Hotel Search Engine')

        # Create labels and widgets
        self.indexing_label = QLabel("Indexing:")
        self.select_all_button = QCheckBox("Select All")

        self.inverted_index_checkbox = QCheckBox("Inverted Index")
        self.incidence_matrix_checkbox = QCheckBox("Incidence Matrix")
        self.biword_index_checkbox = QCheckBox("Bi-Word Index")
        self.positional_index_checkbox = QCheckBox("Positional Index")

        self.indexing_button = QPushButton("Start Indexing")
        self.indexing_button.setDisabled(True)
        self.indexing_message = QLabel("")

        self.search_label = QLabel("Search:")
        self.normal_search_button = QRadioButton("Normal Search")
        self.boolean_search_button = QRadioButton("Boolean Search")
        self.search_edit = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.setDisabled(True)
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)

        self.inverted_index_button = QRadioButton("Inverted Index")
        self.incidence_matrix_button = QRadioButton("Incidence Matrix")
        self.biword_index_button = QRadioButton("Bi-Word Index")
        self.positional_index_button = QRadioButton("Positional Index")
        self.inverted_index_button.setDisabled(True)
        self.incidence_matrix_button.setDisabled(True)
        self.positional_index_button.setDisabled(True)
        self.biword_index_button.setDisabled(True)
        
        self.search_index_type_group = QButtonGroup()
        self.search_index_type_group.addButton(self.inverted_index_button)
        self.search_index_type_group.addButton(self.incidence_matrix_button)
        self.search_index_type_group.addButton(self.biword_index_button)
        self.search_index_type_group.addButton(self.positional_index_button)
        
        # Connect buttons and checkboxes to Functions
        self.select_all_button.toggled.connect(self.handle_select_all)
        self.inverted_index_checkbox.toggled.connect(self.handle_inverted_index)
        self.incidence_matrix_checkbox.toggled.connect(self.handle_incidence_matrix)
        self.biword_index_checkbox.toggled.connect(self.handle_biword_index)
        self.positional_index_checkbox.toggled.connect(self.handle_positional_index)
        
        self.indexing_button.clicked.connect(self.handle_indexing)
        self.search_type_group = QButtonGroup()
        self.search_type_group.addButton(self.normal_search_button)
        self.search_type_group.addButton(self.boolean_search_button)
        self.search_type_group.buttonClicked.connect(self.enable_search_button)
        self.search_index_type_group.buttonClicked.connect(self.enable_search_button)
        self.search_button.clicked.connect(self.handle_search)
        
        # Combo box for boolean operators
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["AND", "OR"])
        
        # self.operator_combo.currentIndexChanged.connect(self.on_operator_selected)
        self.operator_combo.setEnabled(False)   # Initially disabled
        self.boolean_search_button.clicked.connect(self.enable_box)
        self.normal_search_button.clicked.connect(self.disable_box)

        # self.setLayout(vbox)
        vbox_main = QHBoxLayout()  # Main layout with two columns

        # Indexing section (left column)
        vbox_indexing = QVBoxLayout()
        # vbox_indexing.addWidget(QLabel("Indexing:"))
        vbox_indexing.addWidget(self.select_all_button)
        vbox_indexing.addWidget(self.inverted_index_checkbox)
        vbox_indexing.addWidget(self.incidence_matrix_checkbox)
        vbox_indexing.addWidget(self.biword_index_checkbox)
        vbox_indexing.addWidget(self.positional_index_checkbox)
        vbox_indexing.addWidget(self.indexing_button)
        vbox_indexing.addWidget(self.indexing_label)
        vbox_indexing.addWidget(self.indexing_message)
        vbox_indexing.addWidget(self.search_index_type_group.buttons()[0])  # Add first radio button
        vbox_indexing.addWidget(self.search_index_type_group.buttons()[1])  # Add first radio button
        vbox_indexing.addWidget(self.search_index_type_group.buttons()[2])  # Add first radio button
        vbox_indexing.addWidget(self.search_index_type_group.buttons()[3])  # Add first radio button

        vbox_main.addLayout(vbox_indexing)

# Search section (right column)
        vbox_search = QVBoxLayout()
        vbox_search.addWidget(QLabel("Search:"))
        vbox_search.addWidget(QLabel("Search Type:"))
        vbox_search.addWidget(self.search_type_group.buttons()[0])  # Add first radio button
        vbox_search.addWidget(self.search_type_group.buttons()[1])  # Add second radio button
        vbox_search.addWidget(self.search_label)
        vbox_search.addWidget(self.search_edit)
        vbox_search.addWidget(self.search_button)
        vbox_search.addWidget(self.operator_combo)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.search_results)
        vbox_search.addWidget(scroll)
        vbox_main.addLayout(vbox_search)
    
        self.setLayout(vbox_main)
        self.show()
        
    def handle_inverted_index(self,checked):
        if checked:
            self.inverted_index_checkbox.setChecked(True)
            self.selected_indexing_types.add("inverted index")
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
        else:
            self.inverted_index_checkbox.setChecked(False)
            self.selected_indexing_types.discard("inverted index")
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)

    def handle_biword_index(self,checked):
        if checked:
            self.biword_index_checkbox.setChecked(True)
            self.selected_indexing_types.add("biword index")
            # self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)  
        else:
            self.biword_index_checkbox.setChecked(False)
            self.selected_indexing_types.discard("biword index")
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)

    def handle_positional_index(self,checked):
        if checked:
            self.positional_index_checkbox.setChecked(True)
            self.selected_indexing_types.add("positional index")
            # self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
        else:
            self.positional_index_checkbox.setChecked(False)
            self.selected_indexing_types.discard("positional index")
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)

    def handle_incidence_matrix(self,checked):
        if checked:
            self.incidence_matrix_checkbox.setChecked(True)
            self.selected_indexing_types.add("incidence matrix")
            # self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
        else:
            self.incidence_matrix_checkbox.setChecked(False)
            self.selected_indexing_types.discard("incidence matrix")
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
      
    def handle_select_all(self, checked):
        if checked:
            # Select all indexing options when "Select All" is checked
            self.inverted_index_checkbox.setChecked(True)
            self.incidence_matrix_checkbox.setChecked(True)
            self.biword_index_checkbox.setChecked(True)
            self.positional_index_checkbox.setChecked(True)
            self.selected_indexing_types = {
                "inverted index" if self.inverted_index_checkbox.isChecked() else "",
                "incidence matrix" if self.incidence_matrix_checkbox.isChecked() else "",
                "biword index" if self.biword_index_checkbox.isChecked() else "",
                "positional index" if self.positional_index_checkbox.isChecked() else "",
            }
            self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
            
        else:
            # Deselect all indexing options when "Select All" is unchecked
            self.select_all_button.setChecked(False)
            self.inverted_index_checkbox.setChecked(False)
            self.incidence_matrix_checkbox.setChecked(False)
            self.biword_index_checkbox.setChecked(False)
            self.positional_index_checkbox.setChecked(False)
            self.selected_indexing_types = set()  # Clear the selected types
            # Update indexing button state based on selection
            self.update_indexing_button()

    def update_indexing_button(self):
        # Enable indexing button only if at least one indexing option is selected
        self.indexing_button.setEnabled(len(self.selected_indexing_types) > 0)
        self.indexing_button.setDisabled(len(self.selected_indexing_types) == 0)

    def handle_indexing(self):
        # Implement indexing logic here based on selected_indexing_types
        # (e.g., call Functions to create inverted index, incidence matrix, etc.)
        self.indexing_message.setText("Indexing in progress...")
        # Simulate indexing time
        # QThread.sleep(2)  # Replace with actual indexing process
        if "inverted index" in self.selected_indexing_types :
            self.inverted_index=Functions.create_inverted_index(prep_data)
            self.inverted_index_button.setDisabled(False)
        
        if "incidence matrix" in self.selected_indexing_types :
            self.incidence_matrix=Functions.create_incidence_matrix(prep_data)
            self.incidence_matrix_button.setDisabled(False)
        
        if "biword index" in self.selected_indexing_types :
            self.biword_index=Functions.create_biword_index(prep_data)
            self.biword_index_button.setDisabled(False)
        
        if "positional index" in self.selected_indexing_types :
            self.positional_index=Functions.create_positional_index(prep_data)
            self.positional_index_button.setDisabled(False)
        
        selected_types = ", ".join(self.selected_indexing_types)

        self.indexing_message.setText(f"Indexing completed. {selected_types}")

    def enable_search_button(self):
        # Enable search button only if a search type is selected
        self.search_button.setEnabled(self.search_type_group.checkedButton() is not None and self.search_index_type_group.checkedButton() is not None )
        
    def enable_box(self):
        self.operator_combo.setEnabled(self.boolean_search_button is not None)

    def disable_box(self):
        self.operator_combo.setDisabled(self.normal_search_button is not None)
    
    def handle_search(self):
        # Implement search logic here based on search type (normal or boolean)
        # and search query from search_edit
        search_text = self.search_edit.text()
        if self.normal_search_button.isChecked():
            if self.inverted_index_button.isChecked() :
                # self.inverted_index_button.setDisabled(False)
                result=Functions.search_inverted_index(self.inverted_index,search_text,operator="")
        
            if self.incidence_matrix_button.isChecked() :
                result=Functions.search_inverted_index(self.inverted_index,search_text,operator="")
                # self.incidence_matrix_button.setDisabled(False)
        
            if self.biword_index_button.isChecked() :
                result=Functions.search_biword_index(self.biword_index,search_text,original_Data)
                # self.biword_index_button.setDisabled(False)
        
            if self.positional_index_button.isChecked() :
                result=Functions.search_positional_index(self.positional_index,search_text,original_Data,proximity=3)
                # self.positional_index_button.setDisabled(False)
            # Perform normal search using selected indexing types
            self.search_results.setText("Normal search results for: " + result)
        else:
            if self.inverted_index_button.isChecked() :
                # self.inverted_index_button.setDisabled(False)
                result=Functions.search_inverted_index(self.inverted_index,search_text,operator=self.operator_combo.currentText)
                
        
            if self.incidence_matrix_button.isChecked() :
                result=Functions.search_inverted_index(self.inverted_index,search_text,operator=self.operator_combo.currentText)
        
            if self.biword_index_button.isChecked() :
                result=Functions.search_biword_index(self.biword_index,search_text,original_Data)

        
            if self.positional_index_button.isChecked() :
                result=Functions.search_positional_index(self.positional_index,search_text,original_Data,proximity=3)
            # Perform boolean search using selected indexing types
            self.search_results.setText("Boolean search results for: " + result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hotel_search_engine = HotelSearchEngine()
    sys.exit(app.exec_())