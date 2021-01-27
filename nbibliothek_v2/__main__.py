import sys, os
from nbibliothek_v2.service import BibliothekService2


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


def get_lang(sysarg):
    for arg in sysarg:
        string = arg.split("-lang=")
        try:
            if string[1] == "EN":
                return "EN"
            elif string[1] == "IN":
                return "IN"

        except:
            pass
    return "IN"


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
    lang = get_lang(args)
    should_init = find_init(args)
    should_report = find_report(args)
    apps = BibliothekService2(url, lang)
    if should_init:
        apps.init_db()
    if should_report:
        apps.get_report()
    apps.run()


if __name__ == '__main__':
    main_program()
