#!/usr/bin/env python
# coding: utf-8
import os
import pip

package_name="easypv"

package_names=package_name+".py"



current_directory =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:60
file_path = os.path.join(current_directory, package_names)

if current_directory=="":
    csdir =str (os .path .dirname (__file__ ))#
    #print(csdir)
    csdir =csdir +csdir.split (package_name)[0 ][-1 ]#
    file_path = csdir+package_names
    #print(file_path)
    os.system(f"python {file_path}")
else:
    os.system(f"python {file_path}")

