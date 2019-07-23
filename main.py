import argparse
import logging
from sender import Sender
from receiver import Receiver


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-send', '--send', action='store_true')
    parser.add_argument('-receive', '--receive', action='store_true')
    parser.add_argument('-ip', '--ip', type=str)
    parser.add_argument('-file', '--file', type=str)
    parser.add_argument('-threads', '--threads', type=int)
    return parser


def build_logger():
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logs.log")

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logging


if __name__ == '__main__':
    logger = build_logger()
    parser = build_parser()
    logger.info('Parsing arguments...')
    args = parser.parse_args()

    if args.receive:
        receiver = Receiver()
        receiver.receive_info()
        receiver.receive_data()
        receiver.save_data()
    elif args.send:
        sender = Sender(
            ip=args.ip, file=args.file, threads=args.threads
        )

        sender.send_info()
        sender.send_data()
    else:
        raise KeyError('Unknown command')
