# Capsid_IDP_Classifier
Machine Learning Classifier for CRESS-DNA viral capsids

Built by Ryan O. Schenck
Contact: ryanschenck at mail dot usf dot edu

Note: This is not a peer-reviewed published tool. Use at your own risk.

###################
Summary:

This script is designed for high throughput classification of circular rep-encoding 
eukaryotic single-stranded DNA (CRESS) viruses.

The dataset was built from this publication: DOI 10.3389/fmicb.2015.00696

This package utilizes an ensemble (1000) of Decision Trees (non-parametric 
supervised machine learning) for classification of capsid types of CRESS viruses. 
This learning method will provide a user with a file that provides ‘Sequence Name, 
Type Predicted, an array showing the probabilities for that type classification.’

Based on the training and testing sets (80/20 split) taken from Rosario et. al. 2015 
the accuracy of this machine learning method is between 94.23% and 96.15%. 

####################
Input:

VL3 raw scores for  the first 125 amino acids for each sequence (sequences <125 
amino acids will not be possible) in a comma-separated spreadsheet (*.csv or *.txt):

Sequence_Name1, Score_1, Score_2, Score_3, Score_4…
Sequence_Name2, Score_1, Score_2, Score_3, Score_4…

####################
Excecuting:

$python CapClassifier.py input_file.csv


####################
Notes:

In the extra folder is a webdriver for obtaining VL3 scores when given a fasta file of 
multiple sequences. There are several dependencies for this script and thus will not be 
covered in this READ_ME file, but the script is there for those who need it. The Disprot 
website has strict Rate Limits when using this script and thus only a number of samples 
can be ran at one time. Paths will need to be changed in this script to suite your
environment.
