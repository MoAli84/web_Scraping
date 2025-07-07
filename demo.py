# from pptx import Presentation

# prs = Presentation()
# slide_with_bullet_layout = prs.slide_layouts[1]

# slide = prs.slides.add_slide(slide_with_bullet_layout)
# shapes = slide.shapes

# title_shape = shapes.title
# body_shape = shapes.placeholders[1]

# title_shape.text = 'Adding a Bullet Slide'

# text_frame = body_shape.text_frame
# text_frame.text = 'Find the bullet slide layout'

# paragraph = text_frame.add_paragraph()
# paragraph.text = 'Use _TextFrame.text for first bullet'
# paragraph.level = 1

# paragraph = text_frame.add_paragraph()
# paragraph.text = 'Use _TextFrame.add_paragraph() for subsequent bullets'
# paragraph.level = 2

# prs.save('BulletSlideExample.pptx')


from flask import Flask,jsonify,request

app = Flask(__name__)

users = [
    {
        'id': 1,
        'name': 'mohamed'
    },
    {
        'id': 2,
        'name': 'ali'
    },  {
        'id': 3,
        'name': 'Ahmed'
    },
    {
        'id': 4,
        'name': 'mostafa'
    }
]
@app.route('/users', methods=['GET'])
def getusers():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def getuser(user_id):
    user = [user for user in users if user['id'] == user_id]
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'user not found'}), 404
    
@app.route('/users', methods=['POST'])
def createuser():
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name']
    }
    users.append(user)
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['PUT'])
def updateuser(user_id):
    user = [user for user in users if user['id'] == user_id]
    if user:
        user[0]['name'] = request.json['name']
        return jsonify(user)
    else:
        return jsonify({'message': 'user not found'}), 404

@app.route('/<string:name>')
def hello(name):
    return 'hello ' + name
    
if __name__ == '__main__':
    app.run(debug=True)   