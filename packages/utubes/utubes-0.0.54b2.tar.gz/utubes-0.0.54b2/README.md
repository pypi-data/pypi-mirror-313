<p align="center">
 📦 <a href="https://pypi.org/project/utubes" style="text-decoration:none;">UTUBES</a>
</p>


## USAGE
```python
import asyncio
from Utubes.functions import DownloadER

async def main():
    filelink = "https://example.utubes"
    commands = {"quiet": True, "no_warnings": True}
    metadata_result = await DownloadER.metadata(filelink, commands)
    extinfos_result = await DownloadER.extracts(filelink, commands)
    filename_result = await DownloadER.filename(filelink, commands)
    print(metadata_result.result) # metadata_result.errors
    print(extinfos_result.result) # extinfos_result.errors
    print(filename_result.result) # filename_result.errors
    # DO SOMETHING WITH THE RESULTS

asyncio.run(main())
```
