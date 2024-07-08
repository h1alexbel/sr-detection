import subprocess

default = {
    "search": "stars:>10 language:java size:>=20 mirror:false template:false",
    "start": "2019-01-01",
    "end": "2024-05-01",
    "tokens": "tokens"
}


def main(config=default):
    print("Collecting GitHub repositories using GitHub API...")
    print(f"Using config: {config}")
    cmd = f"""
    ghminer --query "{config["search"]}" \
            --start "{config["start"]}" \
            --end "{config["end"]}" \
            --tokens {config["tokens"]}
    """
    err = None
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        err = stderr
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                cmd,
                output=stdout,
                stderr=stderr
            )
    except subprocess.CalledProcessError:
        print(f"Something went wrong: {err}")
