import sys, os
from nbibliothek_v1.service import BibliothekService


def find_url(sysarg):
    project_path = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(project_path)
    for arg in sysarg:
        string = arg.split("-db:url=")
        try:
            return string[1]
        except:
            pass
    return base_dir + "\_resources\library.db"



def find_init(sysarg):
    for arg in sysarg:
        string = arg.split("-db:init=")
        try:
            if string[1] == "true":
                return True
            else:
                return False
        except:
            pass
    return False


def find_report(sysarg):
    for arg in sysarg:
        if arg == "-apps:report":
            return True
        else:
            pass
    return False


def main_program():
    args = sys.argv
    url = find_url(args)
    should_init = find_init(args)
    should_report = find_report(args)
    apps = BibliothekService(url,should_init)
    if should_init:
        apps.init_db()
    if should_report:
        apps.get_report()
    apps.run()


if __name__ == '__main__':
    main_program()
