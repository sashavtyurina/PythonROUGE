# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 10:31:58 2012

author: Miguel B. Almeida
mail: mba@priberam.pt
"""

import os
import re

# Wrapper function to use ROUGE from Python easily
# Inputs:
    # guess_summ_file, a string with the absolute path to the file with your guess summary
    # ref_summ_list, a list of paths to multiple reference summaries.
    # IMPORTANT: all the reference summaries must be in the same directory!
    # (optional) ngram_order, the order of the N-grams used to compute ROUGE
    # the default is 1 (unigrams)
# Output: a tuple of the form (recall,precision,F_measure)
#
# Example usage: PythonROUGE('/home/foo/my_guess_summary.txt',[/home/bar/my_ref_summary_1.txt,/home/bar/my_ref_summary_2.txt])
def PythonROUGE(guess_summ_file,ref_summ_list,ngram_order=1):
    """ Wrapper function to use ROUGE from Python easily. """
    
    # even though we ask that the second argument is a list,
    # if it is a single string we can handle it
    if type(ref_summ_list) == str:
        temp = list()
        temp.append(ref_summ_list)
        ref_summ_list = temp
        del temp
    
    # this is the path to your ROUGE distribution
    ROUGE_path = '/home/miguel/ROUGE/RELEASE-1.5.5/ROUGE-1.5.5.pl'
    data_path = '/home/miguel/ROUGE/RELEASE-1.5.5/data'
    
    # these are the options used to call ROUGE
    # feel free to edit this is you want to call ROUGE with different options
    options = '-a -m -n ' + ngram_order
    
    # this is a temporary XML file which will contain information
    # in the format ROUGE uses
    xml_path = 'temp.xml'
    create_xml(xml_path,guess_summ_file,ref_summ_list)
    
    # this is the file where the output of ROUGE will be stored
    ROUGE_output_path = 'ROUGE_result.txt'
    
    # this is where we run ROUGE itself
    exec_command = ROUGE_path + ' -e ' + data_path + ' ' + options + ' -x ' + xml_path + ' > ' + ROUGE_output_path
    os.system(exec_command)
    
    # here, we read the file with the ROUGE output and
    # look for the recall, precision, and F-measure scores
    ROUGE_output_file = open(ROUGE_output_path,'r')
    for line in ROUGE_output_file:
        match = re.findall('X ROUGE-1 Average_R: ([0-9.]+)',line)
        if match != []:
            recall = float(match[0])
        match = re.findall('X ROUGE-1 Average_P: ([0-9.]+)',line)
        if match != []:
            precision = float(match[0])
        match = re.findall('X ROUGE-1 Average_F: ([0-9.]+)',line)
        if match != []:
            F_measure = float(match[0])

    return (recall,precision,F_measure)
    
    
# This is an auxiliary function
# It creates an XML file which ROUGE can read
# Don't ask me how ROUGE works, because I don't know!
def create_xml(xml_path,guess_summ_file,ref_summ_list):
    xml_file = open(xml_path,'w')
    xml_file.write('<ROUGE-EVAL version="1.0">\n')
    xml_file.write('<EVAL ID="1">\n')
    xml_file.write('<PEER-ROOT>\n')
    guess_summ_dir = os.path.dirname(guess_summ_file)
    xml_file.write(guess_summ_dir + '\n')
    xml_file.write('</PEER-ROOT>\n')
    xml_file.write('<MODEL-ROOT>\n')
    ref_summ_dir = os.path.dirname(ref_summ_list[0] + '\n')
    xml_file.write(ref_summ_dir + '\n')
    xml_file.write('</MODEL-ROOT>\n')
    xml_file.write('<INPUT-FORMAT TYPE="SPL">\n')
    xml_file.write('</INPUT-FORMAT>\n')
    xml_file.write('<PEERS>\n')
    guess_summ_basename = os.path.basename(guess_summ_file)
    xml_file.write('<P ID="X">' + guess_summ_basename + '</P>\n')
    xml_file.write('</PEERS>\n')
    xml_file.write('<MODELS>')
    letter_list = ['A','B','C','D','E','F','G','H','I','J']
    for ref_summ_index,ref_summ_file in enumerate(ref_summ_list):
        ref_summ_basename = os.path.basename(ref_summ_file)
        xml_file.write('<M ID="' + letter_list[ref_summ_index] + '">' + ref_summ_basename + '</M>\n')
    
    xml_file.write('</MODELS>\n')
    xml_file.write('</EVAL>\n')
    xml_file.write('</ROUGE-EVAL>\n')
    xml_file.close()
    
# This is only called if this file is executed as a script.
# It shows an example of usage.
if __name__ == '__main__':
    guess_summ_file = 'Examples/Guess_Summ_1.txt'
    ref_summ_list = list()
    ref_summ_list.append('Examples/Ref_Summ_1.txt')
    ref_summ_list.append('Examples/Ref_Summ_2.txt')
    recall,precision,F_measure = pythonROUGE(guess_summ_file,ref_summ_list)
    print 'recall = ' + str(recall)
    print 'precision = ' + str(precision)
    print 'F = ' + str(F_measure)