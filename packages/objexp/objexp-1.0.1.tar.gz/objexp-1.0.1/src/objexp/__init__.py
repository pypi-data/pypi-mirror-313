import re
import json

def typename_analyzer(type_str):
    typical_type = [
        "function",
        "int",
        "float",
        "bool",
        "str",
        "list",
        "dict",
        "set",
        "tuple",
        "module",
        "type",
        "builtin_function_or_method",
    ]
    
    magic_method = [

    ]

resjson = {
    "objname":"",
    "objitms":[]
}


def ox(someobj="test", savefile = None, ifprint = True):
    """
    savefile: "md", "json", None
    ifprint: True, False
    """
    
    result_content_text = "\n"
    result_content_text += "_________________________\n"
    result_content_text += "\n"+str(type(someobj))+"\n"
    result_content_text += "\n"+str(someobj)+"\n"
    result_content_text += "_________________________\n"

    resjson["objname"]=str(someobj)

    print(result_content_text) if ifprint else None

    dirlist = dir(someobj)

    dirResult_sorted = sorted(
        dirlist, 
        key=lambda x: str(type(getattr(someobj,x)))
        )


    previous_type_str = ""
    dirjson = []
    atypeitm = []
    
    
    for objitem in dirResult_sorted:
        current_type_str = str(type(getattr(someobj,objitem)))

        if (previous_type_str != current_type_str):

            dirjson.append([current_type_str,[]])
            
            previous_type_str = current_type_str

        dirjson[-1][1].append(objitem)

    resjson["objitms"]=dirjson

    for iii in dirjson:
        
        content_title_typename = iii[0]
        result_content_text += "\n"+content_title_typename+"\n"
        print(content_title_typename) if ifprint else None
        
        content_objs_list = ""
        for jjj in iii[1]:
            content_objs_list += jjj + ", "
            
        print(content_objs_list + "\n") if ifprint else None
        result_content_text += content_objs_list + "\n"

    if savefile == "md" or savefile == "both":
        with open("objexp-"+savefile+".md",'w', encoding="UTF-8") as ff:
            ff.write(result_content_text)

    if savefile == "json" or savefile == "both":
        with open("objexp-"+savefile+".json",'w', encoding="UTF-8") as ff:
            ff.write(json.dumps(resjson))
    
    return result_content_text


# vars() is alternative to dirs()
if False:
    vvv = vars().copy()
    for kk,vv in vvv.items():
        print(kk,type())
        
if __name__=="__main__":
    print("__main__ test!")