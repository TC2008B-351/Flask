from os import makedirs, path
from logging import basicConfig, INFO, getLogger
from datetime import datetime

def setup_logging():
    log_directory = 'trafficSystem/logging/logs/'
    makedirs(log_directory, exist_ok=True)
    log_filename = path.join(log_directory, f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

    basicConfig(
        filename=log_filename,
        level=INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

    logger = getLogger(__name__)

    print(f'Logging to {log_filename}')

    return logger