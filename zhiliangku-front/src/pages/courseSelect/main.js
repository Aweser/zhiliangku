// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// import router from './router'

Vue.config.productionTip = false
//引入脚本
import fn from '../../utils/index'
Vue.prototype.$fn=fn;
import Obj from '../../assets/js/const'
Vue.prototype.$myConst=Obj;
//引入选择的插件
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// 引入样式表
import '../../style/base/modifiedel.css'
// 为用到组件结束，需要删除
// import Moment from 'moment'

Vue.use(ElementUI)


import '../../utils/axios'
//引入自写小组件
//home
import ProjectHeader from '../../components/home/projectHeader.vue'
import PostMatch from '../../components/home/postMatch.vue'
import HotCourse from '../../components/home/hotCourse.vue'
import ProjectFooter from '../../components/home/projectFooter.vue'
// courseInfo
import CourseSelect from '../../components/courseInfo/courseSelect.vue'
import ProjectPager from '../../components/courseInfo/pager.vue'
import Container from '../../components/courseInfo/container.vue'
import Pager from '../../components/courseInfo/pager.vue'
//login
import Login from '../../components/login/login.vue'

//引入混合组件
// home
// courseInfo



//声明自写小组件
//首页部分
//home
Vue.component('projectHeader',ProjectHeader)
Vue.component('postMatch',PostMatch)
Vue.component('hotCourse',HotCourse)
Vue.component('projectFooter',ProjectFooter)
//courseInfo
Vue.component('courseSelect',CourseSelect)
Vue.component('projectPager',ProjectPager)
Vue.component('container',Container)
//login
Vue.component('login',Login)

//声明自写混合组件
//home
//courseInfo
Vue.component('pager',Pager)
// 过滤器
Vue.filter("turnToThu",function(value){
  return parseInt(value/1000)+'k'
})

//自写函数
Vue.prototype.$vueself=function(){
  return this;
}
Vue.prototype.deepCopy=function(obj){
  return JSON.parse(JSON.stringify(obj))
}
/* eslint-disable no-new */
new Vue({
  el: '#app',
  // router,
  template: '<App/>',
  components: { App }
})
