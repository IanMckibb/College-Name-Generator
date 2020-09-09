# Program to get college names from wikipedia page

input_file = open("raw_data.txt", 'r')
output_file = open("college_names.txt", 'w')

input_data = [c[:c.find('$')] for c in input_file.read().split('\n')]

for n in range(len(input_data)):
    name = input_data[n]
    if(name.replace('-', '').replace(' ', '').isalpha()):
        write_string = name
        if n != len(input_data) - 1:
            write_string = name + '.\n'
        output_file.write(write_string)

input_file.close()
output_file.close()
        