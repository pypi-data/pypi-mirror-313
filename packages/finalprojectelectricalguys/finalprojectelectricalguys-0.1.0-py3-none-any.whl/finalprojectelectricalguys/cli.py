import sys

def copy_file(input, output):           # Function to copy content of one file to another
    with open(input, 'r') as src:   
        with open(output, 'w') as dest: # Open the source file in read mode and destination file in write mode
            dest.write(src.read())      # Write the content of source file to destination file

def main():                             # Main function to take input and output file names from command line and print a success message or an error message
    try:
        input_file = sys.argv[1]        # Take input file name from command line
        output_file = sys.argv[2]       # Take output file name from command line
        copy_file(input_file, output_file)      # Call the copy_file function
        print(f"Content copied to {output_file}") # Print success message
    except IndexError:                  # Handle error if no input and output file names are provided    
        print("Error: Enter source and destination file names") # Print error message

if __name__ == "__main__":              # Call the main function if the script is run directly and not as a module.
    main()


    """
    TO RUN THIS FUNCTION USE THE FOLLOWING COMMAND IN THE TERMINAL: POETRY RUN RUNPROJECT <INPUT FILE PATH> <OUTPUT FILE PATH>
    """