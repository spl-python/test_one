<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <div class="login-title">
                <img src="../../static/image/logo.png" alt="">
                <p>百知教育给你最优质的学习体验!</p>
            </div>
            <div class="login_box">
                <div class="title">
                    <span @click="login_type=0">密码登录</span>
                    <span @click="login_type=1">短信登录</span>
                </div>
                <div class="inp" v-if="login_type===0">
                    <input v-model='username' type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user">
                    <br><span id="err_name"></span>
                    <input v-model="password" type="password" name="" class="pwd" placeholder="密码">
                    <div id="geetest1"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" class="no" v-model="remember_me"/>
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <button class="login_btn btn btn-primary" @click="get_captcha">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/user/register/">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-else>
                    <input type="text" placeholder="手机号码" class="user" v-model="phone">
                    <span id="tip"></span>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
                        <div class="sms-btn" @click="get_code">{{ sms_text }}</div>
                        <br><span id="tips"></span>
                    </div>
                    <button class="login_btn" @click="get_captcha">登录</button>
                    <span class="go_login">没有账号
                    <router-link to="/register/">立即注册</router-link>
                </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Login",
    data() {
        return {
            username: '',
            password: '',
            remember_me: false,
            login_type: 0,
            sms_text: '获取验证码',
            phone: '',
            code: '',
            sms: '',
        }
    },
    methods: {
        // 短信
        get_code() {
            if (!/1[356789]\d{9}/.test(this.phone)) {
                this.$alert('警告:手机号格式有误')
                return false
            }

            this.$axios({
                url: this.$settings.HOST + 'user/message/',
                method: 'get',
                params: {
                    phone: this.phone
                }
            }).then(res => {
                console.log('code=', res.data);
                this.sms = res.data.code
            }).catch(res => {
                console.log(error);
            })
        },

        //(账户密码) 验证码
        handlerPopup(captchaObj) {
            let self = this;
            captchaObj.onSuccess(function () {
                let validate = captchaObj.getValidate();
                self.$axios({
                    url: self.$settings.HOST + 'user/captcha/',
                    method: 'post',
                    data: {
                        username: self.username,
                        geetest_challenge: validate.geetest_challenge,
                        geetest_validate: validate.geetest_validate,
                        geetest_seccode: validate.geetest_seccode
                    }
                }).then(res => {
                    console.log(res.data);
                    self.usr_login();
                }).catch(error => {
                    console.log(error);
                })
            })
            document.getElementById('geetest1').innerHTML = '';

            captchaObj.appendTo('#geetest1')
        },

        // 点击登录
        get_captcha() {
            let self = this;
            if (this.login_type === 0) {
                if (this.username === '') {
                    this.$message.error("账户不能为空")
                } else {
                    if (this.password === '') {
                        this.$message.error("密码不能为空")
                    } else {
                        this.$axios({
                            url: this.$settings.HOST + 'user/captcha/',
                            method: 'get',
                            params: {
                                username: this.username
                            }
                        }).then(res => {
                            console.log(res.data);

                            let data = JSON.parse(res.data)

                            initGeetest({
                                gt: data.gt,
                                challenge: data.challenge,
                                product: 'popup',
                                offline: !data.success,
                                new_captcha: data.new_captcha
                            }, this.handlerPopup);
                        }).catch(error => {
                            console.log(error);
                            document.getElementById('err_name').innerHTML = ''
                            this.$message.error("您输入的用户不存在")
                        })
                    }
                }
            } else {
                if (this.phone === '') {
                    // document.getElementById('tip').innerHTML='请输入手机号'
                    this.$alert('请输入手机号')
                } else if (!this.code) {
                    this.$alert('请输入验证码')
                } else {
                    if (this.code === this.sms) {
                        this.$alert('正在登陆,请稍后')
                        self.usr_login();
                    } else {
                        this.$alert('验证码错误')
                    }
                }
            }

        }
        ,
        usr_login() {
            if (this.login_type === 0) {
                this.$axios({
                    url: this.$settings.HOST + 'user/login/',
                    method: "post",
                    data: {
                        username: this.username,
                        password: this.password,
                    }
                }).then(res => {
                    console.log(res.data);
                    if (res.data.token) {
                        this.$message({
                            message: '恭喜登陆成功',
                            type: 'success',
                            duration: 1000,
                        })
                        sessionStorage.token = res.data.token;
                        sessionStorage.username = res.data.username;
                        sessionStorage.user_id = res.data.user_id;
                        if (this.remember_me) {
                            localStorage.username = this.username
                            localStorage.pwd = this.password
                        } else {
                            localStorage.clear()
                        }

                        this.$router.push("/")
                    }
                }).catch(error => {
                    this.$message.error("账号或密码错误，请重新输入")
                })
            }else{
                alert('进入captchalogin')
                this.$axios({
                    url:this.$settings.HOST+'user/captchalogin/',
                    methods:'post',
                    data(){
                        return {
                            phone: this.phone,

                        }
                    },
                    params:{
                        code:this.code
                    }

                }).then(res => {
                    console.log(res.data);
                    sessionStorage.token = res.data.token;
                    sessionStorage.username = res.data.username;
                    sessionStorage.user_id = res.data.user_id;
                    this.$router.push("/")
                }).catch(error => {
                    console.log(error);
                    this.$message.error(error)
                })
            }
        }
    }
}
</script>

<style scoped>
.box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.box img {
    width: 100%;
    min-height: 100%;
}

.box .login {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
}

.login .login-title {
    width: 100%;
    text-align: center;
}

.login-title img {
    width: 190px;
    height: auto;
}

.login-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.login_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.login_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}

.login_box .title span:nth-of-type(1) {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp {
    width: 350px;
    margin: 0 auto;
}

.inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp input.user {
    margin-bottom: 16px;
}

.inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}

.inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

}

.sms-box {
    position: relative;
}

#geetest {
    margin-top: 20px;
}

.sms-btn {
    font-size: 14px;
    color: #ffc210;
    letter-spacing: .26px;
    position: absolute;
    right: 16px;
    top: 10px;
    cursor: pointer;
    overflow: hidden;
    background: #fff;
    border-left: 1px solid #484848;
    padding-left: 16px;
    padding-bottom: 4px;
}

.login_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}

.inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}

.inp .go_login span {
    color: #84cc39;
    cursor: pointer;
}
</style>
