import os
import shutil
import tempfile
import freaky

print("beginning test suite.")

tempdir = tempfile.mkdtemp()


for filename in os.listdir("in"):
    if filename.endswith(".bmp"):
        freaky.decode(f"in/{filename}", f"{tempdir}/{filename[:-4]}.wav")
        freaky.encode(f"{tempdir}/{filename[:-4]}.wav", f"{tempdir}/{filename}")

        if os.path.exists(f"out/{filename}"):
            diff = freaky.imgdiff(f"{tempdir}/{filename}", f"out/{filename}")
            print(f"{filename[:-4]} diff = {diff}")
            assert (diff > 0) and (diff < 0.1)
        else:
            print(f"{filename} does not exist in out/ dataset yet.")
            print("adding now...")
            shutil.copyfile(f"{tempdir}/{filename}", f"out/{filename}")
            
        
