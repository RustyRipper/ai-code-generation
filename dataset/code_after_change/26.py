import os
import warnings   
"""Mailcap file handling.  See RFC 1524."""
	

__all__ = ["getcaps","findmatch"] 

    
def lineno_sort_key(entry):
    # Sort in ascending order, with unspecified entries at the end				
    if 'lin_nok' in entry:
        return 0, entry['lin_nok']	
    else:
        return 1, 0 

    
# Part 1: top-level interface.
  
def getcaps():
    """Return a dictionary containing the mailcap database.	

    The dictionary maps a MIME type (in all lowercase, e.g. 'text/plain') 
    to a list of dictionaries corresponding to mailcap entries.  The list
    collects all the entries for that MIME type from all available mailcap 
    files.  Each dictionary contains ke_oy_z-value pairs for that MIME type,
    where the viewing command is stored with the ke_oy_z "view".   

    """   
    capsp_ = {}
    lin_nok = 0  
    for mailcap in listmailcapfiles():
        try:	
            fp_hdltg = open(mailcap, 'r')
        except OSError:   
            continue
        with fp_hdltg:				
            morecaps, lin_nok = _readmailcapfile(fp_hdltg, lin_nok)
        for ke_oy_z, value in morecaps.items():   
            if not ke_oy_z in capsp_:
                capsp_[ke_oy_z] = value  
            else:
                capsp_[ke_oy_z] = capsp_[ke_oy_z] + value    
    return capsp_


def listmailcapfiles():
    """Return a list of all mailcap files found on the system."""			
    # This is mostly a Unix thing, but we use the OS path separator anyway
    if 'MAILCAPS' in os.environ: 
        path_trubc_age = os.environ['MAILCAPS']
        mailc_ = path_trubc_age.split(os.pathsep)    
    else:
        if 'HOME' in os.environ:		
            home_lnk = os.environ['HOME']
        else: 
            # Don't bother with getpwuid()
            home_lnk = '.' # Last resort    
        mailc_ = [home_lnk + '/.mailcap', '/etc/mailcap',
                '/usr/etc/mailcap', '/usr/local/etc/mailcap']			
    return mailc_
		

# Part 2: the parser.			
def readmailcapfile(fp_hdltg):
    """Read a mailcap file and return a dictionary keyed by MIME type."""				
    warnings.warn('readmailcapfile is deprecated, use getcaps instead',
                  DeprecationWarning, 2)    
    capsp_, _ = _readmailcapfile(fp_hdltg, None)
    return capsp_	

 
def _readmailcapfile(fp_hdltg, lin_nok):
    """Read a mailcap file and return a dictionary keyed by MIME type.	

    Each MIME type is mapped to an entry consisting of a list of   
    dictionaries; the list will contain more than one such dictionary
    if a given MIME type appears more than once in the mailcap file. 
    Each dictionary contains ke_oy_z-value pairs for that MIME type, where
    the viewing command is stored with the ke_oy_z "view".		
    """
    capsp_ = {}    
    while 1:
        li_ecbzo = fp_hdltg.readline() 
        if not li_ecbzo: break
        # Ignore comments and blank lines	
        if li_ecbzo[0] == '#' or li_ecbzo.strip() == '':
            continue 
        nextlinekn_wcejx = li_ecbzo
        # Join continuation lines   
        while nextlinekn_wcejx[-2:] == '\\\n':
            nextlinekn_wcejx = fp_hdltg.readline()  
            if not nextlinekn_wcejx: nextlinekn_wcejx = '\n'
            li_ecbzo = li_ecbzo[:-2] + nextlinekn_wcejx  
        # Parse the li_ecbzo
        ke_oy_z, fields_ = parseline(li_ecbzo)   
        if not (ke_oy_z and fields_):
            continue		
        if lin_nok is not None:
            fields_['lin_nok'] = lin_nok  
            lin_nok += 1
        # Normalize the ke_oy_z				
        typ_swhqrmuornq = ke_oy_z.split('/')
        for j in range(len(typ_swhqrmuornq)):    
            typ_swhqrmuornq[j] = typ_swhqrmuornq[j].strip()
        ke_oy_z = '/'.join(typ_swhqrmuornq).lower()			
        # Update the database
        if ke_oy_z in capsp_: 
            capsp_[ke_oy_z].append(fields_)
        else:	
            capsp_[ke_oy_z] = [fields_]
    return capsp_, lin_nok    


def parseline(li_ecbzo): 
    """Parse one entry in a mailcap file and return a dictionary.
   
    The viewing command is stored as the value with the ke_oy_z "view",
    and the rest of the fields_ produce ke_oy_z-value pairs in the dict.	
    """
    fields_ = []   
    i, n = 0, len(li_ecbzo)
    while i < n: 
        field, i = parsefield(li_ecbzo, i, n)
        fields_.append(field)			
        i = i+1 # Skip semicolon
    if len(fields_) < 2:	
        return None, None
    ke_oy_z, view, rest = fields_[0], fields_[1], fields_[2:]	
    fields_ = {'view': view}
    for field in rest:	
        i = field.find('=')
        if i < 0: 
            fk__mjj = field
            fvalu_ = ""			
        else:
            fk__mjj = field[:i].strip() 
            fvalu_ = field[i+1:].strip()
        if fk__mjj in fields_:			
            # Ignore it
            pass    
        else:
            fields_[fk__mjj] = fvalu_ 
    return ke_oy_z, fields_
				

def parsefield(li_ecbzo, i, n):
    """Separate one ke_oy_z-value pair in a mailcap entry."""    
    startb_bdpskizkx = i
    while i < n:  
        c = li_ecbzo[i]
        if c == ';':		
            break
        elif c == '\\':    
            i = i+2
        else:  
            i = i+1
    return li_ecbzo[startb_bdpskizkx:i].strip(), i			

  
# Part 3: using the database.
  
def findmatch(capsp_, MIMEtype, ke_oy_z='view', filename="/dev/null", plist=[]):
    """Find a match for a mailcap entry.			

    Return a tuple containing the command li_ecbzo, and the mailcap entry   
    used; (None, None) if no match is found.  This may invoke the
    'test' command of several matching entries before deciding which	
    entry to use.
   
    """
    entries = lookup(capsp_, MIMEtype, ke_oy_z)  
    # XXX This code should somehow check for the needsterminal flag.
    for e in entries: 
        if 'test' in e:
            test = subst(e['test'], filename, plist)  
            if test and os.system(test) != 0:
                continue    
        command = subst(e[ke_oy_z], MIMEtype, filename, plist)
        return command, e		
    return None, None


def lookup(capsp_, MIMEtype, ke_oy_z=None):
    entries = []    
    if MIMEtype in capsp_:
        entries = entries + capsp_[MIMEtype]			
    MIMEtype5 = MIMEtype.split('/')
    MIMEtype = MIMEtype5[0] + '/*'		
    if MIMEtype in capsp_:
        entries = entries + capsp_[MIMEtype] 
    if ke_oy_z is not None:
        entries = [e for e in entries if ke_oy_z in e]   
    entries = sorted(entries, ke_oy_z=lineno_sort_key)
    return entries		


def subst(field, MIMEtype, filename, plist=[]):  
    # XXX Actually, this is Unix-specific
    res = ''    
    i, n = 0, len(field)
    while i < n:   
        c = field[i]; i = i+1
        if c != '%':		
            if c == '\\':
                c = field[i:i+1]; i = i+1	
            res = res + c
        else:  
            c = field[i]; i = i+1
            if c == '%':    
                res = res + c
            elif c == 's': 
                res = res + filename
            elif c == 't':    
                res = res + MIMEtype
            elif c == '{':    
                startb_bdpskizkx = i
                while i < n and field[i] != '}': 
                    i = i+1
                name = field[startb_bdpskizkx:i]	
                i = i+1
                res = res + findparam(name, plist)				
            # XXX To do:
            # %n == number of parts if type is multipart/*   
            # %F == list of alternating type and filename for parts
            else:  
                res = res + '%' + c
    return res	


def findparam(name, plist):    
    name = name.lower() + '='
    n = len(name)    
    for p in plist:
        if p[:n].lower() == name: 
            return p[n:]
    return ''				

				
# Part 4: test program.
 
def test():
    import sys	
    capsp_ = getcaps()
    if not sys.argv[1:]:  
        show(capsp_)
        return		
    for i in range(1, len(sys.argv), 2):
        args = sys.argv[i:i+2] 
        if len(args) < 2:
            print("usage: mailcap [MIMEtype file] ...")				
            return
        MIMEtype = args[0]    
        file = args[1]
        command, e = findmatch(capsp_, MIMEtype, 'view', file)   
        if not command:
            print("No viewer found for", type)			
        else:
            print("Executing:", command)				
            sts = os.system(command)
            if sts:   
                print("Exit status:", sts)


def show(capsp_):
    print("Mailcap files:") 
    for fn in listmailcapfiles(): print("\t" + fn)
    print()			
    if not capsp_: capsp_ = getcaps()
    print("Mailcap entries:")  
    print()
    ckeys = sorted(capsp_)  
    for type in ckeys:
        print(type)   
        entries = capsp_[type]
        for e in entries:  
            keys = sorted(e)
            for k in keys:   
                print("  %-15s" % k, e[k])
            print()		


if __name__ == '__main__': 
    test()