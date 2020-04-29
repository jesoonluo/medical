<template>
  <div class="modal" id="bingxiangModel">
    <div class="modal-wrap model-sm">
      <div class="modal-content">
        <div class="modal-header">
          <div class="d-flex justify-content-between" style="width: 100%">
            <h5>添加冰箱</h5>
            <i @click="close()" class="el-icon-close cp"></i>
          </div>
        </div>
        <div class="modal-body">
          <el-form :model="form" ref="ruleForm" label-width="110px" class="demo-ruleForm">
            <el-form-item label="设备ID：">
              <el-input v-model="form.storage_id"></el-input>
            </el-form-item>
            <el-form-item label="设备名称">
              <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="终端名称">
              <el-input v-model="form.terminal_name"></el-input>
            </el-form-item>
            <el-form-item label="设备类型">
              <el-select v-model="form.dtype" placeholder="请选择设备类型">
                <el-option label="立式冰箱" value="1"></el-option>
                <el-option label="卧式冰箱" value="2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="选择编码方式">
              <el-select v-model="form.utype" placeholder="请选择编码方式">
                <el-option label="一维纯数字：1，2，3，4，.." value="1"></el-option>
                <el-option label="二维纯数字：11，12...21,22.." value="2"></el-option>
                <el-option label="二维纯字母加数字：A1,A2...B1,B2" value="3"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="行数">
              <el-input v-model="form.storageline"></el-input>
            </el-form-item>
            <el-form-item label="列数">
              <el-input v-model="form.storagecolumn"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">保存</el-button>
              <el-button @click="close()">关闭</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div class="modal-footer"></div>
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
        storage_id: 1,
        name: '冰箱', // 设备名称
        dtype: '1', // 1.立式冰箱 2.卧式冰箱
        terminal_name: '终端名称', // 终端名称=
        utype: '1', // 编码方式 有三种 1.(1234)  =>  2.(11，12，13)，=>  3.(A1,A2,A3...B1,2)
        storageline: 10, // 行数
        storagecolumn: 10,
        rank: 1,
        room_id: ''
      },
      rules: {}
    }
  },

  components: {},

  methods: {
    close() {
      this.$store.commit('modalHidden', 'bingxiangModel')
    },
    onSubmit(formName) {
      var form = new FormData()
      console.log(this.parent_item)

      form.append('name', this.form.name)
      form.append('rank', Number(this.parent_item.rank) + 1)
      form.append('terminal_name', this.form.terminal_name)
      form.append('room_id', this.parent_item.id)
      form.append('storage_id', this.form.storage_id)
      form.append('utype', this.form.utype)
      form.append('dtype', this.form.dtype)
      form.append('storageline', this.form.storageline)
      form.append('storagecolumn', this.form.storagecolumn)

      this.$axios.post('add_storage_device', form).then(res => {
        console.log(res.data)
      })
      this.close()
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
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
