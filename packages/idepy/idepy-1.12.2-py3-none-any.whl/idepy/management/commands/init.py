import json
import os
import shutil
import time


class Command:
    description = "初始化一个新的IDEPY项目."

    def register_arguments(self, subparser):
        """注册命令所需的参数"""
        subparser.add_argument("project_name", type=str, help="要初始化的项目名称",
                               nargs="?",  # 表示参数是可选的
                               default=""  # 默认值为 None
                               )

    def execute(self, args):

        """执行命令逻辑"""
        project_name = args.project_name
        project_dir = os.path.join(os.getcwd(), project_name)

        # 检查目录是否存在且不为空
        if os.path.exists(project_dir) and os.listdir(project_dir):
            print(f'目录"{project_dir}"不为空.')
            return


        # 输入用户信息
        name = input("程序名: ") or project_name
        description = input("程序描述: ") or "Created by IDEPY"
        author = input("版权/作者: ") or "Created by IDEPY"



        # 复制基础项目模板到新目录
        template_dir = os.path.join(os.path.dirname(__file__), "../../templates/base_project")
        try:
            shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
            print(f'项目 "{project_name}" 创建成功')
        except Exception as e:
            print(f"创建项目出错: {e}")


        package_config_path = os.path.join(project_dir, 'idepy.json')
        with open(package_config_path, mode="r+", encoding='utf8') as f:
            data = f.read()
            data = json.loads(data)
            data['name'] = name
            data['author'] = author
            data['copyright'] = author
            data['description'] = description
            f.seek(0)
            f.truncate()

            data = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(data)
