from ttkbootstrap.dialogs import DatePickerDialog

class MyDatePicker:
    def __init__(self, parent):
        self.dialog = DatePickerDialog(
            parent=parent,
            title="Chọn ngày",
            firstweekday=0
        )
        
    def get_date(self):
        return self.dialog.date_selected
