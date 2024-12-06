import asyncio
import sys

from robot_desktop.windows_inspect import InspectServer

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("参数错误", file=sys.stderr)
    else:
        inspect_server = InspectServer(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
        asyncio.run(inspect_server.start())
