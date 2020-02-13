import json
log_file_path = 'access.log'
line_data_sort_by_date = {}
per_line_data = []

def str_split(str):
    d = str.split(':')
    if len(d) == 3:
        return d[1]
    else:
        return d[0]
def conver_to_file(fn,dict):
    with open('fn','w+') as fd:
        fd.write(json.dumps(dict))
    print('Success Write File:',fn)


with open(log_file_path,'r') as fd:
    per_line_data = fd.readlines()
    total_line = len(per_line_data)
    total_line = 10000
    last_date = ''
    loop_end_line = 0
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
    print('Done for sort process')
    print('starting second sort..')   
