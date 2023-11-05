import pandas as pd
import re

# Read the CSV file into a DataFrame
df = pd.read_csv('../data/comp_sci_with_avg_gpa.csv')

# Define a function to extract the course number
def extract_course_number(course_code):
    match = re.search(r'\d+', course_code)
    if match:
        return "COMP SCI " + match.group()
    return course_code

# Apply the extraction to the 'Course Code' column
df['Course Code'] = df['Course Code'].apply(extract_course_number)

# Save the modified DataFrame back to a CSV file
df.to_csv('../data/comp_sci_filtered_avg.csv', index=False)

# import requests
# from bs4 import BeautifulSoup
# import csv
#
# # Send a GET request to the webpage
# url = "https://guide.wisc.edu/courses/comp_sci/"
# response = requests.get(url)
#
# # Parse the HTML content of the webpage
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # Find all course blocks
# course_blocks = soup.find_all('div', class_='courseblock')
#
# # Create and open a CSV file for writing
# with open('courses.csv', 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     # Write the CSV header
#     csv_writer.writerow(['Course Code', 'Course Title', 'Description', 'Requisites', 'Requirements Fulfilled', 'Credits'])
#
#     for block in course_blocks:
#         # Extract course code and title
#         title = block.find('p', class_='courseblocktitle').text.strip()
#         code, course_title = title.split(' — ', 1)
#
#         # Extract course description
#         description = block.find('p', class_='courseblockdesc').text.strip()
#
#         # Extract requisites
#         requisites = ""
#         requisites_tag = block.find('span', class_='cbextra-label', text='Requisites: ')
#         if requisites_tag:
#             requisites = requisites_tag.find_next('span', class_='cbextra-data').text.strip()
#
#         # Extract requirements fulfilled
#         requirements_fulfilled = ""
#         requirements_fulfilled_tag = block.find('span', class_='cbextra-label', text='Course Designation: ')
#         if requirements_fulfilled_tag:
#             requirements_fulfilled = requirements_fulfilled_tag.find_next('span', class_='cbextra-data').text.strip()
#
#         # Extract credits
#         credits_tag = block.find('p', class_='courseblockcredits')
#         if credits_tag:
#             credits = credits_tag.text.strip().split()[0]
#         else:
#             credits = ''
#
#         # Write the data to the CSV file
#         csv_writer.writerow([code, course_title, description, requisites, requirements_fulfilled, credits])
#
# print("CSV file 'courses.csv' has been created.")
#
