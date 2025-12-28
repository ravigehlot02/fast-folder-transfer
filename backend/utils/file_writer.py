# file_writer.py
# Responsible for writing uploaded files to disk.

import os
#import aiofiles

async def save_file(directory: str, file):
    """
    Saves an UploadFile to the specified directory
    using async file IO.
    
    target_path = os.path.join(directory, file.filename)

    async with aiofiles.open(target_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return target_path
    """
    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
