These are worked answers for the assignment 1 question.

For fizzbuzz, I prefer fizzbuzz.py, rather than fizzbuzz2.py, as it
doesn't need a special case when the number divides by both 3 and 5,
but either is OK.

For pi, once you understand the basic algorithm, the question then is
how do you decide if the answer is good enough?  You could just loop a
fixed number of times, but that provides no guarantee of a degree of
accuracy.  The solution here calculates four independent answers, and
compares each to the mean of the four.  It stops when all the
individual answers agree with the mean to the specified accuracy.

For caesar cipher, this solution includes both encryption and
decryption code, so it can test with any string.  It tests all 26
possible shifts, and decides which is the correct solution by using a
table of english language letter frequencies.  This works well for
reasonably long texts, but probably won't work for very short texts.