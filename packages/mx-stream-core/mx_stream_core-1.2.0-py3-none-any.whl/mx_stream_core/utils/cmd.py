import argparse


def extract_args():
    parser = argparse.ArgumentParser(description="Process some named parameters.")
    parser.add_argument('--worker', type=str, required=False, help='Worker to run')
    parser.add_argument('--layer', type=str, required=False, help='Layer to run')
    args = parser.parse_args()
    return args
