<template>
  <div class="store-pad d-flex flex-column">
    <div class="store-hader">
      存储空间管理
    </div>
    <div class="flex-1 d-flex">
      <leftPad />
      <rightPad class="flex-1" />
    </div>

  </div>
</template>

<script>
import leftPad from './left_pad'
import rightPad from './right_pad'

export default {
  props: [],
  data() {
    return {}
  },
  components: { leftPad, rightPad },

  computed: {},

  watch: {},

  methods: {},

  created() {},

  mounted() {}
}
</script>

<style scoped lang="scss">
.store-pad {
  width: 1000px;
  height: 800px;
  margin: 0 auto;
  border: 1px solid #ccc;

  .store-hader {
    height: 40px;
    line-height: 40px;
    text-align: center;
    background-color: #409eff;
    color: white;
    font-size: 16px;
  }
}
</style>
