import argparse
import inspect
import json
import os
import subprocess
import pymysql
import sys
import zipfile
from typing import Union, Dict, Callable, List

from tooly.types import Encoding, Literal

defaultShellEncoding: Encoding = 'utf8'
if sys.platform.find('win'):
    defaultShellEncoding = 'gbk'

isDir = os.path.isdir


def getCallerFolder(depth=0):
    """
    :param depth: 调用者深度，默认为0层——调用者的文件夹位置  1层为调用者的调用者的位置
    """
    # 获取当前帧的上一层帧（即调用者的帧）
    caller_frame = inspect.stack()[1 + depth]
    # 获取该帧对应的文件路径
    caller_file_path = caller_frame.filename
    # 获取该文件的目录
    caller_folder = os.path.dirname(caller_file_path)
    return caller_folder


def getCallerFunction(depth=0):
    caller_frame = inspect.stack()[1 + depth]
    return caller_frame.function


def run(cmd, encoding=defaultShellEncoding, failExit=True, withRetCode=False, log=print, showCmd=True, showOutput=True,
        cwd=None, noStdErr=False, returnJson=False, noExecute=False):
    if not log:
        log = lambda *args: None
    if isinstance(cmd, list):
        cmd = [i for i in cmd if i.strip()]
        if showCmd:
            log("==>>", ' \\\n\t'.join(cmd))
        cmd = ' '.join(cmd)
    else:
        if showCmd:
            log("==>>", cmd)
    errOut = None
    if noStdErr:
        errOut = subprocess.DEVNULL
    if noExecute:
        return
    p = subprocess.Popen(cmd, shell=True, encoding=encoding, stdout=subprocess.PIPE, stderr=errOut, cwd=cwd)
    cmd = " ".join((i.strip("\\") for i in cmd.splitlines()))
    contents = []
    try:
        while p.poll() is None:
            line = p.stdout.readline()
            if showOutput:
                log(line, end="")
            contents.append(line)
    except KeyboardInterrupt:
        sys.exit()
    if failExit and p.returncode != 0:
        log(f'{cmd} 执行失败, code = {p.returncode}, stdout = \n {"".join(contents)}')
        sys.exit()
    retStr = "".join(contents).strip()
    if withRetCode:
        if returnJson:
            return p.returncode, json.loads(retStr)
        return p.returncode, retStr
    else:
        if returnJson:
            return json.loads(retStr)
        else:
            return retStr


def runS(cmd, encoding=defaultShellEncoding, failExit=True, withRetCode=False, log=print, showCmd=False,
         showOutput=False):
    """
    以silent的模式运行命令，仅返回结果
    """
    return run(cmd, encoding=encoding, failExit=failExit, withRetCode=withRetCode, log=log, showCmd=showCmd,
               showOutput=showOutput)


def runMysql(sql: Union[str, List[str]], host: str, user: str, password: str, port=3306, database=None, fetchAll=True,
             showSql=True):
    """
    @param sql 若为list，则仅执行sql，不返回结果
    @param host
    @param user
    @param password
    @param port
    @param database
    @param fetchAll
    @param showSql
    """
    config = {
        "host": host,
        "user": user,
        "password": password,
        "port": port,
        "charset": "utf8mb4",
        "autocommit": True,
    }
    if database:
        config["database"] = database
    with pymysql.connect(**config) as connection:
        with connection.cursor() as cursor:
            # 执行SQL语句
            if isinstance(sql, str):
                sql = [sql, ]
            for s in sql:
                if showSql:
                    print(s)
                cursor.execute(s)

            if len(sql) != 1 or not fetchAll:
                return
            # 获取查询结果的所有行
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            # 返回所有的列名以及结果
            return columns, results


def runDocker(dockerName: str, image: str,
              removeAfterExit=True,
              daemon=True,
              alwaysRestart=False,
              cpus: float = None,
              memoryGb: int = None,
              dockerArgs: List[str] = None,
              removeOldDocker=True,
              network: str = None,
              ipAddr: str = None,
              portMappings: Dict[str, str] = None,
              envMappings: Dict[str, str] = None,
              curDirVolumeMappings: Dict[str, str] = None,
              volumeMappings: Dict[str, str] = None,
              hosts: Dict[str, str] = None,
              extFlags: str = "", noExecute=False):
    if removeOldDocker:
        run(f"docker rm -f {dockerName}", noExecute=noExecute)

    if daemon:
        daemon = "-d"
    else:
        daemon = ""

    if hosts:
        # "--add-host doris-BE-01:192.168.0.121",
        hosts = [f"--add-host {k}:{v}" for k, v in hosts.items()]
    else:
        hosts = []

    if not dockerArgs:
        dockerArgs = []

    memoryStr = ""
    if memoryGb:
        memoryStr = f"--memory={memoryGb}g"
    cpuStr = ""
    if cpus:
        cpuStr = f"--cpus={cpus}"

    alwaysRestartStr = ""
    if alwaysRestart:
        alwaysRestartStr = "--restart always"

    removeAfterExitStr = ""
    if removeAfterExit:
        removeAfterExitStr = "--rm"

    portMappingsStr = []
    if portMappings:
        for k, v in portMappings.items():
            portMappingsStr.append(f"-p {k}:{v}")

    envMappingStr = []
    if envMappings:
        for k, v in envMappings.items():
            envMappingStr.append(f"-e {k}={v}")

    volumeMappingsStr = []
    if volumeMappings:
        for k, v in volumeMappings.items():
            volumeMappingsStr.append(f"-v {k}:{v}")

    if curDirVolumeMappings:
        for k, v in curDirVolumeMappings.items():
            k = os.path.normpath(os.path.join(getCallerFolder(1), k))
            volumeMappingsStr.append(f"-v {k}:{v}")
    networkStr = []
    if network:
        networkStr = ["--network " + network]

    if ipAddr:
        ipAddr = ['--ip=' + ipAddr]
    else:
        ipAddr = []

    cmd = [
        f"docker run --name {dockerName} {daemon} {removeAfterExitStr}",
        cpuStr,
        memoryStr,
        alwaysRestartStr,
        extFlags,
        *hosts,
        *networkStr,
        *ipAddr,
        *portMappingsStr,
        *envMappingStr,
        *volumeMappingsStr,
        f"{image}",
        *dockerArgs
    ]

    run([i for i in cmd if i], noExecute=noExecute)
    try:
        if daemon:
            res = json.loads(run("docker inspect " + dockerName, showOutput=False, showCmd=False))
            ip = res[0]["NetworkSettings"]["Networks"]["IPAddress"]
            print(f"{dockerName} IP: ", ip)
            return ip
    except:
        pass


class CustomHelpFormatter(argparse.HelpFormatter):
    """
    argparse的自定义help信息生成器，能在parser.add_argument函数没有help信息时打印default信息
    使用时，只需要在创建parser时传入即可，示例如下：
    >>> parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    """

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        if action.choices:
            choices_str = "(" + ", ".join(str(c) for c in action.choices) + ")"
            if action.default != argparse.SUPPRESS and hasattr(action, 'default'):
                args = [str(action.default) + "(默认值)"]
                for i in action.choices:
                    if i != action.default:
                        args.append(str(i))
                return "{" + ",".join([str(c) for c in args]) + "}"
            else:
                # 修复这里，确保default_metavar不为None时再进行拼接
                if default_metavar:
                    return super()._format_args(action, default_metavar + choices_str)
                else:
                    return super()._format_args(action, choices_str)
        else:
            if action.default != argparse.SUPPRESS and hasattr(action, 'default'):
                default_val = str(action.default) + "(默认值)"
                return default_val
            else:
                return super()._format_args(action, default_metavar)


def writeText(fname: str, *contents: str, encoding: Encoding = "utf8"):
    mode = 'w'
    with open(fname, mode, encoding=encoding) as fd:
        for content in contents:
            fd.write(content)


def appendText(fname: str, *content: str, encoding: Encoding = 'utf8'):
    with open(fname, 'a+', encoding=encoding) as fd:
        for c in content:
            fd.write(c)


def readAsBytes(fname: str) -> bytes:
    with open(fname, 'rb') as fd:
        return fd.read()


def readAsText(fname: str, encoding: Encoding = "utf8") -> str:
    with open(fname, 'r', encoding=encoding) as fd:
        return fd.read()


def zipFiles(dst: str, *srcFiles: str):
    """
    :param dst: 压缩的目标文件
    :param srcFiles: 要压缩文件列表，支持文件通配符。需要传递相对路径否则会在压缩文件中创建全路径
    :return:
    """
    run(f"tar czf {dst} {' '.join(srcFiles)}")


def unzip(zipFname: str, dstDir: str):
    with zipfile.ZipFile(zipFname) as fd:
        fd.extractall(dstDir)


def p7zip(dst: str, *srcFiles: str):
    run(f"7z a {dst} {' '.join(srcFiles)}")


def p7unzip(zipFname: str, dstDir: str = ""):
    if dstDir:
        dstDir = "-o " + dstDir
    run(f"7z x {zipFname} {dstDir}")


def gitCommitId(requireClean: bool = True, shortId: bool = False, branch: str = "") -> Union[str, None]:
    """
    获取当前文件夹下的git commit id
    :param requireClean: 是否要求git status状态为clean
    :param shortId: 是否返回短ID（8字节）
    :param branch:若不为空，则要求当前的branch为指定branch
    :return:
    """
    if requireClean:
        ret = run("git status")
        if ret.find("nothing to commit, working tree clean") < 0:
            print("git代码未commit")
            return None

    if branch:
        if branch != gitBranch():
            print("git分支与预期不符")
            return None

    ret = run("git rev-parse HEAD")
    if shortId:
        return ret.strip()[:8]
    return ret.strip()


def gitBranch():
    ret = run("git branch")
    lines = ret.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("*"):
            return line.split(" ")[1]


def genDockerRunCmd(dockerName: str,
                    dockerImage: str,
                    command: str = "",
                    customParams: str = "",
                    daemomMode=False,
                    envs: Dict[str, str] = {},
                    fileMapping: Dict[str, str] = {},
                    portMapping: Dict[int, int] = {},
                    workingDirInDocker: str = None,
                    multiLine: bool = False,
                    removeOnExit: bool = True):
    """
    生成docker运行的命令
    :param dockerName: docker名称
    :param dockerImage: docker image
    :param command: 可选，docker的启动命令
    :param customParams: 额外的命令行参数可以在此指定
    :param daemomMode: 是否在后台运行
    :param envs: 环境变量列表
    :param fileMapping: 文件映射列表 host -> docker
    :param portMapping: 端口映射列表 host -> docker
    :param workingDirInDocker: docker内pwd
    :param removeOnExit: docker结束后是否删除docker
    :param multiLine 命令是否分割成多行
    :return:
    """
    if not dockerImage:
        raise Exception("docker image不能为空")
    if not dockerName:
        raise Exception("docker name不能为空")

    _removeOnExit = " --rm" if removeOnExit else ""
    _daemonMode = " -d" if daemomMode else ""

    lineStart = "\t" if multiLine else ""
    lineEnd = " \\\n" if multiLine else ""

    mappings = []
    mappings += [f'{lineStart}-e {k}={v}{lineEnd}' for (k, v) in envs.items()]
    mappings += [f'{lineStart}-v {k}:{v}{lineEnd}' for (k, v) in fileMapping.items()]
    mappings += [f'{lineStart}-p {k}:{v}{lineEnd}' for (k, v) in portMapping.items()]
    _workdingDir = f" -w {workingDirInDocker}" if workingDirInDocker else ""

    _mappings = " ".join(mappings)

    return f"docker run{_removeOnExit}{_daemonMode}{customParams} --name {dockerName}{lineEnd}{_mappings}{lineStart}{_workdingDir}{dockerImage}{command}"


def runInTmux(cmd: str, sessionName: str = None):
    """
    新建一个tmux，并在其中运行命令（python脚本退出后，tmux中的命令仍然在运行
    """
    try:
        import libtmux
    except:
        raise Exception("libtmux未安装，请使用如下命令安装：pip install libtmux")
    server = libtmux.Server()
    if sessionName:
        sess = server.find_where({"session_name": sessionName})
        if sess:
            sess.kill_session()
    sess = server.new_session(session_name=sessionName)
    sess.attached_pane.send_keys(cmd.strip() + "\n")


def sshExecWithParamiko(cmd: str):
    try:
        import paramiko
    except:
        raise Exception("libtmux未安装，请使用如下命令安装：pip install paramiko")


def withParamiko(host: str, userName: str, fun: Callable,
                 port: int = 23,
                 isScp: bool = False,
                 passwd: str = None,
                 rsaFile: str = None,
                 rsaPasswd: str = None):
    try:
        import paramiko
        from scp import SCPClient
    except:
        raise Exception("libtmux未安装，请使用如下命令安装：pip install paramiko")

    ssh = paramiko.SSHClient()
    try:
        ssh.load_system_host_keys()
        pkey = None
        if rsaFile:
            pkey = paramiko.RSAKey.from_private_key_file(filename=rsaFile, password=rsaPasswd)
        ssh.connect(hostname=host, port=port, username=userName, pkey=pkey, password=passwd)

        if isScp:
            with SCPClient(ssh.get_transport()) as scp:
                fun(scp)
        else:
            fun(ssh)

    finally:
        ssh.close()


def scpWithParamiko(srcPath: str,
                    dstPath: str,
                    host: str,
                    userName: str,
                    port: int = 23,
                    passwd: str = None,
                    rsaFile: str = None,
                    rsaPasswd: str = None,
                    recursive: bool = True,
                    method: Literal["put", "get"] = "put"):
    def f(scp):
        if "put" == method:
            scp.put(srcPath, dstPath, recursive=recursive)
        else:
            scp.get(srcPath, dstPath, recursive=recursive)

    withParamiko(host, userName, f, isScp=True, port=port, passwd=passwd, rsaFile=rsaFile, rsaPasswd=rsaPasswd)


if __name__ == '__main__':
    # print(ls("*.py"))
    # touch("a/b/c.txt")
    # move("a/*.txt","a/b")
    # rm("a/b/*.txt")
    # print(ls("a/b/"))
    # rm("a")
    # print(ls("a/b/"))
    # touch("a/b/c.txt")
    # touch("a/b.txt")
    # mkdir("a/d")
    # zip("a/", "f.zip")
    # zip("f.zip", "a", excludeFiles=["a/d"])
    # touch("a/b/b1.txt")
    # mkdir("a/b/c/")
    # touch("a/d.txt")
    # mkdir("a/d/")
    # p7zip("out.7z", "a")
    # unzip("out.zip", "extract")
    # p7unzip("out.7z", "extract")
    # print(gitCommitId(requireClean=False))
    # print(genDockerRunCmd("ddd", "nginx", fileMapping={
    #     "/hostDir": "/dockerDir",
    #     "/hostDir2": "/dockerDir"
    # }, portMapping={
    #     22: 33,
    #     44: 55,
    #     23: 4403
    # }, envs={
    #     "NAME": "liyuan"
    # }, multiLine=True))
    run("ls")
