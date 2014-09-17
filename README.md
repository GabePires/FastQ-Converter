FastQ-Converter---Python
========================

Convert between different FastQ formats

FASTQ

By: Gabriel Pires (gapires)
Jeffrey Nguyen (Jehunguy)


Abstract

Within the FASTQ file, there are five different formats for quantifying quality scores. These formats are Sanger, Solexa, Illumina 1.3+, Illumina 1.5+, and Ilummina 1.8+. Each uses its own character mapping to represent quality scores. FASTQ allows one to see the quality and accuracy of a sequence with ASCII characters in a range of quality scores. They each have their own ranges. For example, Sanger ranges from 0:40 and Solexa ranges from -5:40. The ability to quantify and record the quality of each nucleotide of a sequence is both valuable and significant. Because not only one method is used universally and formats change over time, it is valuable to have programs to convert one quality score character format to another. With a program written in python, we can convert from one FASTQ format to another. 

Introduction

A FASTQ file is composed of four lines: the ID header, DNA sequence, optional header, and quality score can be identified. The ID header begins with a ‘@’ character followed by information about the sequence. The second line contains the DNA sequence, and the third line begins with a ‘+’ character and can optionally be followed by another header. The fourth line contains the quality scores of the sequence, and each quality score character corresponds directly to the nucleotides of the DNA sequence given above it. (2) The character ‘!’ represents the lowest quality score, and the character ‘~’ represents the highest quality score. Having a low quality score means the corresponding nucleotide has a high probability of error. Having a high quality score means the corresponding nucleotide has a low probability of error, which is what one wants. The following list represents the quality characters from lowest to highest: ‘‘!”#$%&’( )*+,./0123456789:;⇔?@ABCDEFGHIJ KLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~’. (3)
The Phred quality score was invented by Churchchill and Waterman and the process that they used was chromatogram. The chromatogram would provide 4 fluorescence intensities. The 4 intensities correspond to the nucleotides (A, G, T, C).  The one that has a distinct intensity shows a lower probability of error, but if there are two intensities that overlap near each other, the quality score would drop because it produce a higher change of error.  Each nucleotide was assigned a quality score, which allowed us to figure out the probability of error. (4) The purposes of quality score are for assessment of sequence quality, recognition and removal of low quality nucleotides. (1)
The quality score is mapped to the ASCII table in a way that each character of the quality score value is equivalent to the ASCII character value with an offset of 33 or 64. For example, the Sanger (Phred+33) format uses characters ranging 33:73 in the ASCII table to designate quality scores ranging 0:40. Illumina1.3+(Phred+64), which used to be Solexa, decided to use an offset of 64 instead of 33. This was the creation of PHRED+64, which has a range of ASCII characters 64:104. The quality scores remain consistent with a range of 0:40. The character number 33 is matched with the ASCII symbol ‘!’, whereas the character number 64 is matched with the ASCII symbol ‘@’ and these corresponds to the quality score of 0, which is the lowest quality score possible. 

Materials and Methods

With any given FASTQ file, there are four given lines. Lines one and three were the sequence identifiers, line two was the DNA sequence, and line four was the quality scores. The python 3 programming language was used to convert these quality scores from one fast format to another. Python 3 was used as one of the most recently updated versions. Modules used for this project were sys and argparse. The sys module was used for stdin(input file) and stdout(output file). We also decided to make one file for parsing and reading the FASTQ file as our custom module and the other file as the command line for manipulation of that module.
The first thing done was to clean the sequence, make it upper case and simplify the unknown bases to the letter N for possible future use. 
The next step was to parse the FastQ file. A for loop was used to iterate through every line. At every line, a counter was used to see what line the program was currently iterating. This means at line four, the counter would be at four. After line four, the counter would reset to zero. The original concept was to look for the character “@“ and “+” to signify the header and optional headers, but because quality scores can also be given as “@“ or “+” there are possible errors when iterating fast files. These errors could lead to reading the quality score sequence as a header or counting the lines would be out of sync.
Each conversion takes place within its own method. If the user wanted to convert from Illumina to Sanger, the method used would be Illumina_Sanger(). If the user wanted Sanger to Illumina, the method used would be Sanger_Illumina(). The original idea was to set up two dictionaries to store the ASCII character and value. However, we decided to simply use the chr() and ord() function. Essentially, the dictionary is the ASCII table, and we called the character and its value with chr() ad ord(). Depending on the input format and output format, we would incorporate the offset of -33 or -64 for the quality score, and +33 or +64 for the ASCII value. For example, if the input format was Sanger, we would use ord(quality)-33 to give the quality value of the quality score. Using chr() of that value plus 64 would give the converted output quality score of Illumina.
     There were several assumptions made when converting from Solexa or Illumina 1.5+ to Sanger or Illumina 1.3+. The Solexa FASTQ quality scores range from -5 to 40, but Sanger and Illumina 1.3+ do not have corresponding negative quality score values. These scores cannot simply be ignored. It was assumed that Solexa quality values corresponded to the Sanger equation Q=-10logP. In order to use this equation, P must be calculated from the Solexa equation Q = -10logP/1-P where Q equals the Solexa quality scores. Next, that value for P was used for the Sanger equation for a corresponding quality value for Sanger. 
When converting quality scores of -5:9 from Solexa to Sanger using the equations provided, there were rounding errors. For example, when we converted the Solexa quality score -5 to the Sanger, it gave a quality value of 1.19. There are no ASCII characters that correspond to decimals, so 1.19 was rounded to 1. When a Solexa quality score of -4 converted to Sanger, a quality value of 1.456 was given, but again, this number was rounded to 1. Converting between these formats using their equations may lead to inaccurate quality scores due to rounding these estimations.
Another assumption was made for Illumina 1.5+(B-offset). The Illumina 1.5+ ranges from 3:40 but includes the quality score “B” which corresponds to the quality number 2. “B” stands for an unknown quality score. In this program, we assumed that P(error) = 1, meaning it’s converted quality score will be assumed to be 0 for Sanger or Illumina 1.3+.


Results

Sanger        Phred+33,  raw reads typically (0, 40)  
Solexa        Solexa+64, raw reads typically (-5, 40)  
Illumina 1.3+ Phred+64,  raw reads typically (0, 40)  
Illumina 1.5+ Phred+64,  raw reads typically (3, 40)      
	with 0=unused, 1=unused, 2=assume P(error)=1 (bold).
Illumina 1.8+ Phred+33,  raw reads typically (0, 41)

Figure 1. Sanger and Illumina 1.3+ has the same quality score of (0:40), while Solexa has a quality score ranges from (-5:40) and Illumina 1.5+ ranges from (3:40). Illumina 1.8+ ranges from (0:41)
 
Figure 2. The relationship between the probability and quality scores of Solexa and Sanger. This graph tells us that there is a disparity between the quality score of -5 and 0. 

Illumina 1.3+ and Sanger conversion:
Illumina 1.3+:
@IRIS:7:1:17:394#0/1
GTCAGGACAAGAAAGACAANTCCAATTNACATTATG
+IRIS:7:1:17:394#0/1
aaabaa`]baaaaa_aab]D^^`b`aYDW]abaa`^

Sanger:
@IRIS:7:1:17:394#0/1
GTCAGGACAAGAAAGACAANTCCAATTNACATTATG
+IRIS:7:1:17:394#0/1
BBBCBBA>CBBBBB@BBC>%??ACAB:%8>BCBBA?

Solexa conversion:
Solexa:
@HWI-EAS91_1_30788AAXX:1:1:1761:343
AAAAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAACNNANNGAGTNGNNNNNNNGCTTCCCACAGNNCTGG
+HWI-EAS91_1_30788AAXX:1:1:1761:343
hhhhhhh;;hhhhhhhhhhh^hOhhhhghhhfhhhgh;;h;;hhhh;h;;;;;;;hhhhhhghhhh;;Phhh

Sanger:
@HWI-EAS91_1_30788AAXX:1:1:1761:343
AAAAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAACNNANNGAGTNGNNNNNNNGCTTCCCACAGNNCTGG
+HWI-EAS91_1_30788AAXX:1:1:1761:343
IIIIIII""IIIIIIIIIII?I0IIIIHIIIGIIIHI""I""IIII"I"""""""IIIIIIHIIII""1III

Illumina 1.3+:
@HWI-EAS91_1_30788AAXX:1:1:1761:343
AAAAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAACNNANNGAGTNGNNNNNNNGCTTCCCACAGNNCTGG
+HWI-EAS91_1_30788AAXX:1:1:1761:343
hhhhhhhAAhhhhhhhhhhh^hOhhhhghhhfhhhghAAhAAhhhhAhAAAAAAAhhhhhhghhhhAAPhhh

Illumina 1.5+ conversion:
Illumina 1.5+:
@HWI-ST611_0189:1:1101:1237:2140#0/1
ACTAGCTGTCCTTGGTGCCCGAGTGTATTGAAAGTTGATTCCCTTATAGATGTTCGTTTTCCACACAACTCTGTAGGCACCANCAATNACTAGTAGATCG
+HWI-ST611_0189:1:1101:1237:2140#0/1
___`cccceeeeehh`dcfhe`dQb`deehehebY^aedfdhhhhe_ebaa]cebe_eehfhS__ede_V\HHV^^^acccBBBBBBBBBBBBBBBBBBB

Illumina 1.3+:
@HWI-ST611_0189:1:1101:1237:2140#0/1
ACTAGCTGTCCTTGGTGCCCGAGTGTATTGAAAGTTGATTCCCTTATAGATGTTCGTTTTCCACACAACTCTGTAGGCACCANCAATNACTAGTAGATCG
+HWI-ST611_0189:1:1101:1237:2140#0/1
___`cccceeeeehh`dcfhe`dQb`deehehebY^aedfdhhhhe_ebaa]cebe_eehfhS__ede_V\HHV^^^accc@@@@@@@@@@@@@@@@@@@

Sanger:
@HWI-ST611_0189:1:1101:1237:2140#0/1
ACTAGCTGTCCTTGGTGCCCGAGTGTATTGAAAGTTGATTCCCTTATAGATGTTCGTTTTCCACACAACTCTGTAGGCACCANCAATNACTAGTAGATCG
+HWI-ST611_0189:1:1101:1237:2140#0/1
@@@ADDDDFFFFFIIAEDGIFAE2CAEFFIFIFC:?BFEGEIIIIF@FCBB>DFCF@FFIGI4@@FEF@7=))7???BDDD!!!!!!!!!!!!!!!!!!!

Illumina 1.8+ conversion:
Illumina 1.8+:
@QSEQ57.1 HWI-ST593:7:1101:1224:2156#0/1 PF=1 length=100
CGGTTAAACATCGTCTCGCCGGTCTTGCCGTACTTGTCGCGGATGAACGACGCGCCGCGCGCCTCGGGCCATAGCACGTCGACGTGCGGCGGGGCCGCGC
+
HHHHHHHHHHHHFHHGHFFHHFFHHFHHHHFCHHHHHHFHEFDCB>CCD=FDHFDE@C.@&.207+4=0>:,46:4>8>>>@A>89:;B!!!!!!!!!!!

Illumina 1.3+:
@QSEQ57.1 HWI-ST593:7:1101:1224:2156#0/1 PF=1 LENGTH=100
CGGTTAAACATCGTCTCGCCGGTCTTGCCGTACTTGTCGCGGATGAACGACGCGCCGCGCGCCTCGGGCCATAGCACGTCGACGTGCGGCGGGGCCGCGC
+
ggggggggggggeggfgeeggeeggeggggebggggggegdecba]bbc\ecgecd_bM_EMQOVJS\O]YKSUYS]W]]]_`]WXYZa@@@@@@@@@@@

Sanger:
@QSEQ57.1 HWI-ST593:7:1101:1224:2156#0/1 PF=1 LENGTH=100
CGGTTAAACATCGTCTCGCCGGTCTTGCCGTACTTGTCGCGGATGAACGACGCGCCGCGCGCCTCGGGCCATAGCACGTCGACGTGCGGCGGGGCCGCGC
+
HHHHHHHHHHHHFHHGHFFHHFFHHFHHHHFCHHHHHHFHEFDCB>CCD=FDHFDE@C.@&.207+4=0>:,46:4>8>>>@A>89:;B!!!!!!!!!!!


Discussion

Quality scores refer to probability of being an incorrectly sequenced nucleotide. In most methods except for Solexa, it is usually denoted as P(error) or P(e). To calculate the quality score, the equation that you need to use is -10×〖log〗_10 (p). If there is a ‘!’ character for PHRED+33 with the quality score 0, then it means there is a probability of 1 that the base an error. If there is a ‘@’ character for PHRED+64 with a quality score of 0, it is interpreted as P(error) = 1, which means that the base is 100% probability of error as well.
The quality value Q is an integer mapping of P, which is the probability that the corresponding base is incorrect. There are two different equations that were used. The first one is called the Phred quality score: Q_sanger= -10 〖log〗_10 p or p= 〖10〗^((-Q)/10). The second one is called the Solexa pipeline, which encodes the odds not the probability: Q_(solexa-prior to v.1.3)= -10 〖log〗_10  p/(1-p), which can be changed to  p=  〖10〗^(Q⁄(-10))/(1+〖10〗^(Q⁄(-10)) ). Both mappings are asymptotically identical at higher quality scores, but differ at the lower quality scores (Fig. 2). 
Aside from Sanger and Illumina 1.3+, there are three other unique formats: Solexa, Illumina 1.5+ and Illumina 1.8+. Similar to Illumina 1.3+ is Solexa (Solexa+64). Solexa is unique. Instead of using a quality score range of 0:40, it contains negative quality scores.  It carries a range of -5:40. This format also uses its own quality score formula. Rather than Q= -log⁡〖(p)〗, it uses Q=-10 log⁡〖P/(1-P)〗 . Using a different quality score formula causes a discrepancy between the quality score values when P is greater than 0.3 (Fig. 1). Another format that diverges from the 0:40 quality score range is Illumina 1.5+. Illumina 1.5+ ranges from 3:40. Quality scores 0 and 1 are ignored. However, the quality score 2, corresponding to B, still exists. The character B in this format is an unknown quality score and is assumed to have a quality score of zero. (1) The last format is Illumina 1.8+, which has the quality score range of 0:41. This format is very similar to Sanger, except that it has the extra quality score 41. 
The names ‘PHRED+33’ and ‘PHRED+64’ are used to represent quality scoring, but they can also be used to remind us how the mapping is computed. For example, if you want a quality score of 0 in PHRED+33, all you need to do is add 33 to the quality score 0 and then covert it back to the character according to the ASCII table. Python has some built in functions, such as chr( ) or ord( ) that can be manipulated to convert between different formats. 


Conclusion

We created a python program that would convert each method into another method.  This work implies that it is difficult to convert from one format of Solexa to another or vice versa.  We should introduce a universal agreement to convert between FASTQ formats. 
This program is only able to convert to Sanger (PHRED+33) and to Illumina 1.3+ (PHRED+64). In the future, we should program it to be able to convert to and from all other formats. This can be difficult because if we want to convert from Sanger to Solexa, there aren’t any values for Solexa’s negative quality scores. If we wanted to convert from Sanger to Illumina 1.5+, we would either ignore values 1 and 2 or assume it to be 0. The new hypothesis that was raised is that under our own assumption and understanding, we were able to convert from one format to PHRED+33 and to PHRED+64. In the same manner, we should also be able to convert to other formats under the same understanding. 


Resources

1. "FASTQ Format." Wikipedia. Wikimedia Foundation, 21 May 2014. Web. 03 June 2014.

2. Cock, Peter J. A., Christopher J. Fields, Naohisa Goto, Michael L. Heuer, and Peter M. Rice. "Abstract." National Center for Biotechnology Information. U.S. National Library of Medicine, 16 Dec. 2009. Web. 03 June 2014.

3. Bernick, David. “FASTQ Outline” Ecommons. 

4. Li, Ming, and Magnus Nordborg. "Nucleic Acids Research." Adjust Quality Scores from Alignment and Improve Sequencing Accuracy. Oxford University Press, n.d. Web. 09 June 2014.

