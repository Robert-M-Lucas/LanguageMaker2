# Run before build

from PIL import Image

img = Image.open("BuildUtil/icon.png")
img.save('BuildUtil/icon.ico', format='ICO')# , sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])

with open("VERSION.txt", "r") as f:
    version = f.read()

with open("BuildUtil/file_version_info_not_filled.txt", "r") as f:
    file_ver_text = f.read()

file_ver_text = file_ver_text.replace("%$", version)

with open("BuildUtil/file_version_info.txt", "w+") as f:
    f.write(file_ver_text)

with open("BuildUtil/InnoSetupCompileScriptNotFilled.iss", "r") as f:
    compile_script_text = f.read()

compile_script_text = compile_script_text.replace("%$", version)

with open("BuildUtil/InnoSetupCompileScript.iss", "w+") as f:
    f.write(compile_script_text)
