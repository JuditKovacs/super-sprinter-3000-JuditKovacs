from flask import Flask, render_template, redirect, request
import csv

app = Flask(__name__)


@app.route('/')
def route_index():
    stories = get_stories()
    return render_template('list.html', stories=stories)


@app.route('/', methods=['POST'])
def route_index_saving_data():
    story_id = new_id()
    story_to_add = [story_id,
                    request.form['story_title'],
                    request.form['user_story'],
                    request.form['acc_criteria'],
                    request.form['b_value'],
                    request.form['estimation'],
                    request.form['status']]
    write(story_to_add)
    return redirect('/')


def new_id():
    stories = get_stories()
    last_story = None
    for last_story in stories:
        pass
    if last_story:
        return int(last_story[0]) + 1
    else:
        return 1


@app.route('/story')
@app.route('/story/<int:story_id>', methods=['POST'])
def route_story(story_id=None):
    story_to_edit = []
    stories = get_stories()
    for story in stories:
        if int(story[0]) == story_id:
            story_to_edit = story
    return render_template('form.html',
                           story_id=story_id,
                           story_to_edit=story_to_edit)


@app.route('/story/<int:story_id>/edit', methods=['POST'])
def route_edit_post(story_id):
    stories = get_stories()
    for story in stories:
        if int(story[0]) == story_id:
            story[1] = request.form['story_title']
            story[2] = request.form['user_story']
            story[3] = request.form['acc_criteria']
            story[4] = request.form['b_value']
            story[5] = request.form['estimation']
            story[6] = request.form['status']
    overwrite(stories)
    return redirect('/')


@app.route('/story/<int:story_id>/delete', methods=['POST'])
def route_delete(story_id):
    stories = get_stories()
    for story in stories:
        if int(story[0]) == story_id:
            stories.remove(story)
    overwrite(stories)
    return redirect('/')


def overwrite(stories):
    with open('records.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for story in stories:
            csv_writer.writerow(story)


def write(story_to_add):
    with open('records.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(story_to_add)


def get_stories():
    csv_list_all = []
    with open('records.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for story in csv_reader:
            csv_list_all.append(story)
    return csv_list_all


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
