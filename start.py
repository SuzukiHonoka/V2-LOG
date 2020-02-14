#json_dumps used for save dict file
from json import dumps as json_dumps
#get_time used for get the current system time
from time import time as get_time
#request used for open a url and get some required data
from urllib import request
#log file path
log_file_path = 'access.log'
#store the datas after_sort_process1
line_data_sort_by_date = {}
#store the source file all lines as a list format
per_line_data = []
#IP lookup API key
#website: ipstack.com
#ip: 'ip1,ip2,ip3..'
#request format: api_url+ip+str1+key+str2
ipstack_api = 'http://api.ipstack.com/'
ipstack_str1 = '?access_key='
ipstack_str2 = '&language=zh'
ipstack_key = '34009b6f79cb4c401c6e9faad5891b28'

#split data list:
#list[0]: date
#list[1]: time
#list[2]: source
#list[3]: action
#list[4]: destination

#sometimes the log format will like this:
#tcp:x.x.x.x:233
#so we need to make a check for return the valid data

#str:str
def str_split(str):
    d = str.split(':')
    if len(d) == 3:
        return d[1]
    else:
        return d[0]

#sometimes we need to save the result to a file
#for prevent twice operation like reload logs

#fn:str dict:dict
def conver_to_file(fn,dict):
    with open(fn,'w+') as fd:
        fd.write(json_dumps(dict))
    print('Success Write File:',fn)

#ip:str/list
def get_ip_info(ip):
    ips_format = ''
    if type(ip) == list:
        for per_ip in list:
            ips_format += ',' + per_ip
    else:
        ips_format = ip
        
    r_url = ipstack_api + ips_format + ipstack_str1
+  ipstack_api + ipstack_str2
    r = request(r_url)
    if r.getcode() == 200:
        return r.read()

with open(log_file_path,'r') as fd:
    per_line_data = fd.readlines()
    total_line = len(per_line_data)
    #for test we reset the line value to 10000
    total_line = 10000
    last_date = ''
    time_start_read = get_time()
    for line in range(total_line):
        target_line_str = per_line_data[line]
        line += 1
        print('Current line',line)
        data_list = target_line_str.split()
        #The date line range list:
        #[1,233]
        #list[0] = start line
        #list[1] = end line
        if not data_list[0] in line_data_sort_by_date:
            if last_date == data_list[0]:
                continue
            else:
                if not last_date:
                    last_date = data_list[0]
                    line_data_sort_by_date[data_list[0]] = [line,line]
                    continue
                print(data_list[0])
                last_range = line_data_sort_by_date[last_date]
                last_range[1] = line - 1
            line_data_sort_by_date[data_list[0]] = [line,line]
            last_date = data_list[0]
    if last_date == data_list[0]:
            line_data_sort_by_date[data_list[0]][1] = total_line
    print('Total cost:',get_time() - time_start_read,'for read',total_line,'lines')
date_keys = list(line_data_sort_by_date.keys())
print('Found available keys:',date_keys)
#client_ip = []
#proxy_address = []
sort_by_ip = {}
if input('Do you want to choose a date? (Y/N):').lower() == 'y':
    choose = int(input('Enter the key index:'))
    lines_range = line_data_sort_by_date[date_keys[choose - 1]]
    print(lines_range)
    start_index = lines_range[0] - 1
    end_index = lines_range[1]
    lines_target = per_line_data[start_index:end_index]
    for line in lines_target:
        spilt_data = line.split()
        client_ip_s = str_split(spilt_data[2])
        proxy_address_s = str_split(spilt_data[4])
        #client_ip.append(client_ip_s)
        #proxy_address.append(proxy_address_s)
        if not client_ip_s in sort_by_ip:
            sort_by_ip[client_ip_s] = {proxy_address_s:1}
        else:
            if proxy_address_s in sort_by_ip[client_ip_s]:
                sort_by_ip[client_ip_s][proxy_address_s]+=1
            else:
                sort_by_ip[client_ip_s].update({proxy_address_s:1})
    print(sort_by_ip.keys())
    print('Done for sort process')
    print('starting second sort..')   
