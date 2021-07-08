if count <= (totalWords/4):
                dictionary1[word] += 1
                count += 1
            elif count <= ((totalWords)/2):
                dictionary2[word] += 1
                count += 1
            elif count <= ((3*totalWords)/4):
                dictionary3[word] += 1
                count += 1
            else:
                dictionary4[word] += 1
                count += 1