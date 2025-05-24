import os
import json
import shutil
import hashlib
# Change the current working directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

final_manifest = {}

base_url = "https://github.com/tomasalexandre18/EtiquetteGen-modules/releases/download/latest/"

if os.path.exists("build"):
    print("Removing old build directory...")
    shutil.rmtree("build")
os.mkdir("build")

# for all directories in the current directory
for module in os.listdir('.'):
    if os.path.isdir(module) and not module.startswith('.'):
        if not os.path.exists(os.path.join(module, 'module.py')):
            print(f"Invalid module {module} (no module.py file)")
            continue
        if not os.path.exists(os.path.join(module, 'manifest.json')):
            print(f"Invalid module {module} (no manifest.json file)")
            continue

        with open(os.path.join(module, 'manifest.json'), 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        print(f"Manifest for {module} loaded successfully")
        if 'version' not in manifest:
            print(f"Invalid manifest for {module} (no version key)")
            continue

        print("Valid module found:", module)
        print("zipping module...")
        shutil.make_archive(os.path.join('build', module), 'zip', module)
        md5 = hashlib.md5(open(os.path.join('build', module+".zip"), 'rb').read()).hexdigest()
        print(f"Module {module} zipped successfully with MD5: {md5}")
        final_manifest[module] = manifest
        final_manifest[module]['md5'] = md5
        final_manifest[module]['uri'] = f"{base_url}{module}.zip"
        final_manifest[module]['size'] = os.path.getsize(os.path.join('build', module+".zip"))

# Write the final manifest to a file
with open('manifest.json', 'w', encoding='utf-8') as f:
    json.dump(final_manifest, f, indent=4, ensure_ascii=False)
    print("Final manifest written to manifest.json")