<template>
  <div class="modal" id="folderModel">
    <div class="modal-wrap model-sm">
      <div class="modal-content">
        <div class="modal-header">
          <div class="d-flex justify-content-between" style="width: 100%">
            <h5>添加存储空间</h5>
            <i @click="close()" class="el-icon-close cp"></i>
          </div>
        </div>
        <div class="modal-body">

          <el-form :model="form" ref="ruleForm" label-width="120px" class="demo-ruleForm">
            <el-form-item label="存储空间名称：">
              <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addFolder">保存</el-button>
              <el-button @click="close()">关闭</el-button>
            </el-form-item>
          </el-form>

        </div>
        <div class="modal-footer">

        </div>

      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ['parent_item'],
  data() {
    return {
      form: {
        name: ''
      }
    }
  },

  components: {},

  methods: {
    close() {
      this.$store.commit('modalHidden', 'folderModel')
      this.$store.commit('upData')
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // 添加存储空间
    addFolder(data) {
      if (!this.form.name) {
        return
      }

      var form = new FormData()
      form.append('name', this.form.name)
      form.append('rank', Number(this.parent_item.parent_id) + 1)
      form.append('room_id', this.parent_item.id)

      this.$axios.post('add_room', form).then(res => {
        console.log(res.data)
      })
      this.close()
    }
  },

  created() {},

  mounted() {}
}
</script>
<style lang="scss">
#imgModel {
  .modal-content {
    .modal-body {
      height: 420px;
      width: 720px;
      img {
        width: 100%;
        height: 100%;
      }
    }
  }
}
</style>
