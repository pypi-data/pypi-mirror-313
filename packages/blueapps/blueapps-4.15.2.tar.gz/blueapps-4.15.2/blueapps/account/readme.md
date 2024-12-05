### Account 使用说明

blueapps.account 作为开发框架的登录模块，可解决各环境登录，自动跳转至 PASS 统一登录平台，完成登录认证，获取用户信息。

#### 申明 USER_MODEL

```
AUTH_USER_MODEL = 'account.User'
```

#### USER_MODEL 字段说明

* [a] username  
    用户唯一标识，在内部版为 RTX，在腾讯云为 openid
* [a] nickname
    用于前端展示的用户名，在内部版为 RTX，在腾讯云为 QQ 昵称
* [a] avatar_url
    用户头像 URL
* [m] get_full_name
    用于前端展示的完整用户名，在内部版为 rtx，腾讯云为 昵称


#### 添加统一登录中间件（WeixinLoginRequiredMiddleware 可选添加）

```
MIDDLEWARE = (
    # Auth middleware
    'blueapps.account.middlewares.WeixinLoginRequiredMiddleware',
    'blueapps.account.middlewares.LoginRequiredMiddleware',
)
```

#### 添加统一登录认证 Backend（WeixinBackend 可选添加）

```
AUTHENTICATION_BACKENDS = (
    'blueapps.account.backends.WeixinBackend',
    'blueapps.account.backends.UserBackend',
)
```

#### 登陆模块开发者可配置项
1. BLUEAPPS_SPECIFIC_REDIRECT_KEY 
对于登陆后重定向的页面链接，默认会重定向到跳转登陆页之前请求的页面。开发者可在settings中通过配置BLUEAPPS_SPECIFIC_REDIRECT_KEY来自定义重定向页面。

2. BLUEAPPS_ACCOUNT_XXX
对于每个环境，blueapps account模块会选择对应的登陆模块来进行登陆校验。
开发者可通过在settings中配置BLUEAPPS_ACCOUNT_XXX来进行登陆模块的自定义，该配置会覆盖默认的配置。如BLUEAPPS_ACCOUNT_IFRAME_WIDTH即可自定义登陆弹窗的宽度。

3. BLUEAPPS_AJAX_401_RESPONSE_FUNC BLUEAPPS_PAGE_401_RESPONSE_FUNC BLUEAPPS_PAGE_401_RESPONSE_PLATFORM_FUNC
开发者可通过在settings中配置对应的变量，指定对应的登陆401处理函数，函数需要支持request参数，返回对应函数Response。
