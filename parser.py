import os
import zipfile
import fnmatch
import shutil
from bs4 import BeautifulSoup

def zip_extract():
    """ This function exracts the zip into the webflow directory
    """

    webflow_destination = "../Webflow/"
    webflow_zip = "td-phoenix.webflow.zip"
    print("Extracting zip file")
    webflow_zip = zipfile.ZipFile(webflow_destination+webflow_zip, "r")
    webflow_zip.extractall(webflow_destination)
    webflow_zip.close()
    print("Finished extracting zip file")

zip_extract()

def parse():
    """ This function finds all the html files in the webflow
        directory and moves them to the parsed_html directory
    """

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
                    replace = input("""Would you like to
                                    overwrite your previously parsed files? y/n\n""")

                    if replace.lower() == "y":

                        files = open(new_file, 'w')
                        files.write(read_file)

                    else:
                        pass

                else:
                    files = open(new_file, 'w')
                    files.write(read_file)

            os.system("cd ..")

parse()

def component_builder():
    """ The component builder function is the core function of this script.
        The function searches all the html files in parsed_html, it then look for each
        component data attribute, it then extracts the html and creates angular name.component.ts
        and name.component.html files each within their own directory with in the Component
         directory.The function then builds the index.html file and and inserts the angular base
          script links.
    """

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
        css_scripts = index.find_all("link", {"rel":"stylesheet"})

        for html_wrap in html_wrapper:
            html_wrap.replaceWith('<base href="/">\n<td-app></td-app>')
            new_index = open('../Angular/index2.html', 'w')
            new_index.write(str(index))
            new_index.close()

        for css_script in css_scripts:
            css_script.replaceWith("")
            new_index = open('../Angular/index2.html', 'w')
            new_index.write(str(index))
            new_index.close()

    with open('../Angular/index2.html', "r") as index_file:

        index_lines = index_file.readlines()

        for elem in index_lines:
            if elem.find('</head>') > -1:
                insert_num = index_lines.index(elem)


        angular_lines = [
            '<link href="styles.css" rel="stylesheet">\n',
            '<script src="node_modules/core-js/client/shim.min.js"></script>\n',
            '<script src="node_modules/zone.js/dist/zone.js"></script>\n',
            '<script src="node_modules/systemjs/dist/system.src.js"></script>\n',
            '<script src="systemjs.config.js"></script>\n',
            "<script>System.import('app').catch(function(err){ console.error(err); });</script>\n"
        ]

        new_app = open('../Angular/index.html', 'w').close()
        index_lines[insert_num:1] = angular_lines
        for lines in index_lines:
            lines = lines.replace('&lt;', '<')
            lines = lines.replace('&gt;', '>')
            new_app = open('../Angular/index.html', 'a')
            new_app.write(lines)

component_builder()

def app_component():
    """ The App Component function opens and reads the dashboard.html, parses it into
         a app.component.html file. As this is being done, the script replaces the
          <div class="td-router-outlet w-embed"></div> with <router-outlet></router-outlet>
           and removes <page-dashboard></page-dashboard>
     """

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
            line = line.replace('<div class="td-router-outlet w-embed"></div>',
                                '<router-outlet></router-outlet>')
            line = line.replace('<page-dashboard></page-dashboard>', '')
            new_app = open('../Angular/app/app.component.html', 'a')
            new_app.write(line)

app_component()


def static_files():
    """ This script moves all css files, images and js files from webflow
     to the angular _build folder except images which goes to the root
      directory
    """

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

    angular_image = main_dir + 'images'
    if os.path.exists(angular_image):
        remove_image_q = input("""Image folder exists,
                                 would youlike to replace with the new image folder? y/n \n""")

        if remove_image_q.lower() == 'y':
            shutil.rmtree(angular_image)
            new_images = main_dir
            shutil.move(img_directory, new_images)

        else:
            pass

static_files()

def router_creator():
    """ This function serves in gathering all the necessary info for the
         path_creator() function, and provides the initial data clean.
    """

    html_files = "./parsed_html"
    all_files = os.listdir(html_files)

    function_start = "const AppRoutes: Routes = ["
    function_end = """]\n \nexport const routing:
                     ModuleWithProviders = RouterModule.forRoot(AppRoutes);"""

    file_start = open('./Path/route.start.ts', 'w')
    file_start.write("")
    file_start.close()
    file_start = open('./Path/route.start.ts', 'a')
    file_start.truncate()
    file_start.write(function_start)

    file_end = open('./Path/route.end.ts', 'w')
    file_end.write("")
    file_end.close()
    file_end = open('./Path/route.end.ts', 'a')
    file_end.write(function_end)
    file_import = open('./Path/route.import.ts', 'w')
    file_import.write("")
    file_import.close()
    file_content = open('./Path/route.content.ts', 'w')
    file_content.write("")
    file_content.close()
    path_content = open('./Path/path.content.ts', 'a')
    path_content.write("")
    path_content.close()
    for files in all_files:

        with open(html_files+"/"+files, "r") as html_file:

            html_page = BeautifulSoup(html_file, "lxml")
            find_link = html_page.find_all("", {"route-to": True})
            href = html_page.find_all("a", {"href": True})

            for link in find_link:
                component = link["route-to"]
                component_name = component.capitalize().split("-")
                component_name = "".join(component_name)
                component_name = component_name+"Component"

                href = link["href"]
                href = href.rsplit(".", 1)[0]
                href = href.rsplit("..", 1)

                href = "".join(href)

                ts_import = 'import { '+ component_name +' } from "./Components/'+component+'/'+component+'.component";\n',
                ts_content = '   {\n       path:"' + href + '",\n       component:'+ component_name+'\n   },\n'

                for imp in ts_import:
                    file_import = open('./Path/route.import.ts', 'a')
                    file_import.write(imp)
                    file_import.close()

                file_content = open('./Path/route.content.ts', 'a')
                path_content = open('./Path/path.content.ts', 'a')

                flattened_list = []
                path_list = []
                flattened_list.append(component)
                path_list.append(href)

                print(path_list)

                for i in flattened_list:
                    i = i.capitalize()
                    file_content.write(i+"Component")
                    file_content.write("\n")

                for path in path_list:
                    path_content.write(path)
                    path_content.write("\n")



# router_creator()

def path_creator():
    """ This function serves in creating the app.routes.ts file
         and dynamicall adding all components and their paths.
    """

    file_start = open('./Path/route.start.ts', 'r')
    file_end = open('./Path/route.end.ts', 'r')
    file_import = open('./Path/route.import.ts', 'r')
    file_content = open('./Path/route.content.ts', 'r')
    file_path = open('./Path/path.content.ts', 'r')
    path_file = open('./Path/app.route.ts', "a")

    with open('./Path/app.route.ts', "r+") as path_file:
        path_file.truncate()
        path_file.write("""import { ModuleWithProviders} from '@angular/core';\n
                        import { Routes, RouterModule } from '@angular/router';\n""")
        imports = file_import.readlines()
        s = []
        for port in imports:

            if port not in s:
                s.append(port)

        for i in s:
            path_file.write(i)

        function_start = file_start.read()
        path_file.write("\n"+function_start)

        path_contents = file_content.readlines()
        path_hrefs = file_path.readlines()

        path = []
        lines = []

        for href in path_hrefs:

            if href not in path:
                href = str(href)
                if href.startswith("/"):
                    pass
                if href == "#":
                    pass

                if not href.startswith("/") and not href.startswith("#"):
                    path.append(href)

        print(path)

        for contents in path_contents:

            if contents not in lines:
                lines.append(contents)

        for line, h in zip(lines, path):
            h = h.strip("\n")
            line = line.split('-')
            line = "".join(line)
            line = line.strip("\n")
            path_file.write("\n    {\n    path: '"+ h +"',\n    component:'"+ line +"'\n    },")

        function_end = file_end.read()
        path_file.write("\n"+function_end)



def router_link():
    """ The router link function reads all the html files in components
        searching for all a tags with the route-to data attribute.
        The script then adds a [routerLink] = ['href value] and removes the href.
     """

    html_files = "../Angular/app/Components/"

    for root, dirnames, filenames in os.walk(html_files):

        for filename in fnmatch.filter(filenames, '*.html'):
            original_file = os.path.join(root, filename)

            with open(original_file, "r+") as component_files:

                read_file = component_files.readlines()
                over_write = open(original_file, "w")
                over_write.write("")
                over_write.close()
                append_write = open(original_file, "a")
                for lines in read_file:
                    a_filter = "route-to"
                    # if check is True:
                    if a_filter in lines:
                        soup = BeautifulSoup(lines, "lxml")
                        href = soup.find_all("a", {"href": True})

                        for h in href:
                            h_url = h["href"]
                            striped_url = h_url.strip('..')
                            striped_url = striped_url.strip('html')
                            striped_url = striped_url.strip('.')
                            striped_url = striped_url.replace("/dashboard", "/")
                            tracker = "['"+striped_url +"']"

                        print(lines)
                        route = '[routerLink]='+'"'+tracker+'"'
                        split_line = lines.split('href="'+h_url+'"')
                        split_line = route.join(split_line)
                        lines = lines.replace(str(h), split_line)

                        print(split_line)
                        append_write.write(split_line)

                    else:
                        print(lines)
                        append_write.write(lines)

router_link()

def directory_cleaner():
    """ This function cleans the angular app directory of all the files created
         by all the other functions that are no longer needed.
     """

    directory = "../Webflow/*"
    print("Cleaning files")
    os.system("rm -rf " +directory)
    os.remove('../Angular/index2.html')
    os.remove('../Angular/dashboard.html')

# directory_cleaner()
