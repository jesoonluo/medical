<template>
  <div class="binxiang">
    <div class="cube">
      <div class="cube-inner running">
        <p class="single-side s1"><span data-type="1"></span></p>
        <div class="single-side s2">
          <span data-type="2"></span>
          <div class="dongcunjia"></div>
        </div>
        <!-- <p class="single-side s3"><span>你</span></p>
        <p class="single-side s4"><span>的</span></p>
        <p class="single-side s5"><span>魔</span></p> -->
        <p class="single-side s6"><span data-type="3"></span></p>
      </div>
    </div>
  </div>
</template>

<script>
import ElfCubes from './index.js'

export default {
  name: '',
  data() {
    return {}
  },
  computed: {},
  watch: {},
  methods: {},
  created() {},

  mounted() {
    // createdBox.componentDodMount
    console.log(ElfCubes)
    ElfCubes.componentDodMount()
  }
}
</script>

<style lang='scss' scoped>
@import './index.scss';
.binxiang {
  display: flex;
  justify-content: center;
  height: 100%;
  .cube {
    margin-top: 250px;
  }
  .dongcunjia {
    width: 90%;
    margin: 0 auto;
    background-color: #fff;
  }
}
</style>
