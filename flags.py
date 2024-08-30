import streamlit as st
import requests
import random

if "countries" not in st.session_state:
	st.session_state.countries = {}
if "country" not in st.session_state:
	st.session_state.country = []
if "option" not in st.session_state:
	st.session_state.option = []
if "correct_option" not in st.session_state:
	st.session_state.correct_option = []
# if "grade" not in st.session_state:
# 	st.session_state.grade = []
if "startgame" not in st.session_state:
	st.session_state.startgame = False
if "submit" not in st.session_state:
	st.session_state.submit = False
if "first_run" not in st.session_state:
	st.session_state.first_run = False



st.session_state.num = st.number_input('How many questions do you need loaded?', step=1, min_value = 1)
def question_loader():
	if "score" not in st.session_state:
		st.session_state.score = [None for i in range(st.session_state.num)]
	if "answers" not in st.session_state:
		st.session_state.answers = [None for i in range(st.session_state.num)]
	for i in range(st.session_state.num):
		country_query = random.choice(st.session_state.country_list)
		st.session_state.country.append(country_query)
		wrong_options = [st.session_state.countries[country]['capital'] for country in random.sample(st.session_state.country_list,3)]
		correct_option = st.session_state.countries[country_query]['capital']
		st.session_state.correct_option.append(correct_option)
		options = wrong_options + [correct_option]
		random.shuffle(options)
		st.session_state.option.append(options)

if st.button("load questions"):
	if st.session_state.first_run == False:
		
		response = requests.get('https://restcountries.com/v3.1/all')

		data = response.json()

		for country in data:
			try:
				st.session_state.countries[country['name']['common']] = {'iso': country['cca2'],
														'capital': country['capital'][0],
														'currency': country['currencies'][list(country['currencies'].keys())[0]]['name'],
														'flag': country['flags']['png'],
														'population': country['population'],
														'continent': country['region'],
														'map': country['maps']['googleMaps']}
			except:
				pass

		st.session_state.capital = [st.session_state.countries[country]['capital'] for country in st.session_state.countries]
		st.session_state.country_list = list(st.session_state.countries.keys())
		st.session_state.first_run = True
		question_loader()
		st.session_state.startgame = True
	# if load:
	else:
		question_loader()
		st.session_state.startgame = True

def restart():
	st.session_state.indexer = 0
	st.session_state.country = []
	st.session_state.option = []
	st.session_state.correct_option = []
	st.session_state.submit = False
	st.session_state.startgame = False
	# st.experimental_rerun()

st.button('Restart', on_click=restart)


if "indexer" not in st.session_state:
	st.session_state.indexer = 0

def next():
	if st.session_state.indexer < st.session_state.num - 1:
		st.session_state.indexer += 1		


def previous():
	if st.session_state.indexer > 0:
		st.session_state.indexer -= 1


def grader():
	st.session_state.submit = True
	index = 0
	for i in st.session_state.correct_option:
		if i == st.session_state.answers[index]:
			st.session_state.score[index] = True
		else:
			st.session_state.score[index] = False
		index += 1
	# return st.session_state.score.count(True)
	if st.session_state.score.count(True) == st.session_state.num:
		st.balloons()
		st.success('Hurray, you got everything!')
	else:
		st.info(f'You scored {st.session_state.score.count(True)}/{st.session_state.num}. Try harder to get everything 😁')

def correction():
	return st.session_state.correct_option[st.session_state.indexer]

if st.session_state.startgame == True:

	st.header(f"What is the capital of {st.session_state.country[st.session_state.indexer]}?")

	st.session_state.answers[st.session_state.indexer] = st.radio('Options',st.session_state.option[st.session_state.indexer])

	col1,col2 = st.columns(2)

	with col1:
		st.button('Previous', use_container_width=True, on_click=previous)
	with col2:
		st.button('Next', use_container_width=True, on_click=next)


	if st.button('Submit',use_container_width=True):
		grader()

	if st.session_state.submit == True:
		if st.session_state.answers[st.session_state.indexer] == st.session_state.correct_option[st.session_state.indexer]:
			st.success(correction())
		else:
			st.error(correction())
	else:
		st.write('')

	# st.write(st.session_state.answers)

else:
	st.info('Please load your questions')