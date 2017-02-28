from flask import Flask, render_template, request, redirect, url_for
from regis.service import services
from regis.registry import Registry
from regis.error import ConnectionError
from regis.service import registry

app = Flask(__name__, static_folder='regis/static', template_folder='regis/templates')

# Blueprints
app.register_blueprint(services, url_prefix='/services')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', data=get_data())
    else:
        digest = request.form.get('digest', None)
        image = request.form.get('image', None)

        registry.delete_tag(image, digest)

        return redirect(url_for('.index'))


def get_data():
    try:
        images, link = registry.get_images()

        image_list = []
        while link is not None:
            images, link = registry.get_images()

        for image in images:
            tags = registry.get_tags(image)

            tags_list = []
            for tag in tags:
                tag_data = {'name': tag, 'escaped_name': tag.replace('.', '_')}

                manifests_data = registry.get_manifests(image, tag)
                if 'digest' in manifests_data:
                    tag_data['digest'] = manifests_data['digest']

                tags_list.append(tag_data)

            if len(tags_list) > 0:
                image_list.append({'image': image, 'escaped_image': image.replace('/', '_'), 'tags': tags_list})

        return {'registry': registry.get_url(), 'images': image_list}
    except ConnectionError:
        return {'error': 'Error'}


def escape_tag(tag):
    tag.replace('.', '_').replace('/', '_')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)