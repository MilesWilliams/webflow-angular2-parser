#Python scrapper for scrapping webflow content

import os
import zipfile
import fnmatch
from bs4 import BeautifulSoup
import shutil


def zip_extract():

    webflow_destination = "../Webflow/"
    webflow_zip = "td-phoenix.webflow-friday.zip"
    print("Extracting zip file")
    webflow_zip = zipfile.ZipFile(webflow_destination+webflow_zip, "r")
    webflow_zip.extractall(webflow_destination)
    webflow_zip.close()
    print("Finished extracting zip file")

# zip_extract()

def parse():

    parsed_html = "./parsed_html/"
    for root, dirnames, filenames in os.walk('../Webflow'):

        if not os.path.exists(parsed_html):
            os.mkdir(parsed_html)

        for filename in fnmatch.filter(filenames, '*.html'):
            new_file = parsed_html+filename
            original_file = os.path.join(root, filename)

            os.system("cd parsed_html")

            with open(original_file) as File:
                read_file = File.read()

                if os.path.exists(new_file):
                    replace = input("Would you like to overwrite your previously parsed files? y/n\n")

                    if replace.lower() == "y":

                        files = open(new_file, 'w')
                        files.write(read_file)

                    else:
                        pass

                    pass

                else:
                    files = open(new_file, 'w')
                    files.write(read_file)

            os.system("cd ..")

# parse()

def component_builder():

    html_files = "./parsed_html"
    all_files = os.listdir(html_files)

    for files in all_files:

        with open(html_files+"/"+files, "r") as html_file:

            html_page = BeautifulSoup(html_file, 'lxml')
            component_tag = html_page.find_all("", {"component": True})

            for component in component_tag:
                component_name = component["component"]
                ts_component = component_name.capitalize()
                ts_component = ts_component.split('-')
                # ts_component.capitalize()
                ts_component = ''.join(ts_component)


                ts_content = [
                    'import { Component } from "@angular/core";\n',
                    '\n',
                    '@Component({\n',
                    '    moduleId: module.id,\n',
                    '    selector: "'+ component_name +'",\n',
                    '    templateUrl: "'+ component_name +'.component.html",\n',
                    '\n',
                    '})\n',
                    '\n',
                    'export class '+ ts_component +'Component{\n',
                    '\n',
                    '}\n'
                ]

                if os.path.exists("../Angular/app/Components/"+component_name):
                    pass
 
                else:
                    os.system("mkdir ../Angular/app/Components/"+component_name)

                if os.path.exists("../Angular/app/Components/"+component_name+"/"
                                  +component_name+".component.ts"):
                    pass

                else:

                    new_ts_file = open("../Angular/app/Components/"+component_name+"/"
                                       +component_name+".component.ts", "w")
                    for ts_line in ts_content:
                        new_ts_file.write(ts_line)


                if os.path.exists("../Angular/app/Components/"+component_name+"/"+component_name
                                  +".component.html"):

                    new_file = open("../Angular/app/Components/"+component_name+"/"+component_name
                                    +".component.html", "w")

                    component = component.prettify()

                    new_file.write(str(component))
                    # print(component)

                else:
                    new_file = open("../Angular/app/Components/"+component_name+"/"+component_name
                                    +".component.html", "w")

                    new_file.write(str(component))
                    # print(component)



    with open(html_files+"/dashboard.html", "r+") as new_html:

        new_html = BeautifulSoup(new_html, 'lxml')

        component = new_html.find_all("", {"component": True})

        for comp in component:
            prefix = "&lt;"
            last_pref = "&lt;/"
            suffix = "&gt;"
            new_component = prefix+comp["component"]+suffix+last_pref+comp["component"]+suffix
            comp.replaceWith(new_component)

            if os.path.exists("../Angular/dashboard.html"):
                os.remove("../Angular/dashboard.html")

            else:
                pass

            index = open("../Angular/dashboard.html", "w")
            html_wrapper = new_html.find_all("div", {"class": "td-app"})
            index.write(str(html_wrapper[0]))

    with open("../Webflow/dashboard.html", "r+") as index:

        index = BeautifulSoup(index, 'lxml')
        html_wrapper = index.find_all("div", {"class": "wrap"})

        for html_wrap in html_wrapper:
            html_wrap.replaceWith("<td-app></td-app>")
            new_index = open('../Angular/index2.html', 'w')
            new_index.write(str(index))
            new_index.close()

    with open('../Angular/index2.html', "r") as index_file:

        index_lines = index_file.readlines()
        angular_lines = [
            '<script src="node_modules/core-js/client/shim.min.js"></script>\n',
            '<script src="node_modules/zone.js/dist/zone.js"></script>\n',
            '<script src="node_modules/reflect-metadata/Reflect.js"></script>\n',
            '<script src="node_modules/systemjs/dist/system.src.js"></script>\n',
            '<script src="systemjs.config.js"></script>\n',
            "<script>System.import('app').catch(function(err){ console.error(err); });</script>\n"
        ]

        new_app = open('../Angular/index.html', 'w').close()
        index_lines[20:1] = angular_lines
        for lines in index_lines:
            lines = lines.replace('&lt;', '<')
            lines = lines.replace('&gt;', '>')
            new_app = open('../Angular/index.html', 'a')
            new_app.write(lines)

component_builder()

def app_component():

    with open("../Angular/dashboard.html", "r+") as app_html:
        lines = app_html.readlines()

        if os.path.exists("../Angular/app/app.component.html"):
            os.remove("../Angular/app/app.component.html")
            os.system("touch ../Angular/app/app.component.html")

        else:
            os.system("touch ../Angular/app/app.component.html")

        for line in lines:

            line = line.replace('&amp;lt;', '<')
            line = line.replace('&amp;gt;', '>')
            new_app = open('../Angular/app/app.component.html', 'a')
            new_app.write(line)



app_component()

def static_files():

    css_directory = "../Webflow/css/"
    img_directory = "../Webflow/images/"
    js_directory = "../Webflow/js/"
    angular_directory = "../Angular/app/"
    main_dir = "../Angular/"
    list_css = os.listdir(css_directory)
    list_js = os.listdir(js_directory)

    for css_files in list_css:

        new_css = angular_directory+"_build/scss/01-Tools/webflow/"+css_files
        with open(css_directory+css_files, "r") as files:

            files = files.read()
            new_css = open(new_css, 'w')
            new_css.write(files)

    for js_files in list_js:

        new_js = angular_directory+"_build/js/"+js_files
        with open(js_directory+js_files, "r") as files:

            files = files.read()
            new_js = open(new_js, 'w')
            new_js.write(files)


    new_images = main_dir
    shutil.move(img_directory, new_images)

# static_files()

def director_cleaner():

    directory = "../Webflow/*"
    print("Cleaning files")
    os.system("rm -rf " +directory)
    os.remove('../Angular/index2.html')
    os.remove('../Angular/dashboard.html')


# director_cleaner()
