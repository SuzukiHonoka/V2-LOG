#json_dumps used for save dict file
from json import dumps as json_dumps
#json_loads used for parse json and conver to dict format
from json import loads as json_loads
#get_time used for get the current system time
from time import time as get_time
#request used for open a url and get some required data
from urllib import request
#path_exists used for check if path exist
from os.path import exists as path_exists

#log file path
log_file_path = 'access.log'
#ip info cache file path
ip_info_cache_path = 'ips.info'
#temp store the ips info to mem
ips_info_cache = {}
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
ipstack_str2 = '&language=en'
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
    print('Get Info for IP:',ip)
    ips_format = ''
    if type(ip) == list:
        for per_ip in ip:
            ips_format += ',' + per_ip
    else:
        ips_format = ip
        
    r_url = ipstack_api + ips_format + ipstack_str1 + ipstack_key + ipstack_str2
    r = request.urlopen(r_url)
    if r.getcode() == 200:
        rd = r.read().decode('utf-8')
        return json_loads(rd)
 
#get difference between two list
def list_dif(li1,li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    li_fae = []
    if len(li_dif) != 0:
        for li_a in li_dif:
            if li_a in li2:
                li_fae.append(li_a)
    return li_fae

#simple write/read
def rw(path,mode,data=None):
    r = 'r'
    w = 'w'
    if mode == r:
        with open(path,r) as fd:
            res = fd.read()
            print('Read:',path)
            return res
    elif mode == w:
        with open(path,w) as fd:
            fd.write(data)
            print('Written:',path)

#temp ip info cache

def update_ip_info_cache(l_ips_info):
    global ips_info_cache
    if not path_exists(ip_info_cache_path):
        rw(ip_info_cache_path,'w',json_dumps(l_ips_info))
       # with open(ip_info_cache_path,'w') as fd:
      #      fd.write(json_dumps(l_ips_info))
        print('IPS Created.')
    else:
        res = rw(ip_info_cache_path,'r')
        l_ips = list(l_ips_info.keys())
        o_ips = list(ips_info_cache.keys())
        d_ips = list_dif(o_ips,l_ips)
        print(o_ips,l_ips)
        if len(d_ips) != 0:
            print('Add IPS List:',d_ips)
            for un_met in d_ips:
                ips_info_cache[un_met] = l_ips_info[un_met]
                rw(ip_info_cache_path,'w',json_dumps(ips_info_cache))
                print('IPS Updated')
        else:
            print('IPS is up to date')

def setup_ip_info_cache():
    global ips_info_cache
    if path_exists(ip_info_cache_path):
        print('Starting to read old IPS')
        res = rw(ip_info_cache_path,'r')
        if len(res) != 0:
            ips_info_cache = json_loads(res)
            print('IPS:',list(ips_info_cache.keys()))
setup_ip_info_cache()
with open(log_file_path,'r') as fd:
    per_line_data = fd.readlines()
    total_line = len(per_line_data)
    #for test we reset the line value to 10000
    total_line = 10000
    last_date = ''
    time_start_read = get_time()
    print('Starting read line process')
    for line in range(total_line):
        target_line_str = per_line_data[line]
        line += 1
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
                last_range = line_data_sort_by_date[last_date]
                last_range[1] = line - 1
            line_data_sort_by_date[data_list[0]] = [line,line]
            last_date = data_list[0]
    if last_date == data_list[0]:
            line_data_sort_by_date[data_list[0]][1] = total_line
    print('Total read line:',total_line)
    print('Total cost:',get_time() - time_start_read,'for read',total_line,'lines')
date_keys = list(line_data_sort_by_date.keys())
print('Found available keys:',date_keys)
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
    print('Done for sort process')
    print('starting second sort..')
    proxy_address = []
    client_ip = list(sort_by_ip.keys())

    ips_info = {}
    for per_ip in client_ip:
        if per_ip in ips_info_cache:
            print('IP included in IPS:',per_ip)
            continue
        ips_info[per_ip] = get_ip_info(per_ip)
        update_ip_info_cache(ips_info)
        
#print(get_ip_info('1.1.1.1'))
