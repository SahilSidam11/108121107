# Function to create a set of unique items from a list of itemsets
def addSet(input: list) -> list: # T.C = O(n^2)
    mainSet = set()              # S.C = O(n)
    
    for obj in input:
        
        for item in obj:
            mainSet.add(item)
    
    mainList = list(mainSet)
    return mainList


def addlist(input):              # T.C = O(n)
    newList = list()             # S.C = O(n)
    
    for item in input:
        newList = newList + item
    
    return newList

def makeList(input) -> list:     # T.C = O(n)
    newList = list()             # S.C = O(n)
    
    for item in input:
        newList.append(set(item))
    
    return newList

# Function to convert a list of items into a list of single-item sets
def makeSet(input) -> list:      # T.C = O(n)
    candi = list()               # S.C = O(n)
    
    for obj in input:
        candi2 = set()
        candi2.add(obj)
        candi.append(candi2)
    
    return candi

# Function to extract items from candidate itemsets
def makeLk(candidate) -> list:   # T.C = O(n)
    Ck_items = list()            # S.C = O(n)
    
    for item, value in candidate:
        Ck_items.append(item)
    
    return Ck_items

# Function to check the support of itemsets and keep those with support >= minSup
def checkSup(candidate, minSup) -> list: 
    freqSup = list()             # T.C = O(n)
                                 # S.C = O(n)
    for item in candidate:
        
        if item[1] >= minSup:
            freqSup.append(item)
    
    return freqSup

# Function to count the support of candidate itemsets in the data
def countSup(input, candidate) -> list:  
    Ck = list()                  # T.C = O(n^2)
    for item in candidate:       # S.C = O(n)
        count = 0
        
        for obj in input:
            
            if obj.issuperset(item):
                count = count + 1
        
        Ck.append((item, count))
    return Ck

# Function to efficiently add an item to a set
def checkList(item, data: list):
    if item in data:            # T.C = O(1)
        pass                    # S.C = O(1)
    else:
        data.append(item)
    return

# Function to sort candidate itemsets in decreasing order of support count
def sortDec(candidate) -> list: # T.C = O(nlogn)
    dec = lambda kv: (kv[1], kv[0])
    candidate = sorted(candidate, key=dec, reverse=True)
    return candidate

def total(input) -> int:        # T.C = O(n)
    count = 0
    
    for obj in input:
        count = count + len(obj)
    
    return count
            
# Function to generate candidate itemsets of size k by taking unions of smaller itemsets
def makeUnion(input: list, k: int) -> list:
    thisList = list()           # T.C = O(n^2)
                                # S.C = O(n)
    for item in input:
        
        for obj in input:
            x = item.union(obj)
            
            if len(x) == k:
                checkList(x, thisList)
    
    return thisList

# Function to read data from a file and convert it into a list of itemsets
def readFile(readPath) -> list:
    with open(readPath, 'r') as rf:
        file_contents = rf.read()
        itemsets = file_contents.splitlines()
        items = list()          # T.C = O(n)
                                # S.C = O(n)
        for line in itemsets:
            items.append(set(line.split(';')))
    
    return items

# Function to write frequent itemsets and their support counts to a file
def writeFile(writePath, input, totalCount):
    with open(writePath, 'w') as wf:
        wf.write(str(totalCount) + '\n')
                                # T.C = O(n^2)
        for key, value in input:
            
            if len(key) >= 2:
                count = 0
                
                for word in list(key):
                    count = count + 1
                    wf.write(word)
                    
                    if count < len(key):
                        wf.write('; ')
                
                wf.write(' : ' + str(value) + '\n')
            
            else:
                
                for word in list(key):
                    wf.write(str(word) + ' : ' + str(value) + '\n')              
    return        

# Apriori algorithm function
def apriori(input, data, minSup, k, freqSet, countSet):
    if len(input) <= 1:
        return freqSet, countSet
                                # T.C = O((n^2)*logn)
    for item in input:
        
        for obj in item:
            freqSet.append(obj)   
    
    unionSet = makeUnion(input, k)
    Ck = countSup(data, unionSet)
    sortCk = sortDec(Ck)
    len_k_set = checkSup(sortCk, minSup)
    countSet.append(len_k_set)
    
    if k == 1:
        path = 'patterns_1.txt'
        len_1_set = addlist(countSet)
        writeFile(path, len_1_set, total(countSet))
    
    Lk = makeLk(len_k_set)
    return apriori(Lk, data, minSup, k+1, freqSet, countSet)
    
    
# Driver Code:    
readpath = 'categories.txt'
writepath = 'patterns_all.txt'
write_path = 'patterns_close.txt'
freqSet = list()
countSet = list()
minSup = 771
k = 1

dataBase = readFile(readpath)
total_categories = addSet(dataBase)
categories = makeSet(total_categories)
itemSet, itemCount = apriori(categories, dataBase, minSup, k, freqSet, countSet)
final = sortDec(addlist(itemCount))
total_count = len(final)
writeFile(writepath, final, total_count)
writeFile(write_path, final, total_count)
print(sortDec(final))

