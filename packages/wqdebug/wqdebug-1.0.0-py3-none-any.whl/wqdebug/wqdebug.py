import os
import sys
import re
import shutil
import argparse
import traceback
import tarfile
import glob
#import wq_coredump
from coredump.elf32 import *
from coredump.corefile import *

class WqDebug:
    def __init__(self, log: str = "", wpk: str = "", elf: str = ""):
        self.log = log
        self.wpk = wpk
        self.elf = elf
        self.dumps = {}
        self.dumps_index = 0
        if self.log == "":
            self.log = "test/test.log"

    def start(self):
        if self.select_log_file():
            if self.find_coredump():
                self.select_coredump()

    def select_log_file(self):
        user_input = input(
            f"log:\n{self.log}\n请拖入LOG文件或输入文件路径, 输入回车Enter使用推荐文件:\n"
        )
        if user_input:
            self.log = user_input
            while not os.path.isfile(self.log):
                print("文件路径不存在，请重新输入。")
                self.select_log_file()
        return True

    @staticmethod
    def serach_elf_file(core: str, log_path: str, wpk_path: str):
        core_name_mapping = {"acore": "core0", "bcore": "core1", "dcore": "core4"}
        core_name = core_name_mapping.get(core, "core0")
        file_paths = [
            os.path.join(os.path.dirname(log_path), f"*_{core}.elf"),  # opencore
            os.path.join(os.path.dirname(log_path), f"*_{core_name}.elf"),  # ADK
            os.path.join(os.path.dirname(wpk_path), f"*_{core_name}.elf"),  # ADK
            os.path.join(os.path.dirname(wpk_path), f"*_{core}.elf"),  # opencore
            os.path.join(
                os.path.dirname(wpk_path), f"{core_name}", f"*_{core_name}.elf"
            ),  # ADK
            os.path.join(
                os.path.dirname(wpk_path).replace("package", "bin"),
                "tws_2_0",
                f"{core}",
                f"*_{core}.elf",
            ),  # opencore
        ]
        for file_path in file_paths:
            # print(file_path)
            for f in glob.glob(file_path):
                # print(f)
                if os.path.isfile(f):
                    return f

    def select_elf_file(self, core="core0"):
        # print(f"select_elf_file {core}")
        if not os.path.isfile(self.elf):
            self.elf = self.serach_elf_file(core, self.log, self.wpk)
        user_input = input(
            f"elf:\n{self.elf}\n请拖入ELF文件或输入文件路径, 输入回车Enter使用推荐文件:\n"
        )

        if user_input:
            self.elf = user_input
            while not os.path.isfile(self.elf) or not self.elf.split(".")[-1] == "elf":
                print("无效的ELF文件，请重新输入。")
                self.select_elf_file("")
        return self.elf

    def find_coredump(self):
        rc_mcause_coredump_old = re.compile(
            r"[\[|【].*?([m|c]cause: .*?)\n[\s\S]*?"
            r"================= CORE DUMP START =================([\s\S]*?)"
            r"================= CORE DUMP END ================="
        )
        rc_mcause_coredump = re.compile(
            r"[\[|【]([A|B|D]).*?([m|c]cause: .*?)\n[\s\S]*?"
            r"================= CORE\d? DUMP START =================([\s\S]*?)"
            r"================= CORE\d? DUMP END ================="
        )
        rc_time_coredump = re.compile(r".*?>")
        rc_time_coredump_old = re.compile(r".*?\] ")
        with open(self.log, "r", encoding="utf-8", errors="ignore") as f:
            log_data_all = f.read()
            print(f"正在查找LOG文件中的coredump信息...")
            log_data_list = log_data_all.split("Core dump has written to uart")
            found_coredump = False
            index = 0
            for log_data in log_data_list:
                # print("log_data=", log_data[0:128])
                match_list = rc_mcause_coredump.finditer(log_data)
                for m in match_list:
                    reason = f"{index}. {m.group(1)}core {m.group(2)}"
                    print(reason)
                    self.dumps[reason] = re.sub(
                        rc_time_coredump_old,
                        "",
                        re.sub(rc_time_coredump, "", m.group(3)),
                    )
                    found_coredump = True
                    index += 1
                    if index >= 2:
                        break
            if not found_coredump:
                print(f"正在查找rc_mcause_coredump_old...")
                for log_data in log_data_list:
                    # print("log_data=", log_data[0:128])
                    match_list = rc_mcause_coredump_old.finditer(log_data)
                    for m in match_list:
                        reason = f"{index}. {m.group(1)}"
                        print(reason)
                        self.dumps[reason] = re.sub(
                            rc_time_coredump_old,
                            "",
                            re.sub(rc_time_coredump, "", m.group(2)),
                        )
                    found_coredump = True
                    index += 1
                    if index >= 2:
                        break

            if not found_coredump:
                print(f"{self.log} LOG 文件无效，未找到有效的coredump信息。")
            else:
                print(f"找到 {len(self.dumps)} 个coredump信息")
                return True

    def get_core_name(self, dump):
        rc_core_name = re.compile(r"([A|B|D])core")
        # print(rc_core_name, dump)
        core_name = re.search(rc_core_name, dump)
        if core_name:
            return core_name.group()
        return "acore"

    def select_coredump(self):
        user_input = input(f"\n请输入 coredump 编号, 输入回车Enter使用默认0\n:")
        if not user_input:
            self.dumps_index = 0
            print(f"{list(self.dumps.keys())[self.dumps_index]}")
        elif user_input.isdigit() and 0 <= int(user_input) < len(self.dumps):
            self.dumps_index = int(user_input)
            print(f"{list(self.dumps.keys())[self.dumps_index]}")
        else:
            print(f"请输入是介于 0 到 {len(self.dumps) - 1} 之间的数字")
            self.select_coredump()

        core_name = self.get_core_name(list(self.dumps.keys())[self.dumps_index])
        elf = self.select_elf_file(core_name)
        if not os.path.exists("temp"):
            os.makedirs("temp")
        shutil.copy(elf, f"temp/coredump_{core_name}.elf")

        reason = list(self.dumps.keys())[self.dumps_index]
        with open(os.path.join(f"temp/coredump_{core_name}.b64"), "w") as f:
            f.write(self.dumps[reason].strip())

        # loader = wq_coredump.WQCoreDumpFileLoader(
        #     f"temp/coredump_{core_name}.b64", True
        # )
        # coredump_bin = loader.create_corefile(f"temp/coredump_{core_name}.bin")

        coredump_bin = f"temp/coredump_{core_name}.bin"
        cf = CoreFile(machine="riscv")
        cf.load(corefile=f"temp/coredump_{core_name}.b64")
        cf.save(coredump_bin)

        coredump_elf = f"temp/coredump_{core_name}.elf"
        gdbinit = "gdbinit.py"
        gdb = "riscv/bin/riscv32-unknown-elf-gdb"
        if not os.path.isfile(gdb):
            self.download_gdb()
        cmd = (
            f"start wsl echo \033[91m {reason} \033[0m;"
            f"{gdb} -q -command={gdbinit} --nw -core={coredump_bin} {coredump_elf};read"
        )
        print(cmd)
        os.system(cmd)
        sys.exit(0)

    def download_gdb(self):
        this_dir = os.path.dirname(__file__)
        gdb_path = f"\\\\192.168.100.55\\share\\wuqi_toolchain\\riscv_gdb.tar.gz"
        local_gdb = os.path.join("\\riscv")
        print("未找到GDB，下载中 ......")
        print(gdb_path)
        if not os.path.exists(local_gdb):
            shutil.copy2(gdb_path, this_dir)
            print("下载完成")
            tarfile.open(os.path.join(this_dir, os.path.basename(gdb_path))).extractall(
                path=this_dir
            )
            os.remove(os.path.join(this_dir, os.path.basename(gdb_path)))
            print(os.path.join(this_dir, os.path.basename(gdb_path)))

def main():
    __version__ = "0.0.0.1"
    print(f"wq debug v:{__version__}")
    os.chdir(os.path.dirname(__file__))
    print(sys.argv)
    try:
        parser = argparse.ArgumentParser(description=f"wq debug v:{__version__}")
        parser.add_argument(
            "-l",
            "--log",
            help="log file path",
            nargs="?",
            const="",
            type=str,
            default="",
        )
        parser.add_argument("-e", "--elf", help="elf file path", type=str, default="")
        parser.add_argument(
            "-w",
            "--wpk",
            help="wpk file path, infer the elf file path from the wpk file path",
            nargs="?",
            const="",
            type=str,
            default="",
        )
        args = parser.parse_args()
        # print(args.log, args.wpk, args.elf)
        wq_debug = WqDebug(args.log, args.wpk, args.elf)
        wq_debug.start()
    except Exception as e:
        print(e)
        traceback.print_exc()
        input("请按下回车键退出...")

if __name__ == "__main__":
    main()
