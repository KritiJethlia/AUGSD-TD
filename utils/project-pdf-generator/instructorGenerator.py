# This generates pdf for projects under each Instructor.
# Place the csv file in the same directory with the name `allotment_list.csv` and later run the script.
# Format of ic_list.csv Course Code,Course Name,IC Name,Email ID
# Format of allotement_list.csv ID NO , STUDENT NAME, FACULTY NAME, PROJECT CODE,EMAIL, ELE TYPE, PROJECT TITLE 

# importing csv module
import csv
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
#from WebKit.Page import Page
from time import strftime
from cStringIO import StringIO
import datetime
styles = getSampleStyleSheet()
 
# csv file name

filename = "instructor_new.csv"
print filename 
# initializing the titles and rows list
fields = []
rows = []
 
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
     
    # extracting field names through first row
    fields = csvreader.next()
 
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
 
    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))
 
# printing the field names
print('Field names are:' + ', '.join(field for field in fields))
 
#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rows[:5]:
    # parsing each column of a row
    for col in row:
        print("%10s , "%col),
    print('\n')

instructors = []
data = []
instructoremails = []


for row in rows :
    if row[2] in instructors:
        data[instructors.index(row[2])].append(row)
    else :
        data.append([row])
        instructors.append(row[2])
        instructoremails.append(row[4])
#making table
for row in data : 
    for col in row :
        if len(col) == 7 :
            del col[6]
        del col[5]
        del col[4]
        del col[2]

for row in data [:6]:
    print row
# print(data[0])

i = 0

for instructor in instructors :
    instructoremail = instructoremails[instructors.index(instructor)]
    print 'instructor: '+instructor +' , email: '+instructoremail
    name = "Dear "+ instructor.title()+ ","
    heading1 = "SECOND SEMESTER 2018-2019"
    heading2 = "LIST OF ALLOTED PROJECT STUDENTS"
    para = "The following is the allotted list of project students under your guidance during Second Semester 2018-19. There is a possibility that some of the allotted project students may not register for the same.The final list of registered students will be available with the IC of the respective project type course. Incase of any discrepancy, please contact the office of AUGSD (Extn: 822) or email at augsd@hyderabad.bits-pilani.ac.in."
    datetoday = datetime.datetime.today().strftime('%d-%m-%Y')
    elements = []
    footer1 = "(Prof. A. Vasan)<br/> Associate Dean <br/>"

    # title = '<para align = "centre"><font size = 18><strong>%s</strong></font></para>' % title
    ptext = '<font size=12>%s</font>' % name
    head1text = '<para align = "centre">"<font size = 18><strong>%s</strong></font></para>' % heading1
    head2text = '<para align = "centre"><font size = 18><strong>%s</strong></font></para>' % heading2
    paratext = '<para leading=22><font size=12>%s</font></para>' % para
    date = '<para align="right"><font>%s</font></para>' % datetoday
    footer = '<para align = "left"><font size = "12">%s</font></para>' % footer1

    j = 0
    im = Image("head.png", width=4*inch, height=0.75*inch)
    im.hAlign = "LEFT"

    elements.append(im)

    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    while j < 5 :
        elements.append(Spacer(1, 12))
        j = j+1

    elements.append(Paragraph(head1text, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12)) 

    elements.append(Paragraph(head2text, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12)) 

    elements.append(Paragraph(date, styles["Normal"])) 
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(ptext, styles["Normal"])) 
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(paratext, styles["Normal"])) 

    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12)) 



    doc = SimpleDocTemplate(("./Instructor-PDF/"+ instructoremail+ ".pdf"), pagesize=letter)
    
    GRID_STYLE = TableStyle(
              [('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('ALIGN', (1,1), (-1,-1), 'LEFT')]
              )
                  
    # container for the 'Flowable' objects
    data[i].insert(0,['S. No','ID No.','Student Name','Course Code'])
    for j in range(1,len(data[i])):
            data[i][j].insert(0,str(j))
    number_of_students = len(data[i])-1
   
    t=Table(data[i])
    t.setStyle(GRID_STYLE)
    i = i+1
    elements.append(t)

    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Number of students alloted to your course: "+str(number_of_students), styles["Normal"]))
    elements.append(Spacer(1, 12)) 
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(footer, styles["Normal"])) 
    doc.build(elements)
