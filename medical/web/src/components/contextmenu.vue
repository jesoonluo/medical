<template>
  <div class="contextmenu" id="context">
    <ul>
      <li v-for="(item,index) in menu" :key="index">
        <a @click="addStore(item)" :data-type="item.type">{{item.name}}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: [],
  data() {
    return {
      menu: [],
      base_data: [
        {
          name: '添加冰箱',
          type: 'binxiang',
          type_id: 1
        },
        {
          name: '添加液氮罐',
          type: 'yedanguan',
          type_id: 2
        },
        {
          name: '添加存储空间',
          type: 'file',
          type_id: 3
        }
      ],
      change_data: [
        {
          name: '修改',
          type: 'change',
          type_id: 4
        },
        {
          name: '复制',
          type: 'copy',
          type_id: 5
        },
        {
          name: '剪切',
          type: 'cut',
          type_id: 6
        },
        {
          name: '删除',
          type: 'del',
          type_id: 7
        }
      ],
      add_item: [
        {
          name: '添加冻存架',
          type: 'dongcunjia',
          type_id: 8
        }
      ],
      dom_id: 'context',
      parent_item: {}
    }
  },
  components: {},

  computed: {},

  watch: {},

  methods: {
    //  添加函数
    addStore(item) {
      this.$emit('addStore', item, this.parent_item)
    },
    onContextMenu(env, data) {
      var self = this
      console.log('onContextMenu')
      this.changeData(data)
      this.parent_item = data

      // document.oncontextmenu = function (env) {
      // env 表示event事件
      // 兼容event事件写法
      var e = env || window.event

      var context = document.getElementById(self.dom_id)
      context.style.display = 'block'

      //  让菜单随着鼠标的移动而移动
      //  获取鼠标的坐标
      var x = e.clientX
      var y = e.clientY

      //  获取窗口的宽度和高度
      var w = window.innerWidth
      var h = window.innerHeight

      //  调整宽度和高度
      context.style.left = Math.min(w - 202, x) + 'px'
      context.style.top = Math.min(h - 230, y) + 'px'

      // return false可以关闭系统默认菜单
      // return false
      // }

      //   当鼠标点击后关闭右键菜单
      document.onclick = function(env) {
        var contextmenu = document.getElementById(self.dom_id)
        contextmenu.style.display = 'none'
      }
    },
    changeData(data) {
      console.log('changeData', data)

      this.menu = []
      if (data.utype == 'dongcunjia') {
        this.menu = JSON.parse(JSON.stringify(this.add_item))
      }
      if (data.utype == 'folder') {
        this.menu = JSON.parse(JSON.stringify(this.base_data))
      }

      if (data.utype == 'yedanguan' || data.utype == 'binxiang') {
        this.menu = JSON.parse(JSON.stringify(this.change_data))
        var nameTemp = ''
        if (data.utype == 'yedanguan') {
          nameTemp = '液氮罐'
        }
        if (data.utype == 'binxiang') {
          nameTemp = '冰箱'
        }
        this.menu.map(item => {
          item.name = item.name + nameTemp
        })
      }
    }
  },

  created() {},

  mounted() {
    // this.onContextMenu()
  }
}
</script>

<style scoped lang="scss">
.contextmenu {
  width: 200px;
  border: 1px solid #999;
  box-shadow: 3px 3px 3px #ccc;
  background-color: #fff;
  position: absolute;
  top: 10px;
  left: 10px;
  display: none;
}
.contextmenu li {
  height: 40px;
  line-height: 40px;
}
.contextmenu li a {
  display: block;
  padding: 0 30px;
}
.contextmenu li a:hover {
  background-color: #ccc;
  font-weight: bold;
  color: #fff;
}
</style>
