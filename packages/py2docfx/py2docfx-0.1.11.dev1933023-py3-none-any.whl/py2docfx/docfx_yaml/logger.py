import asyncio
import os
import logging
import subprocess

def decide_global_log_level(verbose: bool, show_warning: bool) -> None:
    if verbose and show_warning:
        raise ValueError("Cannot use --verbose and --show-warning at the same time")
    if verbose:
        os.environ['LOG_LEVEL'] = 'INFO'
        return
    if show_warning:
        os.environ['LOG_LEVEL'] = 'WARNING'
        return
    
    # Default log level
    os.environ['LOG_LEVEL'] = 'ERROR'

def get_log_level():
    if os.environ.get('LOG_LEVEL') == 'WARNING':
        return logging.WARNING
    elif os.environ.get('LOG_LEVEL') == 'INFO':
        return logging.INFO
    
    return logging.ERROR

def check_log_dir_exists(log_dir_path):
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

def check_log_file_exists(log_file_path):
    # create log file if it doesn't exist
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            f.write('')

def setup_log_handlers(logger, log_file_name):
    check_log_file_exists(log_file_name)
    file_handler = logging.FileHandler(filename=log_file_name, mode='a')
    file_handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(file_handler)
    
    return logger

def get_logger(logger_name: str):
    log_folder_path = os.path.join("logs")
    file_name = os.path.join(log_folder_path, "log.txt")
    
    file_logger = logging.getLogger(logger_name)
    file_logger.setLevel(logging.INFO)
    check_log_dir_exists(log_folder_path)
    if file_logger.hasHandlers():
        return file_logger
    
    file_logger = setup_log_handlers(file_logger, file_name)

    return file_logger

def get_package_logger(logger_name:str):
    log_folder_path = os.path.join("logs", "package_logs")
    package_name = os.environ.get('PROCESSING_PACKAGE_NAME')
    file_name = os.path.join(log_folder_path, f"{package_name}.txt")
    
    file_logger = logging.getLogger(logger_name)
    file_logger.setLevel(logging.INFO)
    check_log_dir_exists(log_folder_path)
    if file_logger.hasHandlers():
        return file_logger

    file_logger = setup_log_handlers(file_logger, file_name)
    
    return file_logger

def log_subprocess_ouput(subprocess_out: subprocess.CompletedProcess, logger: logging.Logger):
    if subprocess_out.stdout:
        logger.info(subprocess_out.stdout)
    if subprocess_out.stderr:
        msgs = subprocess_out.stderr.split('\n')
        for msg in msgs:
            if msg is None or msg == "":
                continue
            logger.warning(msg)
    if subprocess_out.returncode != 0:
        logger.error(f"Subprocess failed with return code {subprocess_out.returncode}")
        raise RuntimeError()

def log_git_clone_subprocess_ouput(subprocess_out: subprocess.CompletedProcess, logger: logging.Logger):
    if subprocess_out.stdout:
        logger.info(subprocess_out.stdout)
    if subprocess_out.stderr:
        msgs = subprocess_out.stderr.split('\n')
        for msg in msgs:
            if msg is None or msg == "":
                continue
            logger.info(msg)
    if subprocess_out.returncode != 0:
        logger.error(f"Subprocess failed with return code {subprocess_out.returncode}")
        raise RuntimeError()

def counts_errors_warnings(log_file_path):
    error_count = 0
    warning_count = 0
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ERROR -"):
                error_count += 1
            elif line.startswith("WARNING -"):
                warning_count += 1
    return warning_count, error_count

def get_warning_error_count():
    main_log_file_path = os.path.join("logs", "log.txt")
    warning_count, error_count = counts_errors_warnings(main_log_file_path)
    
    log_folder_path = os.path.join("logs", "package_logs")
    for log_file in os.listdir(log_folder_path):
        log_file_path = os.path.join(log_folder_path, log_file)
        warnings, errors = counts_errors_warnings(log_file_path)
        warning_count += warnings
        error_count += errors
    
    return warning_count, error_count

def parse_log(log_file_path):
    # reads the log file and parse it into a list of dictionaries
    # the dictionary has the keys: 'name', 'level', 'message'
    log_list = []
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ERROR -"):
                level = logging.INFO
            elif line.startswith("WARNING -"):
                level = logging.WARNING
            elif line.startswith("INFO -"):
                level = logging.INFO
            else:
                # put everything to the previous message
                log_list[-1]['message'] += line
                continue
            temp_info = line.split(" - ")
            logger_name = temp_info[1]
            message = temp_info[2]
            log_list.append({'name': logger_name, 'level': level, 'message': message})
    return log_list

def print_out_log_by_log_level(log_list, log_level):
    for log in log_list:
        if log['level'] >= log_level and log['message'] not in ['', '\n', '\r\n']:
            print(log['message'])

def output_log_by_log_level():
    log_level = get_log_level()
    main_log_file_path = os.path.join("logs", "log.txt")
    print_out_log_by_log_level(parse_log(main_log_file_path), log_level)
    
    package_logs_folder = os.path.join("logs", "package_logs")
    for log_file in os.listdir(package_logs_folder):
        log_file_path = os.path.join(package_logs_folder, log_file)
        print_out_log_by_log_level(parse_log(log_file_path), log_level)

async def run_async_subprocess(exe_path, cmd):
    process = await asyncio.create_subprocess_exec(
        exe_path, *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    py2docfx_logger = get_logger(__name__)
    if process.returncode != 0:
        msg = stderr.decode('utf-8')
        if msg != None and msg != "":
            py2docfx_logger.error(msg)
        raise RuntimeError()
    else:
        msg = stdout.decode('utf-8')
        if msg != None and msg != "":
            py2docfx_logger.info(msg)