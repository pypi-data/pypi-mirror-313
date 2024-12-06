import json
import logging
import os.path
import subprocess
import sys


class DataX:
    def __init__(self, job_name, job_content: json, job_dir="/tmp/datax/job"):
        """
        datax job
        :param job_dir: job存放目录
        :param job_name: job名称
        :param job_content: job内容
        """
        self.envs = self._load_env()
        self.job_dir = job_dir
        self.job_name = job_name
        self.job_content = job_content

        self.job_path = os.path.join(self.job_dir, f"{self.job_name}.json")
        self._save()

    def _load_env(self):
        logging.info("start load env==")
        request_envs = ["DATAX_HOME"]
        my_envs = {}
        for request_env in request_envs:
            if request_env in os.environ:
                my_envs[request_env] = os.environ[request_env]
                logging.info(f"load {request_env}: {os.environ[request_env]} success")
            else:
                logging.error(f"load {request_env} error , please set {request_env} env path ")
        logging.info("end load env ====")
        return my_envs

    def _save(self):
        if not os.path.exists(self.job_dir):
            # 如果目录不存在，则创建目录
            os.makedirs(self.job_dir)
            logging.debug(f"{self.job_dir} 创建成功")
        with open(self.job_path, 'w', encoding='utf8') as fw:
            fw.write(json.dumps(self.job_content))

    def run(self, debug=False):
        logging.info("start run job =========")
        python_exe = sys.executable
        script_path = os.path.join(self.envs["DATAX_HOME"], "bin/datax.py")
        try:
            cmd = [python_exe, script_path]
            if debug:
                cmd.append("--loglevel")  # 添加正确的参数
                cmd.append("debug")
            cmd.append(self.job_path)  # 把 self.job_path 放在最后
            print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                       bufsize=1,
                                       stderr=subprocess.PIPE, text=True)
            # 实时输出子进程的 stdout
            for line in process.stdout:
                print(line.strip())
            # 等待子进程结束
            process.wait()
        except subprocess.CalledProcessError as e:
            print(e)
