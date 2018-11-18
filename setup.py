from setuptools import setup, Command
import os
import platform
import shutil
import site
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/didyoureadme/ --delete-after")
        os.chdir("..")
class PyInstaller(Command):
    description = "We run pyinstaller in build to avoid doing a ./didyoureadme module imort. I had problems with i18n. Before running this command I must have done a install, removing old installations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("python setup.py uninstall")
        os.system("python setup.py install")
        f=open("build/run.py","w")
        f.write("import didyoureadme\n")
        f.write("didyoureadme.main()\n")
        f.close()
        os.chdir("build")
        os.system("""pyinstaller run.py -n didyoureadme-{} --onefile --windowed --icon ../didyoureadme/images/didyoureadme.ico --distpath ../dist""".format(__version__))

class Compile(Command):
    description = "Compile ui and images"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        futures=[]
        with ProcessPoolExecutor(max_workers=cpu_count()+1) as executor:
            for filename in os.listdir("didyoureadme/ui/"):
                if filename.endswith(".ui"):
                    without_extension=filename[:-3]
                    futures.append(executor.submit(os.system, "pyuic5 didyoureadme/ui/{0}.ui -o didyoureadme/ui/Ui_{0}.py".format(without_extension)))
            futures.append(executor.submit(os.system, "pyrcc5 didyoureadme/images/didyoureadme.qrc -o didyoureadme/images/didyoureadme_rc.py"))
        # Overwriting didyoureadme_rc
        for filename in os.listdir("didyoureadme/ui/"):
             if filename.startswith("Ui_"):
                 os.system("sed -i -e 's/didyoureadme_rc/didyoureadme.images.didyoureadme_rc/' didyoureadme/ui/{}".format(filename))
                 os.system("sed -i -e 's/from myqtablewidget/from didyoureadme.ui.myqtablewidget/' didyoureadme/ui/{}".format(filename))
                 os.system("sed -i -e 's/from wdgYear/from didyoureadme.ui.wdgYear/' didyoureadme/ui/{}".format(filename))

class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/didyoureadme*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/didyoureadme*")
            os.system("rm /usr/share/pixmaps/didyoureadme.png")
            os.system("rm /usr/share/applications/didyoureadme.desktop")
        else:
            print(site.getsitepackages())
            for file in os.listdir(site.getsitepackages()[1]):#site packages
                path=site.getsitepackages()[1]+"\\"+ file
                if file.find("didyoureadme")!=-1:
                    shutil.rmtree(path)
                    print(path,  "Erased")
            for file in os.listdir(site.getsitepackages()[0]+"\\Scripts\\"):#Scripts
                path=site.getsitepackages()[0]+"\\scripts\\"+ file
                if file.find("didyoureadme")!=-1:
                    os.remove(path)
                    print(path,  "Erased")

class Procedure(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("""
Nueva versión:
  * Cambiar la versión y la fecha en version.py
  * Escribir el Changelog en CHANGELOG.mc
  * python setup.py doc
  * linguist
  * python setup.py doc
  * python setup.py install
  * python setup.py doxygen
  * git commit -a -m 'didyoureadme-version'
  * git push
  * Hacer un nuevo tag en GitHub y copiar el CHANGELOG de la vsersión
  * python setup.py sdist upload -r pypi
  * Crea un nuevo ebuild de Gentoo con la nueva versión
  * Subelo al repositorio del portage
  * Change to windows. Enter in an Administrator console.
  * Change to didyoureadme source directory and make git pull
  * python setup.py pyinstaller
  * Add file to github release
""")

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("pylupdate5 -noobsolete -verbose didyoureadme.pro")
        os.system("lrelease -qt5 didyoureadme.pro")
    ########################################################################

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

if platform.system()=="Linux":
    data_files=[
    ('/usr/share/pixmaps/', ['didyoureadme/images/didyoureadme.png']), 
    ('/usr/share/applications/', ['didyoureadme.desktop']), 
               ]
else:
    data_files=[]

## Version of officegenerator captured from commons to avoid problems with package dependencies
__version__= None
with open('didyoureadme/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]

setup(name='didyoureadme',
    version=__version__,
    description='System to control who and when a group reads a document send by mail. It uses postgresql to store information',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
              'Intended Audience :: End Users/Desktop',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Programming Language :: Python :: 3',
             ], 
    keywords='mail read when who',
    url='https://github.com/Turulomio/didyoureadme',
    author='Turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['didyoureadme'],
    entry_points = {'console_scripts': [
                                       ],
                    'gui_scripts': ['didyoureadme=didyoureadme.didyoureadme:main',
                                   ],
                },
    install_requires= [ 'setuptools',
                        'psycopg2', 
                        'pytz',
                        'PyQt5;platform_system=="Windows"',
                        'pywin32;platform_system=="Windows"',
                        ], #PyQt5 doesn't have egg-info in Gentoo, so I remove it to install it with ebuild without making 2 installations. Should be added manually when using pip to install
    data_files=data_files,
    cmdclass={
                        'doxygen': Doxygen,
                        'doc': Doc,
                        'uninstall':Uninstall, 
                        'compile': Compile, 
                        'procedure': Procedure,
                        'pyinstaller': PyInstaller,
                     },
    zip_safe=False,
    include_package_data=True
    )

