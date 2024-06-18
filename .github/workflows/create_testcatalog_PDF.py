import json

def escape(strng):
    #\& \% \$ \# \_ \{ \}
    #~ \textasciitilde
    #^ \textasciicircum
    #\ \textbackslash
    if not isinstance(strng, str):
        return strng
    #strng = strng.replace("µ", "\mu")
    strng = strng.replace("&","\&")
    strng = strng.replace("%","\%")
    strng = strng.replace("$","\$")
    strng = strng.replace("#","\#")
    strng = strng.replace(" _ "," \_ ")
    strng = strng.replace("{","\{")
    strng = strng.replace("}","\}")
    strng = strng.replace("~", "\textasciitilde")
    strng = strng.replace("^", "\textasciicircum")
    strng = strng.replace("\\n", "\\\\")
    strng = strng.replace(" \\ ", " \textbackslash ")
    return strng

# Opening JSON file with description of all tests and return dictionary for input to latex document
json_test_file = open('testcatalog.json')
List_of_tests = json.load(json_test_file)


def create_testgroup(fp, type_id, test_group):
    # Gets a single testgroup from the dictionary created from the JSON testfile
    # then creates latex and inserts into the main file that contains the extra information
    # F-String has to be escaped hence code looks a bit ugly

    tgroup_id = escape(test_group['group_id'])
    tgroup_title = f"{type_id}.{tgroup_id}: {escape(test_group['group_name'])}"
    
    rationale = escape(test_group['rationale'])
    description = escape(test_group['description'])
    comment = escape(test_group["comment"])
    
    fp.write(f'\\section{{{tgroup_title}}}\n\n')
    fp.write(f'\\subsection*{{Rationale}}\n\n')
    fp.write(f'{rationale}\n\n')
    if description.strip() != '':
        fp.write(f'\\subsection*{{Test description}}\n\n')
        fp.write(f'{description}\n\n')
    if comment.strip() != '':
        fp.write(f'\\subsection*{{Additional information}}\n\n')
        fp.write(f'{comment}\n\n')
    fp.write('\\section*{Test within this testgroup}\n\n')

    # This section generates information on each test
    for test in test_group['tests']:
        tid = escape(f"{type_id}.{tgroup_id}.{test['test_id']}  {test['name']}")
        t_text = escape(test["description"])
        t_max_power = escape(test["max_power_w"])
        t_min_power = escape(test["min_power_w"])
        t_bands = escape(test["constellation_bands"])
        t_equipment =  escape(test["equipment"])

        fp.write(f'\\subsection{{{tid}}}\n\n')
        fp.write('\\textcolor{lightgray}{\\noindent\\rule[0.5ex]{\linewidth}{1pt} }\n')
        
        
        fp.write(f'{t_text}\n')
        fp.write(f'\\subsubsection*{{Power or power range}}\n')
        fp.write(f'Min: {t_min_power}W'+"\\\\")
        fp.write(f'Max: {t_max_power}W')
        fp.write(f'\\subsubsection*{{Test bands/constellation}}\n')
        fp.write(f'{t_bands}\n'.replace('[','').replace(']',''))
        fp.write(f'\\subsubsection*{{Transmitter equpment}}\n')
        fp.write(f'{t_equipment}\n'.replace('[','').replace(']',''))
        fp.write('\\\\')

       
def create_testtype(fp, testtype):
    type_id = escape(testtype["type_id"])
    type_name = escape(testtype["type"])
    type_title = f"{type_id} {type_name}"
    fp.write(f'\\chapter{{{type_title}}}\n\n')
    for tg in testtype["test_groups"]:
        create_testgroup(fp, type_id, tg)




# create a text file for writing
with open('./Latex/tests.tex', 'w') as fp:
    fp.write('% Content below is autogenerated \n')
    for tf in List_of_tests["test_types"]:
        create_testtype(fp, tf)
