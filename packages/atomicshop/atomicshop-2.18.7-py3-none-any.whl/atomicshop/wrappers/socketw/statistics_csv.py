import datetime

from ...file_io import csvs
from ..loggingw import loggingw


LOGGER_NAME: str = 'statistics'
STATISTICS_HEADER: str = (
    'request_time_sent,thread_id,tls,protocol,protocol2,protocol3,host,path,command,status_code,request_size_bytes,'
    'response_size_bytes,file_path,process_cmd,action,error')


class StatisticsCSVWriter:
    """
    Class to write statistics to CSV file.
    This can be initiated at the main, and then passed to the thread worker function.
    """
    def __init__(
            self,
            statistics_directory_path: str
    ):
        self.csv_logger = loggingw.create_logger(
            logger_name=LOGGER_NAME,
            directory_path=statistics_directory_path,
            add_timedfile=True,
            formatter_filehandler='MESSAGE',
            file_type='csv',
            header=STATISTICS_HEADER
        )

    def write_row(
            self,
            thread_id: str,
            host: str,
            tls_type: str,
            tls_version: str,
            protocol: str,
            protocol2: str,
            protocol3: str,
            path: str,
            status_code: str,
            command: str,
            request_size_bytes: str,
            response_size_bytes: str,
            recorded_file_path: str = None,
            process_cmd: str = None,
            error: str = None,
            action: str = None,
            timestamp=None,
    ):
        if not timestamp:
            timestamp = datetime.datetime.now()

        if not tls_type and not tls_version:
            tls_info = ''
        else:
            tls_info = f'{tls_type}|{tls_version}'

        escaped_line_string: str = csvs.escape_csv_line_to_string([
            timestamp,
            thread_id,
            tls_info,
            protocol,
            protocol2,
            protocol3,
            host,
            path,
            command,
            status_code,
            request_size_bytes,
            response_size_bytes,
            recorded_file_path,
            process_cmd,
            action,
            error
        ])

        self.csv_logger.info(escaped_line_string)

    def write_accept_error(
            self,
            error_message: str,
            host: str,
            process_name: str,
            thread_id: str = str()
    ):
        """
        Write the error message to the statistics CSV file.
        This is used for easier execution, since most of the parameters will be empty on accept.

        :param error_message: string, error message.
        :param host: string, host, the domain or IP address.
        :param process_name: process name, the command line of the process.
        :param thread_id: integer, the id of the thread.
        :return:
        """

        self.write_row(
            thread_id=thread_id,
            host=host,
            tls_type='',
            tls_version='',
            protocol='',
            protocol2='',
            protocol3='',
            path='',
            status_code='',
            command='',
            request_size_bytes='',
            response_size_bytes='',
            recorded_file_path='',
            process_cmd=process_name,
            action='client_accept',
            error=error_message
        )
