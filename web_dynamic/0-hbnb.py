mport os
import shutil
import uuid


def main():
    # Define paths
    source_folder = "web_flask"
    destination_folder = "web_dynamic"

    # Copy necessary files and folders
    shutil.copytree(
        os.path.join(source_folder, "static"),
        os.path.join(destination_folder, "static"),
    )
    shutil.copy(
        os.path.join(source_folder, "templates", "100-hbnb.html"),
        os.path.join(destination_folder, "templates", "0-hbnb.html"),
    )
    shutil.copy(os.path.join(source_folder, "__init__.py"), destination_folder)
    shutil.copy(
        os.path.join(source_folder, "100-hbnb.py"),
        os.path.join(destination_folder, "0-hbnb.py"),
    )

    # Update 0-hbnb.py to replace the existing route to /0-hbnb/
    with open(os.path.join(destination_folder, "0-hbnb.py"), "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if "/0-hbnb/" in line:
                file.write(line.replace("/0-hbnb/", "/0-hbnb/"))
            else:
                file.write(line)
        file.truncate()

    # Add cache_id variable to render_template in 0-hbnb.py
    with open(os.path.join(destination_folder, "0-hbnb.py"), "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if "render_template" in line:
                file.write(line.rstrip() + ", cache_id=str(uuid.uuid4())" + "\n")
            else:
                file.write(line)
        file.truncate()

    # Add cache_id query string to each <link> tag URL in 0-hbnb.html
    with open(
        os.path.join(destination_folder, "templates", "0-hbnb.html"), "r+"
    ) as file:
        html_content = file.read()
        html_content = html_content.replace(
            '<link rel="stylesheet" type="text/css" href="{{ url_for(\'static\', filename=\'styles/main.css\') }}">',
            '<link rel="stylesheet" type="text/css" href="{{ url_for(\'static\', filename=\'styles/main.css\', cache_id=cache_id) }}">',
        )
        file.seek(0)
        file.write(html_content)
        file.truncate()


if __name__ == "__main__":
    main()

