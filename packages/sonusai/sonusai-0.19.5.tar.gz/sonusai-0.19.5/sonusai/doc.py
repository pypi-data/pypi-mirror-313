"""sonusai doc

usage: doc [-h] [TOPIC]

options:
   -h, --help   Display this help.

Show SonusAI documentation.

"""


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    from sonusai import doc

    topic = args["TOPIC"]

    print(f"SonusAI {sonusai.__version__} Documentation")
    print("")

    topics = sorted([item[4:] for item in dir(doc) if item.startswith("doc_")])

    if topic not in topics:
        if topic is not None:
            print(f"Unknown topic: {topic}")
            print("")

        print("Available topics:")
        for item in topics:
            print(f"  {item}")
        return

    text = getattr(doc, "doc_" + topic)()
    print(text[1:])


if __name__ == "__main__":
    main()
