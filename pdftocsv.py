import csv
import re


def convert_to_text(pdf_content_text):
    print(pdf_content_text)
    pdf_content = pdf_content_text
    extracted_data = []
    stringa = ""
    ja = False
    start_extracting = False
        # Iterate through the pages of the PDF
    lines = pdf_content.split('\n')

        # Use a flag to indicate when to start extracting

        # Iterate through the lines
    for line in lines:
        if start_extracting:
             extracted_data.append(line.strip())
             stringa = stringa + line.strip() + "\n"

            # Check for the starting point, in this case, the section you specified
        if "NO     LIBERAL ARTS & SCIENCES (LAS) credits in the DEGREE" in line:
                print("hi1")
        
                start_extracting = True
        elif "SELECT FROM: COURSES  with LAS credit"  in line:
                print("hi2")
                start_extracting = False

    
  



    def is_float_string(s):
        # Regular expression to match valid floating-point number strings
        float_pattern = r'^[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?$'



        if re.match(float_pattern, s):
            return True
        else:
            return False

    # Split the input text into lines
    lines = stringa.strip().split('\n')
    print(lines)

    # Define a regular expression pattern to extract the required information
    pattern = re.compile(r'(SP|FA|SU)(\d+ [A-Z]+\s\d+\.\d+\s[A-Z]+\s.*)')

    # Create a CSV output file
    # Create a CSV output file
    count = 0
    course = ""
    with open('data/output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(['Term', 'Course', 'Credits', 'Grade', 'Name'])
        # Extract and write the information for each line
        for line in lines:

            # Check if the line starts with 'SP,' 'FA,' or 'SU'
            if line.startswith(('SP', 'FA', 'SU')):
                parts = line.split()
                term = parts[0]
                count =1
                while True:
                    if(is_float_string(parts[count])):
                        break
                    else:
                        course = course + " " + parts[count]
                        count = count + 1

                credits = parts[count]
                grade = parts[count+1]
                description = ' '.join(parts[count+2:])
                csv_writer.writerow([term, course, credits, grade, description])
                course =""

