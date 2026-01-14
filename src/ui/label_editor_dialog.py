"""
Label Editor Dialog wrapper for spectrAI.

This module wraps the auto-generated Ui_Dialog to provide
functionality for editing or deleting annotation labels.
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QPushButton
from ui.label_edit import Ui_Dialog


class LabelEditorDialog(QDialog):
    """
    A dialog for editing or deleting a label.
    
    Wraps the auto-generated Ui_Dialog from label_edit.py.
    Receives a reference to the label button to read/modify its text directly.
    
    Attributes:
        label_button (QPushButton): Reference to the label button being edited
        result_action (str): The action taken - "accept", "delete", or "cancel"
    """
    
    def __init__(self, label_button: QPushButton, idx:int, parent=None):
        """
        Initialize the label editor dialog.
        
        Args:
            label_button (QPushButton): The label button to edit
            parent: The parent widget
        """
        super().__init__(parent)
        self.idx = idx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.label_button = label_button
        self.original_name = label_button.text()
        self.result_action = "cancel"
        
        # Set window title
        self.setWindowTitle(f"Edit Label: {self.original_name}")
        
        # Pre-fill the text input with current label name
        self.ui.lineEdit.setText(self.original_name)
        self.ui.lineEdit.selectAll()
        self.ui.lineEdit.setFocus()
        
        # Connect delete button
        self.ui.pushButton.clicked.connect(self.on_delete)
        
        # Disconnect default accepted signal and use our own
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.on_accept)
    
    def on_accept(self):
        """Handle dialog accepted (OK button clicked)."""
        new_name = self.ui.lineEdit.text().strip()
        
        if not new_name:
            QMessageBox.warning(self, "Invalid Name", "Label name cannot be empty.")
            return
        
        # Update the button text directly
        self.label_button.setText(new_name)
        self.result_action = "accept"
        self.accept()
    
    def on_delete(self):
        """Handle delete button click with confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the label '{self.original_name}'?\n\n"
            "Warning: This will affect all existing annotations using this label.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.result_action = "delete"
            self.accept()
    
    def get_result(self):
        """
        Get the result of the dialog.
        
        Returns:
            str: The action taken - "accept", "delete", or "cancel"
        """
        return self.result_action
