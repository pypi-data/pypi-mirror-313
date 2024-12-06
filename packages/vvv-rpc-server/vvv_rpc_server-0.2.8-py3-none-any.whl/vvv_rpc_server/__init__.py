# coding=utf-8
import shutil
import os
import sys
import time
import json
import tempfile
def extractall(self, path=None, members=None, pwd=None):
    if members is None: members = self.namelist()
    path = os.getcwd() if path is None else os.fspath(path)
    for zipinfo in members:
        try:    _zipinfo = zipinfo.encode('cp437').decode('gbk')
        except: _zipinfo = zipinfo.encode('utf-8').decode('utf-8')
        print('[*] unpack...', _zipinfo)
        if _zipinfo.endswith('/') or _zipinfo.endswith('\\'):
            myp = os.path.join(path, _zipinfo)
            if not os.path.isdir(myp):
                os.makedirs(myp)
        else:
            myp = os.path.join(path, _zipinfo)
            youp = os.path.join(path, zipinfo)
            self.extract(zipinfo, path)
            if myp != youp:
                os.rename(youp, myp)
import zipfile
zipfile.ZipFile.extractall = extractall

def creat_windows_shortcut(exe_path):
    vbsscript = '\n'.join([
        'set WshShell = WScript.CreateObject("WScript.Shell" )',
        'set oShellLink = WshShell.CreateShortcut(Wscript.Arguments.Named("shortcut") & ".lnk")',
        'oShellLink.TargetPath = Wscript.Arguments.Named("target")',
        'oShellLink.WindowStyle = 1',
        'oShellLink.Save',
    ])

    s = tempfile.mkdtemp()
    try:
        vbs = os.path.join(s, 'temp.vbs')
        with open(vbs, 'w', encoding='utf-8') as f:
            f.write(vbsscript)
        exe  = exe_path
        link = os.path.join(os.path.expanduser("~"),'Desktop','v_chrome')
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')
        cmd = r'''
        {} /target:"{}" /shortcut:"{}"
        '''.format(vbs, exe, link).strip()
        print('[*] make shortcut in Desktop:', cmd)
        v = os.popen(cmd)
        v.read()
        v.close()
    finally:
        import traceback;
        if traceback.format_exc().strip() != 'NoneType: None':
            print('create shortcut failed.')
            traceback.print_exc()
        shutil.rmtree(s)

def get_v_path_info():
    import vvv_rpc_server_stable
    localpath = os.path.split(vvv_rpc_server_stable.__file__)[0]
    v_chrome_file = os.path.join(localpath, 'chrome-win32-x64.zip')
    v_chrome_main_file = os.path.join(localpath, 'chrome-exe.zip')
    v_chrome_tar_xz = os.path.join(localpath, 'chrome-win32-x64.tar.xz')
    # v_chrome_target = os.path.join(localpath, 'chrome-win32-x64')
    v_chrome_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', 'chrome-win32-x64')
    v_chrome_exec_path = os.path.join(v_chrome_target, 'chrome-win32-x64')
    v_chrome_exec = os.path.join(v_chrome_target, 'chrome-win32-x64', 'v_chrome.exe')
    v_chrome_update = os.path.join(v_chrome_target, 'chrome-win32-x64', 'resources', 'app')
    v_configpath = os.path.join(v_chrome_update, 'config.cfg')
    return v_chrome_tar_xz, v_chrome_file, v_chrome_main_file, v_chrome_exec_path, v_chrome_target, v_chrome_exec, v_chrome_update, v_configpath

import tarfile
def extract_tar_xz(tar_filename, output_dir):
    with tarfile.open(tar_filename, "r:xz") as tar:
        total_files = len(tar.getmembers())
        processed_files = 0
        for member in tar.getmembers():
            tar.extract(member, path=output_dir)
            processed_files += 1
            progress = (processed_files / total_files) * 100
            print(f"[*] Extracting: {member.name} - {progress:.2f}% complete")
    print("[*] Extraction complete!")

def install():
    v_chrome_tar_xz, v_chrome_file, v_chrome_main_file, v_chrome_exec_path, v_chrome_target, v_chrome_exec, v_chrome_update, v_configpath = get_v_path_info()
    if os.path.isfile(v_chrome_file):
        print('[*] zip file path ===>', v_chrome_file)
        print('[*] exe file path ===>', v_chrome_exec)
        if not os.path.isdir(v_chrome_target):
            print('[*] unpack...')
            f = zipfile.ZipFile(v_chrome_file, 'r')
            f.extractall(v_chrome_target)
            f.close()
            f = zipfile.ZipFile(v_chrome_main_file, 'r')
            f.extractall(v_chrome_exec_path)
            f.close()
            print('[*] unpacked path ===>', v_chrome_target)
    elif os.path.isfile(v_chrome_tar_xz):
        print('[*] xz file path ===>', v_chrome_tar_xz)
        if not os.path.isdir(v_chrome_target):
            print('[*] unpack...')
            v_chrome_target_2 = os.path.join(v_chrome_target, 'chrome-win32-x64')
            if not os.path.isdir(v_chrome_target_2):
                os.makedirs(v_chrome_target_2)
            extract_tar_xz(v_chrome_tar_xz, v_chrome_target_2)
    main1, main2, awake_exe = get_update()
    shutil.copy(main1, v_chrome_update)
    shutil.copy(main2, v_chrome_update)
    shutil.copy(awake_exe, v_chrome_update)
    creat_windows_shortcut(v_chrome_exec)
    runbat = os.path.join(os.path.expanduser("~"),'Desktop','v_chrome') + '.bat'
    if os.path.isfile(runbat):
        os.remove(runbat)
    with open(runbat, 'w', encoding='utf-8') as f:
        f.write(v_chrome_exec)

def remove():
    v_chrome_tar_xz, v_chrome_file, v_chrome_main_file, v_chrome_exec_path, v_chrome_target, v_chrome_exec, v_chrome_update, v_configpath = get_v_path_info()
    if os.path.isdir(v_chrome_target):
        os.popen('taskkill /f /im v_chrome.exe /t').read()
        print('[*] remove...', v_chrome_target)
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(v_chrome_target)
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)
        link = os.path.join(os.path.expanduser("~"),'Desktop','v_chrome')
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')
        runbat = os.path.join(os.path.expanduser("~"),'Desktop','v_chrome') + '.bat'
        if os.path.isfile(runbat):
            os.remove(runbat)

def get_update():
    path = os.path.dirname(__file__)
    main1 = os.path.join(path, 'main.js')
    main2 = os.path.join(path, 'main.kfcvme50')
    awake_exe = os.path.join(path, 'Awake.exe')
    return main1, main2, awake_exe

def save_config(data):
    v_chrome_tar_xz, v_chrome_file, v_chrome_main_file, v_chrome_exec_path, v_chrome_target, v_chrome_exec, v_chrome_update, v_configpath = get_v_path_info()
    if os.path.isfile(v_configpath):
        os.remove(v_configpath)
    with open(v_configpath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def get_config():
    v_chrome_tar_xz, v_chrome_file, v_chrome_main_file, v_chrome_exec_path, v_chrome_target, v_chrome_exec, v_chrome_update, v_configpath = get_v_path_info()
    if os.path.isfile(v_configpath):
        with open(v_configpath, 'r', encoding='utf-8') as f:
            return f.read()

def execute():
    argv = sys.argv
    print('v_server :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[install]:  v_server install')
        print('[remove]:   v_server remove')
        print('[config]:   v_server config key1=value1 key2=value2')
        return
    if len(argv) > 1:
        if argv[1] == 'install':
            install()
        if argv[1] == 'remove':
            remove()
        if argv[1] == 'config':
            if len(argv[2:]):
                d = {}
                for i in argv[2:]:
                    kv = i.split('=', 1)
                    if len(kv) == 2:
                        d[kv[0]] = kv[1]
                save_config(d)
                print('[*] save config', d)
            else:
                print('[*] show config', get_config())

if __name__ == '__main__':
    # execute()
    install()
    # remove()
    pass
