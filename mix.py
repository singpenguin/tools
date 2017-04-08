#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import subprocess

def main(path, fname):
    # fname: framework name. eg: tornado 
    if path[-1] == "/":
        return "project name invalid"

    project_root = path
    if path[0] != "/":
        project_root = "%s/%s" % (os.path.abspath("."), path)

    r = subprocess.Popen(["which", "git"], stdout=subprocess.PIPE)
    res, err = r.communicate()
    if res:
        subprocess.Popen(["git", "init", project_root], stdout=subprocess.PIPE).wait()
    else:
        os.mkdir(project_root)
    name = project_root.split("/")[-1]
    for fp, is_folder, content in folder_structure(name):
        if is_folder:
            os.mkdir("%s/%s" % (project_root, fp))
        else:
            with open("%s/%s" % (project_root, fp), "w") as f:
                f.write(content)
                f.close()
    print(green("project %s create done" % name))
    if fname == "tornado":
        with open(project_root + "/config/url.py", "a+") as f:
            f.write("""\nfrom controllers import page\n""")
            f.write("""\nurls=[\n    ("/", page.Index)\n]""")
            f.close()
        with open(project_root + "/config/settings.py", "a+") as f:
            f.write("""\ncookie_secret = ')#@a(750mv)cn&#@c#^y%52-pof*w%)ba%w5kd1*u0k=28&^$)'\ndebug=True\n""")
            f.close()
        with open(project_root + "/controllers/page.py", "w") as f:
            f.write(_common_header())
            f.write("""\nimport tornado.web\n""")
            f.write("""
class Index(tornado.web.RequestHandler):
    def get(self):
        return self.write("Hello World")
            """.strip())
            f.close()
        with open(project_root + "/index.py", "a+") as f:
            f.write("\n")
            f.write("""
import os
import tornado
import tornado.wsgi
from config import settings, url


application = tornado.web.Application(handlers=url.urls, cookie_secret=settings.cookie_secret,
                                    debug=settings.debug, xsrf_cookie=True,
                                    static_path=os.path.join(os.path.abspath("."), "static"))

if __name__ == "__main__":
    port = 8080
    application.listen(port)
    print("http://localhost:%s" % port)
    tornado.ioloop.IOLoop.instance().start()
            """.strip())
        print(green("init tornado project"))
        return

def _common_header():
    h = """
#!/usr/bin/env python
# -*- coding:utf-8 -*-
    """
    return h.strip()

def folder_structure(name):
    #path, is_folder, content
    ignore = ["*.pyc", ".DS_Store", "__pycache__/", "*.db", "*.swp",
            "*.so", "*.egg", "*.egg-info/", "celerybeat-schedule"]
    f = [("README.md", False, "## %s" % name),
        (".gitignore", False, "\n".join(ignore)),
        ("index.py", False, _common_header()),
        ("config", True, ""),
        ("config/__init__.py", False, ""),
        ("config/settings.py", False, _common_header()),
        ("config/url.py", False, _common_header()),
        ("controllers", True, ""),
        ("controllers/__init__.py", False, ""),
        ("models", True, ""),
        ("models/__init__.py", False, ""),
        ("common", True, ""),
        ("common/__init__.py", False, ""),
        ("common/utils.py", False, _common_header()),
        ("backend", True, ""),
        ("backend/__init__.py", False, ""),
        ("static", True, ""),
        ("tests", True, ""),
        ("templates", True, ""),
        ("requirements.txt", False, "")]
    return f

def green(text):
    return "\033[32m%s\033[0m" % text

if __name__ == '__main__':
    param_num = len(sys.argv)
    if param_num >= 2:
        path = sys.argv[1]
        if param_num >= 3:
            framework_name = sys.argv[2]
        else:
            framework_name = ""
        main(path, framework_name)
