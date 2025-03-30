import traceback
import sys

class CustomException(Exception): ## inherited from predefined exception

    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message,error_detail)

    @staticmethod ## we dont need to create custom exp class again and again || function and our method become independent of class creation || not need to create object to use exception
    def get_detailed_error_message(error_message , error_detail:sys):

        _, _, exc_tb = traceback.sys.exc_info() ## last error message will store in exc_tb
        file_name = exc_tb.tb_frame.f_code.co_filename ## in which file the error is occured
        line_number = exc_tb.tb_lineno

        return f"Error in {file_name} , line {line_number} : {error_message}"
    
    def __str__(self):  ## Text extraction of your error message 
        return self.error_message

