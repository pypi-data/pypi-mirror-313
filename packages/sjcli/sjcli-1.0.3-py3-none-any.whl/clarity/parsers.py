import re
from utils import pprint, get_files_path,build_filename_from_path,write_csv_data
import os

def parse_app_access(filepath:str,output_dir:str,file_prefix:str="app-access",ignore_extension:str=".csv"):
    """Parses app-access log/logs from filepath either app-access log file or directory containing such files.
    
    filepath:str - The path to app-access log file or directory containing those files.
    output_dir:str - The output directory where to generate the parsed files.
    file_prefix:str - The file prefix to search in directory which need to be parsed, default=app-access.
    ignore_extension:str - The file extension to be ignored for parsing, default=.csv.
    """
    pprint("Parsing file/s")
    
    paths=get_files_path(filepath,file_prefix=file_prefix,ignore_extension=ignore_extension)
    total_ouput=[]
    for path in paths:
        parsed_lines=[]
        parsed_lines_no_api=[]
        other_lines=[]
        METHOD_LIST=["HEAD","GET","POST","PUT","DELETE","PATCH"]
        with open(path,'r') as f:
            for line in f:
                if re.search("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",line)!=None and line.find('.css')==-1 and line.find('.js')==-1 and line.find('.gif')==-1:
                # removing end line character
                    line=line.rstrip('\n')
                    split_text=line.split('|')
                    if any(ele in line for ele in METHOD_LIST):
                        text_at_index_2=split_text[2].strip()
                        if text_at_index_2.startswith('GET') or text_at_index_2.startswith('POST') or text_at_index_2.startswith('HEAD') or text_at_index_2.startswith('PUT') or text_at_index_2.startswith('DELETE') or text_at_index_2.startswith('PATCH'):
                            split_text.pop(2)
                            url_split=text_at_index_2.split(' ')
                            url_split.reverse()
                            for text in url_split:
                                # with query parameters inclusive
                                if "?" in text:
                                    url_query_params=text.split("?")
                                    url_query_params.reverse()
                                    for split_api in url_query_params:
                                        split_text.insert(2,split_api.strip())
                                else:
                                    split_text.insert(2,text)
                            if len(url_split)==3 and len(split_text)!=11:
                                split_text.insert(4,"")
                
                        parsed_lines.append(split_text)
                    else:
                        parsed_lines_no_api.append(split_text)
                else:
                    line=line.rstrip("\n")
                    split_text=line.split("|")
                    other_lines.append(split_text)

        if len(parsed_lines)>0 or len(parsed_lines_no_api)>0:
            out_file=build_filename_from_path(filepath=path,extension=None)
            column_header=["clientip","timestamp","method","api","query_parameters","httpprotocol_version","status","bytes","responsetime","sessionid","requestid"]
            parsed_lines.insert(0,column_header)
            output_files=[
                os.path.join(output_dir,out_file+".csv"),
                os.path.join(output_dir,out_file+"_non_api.csv"),
                os.path.join(output_dir,out_file+"_others.csv")

            ]
            write_csv_data(output_files[0],parsed_lines) if len(parsed_lines)>0 else None
            write_csv_data(output_files[1],parsed_lines_no_api) if len(parsed_lines_no_api)>0 else None
            write_csv_data(output_files[2],other_lines) if len(other_lines)>0 else None
            pprint(f"Completed: Parsed data written to {output_files}")
        else:
            pprint(f"No data matching criteria to parse in file {path}")

if __name__=="__main__":
    print("Clarity Module")