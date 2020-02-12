# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import uuid

import flask
from pages import PAGES, Page
from survey import SURVEY
from socket_class import SocketClass

from flask import flash, redirect, render_template, request, session, url_for

app = flask.Flask(__name__)

app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True

app.secret_key = 'dfasdfasdfasdf'

trialNum = 0
canSendMarker = False
server_socket = None
DUMMY_IP = "127.0.0.1"
DUMMY_PORT = 8080
SERVER_IP = "0.0.0.0" # Might require change
SERVER_PORT = 8080 # Might require change

def send_data(class_label):
    global trialNum
    print("sending!")

    milliSec = int(round(time.time() * 1000))  # Get current time in milliseconds

    data = "{};{};{};\n".format(trialNum, class_label, milliSec)
    trialNum += 1 # increment trial number
    """
    # THE LINE BELOW CREATE BUGS
    # server_socket.send_data(data) 
    # THE LINE ABOVE CREATE BUG
    """

""" Runs the server in a separate thread
    :param host: Server ip address
    :param port: Server port
"""
def connect_server_socket(dummy_server=False):
    global server_socket
    if dummy_server:
        server_socket = SocketClass(DUMMY_IP, DUMMY_PORT)
    else:
        server_socket = SocketClass(SERVER_IP, SERVER_PORT)
    connected = openSocket()
    if connected:
        print("Connected socket")


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/question/')
def question_start():
    send_data('baselinestart')
    session['uid'] = uuid.uuid1()
    time.sleep(3)
    send_data('baselineend')
    time.sleep(0.5)

    send_data('easystart')

    return redirect(url_for('question', page=0))

@app.route('/question/<int:page>', methods=['GET', 'POST'])
def question(page):
    global canSendMarker
    page_str = str(page)

    if 'error_count' not in session:
        session['error_count'] = {}
    if page_str not in session['error_count']:
        session['error_count'][page_str] = 0

    # this is called after I press next on the survey

    # THE LINE BELOWS CAUSING BUG
    # if canSendMarker and page == 10:
    #     server_socket.send_data('hardstart')
    #     canSendMarker = False # prevent from sending markers on wrong answers

    # Cannot request page larger than number of pages we got
    if page > len(PAGES):
        session.pop('error_count')
        session.pop('uid')
        return render_template("cong.html")

    # Adding condition for method!=POST so, we only send marker when page loads,
    # not twice, for when page loads, and when the user submits an answer.

    """
    # THE LINE BELOWS CAUSING BUG
    # if PAGES[page].marker_data!='' and request.method!='POST':
    #     server_socket.send_data(PAGES[page].marker_data)
    # THE LINE ABOVE CAUSING BUG
    """

    if request.method == 'POST':
        expectAnswer = PAGES[page].answer

        # On the first page, there is no expect answer
        if expectAnswer == '':
            return redirect(url_for('question', page=page+ 1))

        # The answer to the question posted  
        userAnswer = request.form['answer']

        # If the user answer wrong
        if userAnswer != expectAnswer:
            if PAGES[page].is_test:
                return redirect(url_for('question', page=page+1))
            session['error_count'][page_str] += 1
            flash('Wrong!')
            return redirect(url_for('question', page=page))
        else: # means the answer is correct

            canSendMarker = True
            """
            # THE LINE BELOWS CAUSING BUG
            if canSendMarker:
                if page == 9: # I finished the easy and will start survey so I will send easyend before starting the survey
                    send_data('easyend')
                    # I didn't change canSendMarker to false here because I need to send hard start when the new page 10 is loaded

                if page == len(PAGES) - 1: # I finished the hard and will start survey so I will send hardend before starting the survey
                    send_data('hardend')

            # THE LINE ABOVE CAUSING BUG
            """
            # Show survey if the page has one
            if PAGES[page].show_survey != 0:
                return redirect(url_for('survey', survey_num=PAGES[page].show_survey, next_page=page + 1))
            else:
                flash('Correct!')
                session['error_count'][page_str] = 0
                return redirect(url_for('question', page=page + 1))

    

    return render_template('question.html', page=PAGES[page], current_page=page_str)


@app.route('/')
def hello_world():
    connect_server_socket(dummy=False)
    return render_template("welcomePage.html")

@app.route('/survey/<int:survey_num>')
def survey(survey_num):
    next_page = request.args.get('next_page')
    message = ''
    if survey_num == 1:
        message = 'end easy test, begin survey'
    if survey_num == 2:
        message = 'end med test, begin survey'
    if survey_num == 3:
        message = 'end hard test, begin survey'

    return render_template('survey.html', survey_num=survey_num, next_page=next_page, url=SURVEY[survey_num - 1])

