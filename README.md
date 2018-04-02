# Computational-Linguistics
Non-Machine Learning Computational Linguistic Projects

ArtDistance.py
This script records the position of heads relative to their articles.

Details: This script reads every Perseus or PROIEL treebank (in XML format) from an input directory (in my case '/home/chris/Desktop/KoineTB') and creates a file "ArtDistance.csv" in the output directory (in my case 'home/chris/Desktop') which pairs the position of a head relative to its article with the frequency of that occurrence. If, for instance, the output csv file is...

-2, 20
1, 900
4, 18

...this means that over the course of all the treebanks, a head occurred two words before its article 20 times, that a head occurred one word after its article 900 times, and that a head occurred four words after its article 18 times.

Perseus treebanks give every word a sentence a unique sequential id. PROIEL treebanks give every word in the entire treebank a unique sequential id. So this script works by simply subtracting the head's id number from the article's id number. Unfortunately, the count is not yet 100% accurate because Perseus treebanks count punctuation as a word. PROIEL treebanks sometimes provide ellipsed words and give them unusual id numbers. So if an article points to an ellipsed word it might think the head is 10,000 words away. Furthermore, I think there may be some slight inconsistencies within the tagging of articles that can cause some problems. I'm working on solutions to all these.
