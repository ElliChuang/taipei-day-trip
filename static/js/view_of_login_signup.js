login_signup =  '<div class="outer" id="outer">\
                    <div class="login" id="login">\
                        <div class="loginHead"></div>\
                        <div class="loginBody">\
                            <div class="loginTitle">\
                                <div>登入會員帳號</div>\
                                <button type="submit" onclick="closeView()">\
                                    <img src="/static/image/icon_close.png">\
                                </button>\
                            </div>\
                            <div class="form" id="loginForm">\
                                <input type="email" name="loginEmail" id="loginEmail" placeholder="輸入電子信箱" required/>\
                                <input type="password" name="loginPassword" id="loginPassword" placeholder="輸入密碼" required pattern="[A-Za-z0-9]{6,}" title="請輸入至少６個英文字母、數字或符號"/>\
                                <button onclick="memberLogin()">登入帳戶</button>\
                                <div class="loginMessage" id="loginMessage"></div>\
                            </div>\
                            <div class="loginRemind">還沒有帳戶？<span onclick="goSignUp()">點此註冊</span></div>\
                        </div>\
                    </div>\
                    <div class="signup" id="signup">\
                        <div class="signupHead"></div>\
                        <div class="signupBody">\
                            <div class="signupTitle">\
                                <div>註冊會員帳號</div>\
                                <button type="submit" onclick="closeView()">\
                                    <img src="/static/image/icon_close.png">\
                                </button>\
                            </div>\
                            <div class="form" id="signUpForm">\
                                <input type="text" name="signUpName" id="signUpName" placeholder="輸入姓名" required title="請輸入姓名"/>\
                                <input type="email" name="signUpEmail" id="signUpEmail" placeholder="輸入電子郵件" required />\
                                <input type="password" name="signUpPassword" id="signUpPassword" placeholder="輸入密碼" required pattern="[A-Za-z0-9]{6,}" title="請輸入至少６個英文字母、數字或符號"/>\
                                <button onclick="signUp()" > 註冊新帳戶</button>\
                                <div class="signUpMessage" id="signUpMessage"></div>\
                            </div>\
                            <div class="signupRemind">還沒有帳戶了？<span onclick="goLogin()">點此登入</span></div>\
                        </div>\
                    </div>\
                </div>';   

document.write(login_signup);