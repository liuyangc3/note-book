# multiple tasks
`ctrl` + `shift` + `P`,chose configure task to add a task.json,change it blow
```
{
    "version": "0.1.0",
    "command": "cmd", 
    "isShellCommand": true,
    "showOutput": "silent",
    "args": ["/C"],
    "showOutput": "always",
    "tasks": [
        {
            "taskName": "Build Type Script",
            "suppressTaskName": true,
            "isBuildCommand": true,
            "args": ["tsc -p ."]
        },
        {
            "taskName": "Run Type Script",
            "suppressTaskName": true,
            "isBuildCommand": true,
            "args": ["ts-node", "${file}"]
        },
        {
            "taskName": "Run Python Script",
            "suppressTaskName": true,
            "isBuildCommand": true,
            "args": ["c:\\Python27\\python.exe", "-u", "${file}"]
        }
    ]
}
```
shortcut for tasks, overwrite default `ctrl` + `shift` + `B`
```
{ "key": "ctrl+shift+b",          "command": "workbench.action.tasks.runTask" } 
```
