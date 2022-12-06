# Python code to
# demonstrate readlines()
  
result = []
  

  
# Using readlines()
file1 = open('result_subfinder_2.txt', 'r')
Lines = file1.readlines()
  
count = 0
# Strips the newline character
for line in Lines:
    result.append("https://" + line)

file1.close()



# writing to file
file1 = open('myfile.txt', 'w')

for line in result:
    file1.writelines(line)

file1.close()