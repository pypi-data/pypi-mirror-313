from .color import color
from .logger import log

def changelogs():
# Log the latest update version

    log(f"{color('Lumtina', 'red')} Latest Update: 0.2.6")

# Log the changes made in this version
    log(f'''{color('Lumtina', 'red')} Added:
 [ + ] Added a new hosting for your websites! ( host_website() )
 [ + ] Modified some functions
    ''')

    log(f"{color('Lumtina', 'red')} Previous Update: 0.2.5")

# Log the changes made in this version
    log(f'''{color('Lumtina', 'red')} Added:
 [ + ] Added new file utils ( delete_file, copy_file, move_file )
 [ + ] Added new Network Utils ( ping_host, get_ip_info, get_local_ip )
 [ + ] Modified the README
 [ - ] Fixed Bugs
    ''')




