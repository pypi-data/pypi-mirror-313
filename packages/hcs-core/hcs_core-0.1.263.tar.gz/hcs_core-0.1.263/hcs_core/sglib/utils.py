import os
import subprocess
import zipfile

import time

from hcs_core.ctxp import jsondot


def _print_output(text, name):
    if len(text) == 0:
        print(name + ": <EMPTY>")
    else:
        print(name + ":")
        lines = text.splitlines()
        for line in lines:
            print(">> " + line)


def run(cmd, check=True):
    print("CMD: " + cmd)
    parts = cmd.split(" ")
    proc = subprocess.run(
        parts,
        shell=False,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
    )
    if check and proc.returncode != 0:
        _print_output(proc.stdout, "STDOUT")
        _print_output(proc.stderr, "STDERR")
        proc.check_returncode()
    return proc


def _run_and_capture_output(cmd):
    proc = subprocess.run(cmd, shell=True, check=False, text=True, capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        _print_output(proc.stdout, "STDOUT")
        _print_output(proc.stderr, "STDERR")
        proc.check_returncode()
    return proc.stdout.strip()


def run_govc_guest_script(script, args):
    print("Running guest script: " + script + " " + args)
    cmd = f'govc guest.start {script} "{args} >/tmp/script-out 2>/tmp/script-err"'
    output = _run_and_capture_output(cmd)

    # wait for the process to finish
    cmd = f"govc guest.ps -X -x -json -p {output}"
    output = _run_and_capture_output(cmd)
    ret = jsondot.parse(output)

    output = _run_and_capture_output("govc guest.download /tmp/script-out -")
    _print_output(output, "STDOUT")
    output = _run_and_capture_output("govc guest.download /tmp/script-err -")
    if len(output) > 0:
        _print_output(output, "STDERR")

    if ret.ProcessInfo[0].ExitCode != 0:
        raise Exception("Fail running script: " + script)


def waitForVmPowerOff(iPath):
    current_millis = lambda: int(round(time.time() * 1000))
    start_time = current_millis()
    while current_millis() - start_time < 5 * 60 * 1000:
        p = subprocess.run(
            "govc vm.info -vm.ipath=" + iPath,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        if str(p.stdout).find("poweredOff") > 0:
            return
        time.sleep(5)
    raise Exception("Timeout customization. Check log in deployer VM.")


def zipdir(src_dir, target_file):
    with zipfile.ZipFile(target_file, "w", zipfile.ZIP_DEFLATED) as file:
        for root, dirs, files in os.walk(src_dir):
            for name in files:
                filePath = os.path.join(root, name)
                arcname = filePath[len(src_dir) :]
                file.write(filePath, arcname)


def dos2unix(file):
    file = os.path.abspath(file)
    content = ""
    outsize = 0
    with open(file, "rb") as infile:
        content = infile.read()
    with open(file, "wb") as output:
        for line in content.splitlines():
            outsize += len(line) + 1
            output.write(line + b"\n")
    stripped_bytes = len(content) - outsize
    if stripped_bytes != 0:
        print("dos2unix: Stripped %s bytes. %s" % (stripped_bytes, file))
