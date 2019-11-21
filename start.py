import sys
from time import process_time

from creditCardSystem.core import Processor
from creditCardSystem.logsModule import set_logger

log = set_logger('logger')

def main():
    log.info('프로세스 시작')
    t = process_time()
    processor = Processor()

    with open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin as f:
        for line in f:
            processor.parse_event(line)

    log.info('전체 프로세스 동작 시간: {0:.3f} 초'.format(process_time() - t))
    summary = processor.gen_totalinfo()
    processor.write_output(summary)

if __name__ == "__main__":
    main()
