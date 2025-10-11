import sys
import os
from datetime import datetime
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QCalendarWidget, QTextEdit, QListWidget, QMessageBox,
                             QSpinBox)
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor
from playsound import playsound  

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RemindME")
        self.setGeometry(100, 100, 1000, 600)
        
        # Set sound path
        self.sound_path = os.path.join("warning.mp3")
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel for todo list and input
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Todo input
        input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Enter todo item...")
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_todo)
        input_layout.addWidget(self.todo_input)
        input_layout.addWidget(add_button)
        left_layout.addLayout(input_layout)
        
        # Time input for reminder
        time_layout = QHBoxLayout()
        self.hour_input = QSpinBox()
        self.hour_input.setRange(0, 23)
        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 59)
        
        time_layout.addWidget(QLabel("Reminder Time:"))
        time_layout.addWidget(self.hour_input)
        time_layout.addWidget(QLabel(":"))
        time_layout.addWidget(self.minute_input)
        
        # Duration input for alarm
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 60)
        self.duration_input.setValue(5)
        time_layout.addWidget(QLabel("Alarm Duration (sec):"))
        time_layout.addWidget(self.duration_input)
        
        left_layout.addLayout(time_layout)
        
        # Todo list
        self.todo_list = QListWidget()
        self.todo_list.itemClicked.connect(self.show_note)
        left_layout.addWidget(QLabel("Todo Items:"))
        left_layout.addWidget(self.todo_list)
        
        # Delete and stop alarm buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_todo)
        stop_alarm_button = QPushButton("Stop Alarm")
        stop_alarm_button.clicked.connect(self.stop_alarm)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(stop_alarm_button)
        left_layout.addLayout(button_layout)
        
        # Right panel for calendar and notes
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.date_selected)
        right_layout.addWidget(self.calendar)
        
        # Notes
        right_layout.addWidget(QLabel("Notes:"))
        self.notes_edit = QTextEdit()
        right_layout.addWidget(self.notes_edit)
        
        # Save note button
        self.save_note_button = QPushButton("Save Note")
        self.save_note_button.setObjectName("saveNoteButton")
        self.save_note_button.clicked.connect(self.save_note)
        right_layout.addWidget(self.save_note_button)
        
        # Add panels to main layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        
        # Initialize data structures
        self.todos = {}  # Dictionary to store todos with their notes
        self.reminders = {}  # Dictionary to store reminder times
        self.active_alarms = set()  # Set to track active alarms
        
        # Timer for checking reminders (check every second)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(1000)  # Check every second
        
        # Timer for stopping alarms
        self.alarm_timer = QTimer()
        self.alarm_timer.timeout.connect(self.check_alarm_duration)
        self.alarm_timer.start(1000)

    def add_todo(self):
        todo_text = self.todo_input.text()
        hour = self.hour_input.value()
        minute = self.minute_input.value()
        
        if todo_text:
            current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            todo_key = f"{current_date}: {todo_text}"
            self.todo_list.addItem(todo_key)
            self.todos[todo_key] = ""  # Empty note initially
            
            # Add reminder
            reminder_time = f"{hour:02d}:{minute:02d}"
            try:
                reminder_datetime = datetime.strptime(f"{current_date} {reminder_time}", "%Y-%m-%d %H:%M")
                self.reminders[todo_key] = {
                    'time': reminder_datetime,
                    'duration': self.duration_input.value()
                }
            except ValueError:
                QMessageBox.warning(self, "Invalid Time", "Please enter valid time")
            
            self.todo_input.clear()
    
    def play_alarm(self):
        try:
            playsound(self.sound_path)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to play sound: {e}")
    
    def stop_alarm(self):
        self.active_alarms.clear()
    
    def check_reminders(self):
        current_time = datetime.now()
        for todo_key, reminder_info in list(self.reminders.items()):
            reminder_time = reminder_info['time']
            # Check if it's time for the alarm and it's not already active
            if reminder_time <= current_time and todo_key not in self.active_alarms:
                self.play_alarm()
                self.active_alarms.add(todo_key)
                QMessageBox.information(self, "Reminder", f"Todo reminder: {todo_key}")
    
    def check_alarm_duration(self):
        current_time = datetime.now()
        for todo_key in list(self.active_alarms):
            reminder_info = self.reminders.get(todo_key)
            if reminder_info:
                start_time = reminder_info['time']
                duration = reminder_info['duration']
                if (current_time - start_time).total_seconds() >= duration:
                    self.stop_alarm()
                    self.reminders.pop(todo_key)
                    self.active_alarms.remove(todo_key)
    
    def delete_todo(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_key = current_item.text()
            self.todo_list.takeItem(self.todo_list.row(current_item))
            self.todos.pop(todo_key, None)
            self.reminders.pop(todo_key, None)
            if todo_key in self.active_alarms:
                self.active_alarms.remove(todo_key)
     
    def date_selected(self):
        self.todo_list.clear()
        current_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        for todo_key in self.todos.keys():
            if todo_key.startswith(current_date):
                self.todo_list.addItem(todo_key)
    
    def show_note(self, item):
        todo_key = item.text()
        self.notes_edit.setText(self.todos.get(todo_key, ""))
    
    def save_note(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_key = current_item.text()
            self.todos[todo_key] = self.notes_edit.toPlainText()
    
    def closeEvent(self, event):
        self.stop_alarm()
        event.accept()

def main():
    app = QApplication(sys.argv)

    try:
        with open("alarm6.qss", "r") as file:
            qss = file.read()
            app.setStyleSheet(qss)  # Apply globally
    except FileNotFoundError:
        print("QSS file not found. Please check the file path.")

    window = TodoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
