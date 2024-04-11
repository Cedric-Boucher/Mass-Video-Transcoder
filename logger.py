import os
import datetime

class Logger():
    def __init__(self, log_file_path: str):
        if (not os.path.exists(log_file_path) or not os.path.isfile(log_file_path)):
            with open(log_file_path, "x") as file:
                pass
            if (not os.path.exists(log_file_path) or not os.path.isfile(log_file_path)):
                raise Exception("Failed to create log file")

        self.__log_file_path: str = log_file_path

    def append(self, message: str, print_message: bool = False):
        message = str(message)
        with open(self.__log_file_path, "a") as file:
            file.write("["+datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")+"]: "+message+"\n")
        if print_message:
            print(message)
