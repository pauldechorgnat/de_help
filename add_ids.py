import re

with open('temp_auto.html', 'r') as file:
    text = file.read()

counter = 0
for language in ['python', 'sh', 'yml', 'xml', 'pig', 'sql', 'hbase', 'json', 'dockerfile']:
    regular_expression = re.compile('<div class="' + language + ' code">')
    connectors = re.findall(regular_expression, string=text)
    split_text = re.split(regular_expression, string=text)
    text_ = split_text[0]
    for i in range(len(connectors)):
        counter += 1
        new_connector = connectors[i][:-1] + ' id="code-' + str(counter) + '">'
        text_ += new_connector + split_text[i+1]
    text = text_

with open('temp2.txt', 'w') as file:
    file.write(text)