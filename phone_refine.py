import pandas as pd
import warnings
import sys

warnings.filterwarnings('ignore')

# removes number in parenthesis at the end
def remove_end_number(number):
  number = number[:number.index("(", 2)-1]
  return number


# removes all invalid numbers
def remove_invalid_number(number):
  print("")


# formats all nice
def reformat(number):
  return "("+number[:3]+") "+number[3:6]+"-"+number[6:]


### Gets the dataset ###
if (len(sys.argv)==1):
    print("No file specified")
    quit()

else:
    df = pd.read_csv(sys.argv[1])

initial = len(df.index)


### Sorts by Frequency ###
df.sort_values(by=['Files with Hits'], inplace=True, ascending=False)


### Turns into only numbers ###
df.rename(columns={"List Name": "Phone Number"}, inplace=True)
df["Phone Number"] = df["Phone Number"].apply(remove_end_number)
df["Phone Number"] = df["Phone Number"].str.replace(r"[\. \-\(\)]","")


### Removes all invalid numbers with 0s and 1s ###
df = df[(df["Phone Number"].str[:1]!="0") & (df["Phone Number"].str[:1]!="1")]
df = df[(df["Phone Number"].str[3:4]!="0") & (df["Phone Number"].str[3:4]!="1")]


### Reformats the numbers all nice ###
df["Phone Number"] = df["Phone Number"].apply(reformat)


### Sets index to phone number ###
df.set_index('Phone Number', inplace=True)


### Output to csv ###
if (len(sys.argv)>2):
  df.to_csv(sys.argv[2])
else:
  df.to_csv("refined.csv")


### Print statistics ###
final = len(df.index)
print(str(initial-final)+"/"+str(initial)+" results were removed ("+"{:.0%}".format((initial-final)/initial)+")")