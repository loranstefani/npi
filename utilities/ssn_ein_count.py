
import os, sys,  csv

import functools





def count_ssn(csvfile = "sc.csv"):



    #open the csv file.
    csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

    rowindex = 0
    lt_nine = 0
    gt_nine = 0
    blank = 0
    errors = 0
    itin =0
    error_list =[]
    deactive_reson_list =[]
    print "NPI, contact_email, NPI_Deactivation_Reason_Code, ssn, itin"
    for row in csvhandle :
        if deactive_reson_list.__contains__(row[4])==False:
                    deactive_reson_list.append(row[4])
        #skip the first row
        if rowindex!=0:
            ssn = row[3]
            if len(ssn) != 9 and len(row[5])==0:
                errors += 1
                print "%s, %s, %s, %s, %s" % (row[1], row[0], row[4], row[3], row[5])


                if len(ssn) < 9:
                    lt_nine+=1
                    if len(ssn) == 0:
                        blank+=1
                    else:
                        suprise = row[1]
                if len(ssn) > 9:
                        gt_nine+=1

                if str(ssn).startswith("9"):
                    itin += 1
                else:
                    if len(ssn) != 0:
                        print str(ssn)[0]
        rowindex += 1


    print "Greater than 9     :", gt_nine
    print "Less than 9        :", lt_nine, suprise
    print "Blank              :", blank
    print "Total Errors       :", errors
    print "ITINs              :", itin
    print "Total Rows Scanned : ", rowindex
    print "Deactive reasons   : ", deactive_reson_list


if __name__ == "__main__":
    count_ssn()



