
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort



def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post



app = Flask(__name__)

app.config['SECRET_KEY'] = 'Hello'


@app.route('/')
def main():

    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    # conn.close()
    # return render_template('main.html', posts=posts)
    return render_template('main.html')




@app.route('/photo/')
def photo():
    return render_template('gallery.html')
# для рендера render_template обязательно: index.html д.б. в папке templates


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/vector/')
def vector():
    return render_template('vector.html')


@app.route('/module/')
def module():
    return render_template('module.html')

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'user page:'+name+' - '+ str(id)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('main'))



@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('main'))

    return render_template('edit.html', post=post)



# если программа запущена как основная а не как модуль то
if __name__ == '__main__':
    app.run(debug=True)




