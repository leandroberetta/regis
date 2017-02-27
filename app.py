from flask import Flask, render_template, request, redirect, url_for
from regis.service import services
from regis.registry import Registry

app = Flask(__name__, static_folder='regis/static', template_folder='regis/templates')

# Blueprints
app.register_blueprint(services, url_prefix='/services')

registry = Registry()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', data=get_data())
    else:
        return redirect(url_for('.index'))


def get_data():
    images, link = registry.get_images()

    image_list = []
    while link is not None:
        images, link = registry.get_images()

    for image in images:
        tags = registry.get_tags(image)

        tags_list = []
        for tag in tags:
            tag_data = {'name': tag, 'escaped_name': tag.replace('.', '_')}
            tags_list.append(tag_data)

        if len(tags_list) > 0:
            image_list.append({'image': image, 'tags': tags_list})

    return {'registry': registry.get_url(), 'images': image_list}


if __name__ == '__main__':
    app.run(port=4000, debug=True)