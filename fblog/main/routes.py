from flask import Blueprint, request, render_template
import csv
from fblog.models import Post
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/chart")
def chart():

    # openning the csv file which is in the same location of this python file
    File = open('fblog/static/analytics.csv')

    # reading the File with the help of csv.reader()
    Reader = csv.reader(File)

    # storing the values contained in the Reader into Data
    Data = list(Reader)

    user_list = []
    dates_list = []
    session_list = []
    for data in Data:
        dates_list.append(str(data[0]))
        user_list.append(int(data[1].replace(',', '')))
        session_list.append(int(data[2].replace(',', '')))
    File.close()
    dic = {
        'data1' : user_list,
        'data2' : session_list,
        'dates': dates_list
    }
    print(dic['dates'])
    return render_template('chart.html', title='chart', dic=dic)

def get_shell_script_output_using_communicate():
    session = subprocess.Popen(['fblog/main/some.sh'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception("Error "+str(stderr))
    print(stdout)
    return stdout.decode('utf-8')

# def get_shell_script_output_using_check_output():
#     stdout = check_output(['fblog/main/some.sh']).decode('utf-8')
#     return stdout

@main.route('/shell')
def shell():
    return '<pre>'+get_shell_script_output_using_communicate()+'</pre>'