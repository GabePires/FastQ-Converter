#!/usr/bin/env python3
#Name:Gabriel Pires(gapires)
#Group Members:Jeffrey Nguyen (jehunguy)


"""
OVERVIEW:
FastQCommand.py is the main program asking the user for input.
It checks what the user wants and calls the method
from the custom mosdule fastqread.py to do so.

INPUT:
commandline and sys. <input file, >output file, input format, output format.

OUTPUT:
Gives back a txt file of the converted fastq file.

ASSUMPTIONS:
User only want to be able to coonvert to Sanger and Illumina
and not to other formats, but it will still take in all formats
Sanger, Solexa, Illumina, Illumina 1.5, and Illumina1.8
input/formats is case sensitive.
"""

#PSEUDOCODE:
#Use commandline scaffold to determine options.
#Assign .args values to variables.
#Check what format input and output the user wanted.
#   if(variable/mycommandline.args.inType=='format' and variable/mycommandline.args.outtype='format'
#       call this method
#           output given lines to a file.


import FastQReader
import sys

class CommandLine() :
    '''
    Handle the command line, usage and help requests.

    CommandLine uses argparse, now standard in 2.7 and beyond. 
    it implements a standard command line argument parser with various argument options,
    a standard usage and help, and an error termination mechanism do-usage_and_die.

    attributes:
    all arguments received from the commandline using .add_argument will be
    avalable within the .args attribute of object instantiated from CommandLine.
    For example, if myCommandLine is an object of the class, and requiredbool was
    set as an option using add_argument, then myCommandLine.args.requiredbool will
    name that option.
    '''
    
    def __init__(self, inOpts=None) :
        '''
        CommandLine constructor.
        Implements a parser to interpret the command line argv string using argparse.
        '''
        import argparse
        self.parser = argparse.ArgumentParser(description = 'Program prolog - Specify the <input >output files and the input format and output format', 
                                             epilog = 'Program epilog - parameters of infile and outfile must be given.', 
                                             add_help = True, #default is True 
                                             prefix_chars = '-', 
                                             usage = '%(prog)s <input.txt >output.txt -inFormat = Sanger, Solexa, Illumina1.3, Illumina1.5 -outFormat = Sanger, Illumina1.3'
                                             )
        
        self.parser.add_argument('-i', '--inFormat', type=str, nargs='?', help='Fastq format of input') #allows multiple list options
        self.parser.add_argument('-o', '--outFormat', type=str, nargs='?', help='Fastq format of output') #allows multiple list options
       
        if inOpts is None :
            self.args = self.parser.parse_args()
        else :
            self.args = self.parser.parse_args(inOpts)  


def main(myCommandLine=None):
    """
    Calling .args and assigning them variables.
    example: ./fastqread <Solexa.txt >IlluminaOutput.txt -i=Solexa -o=Illumina1.3
    This is the output of the fastq via commandline. Checks what the input is
    and what the output  is. Converts from input specified to output specified.Also
    takes what the input file is and what the output file is.
    """

    
    myCommandLine = CommandLine(myCommandLine)
    #allows us to get the .args

    if not myCommandLine.args.outFormat:
        myCommandLine.args.outFormat = 'Sanger'
        #default output format if not specified is Sanger
        
    inputType = myCommandLine.args.inFormat
    outputType = myCommandLine.args.outFormat
    #assigns commandline arguments to variables for later use.

    
    myReader = FastQReader.FastQreader(sys.stdin)
    #allows use of FastQreader. Passes file from stdin to the reader file.


    
    if(inputType == 'Illumina1.3' and outputType == 'Sanger'):
        #Checks format the user inputs and calls corresponding method for output.
        #iterates through the lines given by that method.
        #same concept below.
        for fqLines in myReader.Illumina_Sanger():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Sanger' and outputType == 'Illumina1.3'):
        for fqLines in myReader.Sanger_Illumina():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Solexa' and outputType == 'Sanger'):
        for fqLines in myReader.Solexa_Sanger():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Solexa' and outputType == 'Illumina1.3'):
        for fqLines in myReader.Solexa_Illumina():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Illumina1.5' and outputType == 'Sanger'):
        for fqLines in myReader.Illumina15_Sanger():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Illumina1.5' and outputType == 'Illumina1.3'):
        for fqLines in myReader.Illumina15_Illumina():
            sys.stdout.write(fqLines + '\n')
        
    if(inputType == 'Illumina1.8' and outputType == 'Sanger'):
        for fqLines in myReader.Illumina18_Sanger():
            sys.stdout.write(fqLines + '\n')

    if(inputType == 'Illumina1.8' and outputType == 'Illumina1.3'):
        for fqLines in myReader.Illumina18_Illumina():
            sys.stdout.write(fqLines + '\n')

           

if __name__ == "__main__":
    main()

