import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Search and replace text in files')
    parser.add_argument('file', help='File to perform search and replace on')
    parser.add_argument('old_string', help='String to search for')
    parser.add_argument('new_string', help='String to replace with')
    parser.add_argument('--inplace', '-i', action='store_true', 
                       help='Modify file in-place instead of printing to stdout')
    
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        content = f.read()

    number_of_replacements = content.count(args.old_string)
    content = content.replace(args.old_string, args.new_string)

    if args.inplace:
        with open(args.file, 'w') as f:
            f.write(content)
    else:
        print(content)

    print(f"Found and replaced {number_of_replacements} occurrences.", file=sys.stderr)


if __name__ == '__main__':
    main()
