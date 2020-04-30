<template>
  <div class="left-pad" @contextmenu.prevent="padMenu($event)" data-type="file">
    <el-tree :data="data" :node-key="data.id" default-expand-all :props="defaultProps" @node-contextmenu="onContextMenu" :expand-on-click-node="true" :render-content="renderContent"></el-tree>

    <costomMenu @addStore="addStore(arguments)" ref="costomMenu" />
    <!-- 添加冰箱 -->
    <bingxiangM :parent_item="parent_item" />
    <!-- 添加液氮罐 -->
    <yeDanguanM :parent_item="parent_item" />
    <!-- 添加冻存架 -->
    <dongcunjiaM :parent_item="parent_item" />
    <!-- 添加存储空间 -->
    <addFolderM :parent_item="parent_item" />
  </div>
</template>

<script>
import costomMenu from '../components/contextmenu'
import bingxiangM from '../components/addBinxnagModel'
import yeDanguanM from '../components/addYeDanGuanModel'
import dongcunjiaM from '../components/addDongcunjiaModel'
import addFolderM from '../components/addFolderModel'

export default {
  props: [],
  data() {
    return {
      data: [
        {
          dtype: '0',
          id: '5ea92ffb4e0e431499e88d5d',
          name: '全部空间',
          parent_id: '0',
          rank: 1,
          utype: 'folder'
        }
      ],
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      parent_item: {}
    }
  },
  components: { costomMenu, bingxiangM, yeDanguanM, dongcunjiaM, addFolderM },

  computed: {
    upData() {
      return this.$store.state.upData
    }
  },

  watch: {
    upData() {
      this.getList()
    }
  },

  methods: {
    // 获取列表
    getList() {
      var self = this
      // this.$axios.get('http://localhost:8989/test.json').then((res) => {
      this.$axios.get('query_node').then(res => {
        var data = res.data.store
        console.log(data)

        this.data = data
        if (data.length > 1) {
          this.data = this.setTreeData(data)
        }
      })
    },
    // 设置树形数据
    setTreeData(source) {
      const cloneData = JSON.parse(JSON.stringify(source)) // 对源数据深度克隆
      return cloneData.filter(father => {
        // 返回每一项的子级数组
        const branchArr = cloneData.filter(child => father.id == child.parent_id)
        // 如果存在子级，则给父级添加一个children属性，并赋值
        branchArr.length > 0 ? (father.children = branchArr) : ''
        return father.parent_id == '0' // 返回第一层
      })
    },
    // 返回自定义 icon
    renderContent(h, { node, data, store }) {
      var img = require('../assets/image/' + data.utype + '_' + data.dtype + '.jpg')
      return (
        <span class="custom-tree-node">
          <img class="file-img" src={img} />
          <span data-type={data.type} class="file">
            {node.label}
          </span>
        </span>
      )
    },
    // 右击结构菜单
    onContextMenu(event, data, node) {
      console.log(data)
      this.$nextTick(() => {
        this.$refs.costomMenu.onContextMenu(event, data)
      })
    },
    // 右击面板结构菜单
    padMenu(event) {
      this.$refs.costomMenu.onContextMenu(event, this.data[0])
    },
    addStore(data) {
      console.log(data)
      this.parent_item = data[1]

      switch (data[0].type_id) {
        case 1:
          // 添加冰箱
          this.$store.commit('modalShow', 'bingxiangModel')
          break
        case 2:
          // 添加液氮罐
          this.$store.commit('modalShow', 'yedanguanModel')
          break
        case 8:
          // 添加冻存架
          this.$store.commit('modalShow', 'dongcunjiaModel')
          break
        case 3:
          // 添加存储空间
          // 添加冻存架
          this.$store.commit('modalShow', 'folderModel')
          break
        case 4:
          // 修改
          break
        case 5:
          // 复制
          break
        case 6:
          // 剪切
          break
        case 7:
          // 删除
          break
      }
    }
  },

  created() {
    this.getList()
  },

  mounted() {}
}
</script>

<style lang="scss">
.left-pad {
  width: 300px;
  height: 100%;
  border-right: 1px solid #222;
  background-color: white;
}
.el-icon-folder-opened {
  color: rgb(246, 224, 144);
  font-size: 24px !important;
}
.el-tree {
  padding-top: 10px;
}
.file-img {
  width: 13px;
  height: 20px;
  margin-right: 5px;
  margin-top: -2px;
}
.el-tree-node__expand-icon.is-leaf {
  color: #333;
  cursor: default;
}
</style>
