import os
import json
import codecs
import collections

def getKeyValueOfJson(data):
    key=""
    value=""
    diData=collections.OrderedDict()
    for key1, value1 in data.items():
        key = key1
        value = value1
        if(isinstance(data[key1], dict)):
            for key2, value2 in data[key].items():
                key = key1 + '%' + key2
                value = value2
                if(isinstance(data[key1][key2], dict)):
                    for key3, value3 in data[key1][key2].items():
                        key = key1 + '%' + key2 + '%' + key3
                        value = value3
                        if(isinstance(data[key1][key2][key3], dict)):
                            print("unsupport")
                        else:
                            diData[key]=value
                else:
                    diData[key]=value
        else:
            diData[key]=value
    return diData

def main():
    fileData = codecs.open('en.json', 'r', 'utf-8-sig').read()
    data = json.loads(fileData)
    data_dict = getKeyValueOfJson(data)
    dataOrderDict = collections.OrderedDict(sorted(data_dict.items(), key=lambda t: t[0]))

    #for key, value in dataOrderDict.items():
    #    print(key + ", " + value)

    with codecs.open('template.resx', 'a', 'utf-8-sig') as resxFile:
        for key, value in dataOrderDict.items():
            resxFile.write('\r  <data name="'+key)
            resxFile.write('" xml:space="preserve">\r')
            resxFile.write('    <value>')
            resxFile.write(value)
            resxFile.write('</value>')
            resxFile.write('\r  </data>')
        
        resxFile.write("\r</root>")


if __name__ == "__main__":
    main()

