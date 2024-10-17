def main():
    input_file_path = 'test_inp.txt'
    #output_file_path = 'scanner_out.txt'

    for i in range(1,4):
        # Read the input file
        with open(input_file_path, 'r') as file:
            input_string = file.read().strip()

        for i in input_string:
            print(i)

if __name__ == '__main__':
    main()