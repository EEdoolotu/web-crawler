import sys

print("Script name:", sys.argv[0]) # example.py


def main():
    print("Hello from web-crawler!")
    

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 2:
        BASE_URL = sys.argv[1]
        print(f"starting crawl of {BASE_URL}")


if __name__ == "__main__":
    main()
