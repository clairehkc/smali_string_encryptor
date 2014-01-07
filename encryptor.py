import os

def encrypt(s):
    encrypted = ""
    skip = -1
    
    for i in xrange(1, len(s)-1):
        if skip != -1:
                skip += 1
                if skip == 4:
                    skip = -1
        elif s[i].isalpha():
            if s[i-1] == '\\' and s[i] == 'u':
                 encrypted += s[i]
                 if len(s) <= 6:
                     return '"' + encrypted + '"'
                    
                 for j in xrange(i+1,i+5):
                     if s[j] == 'f':
                         encrypted += 'a'
                     elif s[j] == 'F':
                         encrypted += 'A'
                     elif s[j].isalpha():
                         encrypted += chr(ord(s[j]) + 1)
                     else:
                         encrypted += s[j]
                 skip += 1
            elif s[i-1] == '\\':
                encrypted += s[i]
            elif s[i] == 'z':
                encrypted += 'a'
            elif s[i] == 'Z':
                encrypted += 'A'
            else:
                encrypted += chr(ord(s[i]) + 1)
        else:
            encrypted += s[i]
    
    return '"' + encrypted 
        
def parse(f):
    inFile = open(f, 'r+') 
    out = ""

    for line in inFile:
        if "const-string" in line:
            qIndex = line.find('"')
            part1 = line[:qIndex]
            part2 = line[qIndex:]
            split = part1.strip().split(' ')
            version = split[1][:-1]
            vNum = int(version[1:])
            encrypted = part1 + encrypt(part2) + "\n"
            if vNum >= 15:
                call = "invoke-static/range {" + version + " .. " + version + "}, Lcom/EncryptString;->applyCaesar(" + \
                       "Ljava/lang/String;)Ljava/lang/String;" + "\n"
            else:
                call = "invoke-static {" + version + "}, Lcom/EncryptString;->applyCaesar(" + \
                       "Ljava/lang/String;)Ljava/lang/String;" + "\n" 
            out += encrypted + call
        else:
            out += line

    inFile.seek(0)
    inFile.write(out)
    inFile.close()

def run(path):
    directory = os.listdir(path)

    if (path == "."):
        path = ""
   
    for item in directory:
        if item.lower().endswith('.smali'):
            parse(path + item)
    
        elif (not item.lower().endswith('.py')):
            run(path + item + "/")   

