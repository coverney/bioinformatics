#Resources:
#https://splinter.readthedocs.io/en/latest/#features 
#http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#DEBUGGING TIPS
# 1) if the program times out while loading the JGI IMG file or Batch BLAST results, try increase the the number in the sleep function
# 2) try running the code in the jupyter notebook version because each section can be ran individually which allows for better debugging

#This program conducts a batch BLAST of multiple genes from JGI img and stores the top ten results for each BLAST.
############################################################################################################################################
#Section 1: imports the necessary libraries and creates the arrays needed to store information from JGI and BLAST You have to make sure that you have the splinter and BeautifulSoup libraries (reference resources above for download process)
from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
sequences = []
results = []

#Section 2: opens up a Chrome browser the file path varies depending on where your chromedriver is located
executable_path = {'executable_path':'C:\Program Files\chromedriver.exe'}
browser = Browser('chrome', **executable_path)
sleep(5)

#Section 3: obtains the top three amino acid sequences from the gene list and stores them in the sequences array
#The gene_url is the link to the gene list of a particular scaffold (replace this url with your own), you may be prompted to sign into JGI. If so, sign in 
#Change the number of genes to blast by changing the "range(0,3)" section to "range(0,n)", n being the number you want
gene_url = "https://img.jgi.doe.gov/cgi-bin/mer/main.cgi?section=MetaScaffoldDetail&page=metaScaffoldGenes&scaffold_oid=Ga0136453_100219&taxon_oid=3300010205"
browser.visit(gene_url) #this is to account to the user logging into JGI
sleep(30)
for i in range(0,3):
    browser.visit(gene_url)
    button = browser.find_by_id('yui-rec' + str(i))
    soup = BeautifulSoup(button.html, "html.parser")
    gene_url2 = soup.a.get('href')
    browser.visit("https://img.jgi.doe.gov/cgi-bin/mer/" + gene_url2)
    soup2 = BeautifulSoup(browser.html, "html.parser")
    tab = soup2.table
    tabs = tab.find_all('tr')
    gene_url3 = tabs[15].a.get('href')
    browser.visit("https://img.jgi.doe.gov/cgi-bin/mer/" + gene_url3)
    soup3 = BeautifulSoup(browser.html, "html.parser")
    a = soup3.pre.get_text()
    b = soup3.pre.font.get_text()
    amino = "".join(a.rsplit(b))
    amino = amino.replace('\n', '')
    sequences.append(amino)

print(sequences)

#Section 4: takes the sequences from section 3 and BLASTs them.It stores the first ten hits into the results array. 
#So each sequence has 10 elements You can change the number 10 by changing the "range(1,10)" into "range(1,n)" n being the number you want 
blast_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins"
for seq in sequences:
    browser.visit(blast_url)
    browser.fill('QUERY', seq)
    button = browser.find_by_id('b1')
    button.click()
    sleep(100) #this is to account for the query time for BLAST
    table = browser.find_by_id('dscTable')
    #find the table
    while len(table) is 0:
        table = browser.find_by_id('dscTable')
    #get the actual data
    result = []
    for i in range(1,10):  
        res = table.find_by_id('deflnDesc_' + str(i)).html
        result.append(res)
    results.append(result)

print(results[0])