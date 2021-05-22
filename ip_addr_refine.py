import pandas as pd
import warnings
import sys

warnings.filterwarnings('ignore')

# removes number in parenthesis at the end
def remove_end_number(number):
  number = number[:number.index("(", 2)-1]
  return number


# Marks all IP addresses with more than two 0's or have the first octet 0 < x < 10 as improbable
def improbable(address):
  octets = address.split(".")
  if (int(octets[0]) < 10) or (octets.count("0") > 1):
    return "Yes"
  return "No"


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
df.rename(columns={"List Name": "IP Address"}, inplace=True)
df["IP Address"] = df["IP Address"].apply(remove_end_number)


### Removes IP addresses that start with 0,240-255
df = df[df["IP Address"].str[:1]!="0"]
df["octet1"] = pd.to_numeric(df["IP Address"].str[:3])
df = df[df["octet1"]<240]
del df["octet1"]


### Improbable marking ###
df["Improbable"] = df["IP Address"].apply(improbable)


### Sorts by Improbable, then File Hits, then IP Address ###
df = df.sort_values(["Improbable", "Files with Hits", "IP Address"], ascending=(True, False, True))


### Sets index to IP address ###
df.set_index('IP Address', inplace=True)


### Output to csv ###
if (len(sys.argv)>2):
  df.to_csv(sys.argv[2])
else:
  df.to_csv("refined.csv")


### Print statistics ###
final = len(df.index)
print(str(initial-final)+"/"+str(initial)+" results were removed ("+"{:.0%}".format((initial-final)/initial)+")")

finalImprobable = len(df[df["Improbable"]=="Yes"])
print(str(finalImprobable)+"/"+str(final)+" results were marked as improbable ("+"{:.0%}".format(finalImprobable/final)+")")