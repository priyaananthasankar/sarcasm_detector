import csv
import sys

# number of tweets or subjects to be rated
tweets = sys.argv[1]
global N
global k
global n
global sum_of_yes_per_tweet
global sum_of_no_per_tweet
global sarcasm_writer
global not_sarcasm_writer

# number of raters n
n = 3

# category assignment (yes/no)
k = 2

# total number of tweets
N = 3000

# Proportion of all assignments to Yes
p_yes = 0
sum_of_yes_per_tweet = 0

# Proportion of all assignments to No
p_no = 0
sum_of_no_per_tweet = 0

total_extent = 0
sarcasm_corpus = 0
non_sarcasm_corpus = 0

f = open("fliess_kappa.csv", 'wt')
fleiss_kappa_writer = csv.writer(f)
i = 0
list_of_tuples = []
with open(tweets, 'r',encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    for tweet,r1,r2,r3 in reader:
      if tweet and r1 and r2 and r3:
         i += 1
         yes_per_tweet = 0
         no_per_tweet = 0
         if(r1.lower() == "yes"):
            yes_per_tweet +=1
         if(r2.lower() == "yes"):
            yes_per_tweet += 1
         if(r3.lower() == "yes"):
            yes_per_tweet += 1
         if((r1.lower() == "no") or (r1.lower() == "not sure")):
            no_per_tweet += 1
         if((r2.lower() == "no") or (r2.lower() == "not sure")):
            no_per_tweet += 1
         if((r3.lower() == "no") or (r3.lower() == "not sure")):
            no_per_tweet += 1

         tuple = (i,yes_per_tweet,no_per_tweet)
         list_of_tuples.append(tuple)
         fleiss_kappa_writer.writerow([i,yes_per_tweet,no_per_tweet])

sum_of_all_yes = 0
sum_of_all_no = 0

list_of_P_i = []
for tweet,n_yes,n_no in list_of_tuples:
   sum_of_all_yes += n_yes
   sum_of_all_no += n_no
   list_of_P_i.append( (1/(float(n)*(n-1))) * (((n_yes**2) + (n_no**2)) - n) )

p_yes = (1/(float(N) * n)) * sum_of_all_yes
p_no = (1/(float(N) * n)) * sum_of_all_no


print("Proportion of all assignments to the YES category (p_yes): ",p_yes)
print("Proportion of all assignments to the NO category (p_no): " ,p_no)

sum_of_all_p_i = 0
for p in list_of_P_i:
   sum_of_all_p_i += p

p_dash = (sum_of_all_p_i/float(N))
print("Overall extent of agreement(p_mean): ", p_dash)
p_expected = (p_yes**2) + (p_no**2)

print("Mean proportion of agreement(p_expected): ", p_expected)

kappa = (p_dash - p_expected)/(1-p_expected)
print("KAPPA: ",kappa)







