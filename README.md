# APChinkin

本仓库包含两个脚本，一个是针对机场的青龙签到脚本，本脚本由于链接写死仅支持[最萌の云](https://www.cutecloud.net/)，当然去抓抓其他机场的签到链接进行替换，理论上支持所有机场。

另一个是[仓库](https://github.com/mrabit/aliyundriveDailyCheck)的阿里云签到脚本，机场签到脚本有一部分也是借鉴了这个脚本。

## 免责声明

* 本仓库发的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
* 本人无法100%保证使用本项目之后不会造成账号异常问题，若出现任何账号异常问题本人概不负责，请根据情况自行判断再下载执行！否则请勿下载运行！
* 如果任何单位或个人认为该项目的脚本可能涉及侵犯其权利，则应及时通知并提供相关证明，我将在收到认证文件后删除相关脚本。
* 任何以任何方式查看此项目的人或直接或间接使用本项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或本项目的规则，则视为您已接受此免责声明。

> 您使用或者复制了本仓库且本人制作的任何脚本，则视为 已接受 此声明，请仔细阅读

## 机场签到脚本

1. 拉取本站

    ```sh
    ql repo https://github.com/yunzimo/APChinkin "jichang|autoSignin|wzyd" "" "notify.py|QLApi.py|qlApi.js|sendNotify.js|env.js"
    ```

    青龙拉库命令解释：

    ```sh
    ql repo <repourl> <path> <blacklist> <dependence> <branch>
            <库地址>   <拉哪些> <不拉哪些> <依赖文件>    <分支>
    ```

2. 在系统设置中新建应用，名字随意，权限添加`环境变量`
3. 修改jichang.py中的`client_id`和`client_secret`，改为新建应用的值。
4. 新建环境变量`JC_Passwd`，值为`email=xxxx;passwd=xxxx`(你的邮箱和密码)
5. 新建环境变量`JC_COOKIE`，值随便填一个，脚本运行的时候会自动登录获取cookie

## 阿里云签到脚本

第一步：获取 refresh_token
自动获取: 登录阿里云盘后，控制台粘贴 JSON.parse(localStorage.token).refresh_token

![](https://raw.githubusercontent.com/yunzimo/APChinkin/main/assets/1.png)

第二步：青龙面板添加依赖项
axios

第三步：添加环境变量
refreshToken：阿里云盘的refresh_token, 添加多个可支持多账户签到

第四步：修改qlApi.js，填入创建的阿里云盘应用的client_id和client_secret