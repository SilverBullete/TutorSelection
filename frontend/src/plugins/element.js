import Vue from 'vue'
import {
    Button, Form, FormItem, Input, Radio, RadioGroup, RadioButton,
    Message, Container, Header, Aside, Main, Carousel, CarouselItem,
    Menu, Submenu, MenuItemGroup, MenuItem, Row, Col, Cascader, Table,
    TableColumn, Tag, MessageBox, Scrollbar, Divider, Link, Breadcrumb,
    BreadcrumbItem
} from 'element-ui'

Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(RadioButton)
Vue.prototype.$message = Message
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Carousel)
Vue.use(CarouselItem)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItemGroup)
Vue.use(MenuItem)
Vue.use(Row)
Vue.use(Col)
Vue.use(Cascader)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Tag)
// Vue.use(MessageBox)
Vue.prototype.$alert = MessageBox.alert
Vue.use(Scrollbar)
Vue.use(Divider)
Vue.use(Link)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
