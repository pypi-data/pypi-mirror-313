from argparse import ArgumentParser

IMPORTS_BLOCK

COLUMNS_BLOCK


def get_context(csv_path):
    CONTEXT_BLOCK
    return context


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Creates a differentially private release from a csv"
    )
    parser.add_argument(
        "--csv", required=True, help="Path to csv containing private data"
    )
    args = parser.parse_args()
    context = get_context(csv_path=args.csv)

    QUERIES_BLOCK
