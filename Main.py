import sys
import os
import random
import LogHours
import subprocess
import ctypes
from RunGame import Launch, LogTime
from LogHours import read_logged_hours
from PySide6 import QtCore, QtWidgets, QtGui
import json
import uuid

log_file_path = "logged_hours.json"
config_file_path = "games_config.json"
setting_file_path = "Settings_config.json"
steamexepath = r"D:\Games\Steam\Steam.exe"


def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with admin privileges."""
    # Get the current Python executable
    python_executable = sys.executable
    # Build the command to run the script with admin rights
    command = f'"{python_executable}" "{__file__}"'
    # Use ShellExecute to run the command as an administrator
    ctypes.windll.shell32.ShellExecuteW(None, "runas", python_executable, __file__, None, 1)


class MyWidget(QtWidgets.QWidget):
    #ADD CLASSES FOR  EACH FUNCTION
    def __init__(self):
        super().__init__()

        self.hourspath = self.load_json(log_file_path, default={})
        self.gamepaths = self.load_json(config_file_path, default={})  # Dictionary to store game paths
        self.settings = self.load_json(setting_file_path, default={'theme': 'dark'})
        self.theme = self.settings.get('theme', 'light')

        self.setWindowIcon(QtGui.QIcon('')) # Set Icon Path
        self.setWindowTitle("Sky Launcher")


        self.settings_button = QtWidgets.QPushButton("Settings")
        self.SetGamePath = QtWidgets.QPushButton("Add New Game")
        self.GameButtonsLayout = QtWidgets.QVBoxLayout()  # Layout to hold game buttons
        self.GameNameText = QtWidgets.QLabel("No Game Path", alignment=QtCore.Qt.AlignCenter)
        self.Empty = QtWidgets.QLabel("")

        self.mainbuttonlayout = QtWidgets.QHBoxLayout()
        self.mainbuttonlayout.addWidget(self.SetGamePath)
        self.mainbuttonlayout.addWidget(self.settings_button)

        self.MAINlayout = QtWidgets.QVBoxLayout(self)
        self.MAINlayout.addLayout(self.mainbuttonlayout)
        self.MAINlayout.addLayout(self.GameButtonsLayout)  # Add dynamic buttons here
        self.MAINlayout.addWidget(self.Empty)

        self.settings_button.clicked.connect(self.open_launcher_settings)
        self.SetGamePath.clicked.connect(self.add_new_game)

        # Create game buttons for already saved games
        self.create_game_buttons()

        self.apply_theme()

    def load_json(self, path, default=None):
        """Helper to load JSON data."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default if default is not None else {}

    def save_json(self, path, data):
        """Helper to save JSON data."""
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def open_launcher_settings(self):
        Dialog  = QtWidgets.QDialog(self)
        Dialog.setWindowTitle("Settings")
        Slayout = QtWidgets.QVBoxLayout()

        Theme_Lable = QtWidgets.QLabel("Select Theme:")
        Slayout.addWidget(Theme_Lable)

        theme_combo = QtWidgets.QComboBox()
        theme_combo.addItems(["Dark", "Light"])
        theme_combo.setCurrentText(self.theme.capitalize())
        Slayout.addWidget(theme_combo)

        Sapply_button = QtWidgets.QPushButton("Apply", clicked=lambda: self.change_theme(theme_combo.currentText().lower()))
        Slayout.addWidget(Sapply_button)

        Dialog.setLayout(Slayout)
        Dialog.exec()

    def open_game_settings(self,  game_id, game_name):
        GSDialog  = QtWidgets.QDialog(self)
        GSDialog.setWindowTitle("Game Settings")
        GSlayout = QtWidgets.QVBoxLayout()
        print("Game Settings")

        GSbuttonlayout = QtWidgets.QHBoxLayout()

        GSremovegame = QtWidgets.QPushButton("Remove Game", clicked=lambda: self.removegame(game_id, game_name))
        GSrenamebutton = QtWidgets.QPushButton("Rename Game", clicked=lambda: self.rename_game(game_id, game_name))
        GSbuttonlayout.addWidget(GSrenamebutton)
        GSbuttonlayout.addWidget(GSremovegame)

        GSlayout.addWidget(QtWidgets.QLabel("Game Settings"))
        GSlayout.addLayout(GSbuttonlayout)
        
        GSDialog.setLayout(GSlayout)
        GSDialog.exec()

    def removegame(self, game_id, game_name):
        # Confirm with the user before removing the game
        reply = QtWidgets.QMessageBox.question(
            self, 'Remove Game', f'Are you sure you want to remove {game_name}?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            # Remove the game from the dictionary
            if game_id in self.gamepaths:
                del self.gamepaths[game_id]
                del self.hourspath[game_id]
                self.save_json(config_file_path, self.gamepaths)  # Save the updated gamepaths

                # Refresh the game buttons
                self.create_game_buttons()

                # Notify the user
                QtWidgets.QMessageBox.information(self, 'Game Removed', f'{game_name} has been removed.')
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', f'{game_name} could not be found.')

    def apply_theme(self):
        if self.theme == 'light':
            self.setStyleSheet("""
                QWidget { background-color: white; color: black; }
                QPushButton { background-color: lightgray; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #2e2e2e; color: white; }
                QPushButton { background-color: #4e4e4e; }
            """)

    def change_theme(self, selected_theme):
        self.theme = selected_theme
        self.apply_theme()
        self.settings['theme'] = self.theme
        self.save_json(setting_file_path, self.settings)

    def add_new_game(self):
        # Ask if the user wants to add a Steam game
        reply = QtWidgets.QMessageBox.question(
            self, 'Steam Game', 'Is this a Steam game?', 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        
        steam_app_id = None  # Default to None, will only store this if it's a Steam game
        
        if reply == QtWidgets.QMessageBox.Yes:
            # If the user selects Yes, prompt for the Steam App ID
            steam_app_id, ok = QtWidgets.QInputDialog.getText(
                self, 'Steam App ID', 'Enter the Steam App ID for this game:'
            )
            if not ok or not steam_app_id.strip():
                # If the user cancels or provides an invalid ID, stop the process
                QtWidgets.QMessageBox.warning(self, 'Error', 'You must enter a valid Steam App ID.')
                return
        
        else:
            # If the user selects No, proceed with file selection dialog for non-Steam games
            file_dialog = QtWidgets.QFileDialog(self)
            file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
            else:
                # If the user cancels the file dialog, stop the process
                return
        
        # Get the game name either from Steam or the file name
        if steam_app_id:
            game_name = f"Steam Game (App ID: {steam_app_id})"
            game_path = None  # Steam games don't require a local path
        else:
            # For non-Steam games, use the file name to generate a game name
            file_name = os.path.basename(file_path)
            game_name, _ = os.path.splitext(file_name)
            game_path = file_path
        
        # Generate a unique ID for the game
        game_id = str(uuid.uuid4())
        
        # Add the new game to the dictionary and save
        self.gamepaths[game_id] = {
            "name": game_name,
            "path": game_path,
            "steam_app_id": steam_app_id  # Add Steam App ID only if applicable
        }
        
        self.save_json(config_file_path, self.gamepaths)
        
        # Add a new button for the new game
        self.add_game_button(game_id, game_name, game_path, steam_app_id)

    def create_game_buttons(self):
        # Clear existing buttons safely
        while self.GameButtonsLayout.count():
            item = self.GameButtonsLayout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

        # Create buttons for each saved game
        for game_id, game_data in self.gamepaths.items():
            game_name = game_data['name']
            game_path = game_data['path']
            steam_app_id = game_data.get('steam_app_id', None)  # Get Steam App ID if present
            self.add_game_button(game_id, game_name, game_path, steam_app_id)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def add_game_button(self, game_id, game_name, game_path, steam_app_id=None):
        # Create a new layout for each button group
        button_layout = QtWidgets.QHBoxLayout()

        play_button = QtWidgets.QPushButton(f"Play {game_name}")
        game_settings_button = QtWidgets.QPushButton("...")

        # Set button functionality
        play_button.clicked.connect(lambda: self.run_game(game_id, game_name, game_path, steam_app_id))
        game_settings_button.clicked.connect(lambda: self.open_game_settings(game_id, game_name))

        # Get the logged hours for all applications
        hours_result, min_result = read_logged_hours(log_file_path)

        # Extract hours for the specific game
        logged_hours = '0 hours'  # Default if the game is not found
        for line in hours_result.split('\n'):
            if f"Application: {game_name}" in line:
                # Extract the total hours from the line
                logged_hours = line.split("Total time: ")[1].strip()  # Get the hours part
                break

        for line in min_result.split('\n'):
            if f"Application: {game_name}" in line:
                # Extract the total minutes from the line
                logged_minutes = line.split("Total time: ")[1].strip()
                break
        


        # Display the Steam App ID if available
        steam_label = QtWidgets.QLabel(f"Steam App ID: {steam_app_id}") if steam_app_id else QtWidgets.QLabel("")

        # Add widgets to the layout
        button_layout.addWidget(play_button)       # Add Play button first
        # Display minutes only if hours are less than 1 hour
        if float(logged_hours.split()[0]) < 1:
            min_label = QtWidgets.QLabel(f"Minutes Played: {logged_minutes}")
            button_layout.addWidget(min_label)
        elif float(logged_hours.split()[0]) >= 1:
            hours_label = QtWidgets.QLabel(f"Hours Played: {logged_hours}")
            button_layout.addWidget(hours_label)
        button_layout.addWidget(steam_label) # Add Steam App ID
        button_layout.addWidget(game_settings_button) # Add Rename button last

        # Now add this new button layout to the GameButtonsLayout   
        self.GameButtonsLayout.addLayout(button_layout)

    def run_game(self, game_id, game_name, gamepaths, steam_app_id=None):
        # Hide the widget
        widget.hide()

        if steam_app_id:
            # If it's a Steam game, launch it using Steam and the App ID
            steampath = f"steam://run/{steam_app_id}"
            elapsed_time = Launch(gamepaths, steampath, steamexepath, steam_app_id)
        else:
            # Otherwise, launch the game normally
            elapsed_time = Launch(gamepaths, None, None, None)

        # Log the time and update the UI
        LogTime(game_id, game_name, elapsed_time)
        read_logged_hours(log_file_path)
        self.create_game_buttons() #refresh for hours played
        widget.show()

    def rename_game(self, game_id, old_game_name):
        # Ask for new game name
        new_game_name, ok = QtWidgets.QInputDialog.getText(
            self, "Rename Game", "Enter new name for the game:", 
            QtWidgets.QLineEdit.Normal, old_game_name
        )
        
        if ok and new_game_name.strip():
            # Ensure the new name is not empty and different from the old name
            if new_game_name != old_game_name:
                # Check if any game already has the new name (using names within the dictionary)
                if any(game_data['name'] == new_game_name for game_data in self.gamepaths.values()):
                    QtWidgets.QMessageBox.warning(self, "Error", 
                        "A game with this name already exists. Please choose another name.")
                    return
                
                # Update the game name for the specific game_id
                self.gamepaths[game_id]['name'] = new_game_name
                self.save_json(config_file_path, self.gamepaths)
                try:
                    # Refresh the UI to show the updated game name
                    self.create_game_buttons()  # Refresh buttons
                except Exception as e:
                    print(f'!!An Error occurred: {e}!!')
            elif new_game_name == new_game_name:
                QtWidgets.QMessageBox.warning(self, "Warning", 
                    "The new name must be different from the old name.")
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', f'{old_game_name} could not be found.')

if __name__ == "__main__":
    #if not is_admin():
    #    print("Requesting administrative privileges...")
    #    run_as_admin()
    #else:
        app = QtWidgets.QApplication([])

        widget = MyWidget()
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
