# PlayBook

YouQu 任务调度系统

## 安装

```bash
pip3 install youqu-playbook
```

## 运行

```bash
playbook -p path/to/json/file.json

# 如果提示找不到命令，请检查是否在 PATH 中添加了 Python 的 bin 目录。
export PATH=$PATH:$HOME/.local/bin
```

## 输入JSON配置文件

JSON 配置示例：
```json
{
  "apps": [
    {
      "app_name": "autotest_dde_file_manager",
      "git_url": "git_url",
      "git_branch": "at-develop/eagle",
      "framework": "youqu2",
      "split_run": true,
      "order": 1
    },
    {
      "app_name": "kernel",
      "git_url": "git_url",
      "git_branch": "at-develop/v25",
      "framework": "youqu3",
      "split_run": false,
      "order": 2
    },
    ...
  ],
  "clients": [
    "uos@10.8.xx.xx",
    "uos@10.8.xx.xx",
    ...
  ],
  "tags": "xxxx",
  "task_id": "xxxx",
  "json_backfill_base_url": "xxxx",
  "json_backfill_user": "xxxx",
  "json_backfill_password": "xxxx",
  "pms_task_id": "xxxx",
  "pms_user": "xxxx",
  "pms_password": "xxxx"
}
```

说明：
- `apps`: 应用列表，用于指定运行应用的应用。
  - `app_name`: 应用名称，对应 `app_name` 字段，用于区分应用，例如 `autotest_dde_file_manager`。
  - `git_url`: 应用 Git 仓库地址，用于下载应用代码。检查 `git_url` 是否正确，可以通过 `git clone ${git_url}` 命令进行验证。
  - `git_branch`: 应用 Git 分支，用于下载应用代码，例如 `at-develop/eagle`。
  - `framework`: 应用框架，用于区分应用框架，可选值有 `youqu2` 和 `youqu3`，分别对应 `youqu2` 和 `youqu3` 框架。
  - `split_run`: 是否启用多线程运行，boolean 类型， 默认为 `false`。
  - `order`: 应用运行顺序，int 类型，默认为 1。
- `clients`: 客户端列表，用于指定运行应用的客户端。
- `tags`: 任务标签，用于区分任务。
- `task_id`: 任务 ID，用于区分任务。
- `json_backfill_base_url`: 数据回填地址。
- `json_backfill_user`: 数据回填用户名。
- `json_backfill_password`: 数据回填密码。
- `pms_task_id`: PMS 任务 ID，用于获取任务。
- `pms_user`: PMS 用户名，用于获取任务。
- `pms_password`: PMS 密码，用于获取任务。

## 流程示意图

![](./images/playbook.png)