# Call these commands with:
# $ doit

import doit
import glob

Python_files = glob.glob("src/*.py")

#def task_test():
#    """Test all fragments"""
#    return {
#        'actions': [r'pytest -vs --doctest-modules %s > testreport.txt' % (" ".join(Python_files)),],
#        'file_dep': Python_files,
#        'targets': ["testreport.txt"],
#        'verbosity': 2,
#        }


def task_build():
    """build cmd """
    return {
        'actions': ['pdflatex -shell-escape 04_Lists ;pdflatex -shell-escape 04_Lists ; bibtex 04_Lists ; pdflatex -shell-escape 04_Lists',],
        'file_dep': ["testreport.txt"] + Python_files +
                     ["04_Lists.tex"],
        'targets': ["04_Lists.pdf"],
        'verbosity': 2,
        }

#def task_cleanup():
#    """cleanup cmd"""
#    return {
#        'actions': ['rm *.aux *.log *.nav *.out *.snm *.toc *.vrb',],
#        'file_dep': ["04_Lists.pdf"],
#        'verbosity': 2,
#        }

