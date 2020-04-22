from datetime import datetime
from dateutil.relativedelta import relativedelta
def pcounter(current,total,step=100) :
  if current%step == 0 :
    print("Processed {} of {} items".format(current,total))

#Find majority political leaning of a county
def Majority(temp2): 
  values=temp2['Party Affiliation'].value_counts(dropna=False).tolist()
  keys=temp2['Party Affiliation'].value_counts(dropna=False).keys().tolist()  
  return (values[0]/temp2.shape[0])*100,keys[0]


#This simply compares two couples at the same address across years
#If a couple in one year is not found in the next we can safely assume they are no longer co-habitating
def check_divorced(dict_1,dict_2) :
  count_present = 0
  count_absent = 0
  total = len(dict_1)
  count = 0
  for k,v in dict_1.items() :
    
    count += 1
    pcounter(count,total,100000)

    if k not in dict_2.keys() :
      count_absent += 1 
      continue
    else :
      try:
        names_1 = sorted([ v[0]['Name First'].strip() ,v[1]['Name First'].strip() ])
        names_2 = sorted([ dict_2[k][0]['Name First'].strip() , dict_2[k][1]['Name First'].strip()  ])
      except Exception as e:
        pdb.set_trace()

    if names_1 == names_2 :
      count_present += 1
    else :
      count_absent +=1   
  pcounter(count,total,100000)    
  
#Calculate divorce but countywise - only used by New York
def check_divorced_countywise(dict_1,dict_2) :
  count_present = 0
  count_absent = 0
  total = len(dict_1)
  count = 0
  for k,v in dict_1.items() :
    
    count += 1
    pcounter(count,total,100000)

    if k not in dict_2.keys() :
      count_absent += 1 
      continue
    else :
      try:
        names_1 = sorted([ v[0]['Name First'].strip() ,v[1]['Name First'].strip() ])
        names_2 = sorted([ dict_2[k][0]['Name First'].strip() , dict_2[k][1]['Name First'].strip()  ])
      except Exception as e:
        pdb.set_trace()

    if names_1 == names_2 :
      count_present += 1
    else :
      count_absent +=1   
  pcounter(count,total,100000)    
  try :
    return (count_absent/(count_present+count_absent))*100
  except Exception as e :
    return 0


#Identify couples
def identify_couples(couples,NY=False) :
  hashmap = {}
  counter = 0
  for index,row in couples.iterrows() :
    counter += 1
    pcounter(counter,couples.shape[0],100000)
    val = row.to_dict()

    if NY == False :
      val['complete_address'] =  val['complete_address'].replace(' ','')   #We use the unique key of the lastname and address to identify people staying at the same location - 
      key = val['complete_address'] + val["Name Last"]
    else :
      add = str(val["Residence House Number"]) + val["Residence Street Name"] + val["Residence City"]
      val['complete_address'] = add
      key = val['complete_address'].replace(' ','')  + val["Name Last"]

    if key not in hashmap :
      hashmap[key] = []
    hashmap[key].append(val)
  pcounter(counter,couples.shape[0],100000) 
    
  same_party = {}
  diff_party = {}

  total = len(hashmap.keys())
  counter = 0
  #Loop through each of the couples and identify whether they have a same or different political leaning - group them accordingly
  for key,value in hashmap.items() :

    if counter%100000 == 0 :
      print("Processed {} of {} items".format(counter,total))

    counter += 1

    if len(value) == 1:
      continue
    if len(value) >= 2 :
      value=sorted(value, key = lambda i: datetime.strptime(i['Birth Date'],"%m/%d/%Y"),reverse=True)
      value[0]['Children']=len(value[2:])
      value[1]['Children']=len(value[2:])
      value=value[0:2]
      d1 = datetime.strptime(value[0]['Birth Date'],"%m/%d/%Y")
      d2 =  datetime.strptime(value[1]['Birth Date'],"%m/%d/%Y")
      diff = abs(relativedelta(d2,d1).years)
      if diff <= 15:
        gen1 = value[0]['Gender'].strip()
        gen2 =  value[1]['Gender'].strip()
        if gen1 == gen2  :
          continue
        value[0]['Party Affiliation'] = value[0]['Party Affiliation'].strip()
        value[1]['Party Affiliation'] = value[1]['Party Affiliation'].strip()
        if value[0]['Party Affiliation'] == value[1]['Party Affiliation'] :
          if key not in same_party :
            same_party[key] = []
            same_party[key] = value 
        else :
          if key not in diff_party :
            diff_party[key] = []      
            diff_party[key] = value


  print("Processed {} of {} items".format(counter,total))
  
  return same_party,diff_party


#Same functionality as identify couples but performed county wise
def identify_couples_countywise(couples,NY=False) :
  hashmap = {}
  counter = 0
  for index,row in couples.iterrows() :
    counter += 1
    pcounter(counter,couples.shape[0],100000)
    val = row.to_dict()

    if NY == False :
      val['complete_address'] =  val['complete_address'].replace(' ','')  
      key = val['complete_address'] + val["Name Last"]
    else :
      add = str(val["Residence House Number"]) + val["Residence Street Name"] + val["Residence City"]
      val['complete_address'] = add
      key = val['complete_address'].replace(' ','')  + val["Name Last"]
    
    county = val["County Code"]
    if county not in hashmap :
        hashmap[county] = {}
        
    
    if key not in hashmap[county] :
      hashmap[county][key] = []
    hashmap[county][key].append(val)
  pcounter(counter,couples.shape[0],100000) 
  

    
  same_party = {}
  diff_party = {}

  total = len(hashmap.keys())

  counter = 0
  
  for county,county_couples in hashmap.items() :
  
    if counter%10 == 0 :
      print("Processed {} counties of {} items".format(counter,total))

    counter += 1
  
    if county not in same_party :
        same_party[county] = {}
        diff_party[county] = {}
    
    for key,couples in county_couples.items() :
        
        value = couples
        

        
        if len(value) == 1:
          continue
        if len(value) >= 2 :
          value=sorted(value, key = lambda i: datetime.strptime(i['Birth Date'],"%m/%d/%Y"),reverse=True)
          value[0]['Children']=len(value[2:])
          value[1]['Children']=len(value[2:])
          value=value[0:2]
          d1 = datetime.strptime(value[0]['Birth Date'],"%m/%d/%Y")
          d2 =  datetime.strptime(value[1]['Birth Date'],"%m/%d/%Y")
          diff = abs(relativedelta(d2,d1).years)
          if diff <= 15:
            gen1 = value[0]['Gender'].strip()
            gen2 =  value[1]['Gender'].strip()
            if gen1 == gen2  :
              continue
            value[0]['Party Affiliation'] = value[0]['Party Affiliation'].strip()
            value[1]['Party Affiliation'] = value[1]['Party Affiliation'].strip()
            if value[0]['Party Affiliation'] == value[1]['Party Affiliation'] :
              if key not in same_party[county] :
                same_party[county][key] = []
                same_party[county][key] = value 
            else :
              if key not in diff_party[county] :
                diff_party[county][key] = []      
                diff_party[county][key] = value
                
  print("Processed {} of {} items".format(counter,total))
    
  return same_party,diff_party



#Segregate couples by generation - boomer, millenial,etc
def couples_by_generation(couples) :

  millenial = [1977,1995]
  boomer = [1946,1964]
  genx = [1965,1976]
  genz = [1996,2019]

  segregated = {
      "millenial" : {},
      "boomer" : {},
      "genz" : {},
      "genx" : {},
      "none" : {}
  }

  for key,couple in couples.items() :
    d1 = datetime.strptime(couple[0]['Birth Date'],"%m/%d/%Y").year
    d2 =  datetime.strptime(couple[1]['Birth Date'],"%m/%d/%Y").year

    if ( millenial[0] <= d1 <= millenial[1] ) and ( millenial[0] <= d2 <= millenial[1] ) :
      segregated["millenial"][key] = couple

    elif ( boomer[0] <= d1 <= boomer[1] ) and ( boomer[0] <= d2 <= boomer[1] ) :
      segregated["boomer"][key] = couple

    elif ( genz[0] <= d1 <= genz[1] ) and ( genz[0] <= d2 <= genz[1] ) :
      segregated["genz"][key] = couple

    elif ( genx[0] <= d1 <= genx[1] ) and ( genx[0] <= d2 <= genx[1] ) :
      segregated["genx"][key] = couple
    
    else :
      d1_1 = d1 + 5
      d1_2 = d1 - 5
      d2_1 = d2 + 5
      d2_2 = d2 - 5

      if ( millenial[0] <= (d1_1 or d1_2) <= millenial[1] ) and ( millenial[0] <= (d2_1 or d2_2) <= millenial[1] ) :
        segregated["millenial"][key] = couple

      elif ( boomer[0] <= (d1_1 or d1_2) <= boomer[1] ) and ( boomer[0] <= (d2_1 or d2_2) <= boomer[1] ) :
        segregated["boomer"][key] = couple

      elif ( genz[0] <= (d1_1 or d1_2) <= genz[1] ) and ( genz[0] <= (d2_1 or d2_2) <= genz[1] ) :
        segregated["genz"][key] = couple

      elif ( genx[0] <= (d1_1 or d1_2) <= genx[1] ) and ( genx[0] <= (d2_1 or d2_2) <= genx[1] ) :
        segregated["genx"][key] = couple
      else :
        segregated["none"][key] = couple

      

  return segregated

#Break couples into Male-Democratic:Female-Republican, Female-Democratic:Male-Republican,etc
def couples_d(data1,data2):
  dem_dem={}
  rep_rep={}
  rep_dem={}
  dem_rep={}
  others_dem={}
  others_rep={}
  others_others={}
  rep_others={}
  dem_others={}
  for keys,values in data1.items():
    if data1[keys][0]['Party Affiliation'] and data1[keys][1]['Party Affiliation'] == 'DEM':
      dem_dem[keys]= data1[keys]    
    elif data1[keys][0]['Party Affiliation'] and data1[keys][1]['Party Affiliation'] == 'REP':
      rep_rep[keys]=data1[keys]
    elif (data1[keys][0]['Party Affiliation'] and data1[keys][1]['Party Affiliation']) not in('DEM','REP'):
      others_others[keys]=data1[keys]
      

  for keys,values in data2.items():
    if (data2[keys][0]['Party Affiliation'] and data2[keys][1]['Party Affiliation']) in ('DEM','REP'):
      if (data2[keys][0]['Gender'] == 'M' and data2[keys][0]['Party Affiliation'] == 'REP') or (data2[keys][1]['Gender'] == 'M' and data2[keys][1]['Party Affiliation'] == 'REP') :
        rep_dem[keys]=data2[keys]
      elif (data2[keys][0]['Gender'] == 'M' and data2[keys][0]['Party Affiliation'] == 'DEM') or (data2[keys][1]['Gender'] == 'M' and data2[keys][1]['Party Affiliation'] == 'DEM') :
        dem_rep[keys]=data2[keys]
    else:
      if (data2[keys][0]['Gender'] == 'M' and data2[keys][0]['Party Affiliation']=='REP') or (data2[keys][1]['Gender'] == 'M' and data2[keys][1]['Party Affiliation']=='REP'): 
        rep_others[keys]=data2[keys]
      elif (data2[keys][0]['Gender'] == 'M' and data2[keys][0]['Party Affiliation']=='DEM') or (data2[keys][1]['Gender'] == 'M' and data2[keys][1]['Party Affiliation']=='DEM'): 
        dem_others[keys]=data2[keys]
      elif (data2[keys][0]['Gender'] == 'F' and data2[keys][0]['Party Affiliation']=='REP') or (data2[keys][1]['Gender'] == 'F' and data2[keys][1]['Party Affiliation']=='REP'): 
        others_rep[keys]=data2[keys]
      elif (data2[keys][0]['Gender'] == 'F' and data2[keys][0]['Party Affiliation']=='DEM') or (data2[keys][1]['Gender'] == 'F' and data2[keys][1]['Party Affiliation']=='DEM'):
        others_dem[keys]=data2[keys]
        
  return dem_dem,rep_rep,rep_dem,dem_rep,others_others,rep_others,dem_others,others_rep,others_dem



#Simply group couples based on the age difference between their marriages
def split_couples_by_age(couples) :

  age_diff = {}
  for i in range(0,16) :
    age_diff[i] = {}

  
  for key,couple in couples.items() :
    d1 = datetime.strptime(couple[0]['Birth Date'],"%m/%d/%Y")
    d2 =  datetime.strptime(couple[1]['Birth Date'],"%m/%d/%Y")
    diff = abs(relativedelta(d2,d1).years)
    if diff <= 15 :
      if diff in age_diff :
        age_diff[diff][key] = couple
  
  return age_diff

###Calculate with/without children groups###
def children(data):
  with_child={}
  without_child={}
  for keys,values in data.items():
    if data[keys][0]['Children'] >= 1:
      with_child[keys]=data[keys]
    else:
      without_child[keys]=data[keys]
  return with_child,without_child
