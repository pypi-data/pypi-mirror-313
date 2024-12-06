import pkg_resources
import os


def get_jar_path(filename):
    package_name = 'mkpipe'  # Adjust according to where the jars are located
    try:
        jar_path = pkg_resources.resource_filename(package_name, f'jars/{filename}')
        if os.path.exists(jar_path):
            return jar_path
        else:
            print(f'JAR file {filename} not found in package')
    except Exception as e:
        print(f'Error accessing JAR files: {e}')
    return None


jar_path = get_jar_path('com.postgresql_driver.jar')
if jar_path:
    print(f'Found JAR at {jar_path}')
