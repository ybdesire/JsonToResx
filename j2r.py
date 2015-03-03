import os
import json
import codecs
import collections
from xml.sax.saxutils import escape

repoDir = 'E:\prog\JsonToResx'  #repository path of EN resouce files 

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

# go through directory(repoDir), detect *.json file, get resources from *.json file and insert into resx file
def getJsonPathAndCopyResxTmp():
    for root,dirs,files in os.walk(repoDir):
        for filesPath in files:
            if os.path.splitext(filesPath)[1] == '.json':
                jsonFilePath = root+'\\'+filesPath
                createBlankResxForJson(os.path.dirname(jsonFilePath), os.path.basename(jsonFilePath)+'.resx')
                dataOrderDict = getKeyValueFromJson(jsonFilePath)
                insertJsonKeyValuesIntoResx(dataOrderDict, os.path.dirname(jsonFilePath) + '\\' + os.path.basename(jsonFilePath)+'.resx')

# Create a blank resx file wth utf-8 encoding
def createBlankResxForJson(jsonFileDir, resxFileName):
    codecs.open(jsonFileDir + '\\' + resxFileName, 'w+', 'utf-8-sig')

# Get key value pairs from json file in ordered dictionary
def getKeyValueFromJson(jsonFilePath):
    jsonFileData = codecs.open(jsonFilePath, 'r', 'utf-8-sig').read()
    jsonDictData = json.loads(jsonFileData)
    jsonKeyValueDictData = getKeyValueOfJson(jsonDictData)
    jsonDataOrderDict = collections.OrderedDict(sorted(jsonKeyValueDictData.items(), key=lambda t: t[0]))#sort by key
    return jsonDataOrderDict

def insertJsonKeyValuesIntoResx(dataOrderDict, resxFilePath):
    with codecs.open(resxFilePath, 'a', 'utf-8-sig') as resxFile:
        #wirte resx file header
        resxFile.write('<?xml version="1.0" encoding="utf-8"?>\n')
        resxFile.write('<root>\n')
        resxFile.write('  <resheader name="resmimetype">\n')
        resxFile.write('    <value>text/microsoft-resx</value>\n')
        resxFile.write('  </resheader>\n')
        resxFile.write('  <resheader name="version">\n')
        resxFile.write('    <value>2.0</value>\n')
        resxFile.write('  </resheader>\n')
        resxFile.write('  <resheader name="reader">\n')
        resxFile.write('    <value>System.Resources.ResXResourceReader, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>\n')
        resxFile.write('  </resheader>\n')
        resxFile.write('  <resheader name="writer">\n')
        resxFile.write('    <value>System.Resources.ResXResourceWriter, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>\n')
        resxFile.write('  </resheader>\n')
  
        #write key & value
        for key, value in dataOrderDict.items():
            resxFile.write('  <data name="'+escape(key))
            resxFile.write('" xml:space="preserve">\n')
            resxFile.write('    <value>')
            resxFile.write(escape(value))
            resxFile.write('</value>\n')
            resxFile.write('  </data>\n')

        #write resx file end
        resxFile.write("\n</root>")

     
if __name__ == "__main__":
    getJsonPathAndCopyResxTmp()

