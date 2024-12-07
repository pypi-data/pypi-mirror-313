# import argparse
# import csv
# from utils.decorators import pprint
# import os
# import re
# import pandas as pd
# LOG_FILE='util-cli.log'
# LOG_CATEGORY="UTILS_CLI"

# # Utility functions shared acrossed

# def open_browser(url:str=None,search:str=None)->None:
#     import webbrowser
#     if url!=None and search==None:
#         webbrowser.open_new_tab(url)
#     elif url==None and search!=None:
#         # Will loop through the JSON and open all search terms
#         # webbrowser.open_new_tab(url)
#         print("TODO.....")
#     else:
#         message="Can't open a new tab, neither URL nor search term provided"
#         print(message)
#         write_log(category=LOG_CATEGORY,message=message)

# def rest_client(url,request_body,method,iterations):
#     pass
# def check_file_dir_exists(system_path):
#     return os.path.exists(system_path)




# def parse_app_access(filepath):
#     pprint("Parsing file")
    
#     paths=get_files_path(filepath,file_prefix='app-access',ignore_extension='.csv')
    
#     for path in paths:
#         parsed_lines=[]
#         parsed_lines_no_api=[]
#         METHOD_LIST=["HEAD","GET","POST","PUT","DELETE","PATCH"]
#         with open(path,'r') as f:
#             for line in f:
#                 if re.search("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",line)!=None and line.find('.css')==-1 and line.find('.js')==-1 and line.find('.gif')==-1:
#                 # removing end line character
#                     line=line.rstrip('\n')
#                     split_text=line.split('|')
#                     if any(ele in line for ele in METHOD_LIST):
#                         text_at_index_2=split_text[2].strip()
#                         if text_at_index_2.startswith('GET') or text_at_index_2.startswith('POST') or text_at_index_2.startswith('HEAD') or text_at_index_2.startswith('PUT') or text_at_index_2.startswith('DELETE') or text_at_index_2.startswith('PATCH'):
#                             split_text.pop(2)
#                             url_split=text_at_index_2.split(' ')
#                             url_split.reverse()
#                             for text in url_split:
#                                 # with query parameters inclusive
#                                 if "?" in text:
#                                     url_query_params=text.split("?")
#                                     url_query_params.reverse()
#                                     for split_api in url_query_params:
#                                         split_text.insert(2,split_api.strip())
#                                 else:
#                                     split_text.insert(2,text)
#                             if len(url_split)==3 and len(split_text)!=11:
#                                 split_text.insert(4,"")
                
#                         parsed_lines.append(split_text)
#                     else:
#                         parsed_lines_no_api.append(split_text)
#         out_file=get_file_name_from_path(path)
#         column_header=["clientip","timestamp","method","api","query_parameters","httpprotocol_version","status","bytes","responsetime","sessionid","requestid"]
#         parsed_lines.insert(0,column_header)
#         write_csv_data(out_file,parsed_lines)
#         write_csv_data(out_file+"_irregular.csv",parsed_lines_no_api)
#         pprint(f"Completed: Parsed data written to {out_file}")

# def get_session_stats(filepath):
#     pprint("Collecting Sessions stats of files!")
#     paths=get_files_path(filepath,ignore_extension='.csv_session',file_prefix='app-access')
    
#     frames_list=[]
#     for path in paths:
#         out_file=get_file_name_from_path(path)
#         df=pd.read_csv(path)
#         session_df=df[['timestamp','sessionid']]
#         session_df=session_df[session_df['sessionid']!="-"]
#         session_df["timestamp"]=session_df["timestamp"].map(normalize_timestamp)
#         session_df[["date","hour","minute","seconds"]]=session_df["timestamp"].str.split(':',expand=True)
#         session_df.drop(["timestamp"],inplace=True,axis=1)
#         session_df["filename"]=out_file
#         frames_list.append(session_df)
#         session_df.to_csv(out_file+"_session",index=False)
#     if len(frames_list)>0:
#         master_df=pd.concat(frames_list)
#         master_df.to_csv("master_session.csv",index=False)

# def get_operations_stats(filepath):
#     pprint("Collecting Operations stats of files!")
#     paths=get_files_path(filepath,ignore_extension='.csv_session',file_prefix='app-access')
#     request_methods=["get","post",'delete','put','patch','head']
#     date_stats_data=[]
#     request_method_stats_dict={}
    
#     for path in paths:
#         df=pd.read_csv(path)
#         # get output file name
#         out_file=get_file_name_from_path(path)
#         # File data datetime statistics
#         stats_col=df.iloc[:,1]
        
#         date_stats_data.append([out_file,stats_col[0],stats_col[len(stats_col)-1]])
#         # HTTP Mehtod statistics
#         http_method_col=df.iloc[:,2]
#         request_stats_tmp_df=df.groupby('method').size().to_frame(name='count').reset_index()
#         method_counts=request_stats_tmp_df.values.tolist()
#         file_key=out_file.replace('.csv','')
#         request_method_stats_dict[file_key]={}
#         for k, v in method_counts:
#             if k.lower() in request_methods: 
#                 request_method_stats_dict[file_key][k]=v

#     if len(request_method_stats_dict)>1:
#         methods_stats=pd.DataFrame(request_method_stats_dict).T
    
#         methods_stats.reset_index(inplace=True)
#         methods_stats.rename(columns={'index':'filename'},inplace=True)
#         methods_stats.to_csv('methods_stats.csv',index=False)
import os
import pandas as pd
# from .decorators import pprint
from utils import pprint

def get_files_path(filepath:str,file_prefix:str,ignore_extension:str)->list:
    """function return list of files path from 'FILEPATH' matching the 'file_prefix', ignoring 'ignore_extension' 
    
        filepath:str - The path of single file or directory
        file_prefix:str - The file name prefix to look for example app-access.* when filepath is path to directory
        ignore_extension:str - The extension to be ignore when filepath is path to directory. Example .csv
    """
    paths=[]
    if os.path.isdir(filepath):
        files_in_directory=os.listdir(filepath)
        app_access_files=filter(lambda f: file_prefix in f and not f.endswith(ignore_extension),files_in_directory)
        paths=[os.path.join(filepath,path) for path in app_access_files]
        
    else:
        paths.append(filepath)
    return paths

def build_filename_from_path(filepath:str,extension:str="csv")->str:
    """Builds the file name from the 'filepath' appending the 'extension' 

        filepath:str - Existing filepath
        extension:str - Extension to append to new filename. defaults to csv
    """
    trace_file_name=os.path.basename(filepath)
    if extension==None:
        out_file=trace_file_name.split('.')[0]
    else:
        out_file=f"{trace_file_name.split('.')[0]}.{extension}"
    return out_file

def get_timestamp_stats_from_csv(input_dir:str,date_col_index:int,output_dir:str,output_file:str='timestamp_stats.csv',file_prefix:str=None,ignore_extension:str='.log'):
    """Get start and end date time from each parsed csv files
    
    input_dir:str - Path of input directory where to look for files
    date_col_index:int - Column index where Date/Time column is present. Example 0 or 1
    output_dir:str - Path to output directory where timestamp_stats.csv will be written
    output_file:str - Output filename
    file_prefix:str - File prefix determines which files will be parse to gather timestamp stats. Example app-access
    ignore_extension:str - The file with specified extension will be ignored in parsing, default .log.
    """
    pprint("Collecting Timestamp stats of files!")
    if os.path.exists(output_dir):
        paths=get_files_path(input_dir,ignore_extension=ignore_extension,file_prefix=file_prefix)
        # start and end of data in each file
        date_stats_headers=["filename","start_timestamp","end_timestamp"]
        date_stats_data=[]
        
        for path in paths:
            df=pd.read_csv(path)
            # get output file name
            out_file=build_filename_from_path(path)
            # File data datetime statistics
            stats_col=df.iloc[:,date_col_index]
            
            date_stats_data.append([out_file,stats_col[0],stats_col[len(stats_col)-1]])
        if len(date_stats_data)>0:
            df=pd.DataFrame(date_stats_data,columns=date_stats_headers)
            df=df.sort_values(by='filename')
            out_file=os.path.join(output_dir,output_file)
            df.to_csv(out_file,index=False)
    else:
        pprint(f"Invalid output_dir {output_dir} path")

def normalize_timestamp(value, chars=["[","]"],remove_timezone:bool=False):
    """Removes the chars i.e. '[', ']' from the value
    
    value:str - Value having special characters to be removed. Example [22/Nov/2024:01:02:36 -0600]
    chars:list(chars) - Special characters to be removed from value, default="[","]"]
    remove_timezone:bool - Removes the timezone mentioned in the date time, default=False. Example [22/Nov/2024:01:02:36 -0600] -0600 will be removed if True.
    """
    for character in chars:
        value=value.replace(character,"")
    if remove_timezone:
        value=value.split(" ")[0]
    return value
    
