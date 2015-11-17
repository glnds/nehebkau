
source='a simple text'
output=''

for i in range (1, len(source)+1):
    output = output + source[-1*i]

print(output)
