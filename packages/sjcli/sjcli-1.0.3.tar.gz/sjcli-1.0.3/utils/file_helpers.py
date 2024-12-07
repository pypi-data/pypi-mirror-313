import csv
import json
from tabulate import tabulate
from itertools import islice
from .enums import TableFormat

LOG_FILE='util-cli.log'
LOG_CATEGORY="UTILS_CLI"

def write_log(category:str,message:str,log_file:str=LOG_FILE)->None:
    """Write log file of the CLI"""
    with open(log_file,'a') as f:
        print("{}: {}".format(category,message),file=f, end='\n')

def write_csv_data(csv_file_path:str,data:list)->None:
    """Write CSV output to the working directory"""
    status_code=0
    try:
        with open(csv_file_path,'w') as f:
            csv_h=csv.writer(f,doublequote=False)
            csv_h.writerows(data)
    except Exception as e:
        write_log("ERROR",e)
        status_code=-1
    return status_code


def preview_json(file_name:str,first_n:int=None,indent:int=2)->str:
    with open(file_name) as f:
        data=json.load(f)
    formatted_data=json.dumps(data,indent=indent)
    if indent==0:
        result=formatted_data.replace("\n","")
    else:
        formatted_data=formatted_data.split("\n")
        if first_n:
            formatted_data=formatted_data[:first_n]
        result="\n".join(formatted_data)
    return result


def preview_csv(
    file_name: str,
    first_n: int = None,
    has_header_row: bool = False,
    table_format: TableFormat = TableFormat.fancy_outline,
) -> str:
    with open(file_name) as f:
        data = csv.reader(f)

        if has_header_row:
            headers = next(data)
        else:
            headers = None

        if first_n:
            rows = list(islice(data, first_n))
        else:
            rows = list(data)
    if headers:
        return tabulate(rows, headers=headers, tablefmt=table_format.value)
    else:
        return tabulate(rows)

if __name__=="__main__":
    write_csv_data('/Users/sj652744/Documents/saurabh/projects/python-cli/sjcli/tests/mocks/test.csv',[])