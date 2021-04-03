import sys


def parse_server_status(input_file, output_file):
    with open(input_file, "r") as input:
        with open(output_file, "w") as output:
            for line in input:
                line = line.strip()
                seperation_index = -1
                while line[seperation_index] != "(":
                    seperation_index += -1
                output.write(
                    line[:seperation_index].strip()
                    + "$"
                    + line[seperation_index:][1:-1]
                    + "\n"
                )


def main(args):
    """main() will be run if you run this script directly"""
    parse_server_status(
        "protopy/vassal_engine/data/2021-03-vassal-players-month.txt",
        "server_status.csv",
    )


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
