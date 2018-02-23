#Make sure you have the pandas library when you run this!!
#This program searches through two annotation spreadsheets in order to look for gene product names for each gene in the edgeAll data sheet.
#The code can easily be applied to other data analysis projects that involve looking through excel spreadsheets and adding additional information
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

#You will need to change the file paths depending on the data you want to look at. In my example, df1 is Halo data, df2 is the less complete annotations, and df3 is the more complete annotations
df1 = pd.read_excel('C:/Users/coverney/Desktop/Research/Halo/edgeAll.xlsx', sheetname='edgeAll.txt')
df2 = pd.read_excel('C:/Users/coverney/Desktop/Research/Halo/gene_locus_tag_annotation_Halobacillus_JH5_genome.xlsx', sheetname='sorttaxon90370_15-jan-2018')
df3 = pd.read_excel('C:/Users/coverney/Desktop/Research/Halo/gene_locus_tag_annotation_gene_info_more_complete_list_Halobacillus_genome.xlsx', sheetname='2622736421.info')

#This section is for testing purposes, it should print out the column headings of df3
print("Column headings:")
print(df3.columns)

#This section makes an array from the elements in the Transcript_ID column in df1, it also prints out its first 10 elements
list_transID = df1['transcript ID']
print(list_transID[0:10])

#This section makes an array from the elements in the Gene Product Name column in df2, it also prints out its first 10 elements
list_geneproductname = df2['Gene Product Name']
print(list_geneproductname[0:10])

#This section makes an array from the elements in the Locus Tag column in df2, it also prints out its first 10 elements
list_locustag1 = df2['Locus Tag']
print(list_locustag1[0:10])

#This section makes an array from the elements in the Locus Tag column in df3, it also prints out its first 10 elements
list_locustag2 = df3['Locus Tag']
print(list_locustag2[0:10])

#This section makes an array from the elements in the Gene Information column in df3, it also prints out its first 10 elements
list_geneinfo = df3['Gene Information']
print(list_geneinfo[0:10])

#This section makes an array from the elements in the Source column in df3, it also prints out its first 10 elements
list_labels = df3['Source']
print(list_labels[0:10])

#This section goes through transcript IDs in df1 to see if they are in the locus tags of df2 and df3.
#If it is in df2, the gene product name from df2 gets appended to list_results If it is not in df2, the locus tag is searched for in df3 and the corresponding product name is extracted and added to list_results. The gene product name is "no match" if the transcript ID is not found in df2 or df3
list_results = []
for i, ID in enumerate(list_transID[0:]):
    try:
        index = list(list_locustag1).index(ID)
        list_results.append(list_geneproductname[index])
    except ValueError:
        try:
            index = list(list_locustag2).index(ID)
            #find the last index of the ID
            index2 = index
            end = 0
            while end is 0 and index2 < len(list_locustag2):
                element = list_locustag2[index2]
                if str(element) == "nan":
                    end = 1
                    break
                else:
                    index2 = index2 + 1
            index3 = 0
            for j, label in enumerate(list_labels[index:index2+1]):
                if str(label) == "Product_name":
                    index3 = j
            result = list_geneinfo[index+(index3)]
            list_results.append(result)
        except ValueError:
            list_results.append("no match")
print(list_results)

#A new column called Gene Product Name is created in df1 and df1 is exported as a Excel file. The file path needs to be change according to your project
df1['Gene Product Name'] = list_results
df1.to_excel("C:/Users/coverney/Desktop/Research/Halo/edgeAll_with_Product_Name.xlsx")