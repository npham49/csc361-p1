import sys

def main():
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        print(f"First argument: {first_arg}")
    else:
        print("No arguments provided")

if __name__ == "__main__":
    main()
