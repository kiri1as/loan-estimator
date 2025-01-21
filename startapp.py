import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "creation_script.py"])
    subprocess.run(["python", "manage.py", "migrate"])
    subprocess.run(["python", "manage.py", "runserver"])
