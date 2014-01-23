from pymongo import Connection
import os, sys, string, json, csv
from collections import OrderedDict

import functools
import pymongo
import time
import hashlib



MONGO_HOST="127.0.0.1"
MONGO_PORT=27017

def org_relations_import_mongo(delete_collection_before_import=True,
                          database_name="nppes",
                          collection_name="orgs"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    rowindex=0
    error_list =[]
    success=0
    try:
        mconnection =   Connection("127.0.0.1")
        db =             mconnection[database_name]
        collection    = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        basic_collection = db["basic"]

        results1 = basic_collection.find({"Entity_Type_Code": "2",},
                                         {"Employer_Identification_Number_EIN":1,
                                          }
                                         )

        print "Count All EINS", results1.count()

        all_eins =[]
        for i in results1:

           #print i.keys()
           #print dir(i)
           all_eins.append(i["Employer_Identification_Number_EIN"])
        # make a set
        distinct_eins = tuple(set(all_eins))
        print "Distinct EINs", len(distinct_eins)

        for i in distinct_eins:
            if success % 1000 == 0:
                print success

            results=basic_collection.find({"Employer_Identification_Number_EIN":i}, {"NPI":1,})
            new_record = {"ein": i,
                          "hash_ein": hashlib.sha224(i).hexdigest() }
            npis =[]
            for j in results:
                npis.append(j["NPI"])

            new_record["npis"] = npis
            rowindex+=1


            try:

               myobjectid=collection.insert(new_record)
               success+=1
            except:
                error_message = "Error on row " + str(rowindex) +  ". " + str(sys.exc_info())
                error_list.append(str(sys.exc_info()))



        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_rows_imported']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict

def basic_csv_import_mongo(csvfile = "basic_npidata_20050523-20120824.csv",
                              delete_collection_before_import=True,
                          database_name="nppes", collection_name="basic"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""
    print "Basic CSV load into Mongo"
    l=[]
    response_dict={}
    try:
        mconnection =   Connection("127.0.0.1")
        db          =             mconnection[database_name]
        collection    = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :
            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:
                #print type(cleaned_headers), len(cleaned_headers), cleaned_headers[0]

                record = dict(zip(cleaned_headers, row))


                #if there is no values, skip the key value pair
                kwargs ={}

                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v

                try:
                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex+=1
            if rowindex % 1000 == 0:
                print rowindex

        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_di

def taxonomy_csv_import_mongo(csvfile = "taxonomy_npidata_20050523-20120824.csv",
                              delete_collection_before_import=True,
                          database_name="nppes", collection_name="taxonomies"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    try:
        mconnection =   Connection("127.0.0.1")
        db          =             mconnection[database_name]
        collection    = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :

            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:

                #print type(cleaned_headers), len(cleaned_headers), cleaned_headers[0]

                record = dict(zip(cleaned_headers[0:3], row[0:3]))

                taxonomies    = [
                                      {"code": row[3],
                                       "primary": row[4]},

                                      {"code": row[5],
                                       "primary":row[6]},

                                      {"code": row[7],
                                       "primary":row[8]},

                                      {"code": row[9],
                                       "primary":row[10]},

                                      {"code": row[11],
                                       "primary":row[12]},

                                      {"code": row[13],
                                       "primary":row[14]},

                                      {"code": row[15],
                                       "primary":row[16]},

                                      {"code": row[17],
                                       "primary":row[18]},

                                      {"code": row[19],
                                       "primary":row[20]},

                                      {"code": row[21],
                                       "primary":row[22]},

                                      {"code": row[23],
                                       "primary":row[24]},

                                      {"code": row[25],
                                       "primary":row[26]},

                                      {"code": row[27],
                                       "primary":row[28]},

                                      {"code": row[29],
                                       "primary":row[30]},

                                      {"code": row[31],
                                       "primary":row[32]},

                                      ]


                cleaned_taxonomies= []

                for r in taxonomies:
                    if r["code"] != "":
                         if r["primary"]=="Y":
                             #print " I am primary"
                             r["is_primary"] = True
                         cleaned_taxonomies.append(r)


                record['taxonomies'] = cleaned_taxonomies
                #if there is no values, skip the key value pair
                kwargs ={}

                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v

                try:

                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex+=1

        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict

def addresses_csv_import_mongo(csvfile = "addresses_npidata_20050523-20120824.csv",
                              delete_collection_before_import=True,
                          database_name="nppes", collection_name="addresses"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    try:
        mconnection = Connection("127.0.0.1")
        db          = mconnection[database_name]
        collection  = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :

            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:

                #print type(cleaned_headers), len(cleaned_headers), cleaned_headers[0]

                record = dict(zip(cleaned_headers[0:3], row[0:3]))

                addresses    = [
                                      {"address_type":        "mailing",
                                       "line_1":              row[3],
                                       "line_2":              row[4],
                                       "city":                row[5],
                                       "state":               row[6],
                                       "country":             row[7],
                                       "postal":              row[8],
                                       "telephone":           row[9],
                                       "telephone_extension": row[10],
                                       "fax":                 row[11],
                                       },

                                      {"address_type":          "practice_location",
                                       "line_1":                row[12],
                                       "line_2":                row[13],
                                       "city":                  row[14],
                                       "state":                 row[15],
                                       "country":               row[16],
                                       "postal":                row[17],
                                       "telephone":             row[18],
                                       "telephone_extension":   row[19],
                                       "fax":                   row[20],
                                       },

                                      ]





                record['addresses'] = addresses
                #if there is no values, skip the key value pair
                kwargs ={}

                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v

                try:

                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex+=1

        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict


def identifiers_csv_import_mongo(csvfile = "identifiers_npidata_20050523-20120824.csv",
                              delete_collection_before_import=True,
                          database_name="nppes", collection_name="identifiers"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    try:
        mconnection = Connection("127.0.0.1")
        db          = mconnection[database_name]
        collection  = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :

            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:

                #print type(cleaned_headers), len(cleaned_headers), cleaned_headers[0]

                record = dict(zip(cleaned_headers[0:9], row[0:9]))

                identifiers    = []

                identifer_range = range(0,49)
                position = 11
                for i in identifer_range:
                    #print position
                    identifier = { "identifier": str("".join(s for s in row[position] if s in string.printable)).lstrip(),
                                   "type_code":   str("".join(s for s in row[position+1] if s in string.printable)).lstrip(),
                                   "state":       str("".join(s for s in row[position+2] if s in string.printable)).lstrip(),
                                   "issuer":      str("".join(s for s in row[position+3] if s in string.printable)).lstrip(),
                                 }
                    #print identifier
                    position += 4
                    identifiers.append(identifier)


                cleaned_identifiers= []

                for i in identifiers:
                    if i["identifier"] != "":
                        cleaned_identifiers.append(i)



                record['identifiers'] = cleaned_identifiers
                #if there is no values, skip the key value pair
                kwargs ={}

                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v

                try:

                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex+=1

        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict




def flat_identifiers_csv_import_mongo( csvfile = "identifiers_npidata_20050523-20120824.csv",
                                       delete_collection_before_import=True,
                                       database_name="nppes",
                                       collection_name="flat-identifiers"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    print "start flat import of identifiers"
    try:

        mconnection = Connection("127.0.0.1")
        db          = mconnection[database_name]
        collection  = db[collection_name]

        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        mongoindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :

            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")
                    cleaned_headers.append(c)
            else:

                record = dict(zip(cleaned_headers[0:3], row[0:3]))

                identifer_range = range(0,49)

                position = 11

                for i in identifer_range:
                    if row[position] != "":
                        flat_record = record
                        flat_record['identifier'] = str("".join(s for s in row[position]   if s in string.printable)).lstrip()
                        flat_record['type_code']  = str("".join(s for s in row[position+1] if s in string.printable)).lstrip()
                        flat_record['state']      = str("".join(s for s in row[position+2] if s in string.printable)).lstrip()
                        flat_record['issuer']     = str("".join(s for s in row[position+3] if s in string.printable)).lstrip()
                        kwargs = {}
                        for k,v in flat_record.items():
                            if v:
                                kwargs[k]=v

                        try:
                            myobjectid=collection.insert(kwargs)
                            mongoindex+=1



                        except:
                            error_message = "Error on row " + str(rowindex) +  ". " + str(sys.exc_info())
                            error_list.append(error_message)
                            print error_message
                            sys.exit()

                        #print identifier
                        position += 4
                        #identifiers.append(identifier)

            rowindex+=1


        if error_list:
                response_dict ={}
                response_dict['num_rows_imported']=rowindex
                response_dict['num_rows_errors']=len(error_list)
                response_dict['errors']=error_list
                response_dict['code']=400
                response_dict['message']="Completed with errors"
                print response_dict
                sys.exit()
        else:

                response_dict ={}
                response_dict['num_rows_imported']=mongoindex
                response_dict['num_csv_rows']=rowindex
                response_dict['code']=200
                response_dict['message']="Completed."

    except:
        print "Error writing to  Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
        return response_dict


    return response_dict


def license_csv_import_mongo(csvfile = "licenses_npidata_20050523-20120824.csv", delete_collection_before_import=True,
                          database_name="nppes",
                          collection_name="licenses"):

    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l=[]
    response_dict={}
    try:
        mconnection =   Connection("127.0.0.1")
        db =             mconnection[database_name]
        collection    = db[collection_name]


        if delete_collection_before_import:
            myobjectid=collection.remove({})

        #open the csv file.
        csvhandle = csv.reader(open(csvfile, 'rb'), delimiter=',')

        rowindex = 0
        errors=0
        error_list =[]
        success =0
        for row in csvhandle :

            if rowindex==0:
                 column_headers = row
                 cleaned_headers = []
                 for c in column_headers:
                    c= c.replace(".", "")
                    c= c.replace("(", "")
                    c= c.replace(")", "")
                    c =c.replace("$", "-")
                    c =c.replace(" ", "_")

                    cleaned_headers.append(c)
            else:

                #print type(cleaned_headers), len(cleaned_headers), cleaned_headers[0]

                record = dict(zip(cleaned_headers[0:3], row[0:3]))

                licenses = [
                                      {"number": row[3],
                                       "state":row[4]},

                                      {"number": row[5],
                                       "state":row[6]},

                                      {"number": row[7],
                                       "state":row[8]},

                                      {"number": row[9],
                                       "state":row[10]},

                                      {"number": row[11],
                                       "state":row[12]},

                                      {"number": row[13],
                                       "state":row[14]},

                                      {"number": row[15],
                                       "state":row[16]},

                                      {"number": row[17],
                                       "state":row[18]},

                                      {"number": row[19],
                                       "state":row[20]},

                                      {"number": row[21],
                                       "state":row[22]},

                                      {"number": row[23],
                                       "state":row[24]},

                                      {"number": row[25],
                                       "state":row[26]},

                                      {"number": row[27],
                                       "state":row[28]},

                                      {"number": row[29],
                                       "state":row[30]},

                                      {"number": row[31],
                                       "state":row[32]},

                                      ]

                cleaned_licenses= []

                for r in licenses:
                    if r["state"]!="" and  r["number"]!="":
                        cleaned_licenses.append(r)
                record['licenses']=cleaned_licenses
                #if there is no values, skip the key value pair
                kwargs ={}

                #Only populate fields that are not blank.
                for k,v in record.items():
                    if v:
                        kwargs[k]=v

                try:

                    myobjectid=collection.insert(kwargs)
                    success+=1
                except:
                    error_message = "Error on row " + rowindex +  ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex+=1

        if error_list:
            response_dict ={}
            response_dict['num_rows_imported']=rowindex
            response_dict['num_rows_errors']=len(error_list)
            response_dict['errors']=error_list
            response_dict['code']=400
            response_dict['message']="Completed with errors"
        else:

            response_dict ={}
            response_dict['num_rows_imported']=success
            response_dict['code']=200
            response_dict['message']="Completed."
        return response_dict
    except:
        #print "Error reading from Mongo"
        #print str(sys.exc_info())
        response_dict['num_results']=0
        response_dict['code']=400
        response_dict['type']="Error"
        response_dict['results']=[]
        response_dict['message']=str(sys.exc_info())
    return response_dict


def load_taxonomy():
    csvfile = csv.reader(open('sample1.csv', 'rb'), delimiter=',')

    outputcsvfileb = open('taxonomy_npidata_20050523-20120824.csv','wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                           quoting=csv.QUOTE_MINIMAL)


    rowindex              = 0
    invalid_ssn           = 0


    """#skip the first row """
    """#next(csvfile)"""
    print "start file iteration"

    for row in csvfile:
        t = row[0:1] + row[7:9] + row[68:69] + row[71:73] + row[75:77] + row[79:81] \
            + row[83:85] + row[87:89] + row[91:93] + row[95:97] + row[99:101] \
            + row[103:105] + row[107:109] + row[111:113] + row[115:117] \
            + row[119:121]+ row[123:125] + row[127:128]

        csvwriterb.writerow(t)
        rowindex+=1

    print "Iterated over", rowindex, "rows."


def load_identifiers():
    csvfile = csv.reader(open('npidata_20050523-20120824.csv', 'rb'), delimiter=',')

    outputcsvfileb = open('identifiers_npidata_20050523-20120824.csv','wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                           quoting=csv.QUOTE_MINIMAL)


    rowindex              = 0
    invalid_ssn           = 0


    """#skip the first row """
    """#next(csvfile)"""
    print "start file iteration"

    for row in csvfile:
        t = row[0:2] + row[6:15] + row[128:327]

        csvwriterb.writerow(t)
        rowindex+=1

    print "Iterated over", rowindex, "rows."


def load_licenses():

    csvfile = csv.reader(open('npidata_20050523-20120824.csv', 'rb'), delimiter=',')

    outputcsvfileb = open('licenses_npidata_20050523-20120824.csv','wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                           quoting=csv.QUOTE_MINIMAL)


    rowindex              = 0
    invalid_ssn           = 0


    """#skip the first row """
    """#next(csvfile)"""
    print "start file iteration"

    for row in csvfile:
        l = row[0:1] + row[7:9]  + row[69:71]+ row[73:75]+ row[77:79]+ row[81:83] + \
                       row[85:87]+ row[89:91]+ row[93:95]+ row[97:99] + row[101:103] + \
                       row[105:107]+ row[109:111]+ row[113:115]+ row[117:119]+ row[121:123] + \
                       row[125:127]

        csvwriterb.writerow(l)
        rowindex+=1

    print "Iterated over", rowindex, "rows."

def load_addresses():

    csvfile = csv.reader(open('npidata_20050523-20120824.csv', 'rb'), delimiter=',')

    outputcsvfileb = open('addresses_npidata_20050523-20120824.csv','wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                           quoting=csv.QUOTE_MINIMAL)

    rowindex              = 0
    invalid_ssn           = 0


    """#skip the first row """
    """#next(csvfile)"""
    print "start file iteration"

    for row in csvfile:
        l = row[0:1] + row[7:9]  + row[22:40]

        csvwriterb.writerow(l)
        rowindex+=1

    print "Iterated over", rowindex, "rows."


def load_basic():

    csvfile = csv.reader(open('npidata_20050523-20120824.csv', 'rb'), delimiter=',')

    outputcsvfileb = open('basic_npidata_20050523-20120824.csv','wb')

    csvwriterb = csv.writer(outputcsvfileb, delimiter=',',
                           quoting=csv.QUOTE_MINIMAL)


    rowindex              = 0
    invalid_ssn           = 0


    """#skip the first row """
    """#next(csvfile)"""
    print "start file iteration"
    for row in csvfile:


        csvwriterb.writerow(row[0:68]+row[328:332])
        rowindex+=1

    print "Done so closing the output file."
    outputcsvfileb.close()

    print "Iterated over", rowindex, "rows."


def buildtax():
  taxdict={}
  csvfile = csv.reader(open('taxonomy.csv', 'rb'), delimiter=',')
  rowindex = 0
  for row in csvfile:
    if len(row)==1:
      pass

    elif len(row)>2:
      name = ",".join(row[:-1])
      value = row[-1]

    elif len(row)==2:
      name = row[0]
      value = row[1]

    taxdict[value]=name
  return taxdict



if __name__ == "__main__":
    #load_taxonomy()
    #load_licenses()
    #load_addresses()
    #load_identifiers()
    #r = addresses_csv_import_mongo()
    #print r
    #load_basic()
    #r = basic_csv_import_mongo()
    #print r
    #r =org_relations_import_mongo()
    #print r
    #taxdict = buildtax()


    #r = taxonomy_csv_import_mongo()
    #print r

    #print identifiers_csv_import_mongo()
    r = flat_identifiers_csv_import_mongo()
    print r


