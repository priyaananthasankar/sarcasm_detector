Perceptron for Sarcasm Detection

Each tweet is converted to a vector using Hash Vectorizer
Percetron is run with the input vectors and labels for 400 iterations. It sets the bias value internally.
Test tweets are also converted to vector and is used for predicting the appropriate class

Installation Instructions: (Write down any installation instructions if any) Need following packages to be installed in addition to python3 to run : (Assuming you have python3 installed on system)

pip3 : sudo apt-get install python3-pip
scikit : sudo pip3 install -U scikit-learn
