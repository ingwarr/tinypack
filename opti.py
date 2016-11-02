#!/usr/bin/env python
import urllib2

package_list = ['wget.tcz','python-pip.tcz','unzip.tcz','sudo.tcz','mksquashfs.tcz','gawk.tcz','genisoimage.tcz','qemu.tcz','pidgin.tcz']
serv_url = "http://distro.ibiblio.org/tinycorelinux/2.x/tcz/"
suffix = ".dep"
UP_SET = set(package_list)
#UP_SET.add('mupen64plus.tcz')
DOWN_SET = set()


def file_exists(location):
    request = urllib2.Request(location)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False

def opendoor(localset):        
    DOWN_SET_LOCAL = set()
    locallist = list(localset)
    for eat_em in locallist:
        url = serv_url + eat_em + suffix
        if file_exists(url) == True:
            file_link = urllib2.urlopen(url)
            data = file_link.read()
            deps = data.split()
            for dep in deps:
                if dep not in UP_SET:
                    print dep
                    UP_SET.add(dep)
                    DOWN_SET_LOCAL.add(dep)
                    package_list.append(dep)
                else:
                    print dep,"already in UP_SET ergo deepness should be updated"
                    for index in range(len(package_list))[::-1]:
                        print package_list[index]
                        if package_list[index] == dep: 
                            delpack = package_list.pop(index)
                            package_list.append(dep)
                            DOWN_SET_LOCAL.add(dep)
        else:
            print "File not found (package", eat_em, "has no deps)"
#    print DOWN_SET_LOCAL
    return DOWN_SET_LOCAL


DOWN_SET = opendoor(UP_SET)
while not len(DOWN_SET) == 0:
    DOWN_SET = opendoor(DOWN_SET)
    



#print opendoor(DOWN_SET)            
for packname in UP_SET:
    print packname
print package_list
#print DOWN_SET
#print UP_SET.difference(DOWN_SET)

