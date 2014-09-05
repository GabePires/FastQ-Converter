#!/usr/bin/env python3
# Name:Gabriel Pires(gapires)
# Group Members: Jeffrey Nguyen (jehunguy)

"""
OVERVIEW:
This is the main converter (custom module).
fastqread.py takes in the input file, parsing the file
and checks for proper formatting. If it's incorrect, go to
next set of FastQ lines starting at the header. This allows for parsing
correctly while not having to have to use the ASCII characters
'@' or '+' to check for headers.

This program also holds the required methods to convert from
one format to either Sanger(Phred+33) or Illumina1.3(Phred+64).

INPUT:
Takes in File name from the commandline file.

OUTPUT:
Each method that maybe called from the FastQCommand program
yields each line given by my fastqread parse method.
For quality score lines, it yields the converted desired output format.

ASSUMPTION:
If incorrect input, does not tell user where, it just ignores it.
"""

#PSEUDOCODE:
#Take in the fastqfile.
#   for line in fastqfile
#       check line 1 for @
#       check line 2
#       check line 3 for +
#       check len(line4)==len(line2)
#       if all checks out: yield this line.
#   for line given from file:
#       yield line if lines 1-3
#       convert quality score in line:
#       convert to quality value ord(char)-33 or -64 to offset ASCII table.
#       convert back to quality score of another format chr(ord(char)-33 or -64)+33 or +64)
#       yield this converted string.

class FastQreader :
    """
    Takes in file and parses it with readFastq.
    Each method aside converts from one format to another.
    This is converting to quality value with ord()
    and conveting back to quality score with chr().
    """

    def __init__ (self, fname):
        """
        initializes filename passed in and the
        output string and the empty store list
        Initializes dictionaries.
        """
        self.fname = fname
        self.QualityScoreOut = ''
        self.storeList=[[],[],[],[]]
        #stores each line in fastq file
        
        self.solexaDict = {-1:3, -2:2, -3:2, -4:1,-5:1,0:3, 1:4,2:4,3:5,4:5,
                          5:6,6:7,7:8,8:9,9:10,10:10,11:11,12:12,13:13,14:14,
                          15:15,16:16,17:17,18:18,19:19,20:20,21:21,22:22,23:23,24:24,
                          25:25,26:26,27:27,28:28,29:29,30:30,31:31,32:32,33:33,34:34,35:35,36:36,37:37,38:38,
                          39:39,40:40}
        #Q conversion for solexa Q values. It was more convenient to type out the dictionary than to do the conversion in code.

    
    def Illumina_Sanger(self):
        """
        Converts Illumina (Phred+64) to Sanger(Phred+33)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut=line
                i+=1
            else:
                for quality in line:
                    newQual = chr((ord(quality)-64)+33)
                    self.QualityScoreOut+=newQual
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''

            
    def Sanger_Illumina(self):
        """
        Converts Sanger (Phred+33) to Illumina(Phred+64)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut=line
                i+=1
            else:
                for quality in line:
                    newQual = chr((ord(quality)-33)+64)
                    self.QualityScoreOut+=newQual
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''


    def Solexa_Sanger(self):
        """
        Converts Solexa (PhredSOL+64) to Sanger(Phred+33)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut=line
                i+=1
            else:
                for quality in line:

                    newVal = (ord(quality)-64)
                    newVal2 = self.solexaDict[newVal]
                    quality = chr((newVal2)+33)
                    self.QualityScoreOut += quality
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''


    def Solexa_Illumina(self):
        """
        Converts Solexa (PhredSOL+64) to Illumina(Phred+64)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut=line
                i+=1
            else:
                for quality in line:
                    newVal = (ord(quality)-64)
                    newVal2 = self.solexaDict[newVal]
                    quality = chr((newVal2)+64)
                    self.QualityScoreOut += quality
            
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''


    def Illumina15_Sanger(self):
        """
        Converts Illumina1.5+ (PhredB+64) to Sanger(Phred+33)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut = line
                i+=1
            else:
                for quality in line:
                    if(quality == 'B'):
                        quality='!'
                        self.QualityScoreOut+=quality
                    else:
                        newVal = chr((ord(quality)-64)+33)
                        self.QualityScoreOut+=newVal
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''
            

    def Illumina15_Illumina(self):
        """
        Converts Illumina1.5+ (PhredB+64) to Illumina(Phred+64)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut = line
                i +=1
            else:
                for quality in line:
                    if(quality == 'B'):
                        quality='@' #quality value = 0 of illumina
                        self.QualityScoreOut+=quality
                    else:
                        newVal = chr((ord(quality)-64)+64)
                        self.QualityScoreOut+=newVal
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''


    def Illumina18_Sanger(self):
        """
        Converts Illumina1.8+ (PhredILL+33) to Sanger(Phred+33)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut = line
                i+=1
            else:
                for quality in line:
                    newVal = chr((ord(quality)-33)+33)
                    self.QualityScoreOut += newVal
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''

            
    def Illumina18_Illumina(self):
        """
        Converts Illumina1.8 (PhredILL+33) to Sanger(Phred+33)
        """
        i=0
        for line in self.readFastq():
            if(i==0 or i==1 or i==2):
                self.QualityScoreOut=line
                i+=1
            else:
                for quality in line:
                    newVal = chr((ord(quality)-33)+64)
                    self.QualityScoreOut += newVal
                i=0
            yield(self.QualityScoreOut)
            self.QualityScoreOut = ''


    def readFastq (self):
        """
        Iterates through lines of FastQ file and parses
        every four lines with a counter.
        It also compensates for incorrect formating and
        resyncs if incorrect. Ignores incorrectly formated
        lines.
        """
        
        i = 0
        for line in self.fname:
            i+=1
            #iterate through lines of FastQ file
            
            if(i==1 and line.startswith('@')):
                #Check condition of line 1 to start with @ then store it.
                lineHeader=line.upper().rstrip()
                self.storeList[0].append(lineHeader)

            elif(i==2):
                lineSeq = line.rstrip().replace('*','N').replace('.','N').replace('n','N')
                self.storeList[1].append(lineSeq)
                                 
            elif(i==3 and line.startswith('+')):
                #Check condition of line 3 to start with + then store it
                lineOption=line.rstrip()
                self.storeList[2].append(lineOption)
                                 
            elif(i==4 and self.storeList[0] and self.storeList[1] and self.storeList[2]):
                 #if conditions for line 1 and 3 are true, and then append line 4
                lineQuality=line.rstrip()
                self.storeList[3].append(lineQuality)
                
                if(len(lineQuality)==len(lineSeq)):
                    #this line 4 is same length as line2 then yield storeList
                    
                    for something in self.storeList:
                        yield(something[0])
                        
                    self.storeList=[[],[],[],[]]
                    lineHeader=''
                    lineSeq=''
                    lineOption=''
                    lineQuality=''
                    i=0
                    
                else:
                    #if line4 isn't same length, skip over to next fastq lines.
                    i=0
                    self.storeList=[[],[],[],[]]
                    lineHeader=''
                    lineSeq=''
                    lineOption=''
                    lineQuality=''

            else:
                 #if any one of these conditions is not correct, clean list and strings.
                i=0
                self.storeList=[[],[],[],[]]
                lineHeader=''
                lineSeq=''
                lineOption=''
                lineQuality=''
                


