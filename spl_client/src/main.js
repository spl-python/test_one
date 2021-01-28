// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from "axios";

import Element from "element-ui"
import "element-ui/lib/theme-chalk/index.css"

Vue.config.productionTip = false

Vue.use(Element)
Vue.prototype.$axios = axios
import "../static/js/gt"
import settings from "./settings";
import '../static/css/global.css'

Vue.prototype.$settings = settings
/* eslint-disable no-new */

// 配置视频播放相关
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'


Vue.use(VideoPlayer);
import store from './store/index'

new Vue({
    el: '#app',
    router,
    components: {App},
    template: '<App/>',
    store
})
