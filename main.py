from capture import main
from datetime import datetime

folder_out = "data"
name = f"ar1_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

main(folder_out, name)
