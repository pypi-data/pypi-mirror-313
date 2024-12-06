s = """
<html translate="no"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,width=device-width,viewport-fit=cover"><meta http-equiv="Content-Security-Policy" content="default-src 'self' blob: data: https://vm.gtimg.cn https://*.tencentcos.cn https://hunyuan-bot-qa-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-bot-prod-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-test-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-prod-125834470.cos.ap-guangzhou.myqcloud.com https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com https://cdn.jsdelivr.net https://*.tencent.com https://*.qq.com https://*.hunyuan.woa.com https://captcha.gtimg.com http://127.0.0.1:* http://localhost:* https://captcha.gtimg.com https://t.captcha.qq.com 'unsafe-inline' 'unsafe-eval' data:; img-src https://* http://* 'self' data: blob: http://127.0.0.1:* http://localhost:*; connect-src 'self' https://*.qq.com https://43.140.59.57 https://app-pre.tchy.net https://hunyuan.tencent.com https://yuanbao.test.hunyuan.woa.com:8080 ws://43.140.59.57:8008 https://yuanqi.tencent.com ws: https://hunyuan-bot-qa-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-bot-prod-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-test-1258344703.cos.ap-guangzhou.myqcloud.com https://hunyuan-prod-125834470.cos.ap-guangzhou.myqcloud.com https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com https://cdn-bot.hunyuan.tencent.com https://aegis.qq.com https://v.qq.com https://api.fy.qq.com http://127.0.0.1:* http://localhost:* https://*.hunyuan.woa.com https://*.hunyuan.tencent.com https://open.test.hunyuna.woa.com https://open.test2.hunyuan.woa.com https://*.aida.qq.com https://xj-psd-1258344703.cos.ap-guangzhou.myqcloud.com https://code-interpreter-1258344706.cos.ap-guangzhou.myqcloud.com https://hy-app-translate-1258344703.cos.ap-guangzhou.myqcloud.com https://asr.cloud.tencent.com https://*.tencent.com https://hunyuan-plugin-gz-1258344706.cos.ap-guangzhou.myqcloud.com https://hunyuan-plugin-nj-1258344706.cos.ap-nanjing.myqcloud.com https://hunyuan-plugin-1258344706.cos.ap-nanjing.myqcloud.com hunyuan-base-test-1258344703.cos.ap-guangzhou.myqcloud.com hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com https://*.tencentcos.cn cdn-test.yuanqi.tencent.com cdn.yuanqi.tencent.com pcg-pdf-1258344706.cos.ap-nanjing.myqcloud.com wvjbscheme://* https://servicewechat.com; child-src blob:; worker-src 'self'; frame-src *.woa.com *.tencent.com https://*.qq.com webcompt: hunyuan-test-1258344703.cos.ap-guangzhou.myqcloud.com view.officeapps.live.com hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com wvjbscheme://* zhuanhuabao-5gqf84946751a1cb-1300912497.tcloudbaseapp.com; media-src 'self' blob: data: https://*;"><title>腾讯元宝</title><meta name="Keywords" content="增强大模型,AIGC,智能客服,腾讯AIGC,腾讯元宝,腾讯元宝app,AI产品,AI工具,AI助手,AI搜索,AI解析,AI写作,AI画图,AI写真,AI头像,腾讯混元app,AI大模型,AI聊天,AI问答,AI口语,AI创作,AIGC,腾讯AIGC,腾讯混元,腾讯混元大模型,腾讯大模型"><script>(function() {
      function checkBrowserVersion() {
        var userAgent = navigator.userAgent;
        var temp;

        // 放开百度搜索
        if (userAgent.indexOf("Baiduspider/") > -1) {
          return true;
        }

        // 搜狗使用的chrome内核版本为80
        if (userAgent.indexOf("SGWebviewClient/") > -1) {
          return true; // 放开搜狗
        }

        if (userAgent.indexOf("wxwork/") > -1) {
          return true; // 放开企微 webview
        }

        // 检测Edge
        var isEdge = userAgent.indexOf("Edg/") > -1;
        if (isEdge) {
            temp = userAgent.match(/Edg\/(\d+)/);
            if (temp && temp.length > 1) {
                return parseInt(temp[1], 10) >= 84;
            }
        }

        // 检测Firefox
        var isFirefox = userAgent.indexOf("Firefox/") > -1;
        if (isFirefox) {
            temp = userAgent.match(/Firefox\/(\d+)/);
            if (temp && temp.length > 1) {
                return parseInt(temp[1], 10) >= 83;
            }
        }

        // 检测Chrome
        var isChrome = userAgent.indexOf("Chrome/") > -1 && userAgent.indexOf("Edg/") === -1; // 排除Edge
        if (isChrome) {
            temp = userAgent.match(/Chrome\/(\d+)/);
            if (temp && temp.length > 1) {
                return parseInt(temp[1], 10) >= 84;
            }
        }

        // 检测Safari
        var isSafari = userAgent.indexOf("Safari/") > -1 && userAgent.indexOf("Chrome/") === -1; // 排除Chrome
        if (isSafari) {
            temp = userAgent.match(/Version\/(\d+\.\d+)/);
            if (temp && temp.length > 1) {
                return parseFloat(temp[1]) >= 14.1;
            }
        }

        if (!!navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|IEMobile)/i)) {
          // 没匹配到的移动端检测 replaceAll
          return typeof String.prototype.replaceAll === "function";
        } else {
          // 没匹配到的PC端
          return -1;
        }
      }

      var checkBrowser = checkBrowserVersion();

      if (checkBrowser === -1) {
        window.location.replace('/browser-support.html');
      } else if (!checkBrowser) {
        window.location.replace('/browser-upgrade.html');
      }
    })();</script><link rel="icon" href="https://cdn-bot.hunyuan.tencent.com/logo.png"><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/runtime.f2a8107760be97bb37fd.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/lib.dfa3c745ccfde1bcc76e.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/widget.ea6afbbc65e311b06e08.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/vendor.1803cfc23577a1aa7cd6.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/7228.b3955a8230eca4c4623a.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/6476.536a990d40139a6c9d1c.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/5277.5799030d635db7392df2.js"></script><script defer="defer" src="https://cdn-bot.hunyuan.tencent.com/index.0daebd6cb2c6ccd00d83.js"></script><link href="https://cdn-bot.hunyuan.tencent.com/lib.a625d82672d245a1a931.css" rel="stylesheet"><link href="https://cdn-bot.hunyuan.tencent.com/vendor.a625d82672d245a1a931.css" rel="stylesheet"><link href="https://cdn-bot.hunyuan.tencent.com/index.a625d82672d245a1a931.css" rel="stylesheet"><link rel="stylesheet" type="text/css" href="https://cdn-bot.hunyuan.tencent.com/component.a625d82672d245a1a931.css"><link rel="stylesheet" type="text/css" href="https://cdn-bot.hunyuan.tencent.com/6730.a625d82672d245a1a931.css"><style id="__TDESIGN_ICON_STYLE__">@keyframes t-spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  .t-icon {
    display: inline-block;
    vertical-align: middle;
    width: 1em;
    height: 1em;
  }
  .t-icon::before {
    font-family: unset;
  }
  .t-icon-loading {
    animation: t-spin 1s linear infinite;
  }
  .t-icon {
    fill: currentColor;
  }
  .t-icon.t-size-s,
  i.t-size-s {
    font-size: 14px;
  }
  .t-icon.t-size-m,
  i.t-size-m {
    font-size: 16px;
  }
  .t-icon.t-size-l,
  i.t-size-l {
    font-size: 18px;
  }
  </style><style data-id="immersive-translate-input-injected-css">.immersive-translate-input {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  z-index: 2147483647;
  display: flex;
  justify-content: center;
  align-items: center;
}
.immersive-translate-attach-loading::after {
  content: " ";

  --loading-color: #f78fb6;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: block;
  margin: 12px auto;
  position: relative;
  color: white;
  left: -100px;
  box-sizing: border-box;
  animation: immersiveTranslateShadowRolling 1.5s linear infinite;

  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-2000%, -50%);
  z-index: 100;
}

.immersive-translate-loading-spinner {
  vertical-align: middle !important;
  width: 10px !important;
  height: 10px !important;
  display: inline-block !important;
  margin: 0 4px !important;
  border: 2px rgba(221, 244, 255, 0.6) solid !important;
  border-top: 2px rgba(0, 0, 0, 0.375) solid !important;
  border-left: 2px rgba(0, 0, 0, 0.375) solid !important;
  border-radius: 50% !important;
  padding: 0 !important;
  -webkit-animation: immersive-translate-loading-animation 0.6s infinite linear !important;
  animation: immersive-translate-loading-animation 0.6s infinite linear !important;
}

@-webkit-keyframes immersive-translate-loading-animation {
  from {
    -webkit-transform: rotate(0deg);
  }

  to {
    -webkit-transform: rotate(359deg);
  }
}

@keyframes immersive-translate-loading-animation {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(359deg);
  }
}


.immersive-translate-input-loading {
  --loading-color: #f78fb6;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: block;
  margin: 12px auto;
  position: relative;
  color: white;
  left: -100px;
  box-sizing: border-box;
  animation: immersiveTranslateShadowRolling 1.5s linear infinite;
}

@keyframes immersiveTranslateShadowRolling {
  0% {
    box-shadow: 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  12% {
    box-shadow: 100px 0 var(--loading-color), 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  25% {
    box-shadow: 110px 0 var(--loading-color), 100px 0 var(--loading-color), 0px 0 rgba(255, 255, 255, 0), 0px 0 rgba(255, 255, 255, 0);
  }

  36% {
    box-shadow: 120px 0 var(--loading-color), 110px 0 var(--loading-color), 100px 0 var(--loading-color), 0px 0 rgba(255, 255, 255, 0);
  }

  50% {
    box-shadow: 130px 0 var(--loading-color), 120px 0 var(--loading-color), 110px 0 var(--loading-color), 100px 0 var(--loading-color);
  }

  62% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 130px 0 var(--loading-color), 120px 0 var(--loading-color), 110px 0 var(--loading-color);
  }

  75% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0), 130px 0 var(--loading-color), 120px 0 var(--loading-color);
  }

  87% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0), 130px 0 var(--loading-color);
  }

  100% {
    box-shadow: 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0), 200px 0 rgba(255, 255, 255, 0);
  }
}


.immersive-translate-search-recomend {
  border: 1px solid #dadce0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  position: relative;
  font-size: 16px;
}

.immersive-translate-search-enhancement-en-title {
  color: #4d5156;
}



.immersive-translate-search-settings {
  position: absolute;
  top: 16px;
  right: 16px;
  cursor: pointer;
}

.immersive-translate-search-recomend::before {
  /* content: " "; */
  /* width: 20px; */
  /* height: 20px; */
  /* top: 16px; */
  /* position: absolute; */
  /* background: center / contain url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAxlBMVEUAAADpTInqTIjpSofnSIfqS4nfS4XqS4nqTIjsTYnrTInqTIroS4jvQIDqTIn////+/v7rSYjpTIn8/v7uaZzrTIr9/f3wfansWJL88/b85e73qc39+/v3xNnylrvrVI/98fb62Obva5/8+fr76vH4y9zpSIj74e353Oj1ocTzm77xhK/veKbtYpjsXJTqU47oTInxjrXyh7L99fj40eH2ttH1udD3sc31ssz1rMnykLXucqPtbqD85e/1xdn2u9DzqcXrUY6FaJb8AAAADnRSTlMA34BgIM8Q37/fz7+/EGOHcVQAAAGhSURBVDjLhZPncuowEEZFTW7bXVU7xsYYTO/p7bb3f6lICIOYJOT4h7/VnFmvrBFjrF3/CR/SajBHswafctG0Qg3O8O0Xa8BZ6uw7eLjqr30SofCDVSkemMinfL1ecy20r5ygR5zz3ArcAqJExPTPKhDENEmS30Q9+yo4lEQkqVTiIEAHCT10xWERRdH0Bq0aCOPZNDV3s0xaYce1lHEoDHU8wEh3qRJypNcTAeKUIjgKMeGLDoRCLVLTVf+Ownj8Kk6H9HM6QXPgYjQSB0F00EJEu10ILQrs/QeP77BSSr0MzLOyuJJQbnUoOOIUI/A8EeJk9E4YUHUWiRyTVKGgQUB8/3e/NpdGlfI+FMQyWsCBWyz4A/ZyHXyiiz0Ne5aGZssoxRmcChw8/EFKQ5JwwkUo3FRT5yXS7q+Y/rHDZmFktzpGMvO+5QofA4FPpEmGw+EWRCFvnaof7Zhe8NuYSLR0xErKLThUSs8gnODh87ssy6438yzbLzxl012HS19vfCf3CNhnbWOL1eEsDda+gDPUvri8tSZzNFrwIZf1NmNvqC1I/t8j7nYAAAAASUVORK5CYII='); */
}

.immersive-translate-search-title {}

.immersive-translate-search-title-wrapper {}

.immersive-translate-search-time {
  font-size: 12px;
  margin: 4px 0 24px;
  color: #70757a;
}

.immersive-translate-expand-items {
  display: none;
}

.immersive-translate-search-more {
  margin-top: 16px;
  font-size: 14px;
}

.immersive-translate-modal {
  display: none;
  position: fixed;
  z-index: 2147483647;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
  font-size: 15px;
}

.immersive-translate-modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 40px 24px 24px;
  border: 1px solid #888;
  border-radius: 10px;
  width: 80%;
  max-width: 270px;
  font-family: system-ui, -apple-system, "Segoe UI", "Roboto", "Ubuntu",
    "Cantarell", "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol", "Noto Color Emoji";
  position: relative
}

@media screen and (max-width: 768px) {
  .immersive-translate-modal-content {
    margin: 50% auto !important;
  }
}

.immersive-translate-modal .immersive-translate-modal-content-in-input {
  max-width: 500px;
}
.immersive-translate-modal-content-in-input .immersive-translate-modal-body {
  text-align: left;
  max-height: unset;
}

.immersive-translate-modal-title {
  text-align: center;
  font-size: 16px;
  font-weight: 700;
  color: #333333;
}

.immersive-translate-modal-body {
  text-align: center;
  font-size: 14px;
  font-weight: 400;
  color: #333333;
  word-break: break-all;
  margin-top: 24px;
}

@media screen and (max-width: 768px) {
  .immersive-translate-modal-body {
    max-height: 250px;
    overflow-y: auto;
  }
}

.immersive-translate-close {
  color: #666666;
  position: absolute;
  right: 16px;
  top: 16px;
  font-size: 20px;
  font-weight: bold;
}

.immersive-translate-close:hover,
.immersive-translate-close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.immersive-translate-modal-footer {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 24px;
}

.immersive-translate-btn {
  width: fit-content;
  color: #fff;
  background-color: #ea4c89;
  border: none;
  font-size: 16px;
  margin: 0 8px;
  padding: 9px 30px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.immersive-translate-btn:hover {
  background-color: #f082ac;
}
.immersive-translate-btn:disabled{
  opacity: 0.6;
  cursor: not-allowed;
}
.immersive-translate-btn:disabled:hover{
  background-color: #ea4c89;
}

.immersive-translate-cancel-btn {
  /* gray color */
  background-color: rgb(89, 107, 120);
}


.immersive-translate-cancel-btn:hover {
  background-color: hsl(205, 20%, 32%);
}

.immersive-translate-action-btn {
  background-color: transparent;
  color: #EA4C89;
  border: 1px solid #EA4C89
}

.immersive-translate-btn svg {
  margin-right: 5px;
}

.immersive-translate-link {
  cursor: pointer;
  user-select: none;
  -webkit-user-drag: none;
  text-decoration: none;
  color: #007bff;
  -webkit-tap-highlight-color: rgba(0, 0, 0, .1);
}

.immersive-translate-primary-link {
  cursor: pointer;
  user-select: none;
  -webkit-user-drag: none;
  text-decoration: none;
  color: #ea4c89;
  -webkit-tap-highlight-color: rgba(0, 0, 0, .1);
}

.immersive-translate-modal input[type="radio"] {
  margin: 0 6px;
  cursor: pointer;
}

.immersive-translate-modal label {
  cursor: pointer;
}

.immersive-translate-close-action {
  position: absolute;
  top: 2px;
  right: 0px;
  cursor: pointer;
}

.imt-image-status {
  background-color: rgba(0, 0, 0, 0.50) !important;
  display: flex !important;
  flex-direction: column !important; 
  align-items: center !important;
  justify-content: center !important;
  border-radius: 16px !important;
}
.imt-image-status img,.imt-image-status svg, .imt-img-loading {
  width: 28px !important;
  height: 28px !important;
  margin: 0 0 8px 0 !important;
  min-height: 28px !important;
  min-width: 28px !important;
}
.imt-img-loading {
  background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAMAAACfWMssAAAAtFBMVEUAAAD////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////oK74hAAAAPHRSTlMABBMIDyQXHwyBfFdDMSw+OjXCb+5RG51IvV/k0rOqlGRM6KKMhdvNyZBz9MaupmxpWyj437iYd/yJVNZeuUC7AAACt0lEQVRIx53T2XKiUBCA4QYOiyCbiAsuuGBcYtxiYtT3f6/pbqoYHVFO5r+iivpo6DpAWYpqeoFfr9f90DsYAuRSWkFnPO50OgR9PwiCUFcl2GEcx+N/YBh6pvKaefHlUgZd1zVe0NbYcQjGBfzrPE8Xz8aF+71D8gG6DHFPpc4a7xFiCDuhaWgKgGIJQ3d5IMGDrpS4S5KgpIm+en9f6PlAhKby4JwEIxlYJV9h5k5nee9GoxHJ2IDSNB0dwdad1NAxDJ/uXDHYmebdk4PdbkS58CIVHdYSUHTYYRWOJblWSyu2lmy3KNFVJNBhxcuGW4YBVCbYGRZwIooipHsNqjM4FbgOQqQqSKQQU9V8xmi1QlgHqQQ6DDBvRUVCDirs+EzGDGOQTCATgtYTnbCVLgsVgRE0T1QE0qHCFAht2z6dLvJQs3Lo2FQoDxWNUiBhaP4eRgwNkI+dAjVOA/kUrIDwf3CG8NfNOE0eiFotSuo+rBiq8tD9oY4Qzc6YJw99hl1wzpQvD7ef2M8QgnOGJfJw+EltQc+oX2yn907QB22WZcvlUpd143dqQu+8pCJZuGE4xCuPXJqqcs5sNpsI93Rmzym1k4Npk+oD1SH3/a3LOK/JpUBpWfqNySxWzCfNCUITuDG5dtuphrUJ1myeIE9bIsPiKrfqTai5WZxbhtNphYx6GEIHihyGFTI69lje/rxajdh0s0msZ0zYxyPLhYCb1CyHm9Qsd2H37Y3lugVwL9kNh8Ot8cha6fUNQ8nuXi5z9/ExsAO4zQrb/ev1yrCB7lGyQzgYDGuxq1toDN/JGvN+HyWNHKB7zEoK+PX11e12G431erGYzwmytAWU56fkMHY5JJnDRR2eZji3AwtIcrEV8Cojat/BdQ7XOwGV1e1hDjGGjXbdArm8uJZtCH5MbcctVX8A1WpqumJHwckAAAAASUVORK5CYII=");
  background-size: 28px 28px;
  animation: image-loading-rotate 1s linear infinite !important;
}

.imt-image-status span {
  color: var(--bg-2, #FFF) !important;
  font-size: 14px !important;
  line-height: 14px !important;
  font-weight: 500 !important;
}

@keyframes image-loading-rotate {
  from {
    transform: rotate(360deg);
  }
  to {
    transform: rotate(0deg);
  }
}
</style><style>wc-waterfall{position:relative;display:block;box-sizing:border-box!important;overflow:unset!important}wc-waterfall>*{position:absolute;box-sizing:border-box}</style></head><body id="hunyuan-bot" class="agent-layout-V3"><div id="app"><div class="agent-layout layout-pc"><div class="agent-layout__nav nav-pc is-expand-nav"><div class="agent-layout__nav__content"><div class="agent-layout__nav__list"><div class="agent-layout__nav__logo"><span class="logo__title">腾讯元宝</span><div class="agent-layout__nav__collapse"><svg width="17" height="17" viewBox="0 0 17 17" fill="none" xmlns="http://www.w3.org/2000/svg"><g opacity="0.6"><path d="M5.35156 8.5H15.3516" stroke="#333333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M9.09347 13.1559L4.4375 8.49981L9.09347 3.84375" stroke="#333333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><rect x="0.351562" y="2.5" width="1.5" height="12" rx="0.75" fill="#333333"></rect></g></svg></div></div><div class="agent-layout__nav__list__item"><img src="https://xj-psd-1258344703.cos.ap-guangzhou.myqcloud.com/image/hunyuan/brand2024/logo64@3x.png" alt=""><div class="agent-layout__nav__list__item__name">元宝<div class="yuanbao-agent-operate"><div class="agent-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div></div></div></div><div class="agent-layout__nav__list__item"><svg width="24" height="24" viewBox="0 0 25 24" fill="none"><rect x="0.0649414" width="24" height="24" rx="12" fill="url(#paint0_linear_5996_106080)"></rect><path d="M15.4149 13.0918C15.429 13.0641 15.4505 13.0409 15.477 13.0248C15.5035 13.0086 15.5339 13 15.5649 13C15.596 13 15.6264 13.0086 15.6529 13.0248C15.6794 13.0409 15.7009 13.0641 15.715 13.0918L16.2091 14.0533C16.3863 14.3983 16.6671 14.679 17.0121 14.8563L17.9732 15.3504C18.0008 15.3645 18.024 15.386 18.0402 15.4125C18.0564 15.4389 18.0649 15.4694 18.0649 15.5004C18.0649 15.5315 18.0564 15.5619 18.0402 15.5884C18.024 15.6148 18.0008 15.6363 17.9732 15.6505L17.0116 16.1442C16.6667 16.3214 16.3859 16.6022 16.2087 16.9471L15.715 17.9082C15.7009 17.9359 15.6794 17.9591 15.6529 17.9752C15.6264 17.9914 15.596 18 15.5649 18C15.5339 18 15.5035 17.9914 15.477 17.9752C15.4505 17.9591 15.429 17.9359 15.4149 17.9082L14.9208 16.9467C14.7436 16.602 14.463 16.3213 14.1182 16.1442L13.1567 15.6501C13.1291 15.6359 13.1059 15.6144 13.0897 15.5879C13.0735 15.5615 13.0649 15.531 13.0649 15.5C13.0649 15.469 13.0735 15.4385 13.0897 15.4121C13.1059 15.3856 13.1291 15.3641 13.1567 15.3499L14.1182 14.8558C14.463 14.6787 14.7436 14.398 14.9208 14.0533L15.4149 13.0918Z" fill="white"></path><path d="M9.82485 6.14681C9.84747 6.10261 9.88187 6.06552 9.92423 6.03961C9.96659 6.01371 10.0153 6 10.0649 6C10.1146 6 10.1633 6.01371 10.2057 6.03961C10.248 6.06552 10.2824 6.10261 10.305 6.14681L11.0956 7.68529C11.3791 8.23721 11.8284 8.68647 12.3803 8.97002L13.9181 9.76057C13.9623 9.7832 13.9994 9.81759 14.0253 9.85995C14.0512 9.90232 14.0649 9.95101 14.0649 10.0007C14.0649 10.0503 14.0512 10.099 14.0253 10.1414C13.9994 10.1837 13.9623 10.2181 13.9181 10.2408L12.3797 11.0306C11.8277 11.3142 11.3785 11.7635 11.0949 12.3154L10.305 13.8532C10.2824 13.8974 10.248 13.9345 10.2057 13.9604C10.1633 13.9863 10.1146 14 10.0649 14C10.0153 14 9.96659 13.9863 9.92423 13.9604C9.88187 13.9345 9.84747 13.8974 9.82485 13.8532L9.03429 12.3147C8.75081 11.7631 8.3018 11.3141 7.75023 11.0306L6.21175 10.2401C6.16755 10.2175 6.13046 10.1831 6.10455 10.1407C6.07865 10.0983 6.06494 10.0497 6.06494 10C6.06494 9.95034 6.07865 9.90165 6.10455 9.85929C6.13046 9.81692 6.16755 9.78253 6.21175 9.7599L7.75023 8.96935C8.3018 8.68587 8.75081 8.23686 9.03429 7.68529L9.82485 6.14681Z" fill="white"></path><defs><linearGradient id="paint0_linear_5996_106080" x1="-1.97096" y1="-9.29523e-08" x2="24.0649" y2="26.3884" gradientUnits="userSpaceOnUse"><stop stop-color="#FFD25E"></stop><stop offset="0.333333" stop-color="#E199DC"></stop><stop offset="0.666667" stop-color="#9986FF"></stop><stop offset="1" stop-color="#6DC9FF"></stop></linearGradient></defs></svg><div class="agent-layout__nav__list__item__name">发现</div></div><div class="t-divider t-divider--horizontal" style="margin: 0px 0px 12px; border-top: 0.5px solid rgb(238, 238, 238);"></div></div><div class="agent-layout__nav__sidebar agent-layout__nav__sidebar-overflow"><div><div class="agent-dialogue__sider-container"><div class="agent-dialogue__sider-wrapper"><div class="agent-dialogue__sider"><div class="latest-nav"><div class="agent-dialogue__sider__list"><div><div class="agent-dialogue__sider__item agent-dialogue__sider__item--active agent-dialogue__sider__item--isexpand"><div class="agent-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div><div class="agent-dialogue__sider__item-start"><img src="https://hy-openapi-public-1258344703.cos.ap-nanjing.myqcloud.com/app/icon/gtcnTp5C1G_icon.png" alt=""></div><div class="agent-dialogue__sider__item-end"><div class="agent-dialogue__sider__item__title"><span class="agent-dialogue__sider__item__text">创意绘画</span></div></div></div></div></div></div></div></div><div class="t-divider t-divider--horizontal" style="margin: 12px 0px; border-top: 0.5px solid rgb(238, 238, 238);"></div></div><div class="chat-history-list"><div class="chat-history-list__item_header" style="margin-bottom: 0px;"><span class="chat-history-list__item_header-left">对话历史</span></div><div class="t-checkbox-group" style="width: 100%; flex: 1 1 0%; overflow: hidden;"><div class="all-chat-history-list-wrapper"><div class="chat-history-list__item_header chat-history-list__item_header-expand">近7天</div><div class=""><label tabindex="0" class="t-checkbox" style="display: none;"><input type="checkbox" class="t-checkbox__former" tabindex="-1" data-value="'08f98d3e-fe46-414f-87d6-374b3b1b1bf5'" value="08f98d3e-fe46-414f-87d6-374b3b1b1bf5"><span class="t-checkbox__input"></span></label><div class="conv-list-item"><div class="conv-list-item__title_wrapper"><p class="conv-list-item__title">a dog</p><div class="conv-list-item-sidbar__operate"><div class="convlist-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div></div></div><div class="conv-list-item__title_wrapper"><p class="conv-list-item__agent_name">元宝</p></div></div></div><div class=""><label tabindex="0" class="t-checkbox" style="display: none;"><input type="checkbox" class="t-checkbox__former" tabindex="-1" data-value="'5e15b222-e2ae-4a16-a56d-6f1914e62568'" value="5e15b222-e2ae-4a16-a56d-6f1914e62568"><span class="t-checkbox__input"></span></label><div class="conv-list-item"><div class="conv-list-item__title_wrapper"><p class="conv-list-item__title">画条狗</p><div class="conv-list-item-sidbar__operate"><div class="convlist-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div></div></div><div class="conv-list-item__title_wrapper"><p class="conv-list-item__agent_name">创意绘画</p></div></div></div><div class=""><label tabindex="0" class="t-checkbox" style="display: none;"><input type="checkbox" class="t-checkbox__former" tabindex="-1" data-value="'bf440996-dcdc-405b-8451-8bf1c55ec028'" value="bf440996-dcdc-405b-8451-8bf1c55ec028"><span class="t-checkbox__input"></span></label><div class="conv-list-item"><div class="conv-list-item__title_wrapper"><p class="conv-list-item__title">11</p><div class="conv-list-item-sidbar__operate"><div class="convlist-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div></div></div><div class="conv-list-item__title_wrapper"><p class="conv-list-item__agent_name">元宝</p></div></div></div><div class=""><label tabindex="0" class="t-checkbox" style="display: none;"><input type="checkbox" class="t-checkbox__former" tabindex="-1" data-value="'312a9291-5329-43f5-b0e5-e1b98ba71563'" value="312a9291-5329-43f5-b0e5-e1b98ba71563"><span class="t-checkbox__input"></span></label><div class="conv-list-item"><div class="conv-list-item__title_wrapper"><p class="conv-list-item__title">sas</p><div class="conv-list-item-sidbar__operate"><div class="convlist-dialogue__sider__action__trigger" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9C2.44775 9 2 8.55228 2 8C2 7.44772 2.44775 7 3 7C3.55225 7 4 7.44772 4 8C4 8.55228 3.55225 9 3 9Z" fill="currentColor"></path><path d="M7 8C7 8.55228 7.44775 9 8 9C8.55225 9 9 8.55228 9 8C9 7.44772 8.55225 7 8 7C7.44775 7 7 7.44772 7 8Z" fill="currentColor"></path><path d="M12 8C12 8.55228 12.4478 9 13 9C13.5522 9 14 8.55228 14 8C14 7.44772 13.5522 7 13 7C12.4478 7 12 7.44772 12 8Z" fill="currentColor"></path></svg></div></div></div><div class="conv-list-item__title_wrapper"><p class="conv-list-item__agent_name">元宝</p></div></div></div></div></div></div><div class="chat-history-list__goto_view_all">查看全部对话<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><g opacity="0.6"><path d="M14 8H2" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"></path><path d="M10 4L14 8L10 12" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"></path></g></svg></div></div></div></div><div class="agent-layout__nav__extra"><div class="t-divider t-divider--horizontal" style="margin: 0px; border-top: 0.5px solid rgb(238, 238, 238);"></div><div class="user-bottom"><div class="agent-layout__nav__extra__wrapper"><div class="agent-layout__nav__extra__item"><span class="icon iconfont icon-phone agent-layout__nav__extra__item-icon" style="font-size: 18px;"></span></div><div class="agent-layout__nav__extra__item "><span class="icon iconfont icon-set agent-layout__nav__extra__item-icon" style="font-size: 20px;"></span></div></div><div class="agent-layout__nav__extra__item agent-layout__nav__extra__item--mine"><div class="t-avatar t-avatar--circle" style="width: 24px; height: 24px; font-size: 12px;"><div class="t-image__wrapper t-image__wrapper--shape-square" style="width: 24px; height: 24px;"><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icibGVnP2Qo2gVLIXSIkBQ1Aob9ktA0doRlj8XR2A1g23rAsRuoJMYEmHSaeib9gdVrUSo8VT01bO2vLKjEtBzBBu1vFEzgK0mwmbicL95NCFUs/132" class="t-image t-image--fit-cover t-image--position-center" alt="avatar"></div></div><span class="user-nickname">Betterme</span></div></div></div></div><div class="agent-layout__content"><div class="agent-dialogue"><div class="agent-dialogue__content-wrapper"><div class="agent-dialogue__content"><div class="agent-dialogue__content--common agent-dialogue__content--common-new"><div class="agent-dialogue__content--common__header "><div class="agent-dialogue__content--common__header__name"><span class="agent-dialogue__content--common__header__name__title">创意绘画</span></div></div><div class="agent-dialogue__content--common__content"><div class="agent-chat__list t2i-agent-list-content"><div class="agent-chat__list__indicator"><div class="agent-chat__list__indicator__content"><div class="agent-chat__list__indicator__button">点击全选以下消息</div></div></div><div class="agent-chat__list__content-wrapper"><div class="agent-chat__list__content"><div class="agent-chat__list__placeholder"></div><div class="agent-chat__list__item agent-chat__list__item--last"><div class="agent-chat__list__item__content"><div class="agent-chat__conv--agent-tpl"><div class="agent-chat__bubble agent-chat__bubble--ai"><div class="agent-chat__bubble__avatar"><div class="agent-chat__bubble__avatar__start"><img src="https://hy-openapi-public-1258344703.cos.ap-nanjing.myqcloud.com/app/icon/gtcnTp5C1G_icon.png" alt="" class="agent-chat__bubble__avatar__logo"><span class="agent-chat__bubble__avatar__text">创意绘画</span></div><div class="agent-chat__bubble__avatar__end"></div></div><div class="agent-chat__bubble__content"><div class="hyc-content-md"><div class="hyc-common-markdown hyc-common-markdown-style"><p>Hi，我是你的智能创意绘画助手，一句话即可生成多风格图片，快点击试试看吧👇</p></div></div></div></div><div class="t2i-prompt-examples"><div class="t2i-prompt-examples__container"><div class="t2i-prompt-example"><img src="https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/public/d41d8cd98f00b204e9800998ecf8427e/20241015145256_1b96df688ac211ef961d1a29980c18e4.png" alt=""><div class="t2i-prompt-example-cover"><div class="t2i-prompt-example-title">潦草小狗</div><div class="t2i-prompt-example-desc">一只在穆夏风格背景下叼着万圣节南瓜糖果筐的可爱小狗，背景是万圣节氛围，镜头为中景镜头
</div></div></div><div class="t2i-prompt-example"><img src="https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/public/d41d8cd98f00b204e9800998ecf8427e/20241015145420_4dd514a38ac211ef961d1a29980c18e4.png" alt=""><div class="t2i-prompt-example-cover"><div class="t2i-prompt-example-title">南瓜房子</div><div class="t2i-prompt-example-desc">奇趣卡通风格，万圣节南瓜造型的房子，女巫的房子，背景是夜空和、黑森林和月亮。</div></div></div><div class="t2i-prompt-example"><img src="https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/public/d41d8cd98f00b204e9800998ecf8427e/20241015145204_fca874b38ac111efb1a306f7c20c05ba.png" alt=""><div class="t2i-prompt-example-cover"><div class="t2i-prompt-example-title">企鹅宝宝</div><div class="t2i-prompt-example-desc">一只童话世界风格的帝企鹅宝宝，戴着夸张的万圣节南瓜帽，笑容满面地站在冰冻的雪地里，背景是万圣节的气氛，镜头为中景镜头</div></div></div><div class="t2i-prompt-example"><img src="https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/public/d41d8cd98f00b204e9800998ecf8427e/20241015145341_36a8a0748ac211efb1a306f7c20c05ba.png" alt=""><div class="t2i-prompt-example-cover"><div class="t2i-prompt-example-title">节日海报</div><div class="t2i-prompt-example-desc">极简风格，万圣节节日氛围海报</div></div></div><div class="t2i-prompt-example"><img src="https://hunyuan-prod-1258344703.cos.ap-guangzhou.myqcloud.com/public/d41d8cd98f00b204e9800998ecf8427e/20240914110640_5cf9591c724611ef93b65e8f30926190.png" alt=""><div class="t2i-prompt-example-cover"><div class="t2i-prompt-example-title">中秋玉兔诗</div><div class="t2i-prompt-example-desc">“玉兔何年上月宫，夜间捣药特无踪。”生成两个小兔子抱着大大的月饼的画面。糖果色风格。
</div></div></div></div><div class="t2i-prompt-examples__switch"><span class="icon iconfont icon-refresh2" style="font-size: 14px;"></span>换一批</div></div></div></div></div><i></i></div><div class="agent-chat__list__content-loading"><img src="https://cdn-bot.hunyuan.tencent.com/assets/f3f0720e71ce76776867.svg" alt=""></div></div></div></div><div class="agent-dialogue__content--common__input agent-chat__input-box agent-dialogue__content--common__input--text2Image"><div class="t2i-toolbar t2i-toolbar--active"><div class="t2i-toolbar__header"><div class="t2i-toolbar__title">选择风格</div><div class="t2i-toolbar__close"><span class="style-function-beside-close"><svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_366_4638)"><path d="M1 7L5 7L5 11" stroke="black" stroke-opacity="0.4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M11 5L7 5L7 1" stroke="black" stroke-opacity="0.4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></g><defs><clipPath id="clip0_366_4638"><rect width="12" height="12" fill="white"></rect></clipPath></defs></svg>收起</span><span><span class="icon iconfont icon-close" style="font-size: 16px;"></span></span></div></div><div class="t2i-toolbar__content"><div class="turing-section"><div class="turing-section-content turing-section-content--styleFunction"><div class="style-function-stretch-list"><div class="style-function-stretch-list-header-wrapper"><div class="t2i-card-box-card-list__list__page t2i-card-box-card-list__list__page__prev t2i__page__prev swiper-button-disabled swiper-button-lock"><div class="t2i-card-box-card-list__list__page__bg"></div><div class="t2i-card-box-card-list__list__page__op"><span class="icon iconfont icon-arrow-left" style="font-size: 16px;"></span></div></div><div class="t2i-card-box-card-list__list__page t2i-card-box-card-list__list__page__next t2i__page__next swiper-button-disabled swiper-button-lock"><div class="t2i-card-box-card-list__list__page__bg"></div><div class="t2i-card-box-card-list__list__page__op"><span class="icon iconfont icon-arrow-right" style="font-size: 16px;"></span></div></div><div class="swiper swiper-initialized swiper-horizontal swiper-backface-hidden"><div class="swiper-wrapper" style="transform: translate3d(0px, 0px, 0px);"><div class="swiper-slide swiper-slide-active" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item style-function-stretch-list-header-item-active"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_all.png"><span class="style-type">全部</span></span></div><div class="swiper-slide swiper-slide-next" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/ic_category_photography.png"><span class="style-type">摄影</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_cartoon.png"><span class="style-type">卡通</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_anime.png"><span class="style-type">动漫</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_3d.png"><span class="style-type">3D</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_creativity.png"><span class="style-type">创意</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_filter.png"><span class="style-type">滤镜</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_art.png"><span class="style-type">艺术</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_art_school.png"><span class="style-type">流派</span></span></div></div></div></div><div class="style-function-stretch-list-content" style="max-height: 304.6px;"><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_sheying.png" alt=""><span class="stretch-style-name">摄影</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_1.png" alt=""><span class="stretch-style-name">童话世界</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_2.png" alt=""><span class="stretch-style-name">奇趣卡通</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_3.png" alt=""><span class="stretch-style-name">二次元</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_4.png" alt=""><span class="stretch-style-name">纯真动漫</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_5.png" alt=""><span class="stretch-style-name">清新日漫</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_6.png" alt=""><span class="stretch-style-name">3D</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_7.png" alt=""><span class="stretch-style-name">赛博朋克</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_8.png" alt=""><span class="stretch-style-name">像素</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_9.png" alt=""><span class="stretch-style-name">极简</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_10.png" alt=""><span class="stretch-style-name">复古</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_11.png" alt=""><span class="stretch-style-name">暗黑系</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_12.png" alt=""><span class="stretch-style-name">波普风</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_13.png" alt=""><span class="stretch-style-name">中国风</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_14.png" alt=""><span class="stretch-style-name">国潮</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_34.png" alt=""><span class="stretch-style-name">糖果色</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_15.png" alt=""><span class="stretch-style-name">胶片电影</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_16.png" alt=""><span class="stretch-style-name">素描</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_17.png" alt=""><span class="stretch-style-name">水墨画</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_18.png" alt=""><span class="stretch-style-name">油画</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_19.png" alt=""><span class="stretch-style-name">水彩</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_20.png" alt=""><span class="stretch-style-name">粉笔</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_21.png" alt=""><span class="stretch-style-name">粘土</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_22.png" alt=""><span class="stretch-style-name">毛毡</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_23.png" alt=""><span class="stretch-style-name">贴纸</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_24.png" alt=""><span class="stretch-style-name">剪纸</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_25.png" alt=""><span class="stretch-style-name">刺绣</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_35.png" alt=""><span class="stretch-style-name">彩铅</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_28.png" alt=""><span class="stretch-style-name">梵高</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_29.png" alt=""><span class="stretch-style-name">莫奈</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_muxia.png" alt=""><span class="stretch-style-name">穆夏</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_30.png" alt=""><span class="stretch-style-name">毕加索</span></div></div></div></div></div><div class="turing-section"><div class="turing-section-content turing-section-content--styleFunction"><div class="style-function-stretch-list"><div class="style-function-stretch-list-header-wrapper"><div class="t2i-card-box-card-list__list__page t2i-card-box-card-list__list__page__prev t2i__page__prev swiper-button-disabled swiper-button-lock"><div class="t2i-card-box-card-list__list__page__bg"></div><div class="t2i-card-box-card-list__list__page__op"><span class="icon iconfont icon-arrow-left" style="font-size: 16px;"></span></div></div><div class="t2i-card-box-card-list__list__page t2i-card-box-card-list__list__page__next t2i__page__next swiper-button-disabled swiper-button-lock"><div class="t2i-card-box-card-list__list__page__bg"></div><div class="t2i-card-box-card-list__list__page__op"><span class="icon iconfont icon-arrow-right" style="font-size: 16px;"></span></div></div><div class="swiper swiper-initialized swiper-horizontal swiper-backface-hidden"><div class="swiper-wrapper" style="transform: translate3d(0px, 0px, 0px);"><div class="swiper-slide swiper-slide-active" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item style-function-stretch-list-header-item-active"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_all.png"><span class="style-type">全部</span></span></div><div class="swiper-slide swiper-slide-next" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/ic_category_photography.png"><span class="style-type">摄影</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_cartoon.png"><span class="style-type">卡通</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_anime.png"><span class="style-type">动漫</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_3d.png"><span class="style-type">3D</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_creativity.png"><span class="style-type">创意</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_filter.png"><span class="style-type">滤镜</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_art.png"><span class="style-type">艺术</span></span></div><div class="swiper-slide" style="margin-right: 12px;"><span class="style-function-stretch-list-header-item"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/%E5%88%9B%E6%84%8F%E7%BB%98%E7%94%BB/20240807/ic_category_art_school.png"><span class="style-type">流派</span></span></div></div></div></div><div class="style-function-stretch-list-content" style="max-height: 304.6px;"><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_sheying.png" alt=""><span class="stretch-style-name">摄影</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_1.png" alt=""><span class="stretch-style-name">童话世界</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_2.png" alt=""><span class="stretch-style-name">奇趣卡通</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_3.png" alt=""><span class="stretch-style-name">二次元</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_4.png" alt=""><span class="stretch-style-name">纯真动漫</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_5.png" alt=""><span class="stretch-style-name">清新日漫</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_6.png" alt=""><span class="stretch-style-name">3D</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_7.png" alt=""><span class="stretch-style-name">赛博朋克</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_8.png" alt=""><span class="stretch-style-name">像素</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_9.png" alt=""><span class="stretch-style-name">极简</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_10.png" alt=""><span class="stretch-style-name">复古</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_11.png" alt=""><span class="stretch-style-name">暗黑系</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_12.png" alt=""><span class="stretch-style-name">波普风</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_13.png" alt=""><span class="stretch-style-name">中国风</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_14.png" alt=""><span class="stretch-style-name">国潮</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_34.png" alt=""><span class="stretch-style-name">糖果色</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_15.png" alt=""><span class="stretch-style-name">胶片电影</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_16.png" alt=""><span class="stretch-style-name">素描</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_17.png" alt=""><span class="stretch-style-name">水墨画</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_18.png" alt=""><span class="stretch-style-name">油画</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_19.png" alt=""><span class="stretch-style-name">水彩</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_20.png" alt=""><span class="stretch-style-name">粉笔</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_21.png" alt=""><span class="stretch-style-name">粘土</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_22.png" alt=""><span class="stretch-style-name">毛毡</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_23.png" alt=""><span class="stretch-style-name">贴纸</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_24.png" alt=""><span class="stretch-style-name">剪纸</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_25.png" alt=""><span class="stretch-style-name">刺绣</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_35.png" alt=""><span class="stretch-style-name">彩铅</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_28.png" alt=""><span class="stretch-style-name">梵高</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_29.png" alt=""><span class="stretch-style-name">莫奈</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_muxia.png" alt=""><span class="stretch-style-name">穆夏</span></div><div class="style-function-stretch-list-content-item" style="height: 150.8px;"><img src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/pic_style_30.png" alt=""><span class="stretch-style-name">毕加索</span></div></div></div></div></div></div><div class="t2i-toolbar__menu"><div class="t2i-toolbar__menu-item" id="aiEditImage-wrapper"><img class="t2i-toolbar__menu-item-icon" id="aiEditImage-img" src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/creative_session/20240812/ic_ai_repaint0914.png" alt=""><div class="t2i-toolbar__menu-item-text" id="aiEditImage-text">AI修图</div></div><div class="t2i-toolbar__menu-item" id="reviseFunction-wrapper"><img class="t2i-toolbar__menu-item-icon" id="reviseFunction-img" src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/创意绘画/ic_draw_Paraphrasing.png" alt=""><div class="t2i-toolbar__menu-item-text" id="reviseFunction-text">润色</div></div><div class="t2i-toolbar__menu-item t2i-toolbar__menu-item--active" id="styleFunction-wrapper"><img class="t2i-toolbar__menu-item-icon" id="styleFunction-img" src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/创意绘画/ic_draw_style.png" alt=""><div class="t2i-toolbar__menu-item-text" id="styleFunction-text">风格</div></div><div class="t2i-toolbar__menu-item" id="scaleFunction-wrapper"><img class="t2i-toolbar__menu-item-icon" id="scaleFunction-img" src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/创意绘画/ic_draw_proportion.png" alt=""><div class="t2i-toolbar__menu-item-text" id="scaleFunction-text">比例</div></div><div class="t2i-toolbar__menu-item" id="resolutionFunction-wrapper"><img class="t2i-toolbar__menu-item-icon" id="resolutionFunction-img" src="https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/text2image/public/创意绘画/ic_draw_resolution.png" alt=""><div class="t2i-toolbar__menu-item-text" id="resolutionFunction-text">分辨率</div></div></div></div><div class="agent-dialogue__content--common__input-box"><div class="style__text-area___QPXII style__text-area--focus___U54sj style__text-area--pc___uXnLG style__text-area--empty___y4riG agent-input-text-area agent-input-text-area-focus"><div class="style__text-area__mask___DICHk"></div><div class="style__text-area__wrapper___DfOct"><div class="style__text-area__start___AFgHI"><div class="style__text-area__edit___x_smB"><div class="chat-input-editor style__hight-light-text-area-new___J3Up9 style__text-area__edit__content___RnJkL ql-container"><div class="ql-editor ql-blank" contenteditable="true" data-placeholder="用一句话描述想要画的图片吧" enterkeyhint="send"><p><br></p></div></div></div></div><div class="style__text-area__end___HElM7"><div class="style__text-area__attachment___uSO5A"></div><div class="style__text-area__actions___i5NQf"><a class="style__send-btn___GVH0r style__send-btn--disabled___bW0Ww"><span class="hyc-common-icon iconfont icon-send" style="font-size: 20px; color: rgb(255, 255, 255);"></span></a></div></div></div></div></div><div class="document-settings-seat"></div><div class="document-settings"><div class="document-settings-header"><div class="document-settings-header-left"><span class="style__hunyuan-icon-wrapper___lO6Ym" style="height: 16px; width: 16px;"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.58691 4.66238H8.55461V14.7022H7.58691V4.66238Z" fill="black" fill-opacity="0.9"></path><path d="M8.16703 15.4766C8.02188 15.4766 7.87672 15.404 7.77995 15.283C7.39287 14.7508 6.54614 14.3879 5.74779 14.3879H0.981894C0.715778 14.3879 0.498047 14.1702 0.498047 13.904V3.54971C0.498047 3.38036 0.570624 3.23521 0.667394 3.11425C0.885125 2.89651 1.19963 2.89651 1.41736 2.89651H5.60264C6.76387 2.89651 7.9493 3.52552 8.48153 4.44483C8.62669 4.66256 8.55411 4.97706 8.31218 5.09802C8.09445 5.24318 7.77995 5.1706 7.65899 4.92867C7.2961 4.32387 6.40099 3.84002 5.60264 3.84002H1.46574V13.396H5.74779C6.83645 13.396 7.97349 13.904 8.55411 14.654C8.72345 14.8717 8.67507 15.1621 8.45734 15.3314C8.36057 15.4282 8.2638 15.4766 8.16703 15.4766Z" fill="black" fill-opacity="0.9"></path><path d="M8.16788 15.4766C8.07111 15.4766 7.97434 15.4524 7.87757 15.3798C7.65984 15.2104 7.61146 14.9201 7.7808 14.7024C8.36142 13.9524 9.47427 13.4444 10.5871 13.4444H14.5305V3.86421H10.7081C9.86135 3.86421 8.84527 4.34806 8.48238 4.95287C8.33723 5.1706 8.04692 5.26737 7.82919 5.12221C7.61146 4.97706 7.51469 4.68675 7.65984 4.46902C8.26465 3.45294 9.692 2.89651 10.7081 2.89651H14.8934C14.9901 2.89651 15.1837 2.89651 15.3288 3.04167C15.4982 3.21102 15.4982 3.40455 15.4982 3.50132V13.904C15.4982 14.1702 15.2804 14.3879 15.0143 14.3879H10.5629C9.76458 14.3879 8.94204 14.7508 8.53077 15.283C8.45819 15.404 8.31303 15.4766 8.16788 15.4766Z" fill="black" fill-opacity="0.9"></path><path d="M14.4782 1.54975L14.4782 1.54974C14.3392 1.46477 14.1795 1.4198 14.0166 1.4198C13.8537 1.4198 13.694 1.46477 13.555 1.54974L13.555 1.54975C13.4162 1.63462 13.3035 1.75613 13.2292 1.9009L13.2295 1.90042L13.8966 2.24321L13.229 1.90141L14.4782 1.54975ZM14.4782 1.54975C14.6169 1.63453 14.7295 1.75586 14.8037 1.90042M14.4782 1.54975L14.8037 1.90042M11.3965 3.70852C11.4814 3.56976 11.6028 3.45707 11.7476 3.38283L11.7471 3.38306L12.09 4.05003L11.7482 3.38249L11.3965 3.70852ZM11.3965 3.70852C11.3116 3.84749 11.2666 4.00723 11.2666 4.17013C11.2666 4.33304 11.3116 4.49277 11.3965 4.63174C11.4814 4.77047 11.6028 4.88314 11.7475 4.95738L11.3965 3.70852ZM14.8037 1.90042C14.8038 1.90051 14.8038 1.9006 14.8039 1.90069M14.8037 1.90042L14.8039 1.90069M14.8039 1.90069C14.804 1.90093 14.8041 1.90117 14.8042 1.90142M14.8039 1.90069L14.8042 1.90142M14.8042 1.90142L15.199 2.66961C15.199 2.66962 15.199 2.66964 15.199 2.66966C15.2692 2.80614 15.3803 2.91724 15.5167 2.98739C15.5168 2.9874 15.5168 2.98741 15.5168 2.98742L16.285 3.38216C16.2852 3.38229 16.2855 3.38242 16.2858 3.38255C16.2858 3.38259 16.2859 3.38263 16.286 3.38267C16.4305 3.45691 16.5519 3.56953 16.6367 3.70819C16.7216 3.84717 16.7666 4.0069 16.7666 4.1698C16.7666 4.3327 16.7216 4.49243 16.6367 4.63141C16.5518 4.77022 16.4303 4.88293 16.2855 4.95717L16.286 4.95693L14.8042 1.90142ZM15.199 5.66999C15.199 5.66998 15.199 5.66996 15.199 5.66994C15.2692 5.53346 15.3803 5.42236 15.5167 5.35221C15.5168 5.3522 15.5168 5.35219 15.5168 5.35218L16.285 4.95744L15.199 5.66999ZM15.199 5.66999L14.8042 6.43818L15.199 5.66999ZM12.5165 5.35223L11.7482 4.95777L13.8966 6.09639L13.2294 6.43907L13.2292 6.43862C13.2291 6.43848 13.229 6.43833 13.229 6.43818L12.8345 5.67022C12.8345 5.6702 12.8345 5.67018 12.8345 5.67016C12.7643 5.53364 12.6532 5.4225 12.5167 5.35232C12.5166 5.35229 12.5166 5.35226 12.5165 5.35223ZM13.4691 5.75461L13.4696 5.75361L13.4691 5.75461ZM15.6014 4.71734L15.6004 4.71684L15.6014 4.71734Z" fill="black" fill-opacity="0.9" stroke="white" stroke-width="1.5"></path></svg></span><span>深度阅读</span></div><div class="document-settings-header-right"><span class="close-btn"><span class="style__hunyuan-icon-wrapper___lO6Ym" style="height: 16px; width: 16px;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="16" height="16" rx="8" fill="black" fill-opacity="0.05"></rect><g opacity="0.4"><path d="M5.5 5.5L10.5 10.5" stroke="black" stroke-linecap="round" stroke-linejoin="round"></path><path d="M5.5 10.5L10.5 5.5" stroke="black" stroke-linecap="round" stroke-linejoin="round"></path></g></svg></span></span></div></div><div class="document-settings-wrapper"><div class="document-settings-wrapper-content"><div class="document-settings-wrapper-content-icon_wrap"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18.125 20.6155H5.875C5.39175 20.6155 5 20.2298 5 19.754V4.2463C5 3.77049 5.39175 3.38477 5.875 3.38477H14.625L19 7.69246V19.754C19 20.2298 18.6083 20.6155 18.125 20.6155Z" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path><path d="M15.2311 11.9931L12.0003 8.76953L8.76953 12.0003" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12.001 8.76953V16.308" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path></svg></div><p class="document-settings-wrapper-content-text">点击或拖放上传本地文件</p><p class="document-settings-wrapper-content-history_text">历史文件<svg fill="none" viewBox="0 0 24 24" width="1em" height="1em" class="t-icon t-icon-chevron-right"><path fill="currentColor" d="M8.09 17.5l5.5-5.5-5.5-5.5L9.5 5.09 16.41 12 9.5 18.91 8.09 17.5z"></path></svg></p><p class="document-settings-wrapper-content-tip">支持格式：pdf、&nbsp;doc、txt、ppt、excel<br>文件大小：每个不超过100MB，最多50个</p></div></div></div></div><div class="agent-dialogue__tool"><div class="agent-dialogue__tool__item bg-white agent-dialogue__tool-item--assets"><span class="icon iconfont icon-folder" style="font-size: 16px;"></span></div><button type="button" class="agent-dialogue__tool__new-chat t-button t-button--theme-default t-button--variant-outline t-button--shape-round"><svg width="20" height="20" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="0.703125" y="0.53418" width="20" height="20" rx="10" fill="#20C57D"></rect><path d="M5.70312 10.5342H15.7031" stroke="#fff" stroke-width="1.5"></path><path d="M10.7031 5.53418V15.5342" stroke="#fff" stroke-width="1.5"></path></svg><span class="t-button__text">新建对话</span></button><div class="agent-dialogue__tool__item bg-white agent-info"><svg width="10" height="10" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg"><g opacity="0.9"><path d="M3.70312 8.76758C3.70312 7.93915 3.03155 7.26758 2.20312 7.26758C1.3747 7.26758 0.703125 7.93915 0.703125 8.76758C0.703125 9.59601 1.3747 10.2676 2.20312 10.2676C3.03155 10.2676 3.70312 9.59601 3.70312 8.76758Z" fill="currentColor"></path><path d="M3.70312 1.76758C3.70312 0.939151 3.03155 0.267578 2.20312 0.267578C1.3747 0.267578 0.703125 0.939151 0.703125 1.76758C0.703125 2.59601 1.3747 3.26758 2.20312 3.26758C3.03155 3.26758 3.70312 2.59601 3.70312 1.76758Z" fill="currentColor"></path><path d="M10.7031 8.76758C10.7031 7.93915 10.0316 7.26758 9.20312 7.26758C8.3747 7.26758 7.70312 7.93915 7.70312 8.76758C7.70312 9.59601 8.3747 10.2676 9.20312 10.2676C10.0316 10.2676 10.7031 9.59601 10.7031 8.76758Z" fill="currentColor"></path><path d="M10.7031 1.76758C10.7031 0.939151 10.0316 0.267578 9.20312 0.267578C8.3747 0.267578 7.70312 0.939151 7.70312 1.76758C7.70312 2.59601 8.3747 3.26758 9.20312 3.26758C10.0316 3.26758 10.7031 2.59601 10.7031 1.76758Z" fill="currentColor"></path></g></svg></div></div></div></div><div class="agent-dialogue__content-copyright"><div class="copyright-wp"><div class="copyright" style="transform: translateY(-50%) scale(0.833);"><div class="copyright__content"><div class="copyright__paragh"><div class="copyright__paragh__item">所有内容均由AI生成仅供参考</div></div><div class="copyright__paragh">请阅读并知悉<a href="https://rule.tencent.com/rule/202403110001" class="copyright__link" target="_blank">《腾讯元宝用户服务协议》</a><a href="https://privacy.qq.com/document/preview/4d27c22b2e9f47958197aa5ec32f7d6e" class="copyright__link" target="_blank">《腾讯元宝隐私政策》</a><a href="https://zhuanhuabao-5gqf84946751a1cb-1300912497.tcloudbaseapp.com/Attribution_hyaidV2.html" class="copyright__link" target="_blank">《开源条款》</a></div></div></div></div></div><div class="agent-drag-file"><div class="agent-drag-file__content"><div class="agent-drag-file__logo"><span class="icon iconfont icon-upload" style="font-size: 30px;"></span></div><div class="agent-drag-file__name">文件拖动到此处即可上传</div><div class="agent-drag-file__tip">支持文件格式：</div></div></div></div></div></div></div></div><img src="chrome-extension://edahgikmkmohkpionhkbgkdcpioimbei/youdao_icon.png" style="width: 138px; height: 40px; position: fixed; right: 240px; top: 10px; z-index: 100000; cursor: pointer; display: none;">
<div id="starai_prompt_login_container">
    <div id="starai_prompt_login_dialog_mask"></div>
    <div id="starai_prompt_login_dialog">
        <img src="" id="starai_prompt_login_dialog_bg">
        <div class="starai_prompt_login_dialog_content">
            <div id="starai_prompt_login_dialog_close"></div>
            <div class="starai_prompt_login_dialog_title">欢迎登录AIPrompter</div>
            <div class="starai_prompt_login_dialog_desc">未注册的微信号将自动创建 AIPrompter 账号</div>
            <div id="starai_prompt_login_dialog_code_loading">
                <img id="starai_prompt_login_dialog_code_loading_ic" src="" alt="">
            </div>
            <img id="starai_prompt_login_QR_code" src="" alt="">
            <div class="starai_prompt_login_dialog_desc_wx">微信扫码登录</div>
            <div class="starai_prompt_login_dialog_btm">
                注册登录即代表同意<span class="starai_prompt_login_dialog_btm_light" id="starai_prompt_login_btn_user">《用户协议》</span>与<span class="starai_prompt_login_dialog_btm_light" id="starai_prompt_login_btn_privacy">《隐私政策》</span>
            </div>
        </div>
    </div>
</div>

</body><div id="immersive-translate-popup" style="all: initial"></div></html>
"""

from lxml.etree import HTML

from meutils.pipe import *

html = HTML(s)

xpath = """//*[@id="app"]/div/div[2]/div/div/div[1]/div//span//text()"""

print(html.xpath(xpath))
from meutils.pipe import *


['创意绘画', '创意绘画', '收起', '全部', '摄影', '卡通', '动漫', '3D', '创意', '滤镜', '艺术', '流派', '摄影', '童话世界', '奇趣卡通', '二次元', '纯真动漫', '清新日漫', '3D', '赛博朋克', '像素', '极简', '复古', '暗黑系', '波普风', '中国风', '国潮', '糖果色', '胶片电影', '素描', '水墨画', '油画', '水彩', '粉笔', '粘土', '毛毡', '贴纸', '剪纸', '刺绣', '彩铅', '梵高', '莫奈', '穆夏', '毕加索', '全部', '摄影', '卡通', '动漫', '3D', '创意', '滤镜', '艺术', '流派', '摄影', '童话世界', '奇趣卡通', '二次元', '纯真动漫', '清新日漫', '3D', '赛博朋克', '像素', '极简', '复古', '暗黑系', '波普风', '中国风', '国潮', '糖果色', '胶片电影', '素描', '水墨画', '油画', '水彩', '粉笔', '粘土', '毛毡', '贴纸', '剪纸', '刺绣', '彩铅', '梵高', '莫奈', '穆夏', '毕加索', '深度阅读', '新建对话'] | xUnique