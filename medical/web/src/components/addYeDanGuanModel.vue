<template>
  <div class="modal" id="yedanguanModel">
    <div class="modal-wrap model-sm">
      <div class="modal-content">
        <div class="modal-header">
          <div class="d-flex justify-content-between" style="width: 100%">
            <h5>添加冰箱</h5>
            <i @click="close()" class="el-icon-close cp"></i>
          </div>
        </div>
        <div class="modal-body">
          <el-form :model="form" :rules="rules" ref="ruleForm" label-width="110px" class="demo-ruleForm">
            <el-form-item label="设备ID：">
              <el-input v-model="form.id"></el-input>
            </el-form-item>
            <el-form-item label="设备名称">
              <el-input v-model="form.type_name"></el-input>
            </el-form-item>
            <el-form-item label="液氮罐类型">
              <el-select v-model="form.number" placeholder="请选择冻存架数量">
                <el-option :label="1" value="1"></el-option>
                <el-option :label="2" value="2"></el-option>
                <el-option :label="3" value="3"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="冻存架数量">
              <el-select v-model="form.number" placeholder="请选择冻存架数量">
                <el-option v-for="(item, index) in 20" :key="index" :label="item" value="1"></el-option>
              </el-select>
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
  props: ['imgModelSrc'],
  data() {
    return {
      form: {
        type_name: 'binxing', // 设备名称
        type: '1', // 1.立式冰箱 2.卧式冰箱
        number: '1' // 终端名称
      },
      rules: {
        name: [
          { required: true, message: '请输入活动名称', trigger: 'blur' },
          { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
        ],
        region: [{ required: true, message: '请选择活动区域', trigger: 'change' }],
        date1: [
          {
            type: 'date',
            required: true,
            message: '请选择日期',
            trigger: 'change'
          }
        ],
        date2: [
          {
            type: 'date',
            required: true,
            message: '请选择时间',
            trigger: 'change'
          }
        ],
        type: [
          {
            type: 'array',
            required: true,
            message: '请至少选择一个活动性质',
            trigger: 'change'
          }
        ],
        resource: [{ required: true, message: '请选择活动资源', trigger: 'change' }],
        desc: [{ required: true, message: '请填写活动形式', trigger: 'blur' }]
      }
    }
  },

  components: {},

  methods: {
    close() {
      this.$store.commit('modalHidden', 'yedanguanModel')
    },
    onSubmit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
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
