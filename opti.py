#!/usr/bin/env python
import urllib2

package_list = ['wget.tcz', 'python-pip.tcz', 'unzip.tcz', 'sudo.tcz',
                'mksquashfs.tcz', 'gawk.tcz', 'genisoimage.tcz', 'qemu.tcz',
                'pidgin.tcz']
serv_url = "http://distro.ibiblio.org/tinycorelinux/2.x/tcz/"
suffix = ".dep"
UP_SET = set(package_list)
deepness = 0


def file_exists(location):
    request = urllib2.Request(location)
    request.get_method = lambda: 'HEAD'
    try:
        urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False


def opendoor(localset):
    print (deepness)
    DOWN_SET_LOCAL = set()
    locallist = list(localset)
    for eat_em in locallist:
        url = serv_url + eat_em + suffix
        if file_exists(url):
            file_link = urllib2.urlopen(url)
            data = file_link.read()
            deps = data.split()
            for dep in deps:
                if dep not in UP_SET:
                    UP_SET.add(dep)
                    DOWN_SET_LOCAL.add(dep)
                    package_list.append(dep)
                elif dep not in DOWN_SET_LOCAL:
                    print (dep, " already in UP_SET ergo deepness should be"
                                "increased, now it ", deepness, " level")
                    package_list.remove(dep)
                    package_list.append(dep)
                    DOWN_SET_LOCAL.add(dep)
                else:
                    print ("This package", dep, " already processed")
        else:
            print ("File not found (package", eat_em, "has no deps)")

    return DOWN_SET_LOCAL


DOWN_SET = opendoor(UP_SET)
while not len(DOWN_SET) == 0:
    deepness += 1
    DOWN_SET = opendoor(DOWN_SET)

for packname in UP_SET:
    print (packname)
print (package_list[::-1])
